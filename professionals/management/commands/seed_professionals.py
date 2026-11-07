from django.core.management.base import BaseCommand

from core.models import ProfessionalPage
from professionals.models import (
    ADVANTAGE_DEFAULTS, NEED_DEFAULTS, PROCESS_DEFAULTS,
    ProfessionalAdvantage, ProfessionalNeed, ProfessionalProcess,
)


class Command(BaseCommand):
    help = "Crea contenidos iniciales de Profesionales a partir del texto actual, sin borrar ni sobrescribir registros existentes."

    def handle(self, *args, **options):
        pages = ProfessionalPage.objects.all()
        if not pages.exists():
            self.stdout.write(self.style.WARNING("No existe ProfessionalPage. Créela en el administrador primero."))
            return
        total = 0
        for page in pages:
            for model, defaults in (
                (ProfessionalNeed, NEED_DEFAULTS),
                (ProfessionalProcess, PROCESS_DEFAULTS),
                (ProfessionalAdvantage, ADVANTAGE_DEFAULTS),
            ):
                for order, key in enumerate(defaults, start=1):
                    _, created = model.objects.get_or_create(page=page, key=key, defaults={"order": order})
                    total += int(created)
        self.stdout.write(self.style.SUCCESS(f"Profesionales: {total} registros nuevos; los existentes permanecen sin cambios."))
