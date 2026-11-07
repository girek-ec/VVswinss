"""Auditoría de lectura para V&V Swiss Services. No modifica la base de datos.
Uso: python manage.py audit_vvswiss_site --report reports/auditoria.json
"""
import json
import re
from collections import Counter
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

from django.apps import apps
from django.conf import settings
from django.core.checks import run_checks
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.migrations.executor import MigrationExecutor
from django.db.models import ImageField
from django.test import Client
from django.urls import NoReverseMatch, URLPattern, URLResolver, get_resolver, resolve, reverse
from django.utils import translation
from django.contrib.staticfiles import finders

LANGUAGES = ('fr', 'de', 'it', 'en')
SITE_APPS = ('core', 'professionals', 'services', 'projects', 'blog', 'contact')
STATIC_REF = re.compile(r"{%\s*static\s+['\"]([^'\"]+)['\"]\s*%}")
SKIP_ROUTE_TOKENS = ('admin', 'delete', 'logout', 'submit', 'download', 'export', 'import', 'webhook', 'api', 'ajax', 'feed', 'preview', 'upload', 'unsubscribe')


class PageHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ''
        self.title_open = False
        self.descriptions = []
        self.canonicals = []
        self.hreflangs = []
        self.images_without_alt = 0
        self.h1 = 0
        self.links = []
        self.assets = []
        self.document_lang = None
        self.robots = ''

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html':
            self.document_lang = a.get('lang')
        if tag == 'title':
            self.title_open = True
        if tag == 'h1':
            self.h1 += 1
        if tag == 'meta':
            name = (a.get('name') or '').lower()
            if name == 'description':
                self.descriptions.append(a.get('content') or '')
            if name == 'robots':
                self.robots = (a.get('content') or '').lower()
        if tag == 'link':
            rel = (a.get('rel') or '').lower()
            if rel == 'canonical':
                self.canonicals.append(a.get('href') or '')
            if rel == 'alternate' and a.get('hreflang'):
                self.hreflangs.append(a['hreflang'])
            if rel in ('stylesheet', 'icon', 'preload', 'modulepreload'):
                if a.get('href'):
                    self.assets.append(a['href'])
        if tag == 'a' and a.get('href'):
            self.links.append(a['href'])
        if tag in ('img', 'script', 'source', 'video', 'audio', 'iframe'):
            if tag == 'img' and 'alt' not in a:
                self.images_without_alt += 1
            for k in ('src', 'data-src', 'poster'):
                if a.get(k):
                    self.assets.append(a[k])
            if a.get('srcset'):
                self.assets.extend(p.strip().split()[0] for p in a['srcset'].split(',') if p.strip())
        for k in ('data-background', 'data-bg'):
            if a.get(k):
                self.assets.append(a[k])

    def handle_endtag(self, tag):
        if tag == 'title':
            self.title_open = False

    def handle_data(self, data):
        if self.title_open:
            self.title += data


def public_routes():
    """Solo rutas GET públicas con nombre y sin argumentos; sin admin ni endpoints mutadores."""
    results = []

    def visit(patterns, namespaces=()):
        for entry in patterns:
            if isinstance(entry, URLResolver):
                ns = namespaces + ((entry.namespace,) if entry.namespace else ())
                if any(s.lower() in SKIP_ROUTE_TOKENS for s in ns):
                    continue
                visit(entry.url_patterns, ns)
            elif isinstance(entry, URLPattern) and entry.name:
                namespace = namespaces[0] if namespaces else None
                if namespace not in SITE_APPS:
                    continue
                name = ':'.join((*namespaces, entry.name))
                if any(word in name.lower() for word in SKIP_ROUTE_TOKENS):
                    continue
                results.append(name)
    visit(get_resolver().url_patterns)
    return sorted(set(results))


