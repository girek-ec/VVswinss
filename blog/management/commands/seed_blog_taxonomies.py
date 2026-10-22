from collections import Counter

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.text import slugify

from blog.models import BlogCategory, BlogTag


class Command(BaseCommand):
    help = (
        "Crea o actualiza las categorías y etiquetas del blog "
        "de V&V Swiss Services."
    )

    def handle(self, *args, **options):

        # ==========================================================
        # CATEGORÍAS
        # ==========================================================

        categories = [
            {
                "name_fr": "Rénovation et entretien",
                "name_de": "Renovation und Unterhalt",
                "name_it": "Ristrutturazione e manutenzione",
                "name_en": "Renovation and maintenance",
                "is_active": True,
            },
            {
                "name_fr": "Isolation et performance énergétique",
                "name_de": "Dämmung und Energieeffizienz",
                "name_it": "Isolamento ed efficienza energetica",
                "name_en": "Insulation and energy efficiency",
                "is_active": True,
            },
            {
                "name_fr": "Conseils aux propriétaires",
                "name_de": "Tipps für Eigentümer",
                "name_it": "Consigli per proprietari",
                "name_en": "Advice for property owners",
                "is_active": True,
            },
            {
                "name_fr": "Régies et professionnels",
                "name_de": "Immobilienverwaltungen und Fachpartner",
                "name_it": "Amministrazioni immobiliari e professionisti",
                "name_en": "Property managers and professionals",
                "is_active": True,
            },
            {
                "name_fr": "Aides et rénovation énergétique",
                "name_de": "Förderbeiträge und energetische Sanierung",
                "name_it": "Incentivi e risanamento energetico",
                "name_en": "Grants and energy renovation",
                "is_active": True,
            },
        ]

        # ==========================================================
        # TAGS
        # ==========================================================

        tags = [
            {
                "name_fr": "Rénovation",
                "name_de": "Renovation",
                "name_it": "Ristrutturazione",
                "name_en": "Renovation",
            },
            {
                "name_fr": "Isolation thermique",
                "name_de": "Wärmedämmung",
                "name_it": "Isolamento termico",
                "name_en": "Thermal insulation",
            },
            {
                "name_fr": "Façades",
                "name_de": "Fassaden",
                "name_it": "Facciate",
                "name_en": "Façades",
            },
            {
                "name_fr": "Maçonnerie",
                "name_de": "Maurerarbeiten",
                "name_it": "Muratura",
                "name_en": "Masonry",
            },
            {
                "name_fr": "Plâtrerie",
                "name_de": "Gipserarbeiten",
                "name_it": "Intonacatura",
                "name_en": "Plastering",
            },
            {
                "name_fr": "Peinture",
                "name_de": "Malerarbeiten",
                "name_it": "Pittura",
                "name_en": "Painting",
            },
            {
                "name_fr": "Entretien immobilier",
                "name_de": "Immobilienunterhalt",
                "name_it": "Manutenzione immobiliare",
                "name_en": "Property maintenance",
            },
            {
                "name_fr": "Régies immobilières",
                "name_de": "Immobilienverwaltungen",
                "name_it": "Amministrazioni immobiliari",
                "name_en": "Property management",
            },
            {
                "name_fr": "PPE",
                "name_de": "Stockwerkeigentum",
                "name_it": "Proprietà per piani",
                "name_en": "Condominium ownership",
            },
            {
                "name_fr": "Efficacité énergétique",
                "name_de": "Energieeffizienz",
                "name_it": "Efficienza energetica",
                "name_en": "Energy efficiency",
            },
            {
                "name_fr": "Subventions",
                "name_de": "Förderbeiträge",
                "name_it": "Incentivi",
                "name_en": "Grants",
            },
            {
                "name_fr": "Canton de Vaud",
                "name_de": "Kanton Waadt",
                "name_it": "Canton Vaud",
                "name_en": "Canton of Vaud",
            },
        ]

        # ==========================================================
        # SEGURIDAD · CATEGORÍAS
        # ==========================================================

        expected_categories = {
            item["name_fr"]
            for item in categories
        }

        existing_categories = list(
            BlogCategory.objects.values_list(
                "name_fr",
                flat=True,
            )
        )

        duplicated_categories = [
            name
            for name, count in Counter(existing_categories).items()
            if count > 1
        ]

        if duplicated_categories:
            raise CommandError(
                "Existen categorías de blog duplicadas: "
                + ", ".join(duplicated_categories)
                + ". No se modificó nada."
            )

        unexpected_categories = [
            name
            for name in existing_categories
            if name not in expected_categories
        ]

        if unexpected_categories:
            raise CommandError(
                "Existen categorías de blog no reconocidas: "
                + ", ".join(unexpected_categories)
                + ". No se modificó nada para proteger el contenido existente."
            )

        # ==========================================================
        # SEGURIDAD · TAGS
        # ==========================================================

        expected_tags = {
            item["name_fr"]
            for item in tags
        }

        existing_tags = list(
            BlogTag.objects.values_list(
                "name_fr",
                flat=True,
            )
        )

        duplicated_tags = [
            name
            for name, count in Counter(existing_tags).items()
            if count > 1
        ]

        if duplicated_tags:
            raise CommandError(
                "Existen etiquetas de blog duplicadas: "
                + ", ".join(duplicated_tags)
                + ". No se modificó nada."
            )

        unexpected_tags = [
            name
            for name in existing_tags
            if name not in expected_tags
        ]

        if unexpected_tags:
            raise CommandError(
                "Existen etiquetas de blog no reconocidas: "
                + ", ".join(unexpected_tags)
                + ". No se modificó nada para proteger el contenido existente."
            )

        # ==========================================================
        # CREAR / ACTUALIZAR
        # ==========================================================

        with transaction.atomic():

            created_categories = 0
            updated_categories = 0

            for item in categories:
                name_fr = item["name_fr"]

                defaults = item.copy()
                defaults.pop("name_fr")

                defaults["slug_fr"] = slugify(name_fr)
                defaults["slug_de"] = slugify(item["name_de"])
                defaults["slug_it"] = slugify(item["name_it"])
                defaults["slug_en"] = slugify(item["name_en"])

                obj, created = BlogCategory.objects.update_or_create(
                    name_fr=name_fr,
                    defaults=defaults,
                )

                if created:
                    created_categories += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"CREADA categoría: {obj.name_fr}"
                        )
                    )
                else:
                    updated_categories += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"ACTUALIZADA categoría: {obj.name_fr}"
                        )
                    )

            created_tags = 0
            updated_tags = 0

            for item in tags:
                name_fr = item["name_fr"]

                defaults = {
                    "name_de": item["name_de"],
                    "name_it": item["name_it"],
                    "name_en": item["name_en"],

                    "slug_fr": slugify(name_fr),
                    "slug_de": slugify(item["name_de"]),
                    "slug_it": slugify(item["name_it"]),
                    "slug_en": slugify(item["name_en"]),

                    "is_active": True,
                }

                obj, created = BlogTag.objects.update_or_create(
                    name_fr=name_fr,
                    defaults=defaults,
                )

                if created:
                    created_tags += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"CREADA etiqueta: {obj.name_fr}"
                        )
                    )
                else:
                    updated_tags += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"ACTUALIZADA etiqueta: {obj.name_fr}"
                        )
                    )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "Taxonomías del blog cargadas correctamente."
            )
        )

        self.stdout.write(
            f"Categorías creadas: {created_categories} | "
            f"actualizadas: {updated_categories}"
        )

        self.stdout.write(
            f"Etiquetas creadas: {created_tags} | "
            f"actualizadas: {updated_tags}"
        )
