"""Auditoría SEO multilingüe V&V Swiss Services · solo lectura.
Uso:
    python manage.py audit_vvswiss_seo --report auditoria_seo.json
    python manage.py audit_vvswiss_seo --domain vvswiss-services.ch --report auditoria_seo.json
No realiza solicitudes externas ni altera registros.
"""
import json
from collections import Counter
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from django.apps import apps
from django.core.management.base import BaseCommand
from django.test import Client
from django.urls import NoReverseMatch, URLPattern, URLResolver, get_resolver, reverse
from django.utils import translation

LANGUAGES = ('fr', 'de', 'it', 'en')
PUBLIC_APPS = ('core', 'professionals', 'services', 'projects', 'blog', 'contact')
EXCLUDED = ('admin', 'inbox', 'login', 'logout', 'success', 'design_system', 'api', 'submit', 'download', 'preview', 'webhook', 'unsubscribe')
DETAILS = (
    ('services', 'Service', ('services:detail',), ('is_active',)),
    ('services', 'ServiceCategory', ('services:category_detail',), ('is_active',)),
    ('projects', 'Project', ('projects:detail',), ('is_published',)),
    ('blog', 'Post', ('blog:detail', 'blog:post_detail'), ('is_published',)),
)


class SeoHeadParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_head = False
        self.canonicals = []
        self.alternates = []
        self.robots = []
        self.html_lang = ''
        self.title_open = False
        self.title = ''
        self.descriptions = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.html_lang = attrs.get('lang', '')
        if tag == 'head':
            self.in_head = True
        if tag == 'title' and self.in_head:
            self.title_open = True
        if tag == 'meta' and self.in_head:
            if (attrs.get('name') or '').lower() == 'robots':
                self.robots.append(attrs.get('content', '').lower())
            if (attrs.get('name') or '').lower() == 'description':
                self.descriptions.append(attrs.get('content', ''))
        if tag != 'link' or not self.in_head:
            return
        rel = set((attrs.get('rel') or '').lower().split())
        href = (attrs.get('href') or '').strip()
        if 'canonical' in rel:
            self.canonicals.append(href)
        if 'alternate' in rel and attrs.get('hreflang'):
            self.alternates.append((attrs.get('hreflang', '').strip(), href))

    def handle_endtag(self, tag):
        if tag == 'title':
            self.title_open = False
        if tag == 'head':
            self.in_head = False

    def handle_data(self, data):
        if self.title_open:
            self.title += data


def public_route_names():
    result = set()

    def walk(entries, namespaces=()):
        for entry in entries:
            if isinstance(entry, URLResolver):
                next_namespaces = namespaces + ((entry.namespace,) if entry.namespace else ())
                walk(entry.url_patterns, next_namespaces)
                continue
            if not isinstance(entry, URLPattern) or not entry.name or not namespaces:
                continue
            if namespaces[0] not in PUBLIC_APPS:
                continue
            route_name = ':'.join((*namespaces, entry.name))
            if any(token in route_name.lower() for token in EXCLUDED):
                continue
            result.add(route_name)
    walk(get_resolver().url_patterns)
    return sorted(result)


def normalized_path(value):
    path = unquote(urlsplit(value).path or '/')
    return path if path.endswith('/') or '.' in path.rsplit('/', 1)[-1] else path + '/'


def language_code(value):
    return value.strip().lower().split('-')[0]


