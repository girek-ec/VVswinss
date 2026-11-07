"""Auditoría preventiva de configuración y datos de producción, de solo lectura.
Uso: python manage.py audit_vv_production --report auditoria_produccion.json
"""
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.urls import Resolver404, resolve


class Command(BaseCommand):
    help = 'Revisa configuración de producción, privacidad de adjuntos y contenido demo sin modificar datos.'

    def add_arguments(self, parser):
        parser.add_argument('--domain', default='vvswiss-services.ch', help='Dominio esperado, sin https://.')
        parser.add_argument('--report', default='auditoria_produccion.json', help='Archivo JSON de salida.')
        parser.add_argument('--strict', action='store_true', help='Código de salida distinto de cero si hay errores.')

    def handle(self, *args, **options):
        domain = options['domain'].strip().lower().removeprefix('https://').removeprefix('http://').split('/')[0]
        if not domain or ':' in domain or ' ' in domain:
            raise CommandError('Indica un dominio válido en --domain, sin protocolo ni puerto.')
        issues = []
        def record(level, area, detail):
            issues.append({'level': level, 'area': area, 'detail': str(detail)})

        self.stdout.write('\nV&V SWISS SERVICES · PREDEPLOY PRODUCCIÓN · SOLO LECTURA')
        self.stdout.write(f'Dominio esperado: {domain} | DEBUG={settings.DEBUG}')

        # SETTINGS · PRODUCCIÓN | PRODUCTION SETTINGS
        if settings.DEBUG:
            record('WARN', 'Seguridad', 'DEBUG=True; válido en local, debe ser False en el VPS.')
        if settings.SECRET_KEY.startswith('REEMPLAZAR_') or len(settings.SECRET_KEY) < 40:
            record('WARN', 'Seguridad', 'Revisar que SECRET_KEY sea larga y privada.')
        hosts = list(settings.ALLOWED_HOSTS)
        if domain not in hosts or f'www.{domain}' not in hosts:
            record('WARN' if settings.DEBUG else 'ERROR', 'Hosts', f'ALLOWED_HOSTS debe incluir {domain} y www.{domain}.')
        if '*' in hosts:
            record('WARN', 'Hosts', 'ALLOWED_HOSTS contiene *; evitarlo en producción.')
        trusted = list(settings.CSRF_TRUSTED_ORIGINS)
        required_origins = [f'https://{domain}', f'https://www.{domain}']
        if any(origin not in trusted for origin in required_origins):
            record('WARN' if settings.DEBUG else 'ERROR', 'CSRF', f'CSRF_TRUSTED_ORIGINS debe incluir {required_origins}.')
        site_url = str(getattr(settings, 'SITE_URL', '')).rstrip('/')
        if site_url != f'https://{domain}':
            record('WARN' if settings.DEBUG else 'ERROR', 'SEO', f'SITE_URL={site_url!r}; se espera https://{domain}.')
        if getattr(settings, 'SECURE_PROXY_SSL_HEADER', None) != ('HTTP_X_FORWARDED_PROTO', 'https'):
            record('WARN', 'Proxy', 'Revisar SECURE_PROXY_SSL_HEADER para Nginx Proxy Manager.')
        if not getattr(settings, 'SECURE_SSL_REDIRECT', False):
            record('WARN' if settings.DEBUG else 'ERROR', 'HTTPS', 'SECURE_SSL_REDIRECT=False; activar al tener HTTPS operativo.')
        for key in ('SESSION_COOKIE_SECURE', 'CSRF_COOKIE_SECURE'):
            if not getattr(settings, key, False):
                record('WARN' if settings.DEBUG else 'ERROR', 'Cookies', f'{key}=False; activar en producción.')
        if getattr(settings, 'LANGUAGE_CODE', '').split('-')[0] != 'fr':
            record('WARN', 'I18N', 'El idioma principal debería ser francés (fr).')
        languages = {lang for lang, _ in settings.LANGUAGES}
        if not {'fr', 'de', 'it', 'en'}.issubset(languages):
            record('ERROR', 'I18N', 'Falta algún idioma público FR/DE/IT/EN.')
        if str(settings.DATABASES['default'].get('ENGINE')) != 'django.db.backends.postgresql':
            record('WARN', 'Database', 'El despliegue previsto usa PostgreSQL.')
        if not getattr(settings, 'EMAIL_HOST', ''):
            record('WARN', 'Correo', 'EMAIL_HOST vacío; comprobar SMTP y envío real antes de producción.')
        if not getattr(settings, 'EMAIL_HOST_USER', ''):
            record('WARN', 'Correo', 'EMAIL_HOST_USER vacío; confirmar credenciales del remitente.')

        # SEGURIDAD · RUTA PRIVADA | PRIVATE UPLOAD ROUTING
        route = '/media/contact/attachments/auditoria-prohibido.jpg'
        try:
            match = resolve(route)
            if match.url_name != 'private_contact_attachment':
                record('ERROR', 'Adjuntos', f'{route} no llega a la ruta privada (encontrado: {match.url_name}).')
            else:
                record('INFO', 'Adjuntos', 'Ruta privada de adjuntos registrada y priorizada en Django.')
        except Resolver404:
            record('ERROR', 'Adjuntos', 'No existe la ruta privada para /media/contact/attachments/.')
        record('INFO', 'Adjuntos', 'Verificar en Nginx Proxy Manager que /media/contact/attachments/ NO tenga alias público ni acceso directo.')
        from django.conf import settings as s
        base = Path(s.BASE_DIR)
        dockerignore = base / '.dockerignore'
        if not dockerignore.is_file():
            record('WARN', 'Docker', 'Falta .dockerignore; podrían entrar secretos y archivos de clientes al build.')
        else:
            content = dockerignore.read_text(encoding='utf-8', errors='replace')
            for entry in ('.env', 'media/', 'staticfiles/', '.git/'):
                if entry not in content:
                    record('WARN', 'Docker', f'.dockerignore no menciona {entry!r}.')
            if '\nstatic/\n' in '\n' + content + '\n':
                record('ERROR', 'Docker', 'No excluir static/ del contexto Docker: la web necesita estos recursos.')
        if not (base / 'docker-compose.yml').exists() or not (base / 'Dockerfile').exists():
            record('ERROR', 'Docker', 'Falta Dockerfile o docker-compose.yml.')
        if (base / '.env').is_file():
            record('INFO', 'Secretos', 'Existe .env local: debe permanecer fuera de Git y de la imagen Docker.')
        if not (base / '.gitignore').is_file():
            record('WARN', 'Git', 'Falta .gitignore.')
        else:
            ignored = (base / '.gitignore').read_text(encoding='utf-8', errors='replace')
            if '.vv-backups/' not in ignored:
                record('WARN', 'Git', 'Añadir .vv-backups/ a .gitignore antes del commit.')

        # CONTENIDO · DEMOSTRACIONES PUBLICADAS | PUBLIC DEMO PROJECTS
        try:
            from projects.models import Project
            demos = list(Project.objects.filter(is_published=True, slug_fr__startswith='demo-').values_list('slug_fr', flat=True)[:30])
            if demos:
                record('ERROR', 'Contenido', f'Proyectos demostrativos publicados: {", ".join(demos)}. Despublicarlos antes del VPS.')
            else:
                record('INFO', 'Contenido', 'No hay proyectos publicados cuyo slug_fr comience por demo-.')
        except Exception as exc:
            record('WARN', 'Contenido', f'No se pudo comprobar proyectos demo: {type(exc).__name__}.')
        try:
            from services.models import Service, ServiceBenefit, ServiceCategory
            total = (ServiceCategory.objects.filter(is_active=True).count(), Service.objects.filter(is_active=True).count(), ServiceBenefit.objects.count())
            if total != (7, 37, 111):
                record('WARN', 'Catálogo', f'Cantidad actual (categorías, servicios, beneficios): {total}; esperado en BD limpia (7, 37, 111).')
            else:
                record('INFO', 'Catálogo', 'Catálogo esperado (7, 37, 111) presente.')
        except Exception as exc:
            record('WARN', 'Catálogo', f'No se pudo comprobar el catálogo: {type(exc).__name__}.')

        counts = Counter(item['level'] for item in issues)
        result = {
            'generated_utc': datetime.now(timezone.utc).isoformat(),
            'domain': domain,
            'debug': settings.DEBUG,
            'summary': dict(counts),
            'issues': issues,
            'notes': [
                'Auditoría sin escrituras de base de datos y sin comprobaciones externas.',
                'No sustituye la prueba de correo, seguridad del proxy, HTTPS, recursos ni formulario.',
                'No incluye valores secretos ni contraseñas.',
            ],
        }
        report = Path(options['report'])
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        for entry in issues:
            self.stdout.write(f'  [{entry["level"]}] {entry["area"]}: {entry["detail"]}')
        self.stdout.write(f'\nERROR={counts["ERROR"]} WARN={counts["WARN"]} INFO={counts["INFO"]}')
        self.stdout.write(f'Informe: {report.resolve()}')
        if options['strict'] and counts['ERROR']:
            raise CommandError(f'Predeploy bloqueado: {counts["ERROR"]} error(es).')
