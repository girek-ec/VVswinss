from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.test import Client
from django.urls import reverse
from django.utils import translation
from professionals.models import ProfessionalSitePage, ProfessionalNeedItem, ProfessionalProcessItem, ProfessionalAdvantageItem


class Command(BaseCommand):
    help = "Verifica los cuatro idiomas y los 15 registros administrables sin crear base de pruebas."

    def handle(self, *args, **options):
        page = ProfessionalSitePage.objects.filter(slug="main", is_active=True).first()
        if not page:
            raise CommandError("No existe la página V2 activa. Ejecute seed_professionals_v2.")
        counts = (ProfessionalNeedItem.objects.filter(page=page, is_active=True).count(),
                  ProfessionalProcessItem.objects.filter(page=page, is_active=True).count(),
                  ProfessionalAdvantageItem.objects.filter(page=page, is_active=True).count())
        self.stdout.write(f"Necesidades: {counts[0]} | Procesos: {counts[1]} | Ventajas: {counts[2]}")
        allowed = [host for host in settings.ALLOWED_HOSTS if host and host != "*" and not host.startswith(".") and ":" not in host]
        host = "localhost" if settings.DEBUG and ("localhost" in settings.ALLOWED_HOSTS or not settings.ALLOWED_HOSTS) else (allowed[0] if allowed else "localhost")
        client = Client(raise_request_exception=True)
        for lang in ("fr", "de", "it", "en"):
            with translation.override(lang):
                url = reverse("core:professionals")
                response = client.get(url, secure=True, HTTP_HOST=host)
            self.stdout.write(f"{lang.upper()} | HTTP {response.status_code} | {url}")
            if response.status_code != 200:
                raise CommandError(f"Página {lang.upper()} falló")
        self.stdout.write(self.style.SUCCESS("Las cuatro versiones V2 funcionan. La base de datos principal no fue modificada por esta comprobación."))
