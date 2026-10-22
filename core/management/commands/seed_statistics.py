from django.core.management.base import BaseCommand, CommandError

from core.models import Statistic


class Command(BaseCommand):
    help = "Crea o actualiza las estadísticas confirmadas de V&V Swiss Services."

    def handle(self, *args, **options):

        statistics = [
            {
                "value": "20+",

                "title_es": "Años de experiencia del equipo",
                "title_fr": "Années d’expérience de l’équipe",
                "title_de": "Jahre Erfahrung des Teams",
                "title_it": "Anni di esperienza del team",
                "title_en": "Years of team experience",

                "order": 1,
                "is_active": True,
            },
        ]

        expected_values = {item["value"] for item in statistics}

        existing = Statistic.objects.all()

        unexpected = [
            f"{obj.value} - {obj.title_fr}"
            for obj in existing
            if obj.value not in expected_values
        ]

        if unexpected:
            raise CommandError(
                "Existen estadísticas no reconocidas en la base de datos: "
                + "; ".join(unexpected)
                + ". No se modificó nada para evitar sobrescribir información."
            )

        created_count = 0
        updated_count = 0

        for item in statistics:
            value = item["value"]

            defaults = item.copy()
            defaults.pop("value")

            obj, created = Statistic.objects.update_or_create(
                value=value,
                defaults=defaults,
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"CREADO: {obj.value} - {obj.title_fr}"
                    )
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"ACTUALIZADO: {obj.value} - {obj.title_fr}"
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

        self.stdout.write(
            "No se añadieron estadísticas no confirmadas."
        )
