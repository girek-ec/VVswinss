from django.core.management.base import BaseCommand, CommandError

from core.models import ServiceArea


class Command(BaseCommand):
    help = "Crea o actualiza las zonas de intervención de V&V Swiss Services."

    def handle(self, *args, **options):

        areas = [
            {
                "name": "Canton de Vaud et environs",
                "canton": "Vaud",

                "description_es": (
                    "Zona principal de intervención de V&V Swiss Services para "
                    "proyectos de renovación, aislamiento, mantenimiento y "
                    "trabajos del edificio."
                ),

                "description_fr": (
                    "Zone principale d’intervention de V&V Swiss Services pour "
                    "les projets de rénovation, d’isolation, d’entretien et "
                    "de travaux du bâtiment."
                ),

                "description_de": (
                    "Haupttätigkeitsgebiet von V&V Swiss Services für "
                    "Renovations-, Dämmungs-, Unterhalts- und Bauarbeiten."
                ),

                "description_it": (
                    "Area principale d’intervento di V&V Swiss Services per "
                    "progetti di ristrutturazione, isolamento, manutenzione "
                    "e lavori edili."
                ),

                "description_en": (
                    "V&V Swiss Services' main service area for renovation, "
                    "insulation, property maintenance and building works."
                ),

                "order": 1,
                "is_active": True,
            },

            {
                "name": "Suisse romande",
                "canton": "",

                "description_es": (
                    "Intervenciones en la Suiza francófona según el tipo de "
                    "proyecto, su ubicación y las condiciones de ejecución."
                ),

                "description_fr": (
                    "Interventions en Suisse romande selon la nature du projet, "
                    "sa localisation et les conditions d’exécution."
                ),

                "description_de": (
                    "Einsätze in der Westschweiz je nach Art des Projekts, "
                    "Standort und Ausführungsbedingungen."
                ),

                "description_it": (
                    "Interventi nella Svizzera romanda in funzione della natura "
                    "del progetto, della sua ubicazione e delle condizioni "
                    "di esecuzione."
                ),

                "description_en": (
                    "Projects may also be undertaken across French-speaking "
                    "Switzerland depending on the nature, location and practical "
                    "requirements of the work."
                ),

                "order": 2,
                "is_active": True,
            },
        ]

        expected_names = {item["name"] for item in areas}

        existing = ServiceArea.objects.all()

        unexpected = [
            obj.name
            for obj in existing
            if obj.name not in expected_names
        ]

        if unexpected:
            raise CommandError(
                "Existen zonas de intervención no reconocidas: "
                + ", ".join(unexpected)
                + ". No se modificó nada para evitar sobrescribir contenido."
            )

        created_count = 0
        updated_count = 0

        for item in areas:
            name = item["name"]

            defaults = item.copy()
            defaults.pop("name")

            obj, created = ServiceArea.objects.update_or_create(
                name=name,
                defaults=defaults,
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"CREADO: {obj.name}"
                    )
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"ACTUALIZADO: {obj.name}"
                    )
                )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Proceso completado. "
                f"Creados: {created_count} | "
                f"Actualizados: {updated_count}"
            )
        )