class Command(BaseCommand):
    help = 'Verifica canonical, hreflang, reciprocidad y slugs traducidos sin alterar la BD.'

    def add_arguments(self, parser):
        parser.add_argument('--report', default='auditoria_seo_multilingue.json', help='Ruta del informe JSON.')
        parser.add_argument('--domain', default='', help='Dominio canónico esperado en producción (opcional).')
        parser.add_argument('--host', default='localhost', help='Host de prueba interno para Django Client.')
        parser.add_argument('--max-items', type=int, default=12, help='Máximo de registros por modelo (0 = todos).')
        parser.add_argument('--max-pages', type=int, default=350, help='Máximo de URL a comprobar.')

    def issue(self, severity, category, path, detail):
        self.issues.append({'level': severity, 'category': category, 'url': path, 'detail': detail})

    def handle(self, *args, **options):
        self.issues = []
        self.pages = []
        self.group_results = {}
        self.client = Client(raise_request_exception=False)
        self.host = options['host']
        self.domain = options['domain'].strip().lower().removeprefix('https://').removeprefix('http://').strip('/')
        self.max_pages = max(1, options['max_pages'])
        self.stdout.write('V&V SWISS SERVICES · SEO FR / DE / IT / EN · SOLO LECTURA')
        self.stdout.write('El comando no realiza solicitudes externas ni modifica datos.\n')
        groups = self.build_groups(options['max_items'])
        scanned = set()
        for group_name, target_paths in groups.items():
            if len(scanned) >= self.max_pages:
                break
            for lang, path in target_paths.items():
                if path in scanned or len(scanned) >= self.max_pages:
                    continue
                scanned.add(path)
                result = self.inspect(path, lang, group_name, target_paths)
                self.pages.append(result)
                self.group_results[(group_name, lang)] = result
                self.stdout.write(f'  [{result["status"]}] {lang.upper()} {path} | canonical={result["canonical"] or "SIN"} | alternates={len(result["alternates"])}')
        self.check_reciprocity(groups)
        if len(scanned) >= self.max_pages:
            self.issue('WARN', 'Cobertura', '', f'Se alcanzó el límite de {self.max_pages} URL.')
        counts = Counter(item['level'] for item in self.issues)
        self.stdout.write('\n' + '=' * 76)
        self.stdout.write(f'PÁGINAS: {len(self.pages)} | ERRORES: {counts["ERROR"]} | AVISOS: {counts["WARN"]} | INFO: {counts["INFO"]}')
        self.stdout.write('=' * 76)
        for item in self.issues[:100]:
            self.stdout.write(f'[{item["level"]}] [{item["category"]}] {item["url"]} · {item["detail"]}')
        if len(self.issues) > 100:
            self.stdout.write(f'... y {len(self.issues)-100} observaciones adicionales en el JSON.')
        output = Path(options['report'])
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps({
            'generated_utc': datetime.now(timezone.utc).isoformat(),
            'environment_host': self.host,
            'expected_domain': self.domain,
            'pages_checked': len(self.pages),
            'totals': dict(counts),
            'pages': self.pages,
            'issues': self.issues,
        }, ensure_ascii=False, indent=2), encoding='utf-8')
        self.stdout.write(f'\nInforme guardado en: {output.resolve()}')

    def build_groups(self, max_items):
        groups = {}
        for name in public_route_names():
            targets = {}
            for lang in LANGUAGES:
                try:
                    with translation.override(lang):
                        targets[lang] = reverse(name)
                except NoReverseMatch:
                    pass
            if targets:
                groups[name] = targets
        for app_label, model_name, route_names, flags in DETAILS:
            try:
                model = apps.get_model(app_label, model_name)
                qs = model._default_manager.all()
                model_fields = {f.name for f in model._meta.fields}
                for flag in flags:
                    if flag in model_fields:
                        qs = qs.filter(**{flag: True})
                qs = qs.order_by('pk')
                if max_items > 0:
                    qs = qs[:max_items]
                for item in qs:
                    targets = {}
                    for lang in LANGUAGES:
                        slug = getattr(item, f'slug_{lang}', None) or getattr(item, 'slug_fr', None) or getattr(item, 'slug', None)
                        if not slug:
                            continue
                        for name in route_names:
                            try:
                                with translation.override(lang):
                                    targets[lang] = reverse(name, args=[slug])
                                break
                            except NoReverseMatch:
                                continue
                    if targets:
                        groups[f'{app_label}.{model_name}#{item.pk}'] = targets
            except Exception as exc:
                self.issue('WARN', 'Cobertura', f'{app_label}.{model_name}', f'No se pudieron enumerar registros: {type(exc).__name__}: {exc}')
        return groups

    def inspect(self, path, lang, group_name, expected_paths):
        result = {'url': path, 'language': lang, 'group': group_name, 'status': None, 'canonical': '', 'alternates': [], 'indexable': True}
        try:
            response = self.client.get(path, secure=True, HTTP_HOST=self.host, follow=False)
        except Exception as exc:
            result['status'] = 'EXCEPTION'
            self.issue('ERROR', 'HTTP', path, f'{type(exc).__name__}: {exc}')
            return result
        result['status'] = response.status_code
        if response.status_code != 200:
            self.issue('WARN' if response.status_code in (301, 302, 307, 308) else 'ERROR', 'HTTP', path, f'HTTP {response.status_code} (la auditoría necesita HTML 200)')
            return result
        if 'text/html' not in response.get('Content-Type', ''):
            self.issue('INFO', 'Cobertura', path, 'Contenido no HTML; se omite SEO de cabecera.')
            return result
        parser = SeoHeadParser()
        parser.feed(response.content.decode(response.charset or 'utf-8', errors='replace'))
        result['canonical'] = parser.canonicals[0] if parser.canonicals else ''
        result['alternates'] = [{'hreflang': code, 'href': href} for code, href in parser.alternates]
        result['indexable'] = 'noindex' not in ','.join(parser.robots + [response.get('X-Robots-Tag', '').lower()])
        if not result['indexable']:
            self.issue('INFO', 'Indexación', path, 'La página tiene noindex; revisar si es intencional.')
            return result
        if not parser.title.strip():
            self.issue('WARN', 'Title', path, 'Falta <title>.')
        if not any(x.strip() for x in parser.descriptions):
            self.issue('WARN', 'Meta description', path, 'Falta meta description.')
        if parser.html_lang and language_code(parser.html_lang) != lang:
            self.issue('WARN', 'HTML lang', path, f'lang del documento es {parser.html_lang!r}; se esperaba {lang}.')
        if len(parser.canonicals) != 1:
            self.issue('ERROR', 'Canonical', path, f'Se detectaron {len(parser.canonicals)} etiquetas canonical; se espera exactamente una.')
        for canonical in parser.canonicals:
            parts = urlsplit(canonical)
            if parts.scheme not in ('http', 'https') or not parts.netloc:
                self.issue('WARN', 'Canonical', path, f'La URL canónica no es absoluta: {canonical}')
            if parts.scheme == 'http' and parts.hostname not in ('localhost', '127.0.0.1'):
                self.issue('WARN', 'Canonical', path, f'URL canónica sin HTTPS: {canonical}')
            if parts.query or parts.fragment:
                self.issue('WARN', 'Canonical', path, f'El canonical incluye query/fragment: {canonical}')
            if normalized_path(canonical) != normalized_path(path):
                self.issue('ERROR', 'Canonical', path, f'Canonical apunta a otra página: {canonical}')
            if self.domain and parts.netloc.lower() != self.domain:
                self.issue('WARN', 'Canonical', path, f'Dominio canónico {parts.netloc or "ausente"} no coincide con {self.domain}.')
        by_language = {}
        for code, href in parser.alternates:
            short = language_code(code)
            if short == 'x':
                continue
            if short not in LANGUAGES:
                continue
            if short in by_language:
                self.issue('WARN', 'Hreflang', path, f'Idioma {short.upper()} duplicado en hreflang.')
            by_language[short] = href
            parts = urlsplit(href)
            if parts.scheme not in ('http', 'https') or not parts.netloc:
                self.issue('WARN', 'Hreflang', path, f'Alternates deben usar URL absoluta: {short}={href}')
            if parts.scheme == 'http' and parts.hostname not in ('localhost', '127.0.0.1'):
                self.issue('WARN', 'Hreflang', path, f'Alternate sin HTTPS: {short}={href}')
            expected = expected_paths.get(short)
            if expected and normalized_path(href) != normalized_path(expected):
                self.issue('ERROR', 'Equivalencia', path, f'{short.upper()} apunta a {href}; se esperaba ruta {expected}.')
            if self.domain and parts.netloc.lower() != self.domain:
                self.issue('WARN', 'Hreflang', path, f'Alternate {short.upper()} usa dominio distinto de {self.domain}: {href}')
        for target_lang, expected in expected_paths.items():
            if target_lang not in by_language:
                self.issue('WARN', 'Hreflang', path, f'Falta alternate {target_lang.upper()} → {expected}')
        return result

    def check_reciprocity(self, groups):
        for group_name, targets in groups.items():
            for source_lang in targets:
                page = self.group_results.get((group_name, source_lang))
                if not page or page['status'] != 200 or not page['indexable']:
                    continue
                for alt in page['alternates']:
                    target_lang = language_code(alt['hreflang'])
                    if target_lang not in targets or target_lang == source_lang:
                        continue
                    other_page = self.group_results.get((group_name, target_lang))
                    if not other_page or other_page['status'] != 200 or not other_page['indexable']:
                        continue
                    reverse_link = next((x['href'] for x in other_page['alternates'] if language_code(x['hreflang']) == source_lang), None)
                    if not reverse_link or normalized_path(reverse_link) != normalized_path(page['url']):
                        self.issue('WARN', 'Reciprocidad', page['url'], f'{target_lang.upper()} no devuelve hreflang correcto hacia {source_lang.upper()}.')
