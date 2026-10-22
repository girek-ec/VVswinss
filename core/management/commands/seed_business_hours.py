from collections import Counter

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.models import BusinessHour


class Command(BaseCommand):
    help = "Crea o actualiza los horarios de atención de V&V Swiss Services."

    def handle(self, *args, **options):

        business_hours = [
            {
                "day_fr": "Lundi",
                "day_de": "Montag",
                "day_it": "Lunedì",
                "day_en": "Monday",
                "hours": "08:00–18:00",
                "order": 1,
                "is_active": True,
            },
            {
                "day_fr": "Mardi",
                "day_de": "Dienstag",
                "day_it": "Martedì",
                "day_en": "Tuesday",
                "hours": "08:00–18:00",
                "order": 2,
                "is_active": True,
            },
            {
                "day_fr": "Mercredi",
                "day_de": "Mittwoch",
                "day_it": "Mercoledì",
                "day_en": "Wednesday",
                "hours": "08:00–18:00",
                "order": 3,
                "is_active": True,
            },
            {
                "day_fr": "Jeudi",
                "day_de": "Donnerstag",
                "day_it": "Giovedì",
                "day_en": "Thursday",
                "hours": "08:00–18:00",
                "order": 4,
                "is_active": True,
            },
            {
                "day_fr": "Vendredi",
                "day_de": "Freitag",
                "day_it": "Venerdì",
                "day_en": "Friday",
                "hours": "08:00–18:00",
                "order": 5,
                "is_active": True,
            },
            {
                "day_fr": "Samedi",
                "day_de": "Samstag",
                "day_it": "Sabato",
                "day_en": "Saturday",
                "hours": "08:00–13:00",
                "order": 6,
                "is_active": True,
            },
            {
                "day_fr": "Dimanche",
                "day_de": "Sonntag",
                "day_it": "Domenica",
                "day_en": "Sunday",
                "hours": "—",
                "order": 7,
                "is_active": True,
            },
        ]

        # ==========================================================
        # VALIDACIÓN DE SEGURIDAD
        # ==========================================================

        expected_days = {
            item["day_fr"]
            for item in business_hours
        }

        existing_days = list(
            BusinessHour.objects.values_list(
                "day_fr",
                flat=True,
            )
        )

        duplicates = [
            day
            for day, count in Counter(existing_days).items()
            if count > 1
        ]

        if duplicates:
            raise CommandError(
                "Existen días duplicados en BusinessHour: "
                + ", ".join(duplicates)
                + ". No se modificó nada."
            )

        unexpected = [
            day
            for day in existing_days
            if day not in expected_days
        ]

        if unexpected:
            raise CommandError(
                "Existen horarios no reconocidos: "
                + ", ".join(unexpected)
                + ". No se modificó nada para proteger "
                  "el contenido existente."
            )

        # ==========================================================
        # CREAR / ACTUALIZAR
        # ==========================================================

        created_count = 0
        updated_count = 0

        with transaction.atomic():

            for item in business_hours:

                day_fr = item["day_fr"]

                defaults = item.copy()
                defaults.pop("day_fr")

                obj, created = BusinessHour.objects.update_or_create(
                    day_fr=day_fr,
                    defaults=defaults,
                )

                if created:
                    created_count += 1

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"CREADO: "
                            f"{obj.day_fr} | {obj.hours}"
                        )
                    )

                else:
                    updated_count += 1

                    self.stdout.write(
                        self.style.WARNING(
                            f"ACTUALIZADO: "
                            f"{obj.day_fr} | {obj.hours}"
                        )
                    )

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                f"Horarios completados. "
                f"Creados: {created_count} | "
                f"Actualizados: {updated_count}"
            )
        )
