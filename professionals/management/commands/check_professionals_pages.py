from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.test import Client
from django.urls import reverse
from django.utils import translation


class Command(BaseCommand):
    help = "Verifica las rutas FR/DE/IT/EN de Profesionales sin crear una base de datos de pruebas."

    def handle(self, *args, **options):
        # Usa un host permitido por Django, sin exponer claves ni modificar configuraciones.
        allowed = [host for host in settings.ALLOWED_HOSTS if host and host != "*" and not host.startswith(".") and ":" not in host]
        host = "localhost" if (settings.DEBUG and ("localhost" in settings.ALLOWED_HOSTS or not settings.ALLOWED_HOSTS)) else (allowed[0] if allowed else "localhost")
        client = Client(raise_request_exception=True)
        failed = False
        for language in ("fr", "de", "it", "en"):
            with translation.override(language):
                url = reverse("core:professionals")
                response = client.get(url, secure=True, HTTP_HOST=host)
            self.stdout.write(f"{language.upper()} | HTTP {response.status_code} | {url}")
            failed = failed or response.status_code != 200
        if failed:
            raise CommandError("Alguna variante de la página no respondió HTTP 200.")
        self.stdout.write(self.style.SUCCESS("Las cuatro versiones de Profesionales responden HTTP 200."))