class Command(BaseCommand):
    help = 'Audita la web V&V en FR/DE/IT/EN, Django, migraciones, SEO, recursos static/media y enlaces (solo lectura).'

    def add_arguments(self, parser):
        parser.add_argument('--report', metavar='ARCHIVO.JSON', help='Guarda el resultado como JSON (sin contraseñas).')
        parser.add_argument('--max-pages', type=int, default=120, help='Máximo de páginas GET para visitar (120).')
        parser.add_argument('--max-media', type=int, default=100, help='Máximo de archivos media a verificar (100).')
        parser.add_argument('--only-urls', action='store_true', help='Solo visita páginas, enlaces y recursos. Omite revisión de BD y migraciones.')
        parser.add_argument('--no-details', action='store_true', help='Omite una página de detalle de cada sección.')

    def handle(self, *args, **options):
        self.issues = []
        self.stats = Counter()
        self.pages = []
        self.checked_media = set()
        self.checked_static = set()
        self.max_media = max(0, options['max_media'])
        self.max_pages = max(1, options['max_pages'])
        self.host = self.get_host()
        self.client = Client(raise_request_exception=True)
        self.stdout.write('\n' + '=' * 68)
        self.stdout.write('V&V SWISS SERVICES · AUDITORÍA GENERAL · SOLO LECTURA')
        self.stdout.write('=' * 68)
        self.stdout.write(f'Entorno: {"DESARROLLO" if settings.DEBUG else "PRODUCCIÓN"} | Host de prueba: {self.host}')
        self.stdout.write('Idiomas: FR / DE / IT / EN | No se envían formularios ni mensajes.')
        self.stdout.write('')

        if not options['only_urls']:
            self.check_django()
            self.check_db()
            self.check_migrations()
            self.check_static_templates()
            self.check_media_models()
            self.check_counts()
            self.check_settings()
        self.check_pages(include_details=not options['no_details'])
        self.print_results()

        if options.get('report'):
            self.save_report(options['report'])

    def problem(self, level, category, message, detail=''):
        self.issues.append({'level': level, 'category': category, 'message': str(message), 'detail': str(detail)[:900]})
        self.stats[level] += 1

    def get_host(self):
        hosts = [h for h in settings.ALLOWED_HOSTS if h and h != '*' and not h.startswith('.') and ':' not in h]
        if settings.DEBUG and ('localhost' in hosts or not hosts):
            return 'localhost'
        return hosts[0] if hosts else 'localhost'

    def check_django(self):
        self.stdout.write('[1/8] Comprobaciones internas de Django')
        try:
            problems = run_checks()
            if not problems:
                self.stdout.write('  [OK] django checks: sin incidencias.')
            for problem in problems:
                level = 'ERROR' if problem.is_serious() else 'WARN'
                self.problem(level, 'Django', f'{problem.id}: {problem.msg}', problem.hint or '')
        except Exception as exc:
            self.problem('ERROR', 'Django', 'No fue posible ejecutar run_checks()', repr(exc))

    def check_db(self):
        self.stdout.write('[2/8] Conexión a base de datos')
        for alias in connections:
            try:
                cn = connections[alias]
                with cn.cursor() as c:
                    c.execute('SELECT 1')
                    if c.fetchone()[0] != 1:
                        raise RuntimeError('SELECT 1 devolvió un resultado inesperado')
                self.stdout.write(f'  [OK] Conexión: {alias}')
            except Exception as exc:
                self.problem('ERROR', 'Database', f'No hay conexión: {alias}', repr(exc))

    def check_migrations(self):
        self.stdout.write('[3/8] Migraciones pendientes (sin ejecutar migrate)')
        try:
            connection = connections['default']
            executor = MigrationExecutor(connection)
            plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
            pending = [f'{m.app_label}.{m.name}' for m, backward in plan if not backward]
            if pending:
                self.problem('ERROR', 'Migrations', f'{len(pending)} migraciones sin aplicar', ', '.join(pending[:25]))
            else:
                self.stdout.write('  [OK] Ninguna migración pendiente.')
        except Exception as exc:
            self.problem('ERROR', 'Migrations', 'No se pudieron revisar las migraciones', repr(exc))

    def check_static_templates(self):
        self.stdout.write('[4/8] Referencias estáticas en plantillas')
        base = Path(settings.BASE_DIR) / 'templates'
        if not base.is_dir():
            self.problem('WARN', 'Static', 'No existe la carpeta templates/ en BASE_DIR; se revisarán solo recursos renderizados.')
            return
        seen = 0
        for file in base.rglob('*.html'):
            # Se ignoran plantillas de dependencias externas si se encuentran bajo templates.
            try:
                source = file.read_text(encoding='utf-8')
            except (UnicodeError, OSError):
                continue
            for relative in STATIC_REF.findall(source):
                seen += 1
                self.check_static(relative, str(file.relative_to(base)))
        self.stdout.write(f'  Referencias estáticas analizadas: {seen} | únicas: {len(self.checked_static)}')

    def check_static(self, relative, where):
        key = unquote(relative).lstrip('/')
        if not key or key in self.checked_static:
            return
        self.checked_static.add(key)
        try:
            if not finders.find(key):
                self.problem('ERROR', 'Static missing', f'No existe en static: {key}', where)
        except Exception as exc:
            self.problem('ERROR', 'Static', f'No se pudo verificar {key}', repr(exc))

    def check_media_models(self):
        self.stdout.write('[5/8] Archivos de imagen guardados en modelos')
        inspected = 0
        for model in apps.get_models():
            if inspected >= self.max_media:
                break
            if model._meta.app_label not in SITE_APPS:
                continue
            fields = [f for f in model._meta.fields if isinstance(f, ImageField)]
            if not fields:
                continue
            try:
                # Un máximo de 40 registros por modelo evita consultas masivas.
                records = model._default_manager.all().order_by('pk')[:40]
                for obj in records:
                    for f in fields:
                        value = getattr(obj, f.name, None)
                        if not value or not value.name or value.name in self.checked_media:
                            continue
                        self.checked_media.add(value.name)
                        inspected += 1
                        try:
                            if not value.storage.exists(value.name):
                                self.problem('ERROR', 'Media missing', f'{model._meta.label} #{obj.pk}.{f.name}', value.name)
                            elif model._meta.app_label == 'professionals' and not value.name.lower().endswith('.webp'):
                                self.problem('WARN', 'Media format', f'Imagen no WebP en {model._meta.label} #{obj.pk}.{f.name}', value.name)
                        except Exception as exc:
                            self.problem('WARN', 'Media read', f'No se pudo comprobar {value.name}', repr(exc))
                        if inspected >= self.max_media:
                            break
                    if inspected >= self.max_media:
                        break
            except Exception as exc:
                self.problem('WARN', 'Media', f'No se pudo revisar {model._meta.label}', repr(exc))
        self.stdout.write(f'  Archivos media verificados (máximo configurable): {inspected}')

    def check_counts(self):
        self.stdout.write('[6/8] Estado de los contenidos (solo lectura)')
        names = (
            ('professionals', 'ProfessionalSitePage'), ('professionals', 'ProfessionalNeedItem'),
            ('professionals', 'ProfessionalProcessItem'), ('professionals', 'ProfessionalAdvantageItem'),
            ('professionals', 'ProfessionalProjectItem'), ('professionals', 'ProfessionalExtraBlock'),
            ('services', 'Service'), ('services', 'ServiceCategory'),
            ('projects', 'Project'), ('blog', 'Post'), ('contact', 'ContactRequest'),
        )
        for app_label, name in names:
            try:
                model = apps.get_model(app_label, name)
                total = model._default_manager.count()
                live_field = next((field for field in ('is_published', 'is_active') if field in {f.name for f in model._meta.fields}), None)
                active = model._default_manager.filter(**{live_field: True}).count() if live_field else None
                output = f'{app_label}.{name}: {total} registros'
                if active is not None:
                    output += f' / {active} publicados o activos'
                self.stdout.write('  ' + output)
                if total == 0 and app_label in ('services', 'projects'):
                    self.problem('WARN', 'Content', f'Sin registros en {app_label}.{name}')
            except LookupError:
                continue
            except Exception as exc:
                self.problem('WARN', 'Content', f'Error al consultar {app_label}.{name}', repr(exc))

    def check_settings(self):
        self.stdout.write('[7/8] Configuración básica de publicación')
        if settings.DEBUG:
            self.stdout.write('  [INFO] DEBUG=True: revisión de seguridad de producción no aplica a este entorno.')
        else:
            if not getattr(settings, 'SECURE_SSL_REDIRECT', False):
                self.problem('WARN', 'Security', 'SECURE_SSL_REDIRECT=False (verifica si Nginx Proxy Manager fuerza HTTPS).')
            if not getattr(settings, 'SESSION_COOKIE_SECURE', False):
                self.problem('WARN', 'Security', 'SESSION_COOKIE_SECURE=False en producción.')
            if not getattr(settings, 'CSRF_COOKIE_SECURE', False):
                self.problem('WARN', 'Security', 'CSRF_COOKIE_SECURE=False en producción.')
        if not getattr(settings, 'ALLOWED_HOSTS', []):
            self.problem('WARN', 'Settings', 'ALLOWED_HOSTS está vacío.')
        if not getattr(settings, 'STATIC_URL', None):
            self.problem('ERROR', 'Settings', 'STATIC_URL no está definido.')
        if not getattr(settings, 'MEDIA_URL', None):
            self.problem('WARN', 'Settings', 'MEDIA_URL no está definido.')

    def check_pages(self, include_details=True):
        self.stdout.write('[8/8] Renderizado de páginas públicas, enlaces e imágenes · 4 idiomas')
        names = public_routes()
        if not names:
            self.problem('WARN', 'Routes', 'No se encontraron nombres de URL públicos automáticamente.')
        scanned = set()
        for language in LANGUAGES:
            with translation.override(language):
                for name in names:
                    if len(self.pages) >= self.max_pages:
                        break
                    try:
                        url = reverse(name)
                    except NoReverseMatch:
                        continue  # Es normal para rutas que requieren slug/ID.
                    if url in scanned:
                        continue
                    scanned.add(url)
                    self.test_url(url, language, name)
                if include_details:
                    for name, url in self.sample_detail_urls(language):
                        if len(self.pages) >= self.max_pages:
                            break
                        if url not in scanned:
                            scanned.add(url)
                            self.test_url(url, language, name)
        self.stdout.write(f'  Rutas con GET: {len(self.pages)} | rutas descubiertas (con nombre): {len(names)}')
        if len(self.pages) >= self.max_pages:
            self.problem('WARN', 'Routes', f'Límite de {self.max_pages} páginas alcanzado; algunas pueden no haberse visitado.')

    def sample_detail_urls(self, language):
        result = []
        specs = [
            ('services', 'Service', ('services:detail',), ('is_active',)),
            ('services', 'ServiceCategory', ('services:category_detail',), ('is_active',)),
            ('projects', 'Project', ('projects:detail',), ('is_published',)),
            ('blog', 'Post', ('blog:detail', 'blog:post_detail'), ('is_published',)),
        ]
        for app_label, model_name, routes, conditions in specs:
            try:
                model = apps.get_model(app_label, model_name)
            except LookupError:
                continue
            try:
                qs = model._default_manager.all()
                field_names = {f.name for f in model._meta.fields}
                for flag in conditions:
                    if flag in field_names:
                        qs = qs.filter(**{flag: True})
                item = qs.order_by('pk').first()
                if not item:
                    continue
                slug = getattr(item, f'slug_{language}', None) or getattr(item, 'slug_fr', None) or getattr(item, 'slug', None)
                if not slug:
                    continue
                for route in routes:
                    try:
                        url = reverse(route, args=[slug])
                    except NoReverseMatch:
                        continue
                    result.append((route + ' [muestra]', url))
                    break
            except Exception as exc:
                self.problem('WARN', 'Details', f'No se pudo seleccionar muestra de {app_label}.{model_name}', repr(exc))
        return result

    def test_url(self, url, language, name):
        try:
            response = self.client.get(url, secure=True, HTTP_HOST=self.host)
            status = response.status_code
            record = {'lang': language, 'name': name, 'url': url, 'status': status}
            self.pages.append(record)
            self.stats['visited'] += 1
            if status >= 400:
                self.problem('ERROR', 'HTTP', f'{status} {url}', name)
                self.stdout.write(f'  [ERROR] {language.upper()} HTTP {status}: {url}')
                return
            if 300 <= status < 400:
                location = response.get('Location', '')
                self.problem('WARN', 'Redirect', f'{status} {url}', location)
                self.stdout.write(f'  [REDIRECT] {language.upper()} {status}: {url}')
                return
            if 'text/html' not in response.get('Content-Type', ''):
                return
            html = response.content.decode(response.charset or 'utf-8', errors='replace')
            parser = PageHTML()
            parser.feed(html)
            if not parser.title.strip():
                self.problem('WARN', 'SEO', f'Página sin <title>: {url}')
            if not any(x.strip() for x in parser.descriptions):
                self.problem('WARN', 'SEO', f'Página sin meta description: {url}')
            if not parser.canonicals:
                self.problem('INFO', 'SEO', f'No se encontró rel=canonical: {url}')
            if len(set(parser.hreflangs).intersection(LANGUAGES)) < 2:
                self.problem('INFO', 'I18N', f'No se verificaron alternates hreflang suficientes: {url}')
            if parser.h1 == 0:
                self.problem('WARN', 'SEO', f'Página sin H1: {url}')
            if parser.h1 > 1:
                self.problem('INFO', 'SEO', f'{parser.h1} elementos H1 en {url} (revisar jerarquía)')
            if parser.document_lang and not parser.document_lang.lower().startswith(language):
                self.problem('WARN', 'I18N', f'lang={parser.document_lang!r} en página {language.upper()}', url)
            if parser.images_without_alt:
                self.problem('WARN', 'Accessibility', f'{parser.images_without_alt} imágenes sin atributo alt: {url}')
            if not settings.DEBUG and 'noindex' in parser.robots:
                self.problem('WARN', 'SEO', f'Meta robots noindex en producción: {url}')
            for asset in parser.assets:
                self.test_asset(asset, url)
            for link in parser.links:
                self.test_link(link, url)
            self.stdout.write(f'  [OK] {language.upper()} HTTP {status}: {url}')
        except Exception as exc:
            self.stats['visited'] += 1
            self.pages.append({'lang': language, 'name': name, 'url': url, 'status': 'EXCEPTION'})
            self.problem('ERROR', 'Exception', f'{language.upper()} {url}', f'{type(exc).__name__}: {exc}')
            self.stdout.write(f'  [ERROR] {language.upper()} EXCEPTION: {url} | {type(exc).__name__}: {str(exc)[:140]}')

    def test_asset(self, asset, source):
        url = (asset or '').strip()
        if not url or url.startswith(('data:', 'blob:', '#', 'javascript:')) or '{{' in url or '{%' in url:
            return
        u = urlsplit(url)
        if u.scheme in ('https', 'http') and u.netloc and u.netloc not in (self.host, f'www.{self.host}'):
            return
        path = unquote(u.path)
        static_url = urlsplit(settings.STATIC_URL or '/static/').path
        media_url = urlsplit(settings.MEDIA_URL or '/media/').path
        if static_url and path.startswith(static_url):
            self.check_static(path[len(static_url):], f'HTML {source}')
        elif media_url and path.startswith(media_url):
            relative = path[len(media_url):]
            if relative and relative not in self.checked_media and len(self.checked_media) < self.max_media:
                self.checked_media.add(relative)
                try:
                    from django.core.files.storage import default_storage
                    if not default_storage.exists(relative):
                        self.problem('ERROR', 'Media missing', f'No existe media: {relative}', source)
                except Exception as exc:
                    self.problem('WARN', 'Media read', relative, repr(exc))

    def test_link(self, link, source):
        raw = (link or '').strip()
        if not raw or raw.startswith(('#', 'mailto:', 'tel:', 'javascript:', 'sms:', 'whatsapp:', 'data:')):
            return
        parsed = urlsplit(raw)
        if parsed.scheme in ('http', 'https'):
            if parsed.netloc not in (self.host, f'www.{self.host}', 'localhost', '127.0.0.1'):
                return
        elif parsed.scheme or parsed.netloc:
            return
        path = unquote(parsed.path)
        if not path:
            return
        if not path.startswith('/'):
            path = unquote(urlsplit(urljoin(source, path)).path)
        if path.startswith(('/admin/', '/static/', '/media/')):
            return
        try:
            resolve(path)
        except Exception:
            item = (path, source)
            if item not in getattr(self, '_bad_links', set()):
                self._bad_links = getattr(self, '_bad_links', set())
                self._bad_links.add(item)
                self.problem('WARN', 'Link', f'No se reconoce la ruta interna {path}', source)

    def print_results(self):
        self.stdout.write('\n' + '=' * 68)
        self.stdout.write(f'RESUMEN · páginas visitadas: {self.stats["visited"]} | ERRORES: {self.stats["ERROR"]} | AVISOS: {self.stats["WARN"]} | INFO: {self.stats["INFO"]}')
        self.stdout.write('=' * 68)
        for level in ('ERROR', 'WARN', 'INFO'):
            problems = [p for p in self.issues if p['level'] == level]
            if not problems:
                continue
            self.stdout.write(f'\n{level} ({len(problems)}):')
            for p in problems[:35]:
                self.stdout.write(f'  [{p["category"]}] {p["message"]}' + (f' | {p["detail"]}' if p['detail'] else ''))
            if len(problems) > 35:
                self.stdout.write(f'  ... y {len(problems) - 35} incidencias adicionales (ver JSON).')
        if self.stats['ERROR'] == 0:
            self.stdout.write('\n[OK] No se detectaron errores críticos EN LAS COMPROBACIONES EJECUTADAS.')
        else:
            self.stdout.write('\n[REVISAR] Hay errores detectados; no desplegar sin investigarlos.')
        self.stdout.write('NOTA: no sustituye pruebas reales de formularios, entrega de correos, WhatsApp, DNS, SSL o rendimiento de producción.')

    def save_report(self, requested):
        target = Path(requested).expanduser()
        if not target.is_absolute():
            target = Path(settings.BASE_DIR) / target
        target.parent.mkdir(parents=True, exist_ok=True)
        report = {
            'generated_at': datetime.now().astimezone().isoformat(),
            'debug': bool(settings.DEBUG),
            'host': self.host,
            'counts': dict(self.stats),
            'pages': self.pages,
            'issues': self.issues,
            'disclaimer': 'Solo lectura. No comprueba envío de formularios ni infraestructura externa.',
        }
        target.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        self.stdout.write(f'\nInforme JSON guardado en: {target}')
