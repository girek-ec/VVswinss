from collections import Counter

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from projects.models import ProjectType, BuildingType


class Command(BaseCommand):
    help = (
        "Crea o actualiza las taxonomías de proyectos "
        "de V&V Swiss Services."
    )

    def handle(self, *args, **options):

        # ==========================================================
        # TIPOS DE PROYECTO
        # ==========================================================

        project_types = [
            {
                "order": 1,
                "name_es": "Renovación interior",
                "name_fr": "Rénovation intérieure",
                "name_de": "Innenrenovation",
                "name_it": "Ristrutturazione interna",
                "name_en": "Interior renovation",
                "is_active": True,
            },
            {
                "order": 2,
                "name_es": "Renovación exterior",
                "name_fr": "Rénovation extérieure",
                "name_de": "Aussenrenovation",
                "name_it": "Ristrutturazione esterna",
                "name_en": "Exterior renovation",
                "is_active": True,
            },
            {
                "order": 3,
                "name_es": "Aislamiento térmico",
                "name_fr": "Isolation thermique",
                "name_de": "Wärmedämmung",
                "name_it": "Isolamento termico",
                "name_en": "Thermal insulation",
                "is_active": True,
            },
            {
                "order": 4,
                "name_es": "Rehabilitación y puesta a punto",
                "name_fr": "Remise en état",
                "name_de": "Instandsetzung",
                "name_it": "Ripristino",
                "name_en": "Refurbishment",
                "is_active": True,
            },
            {
                "order": 5,
                "name_es": "Mantenimiento inmobiliario",
                "name_fr": "Entretien immobilier",
                "name_de": "Immobilienunterhalt",
                "name_it": "Manutenzione immobiliare",
                "name_en": "Property maintenance",
                "is_active": True,
            },
        ]

        # ==========================================================
        # TIPOS DE EDIFICIO
        # ==========================================================

        building_types = [
            {
                "order": 1,
                "name_es": "Casa unifamiliar",
                "name_fr": "Maison individuelle",
                "name_de": "Einfamilienhaus",
                "name_it": "Casa unifamiliare",
                "name_en": "Detached house",
                "is_active": True,
            },
            {
                "order": 2,
                "name_es": "Apartamento / PPE",
                "name_fr": "Appartement / PPE",
                "name_de": "Wohnung / Stockwerkeigentum",
                "name_it": "Appartamento / proprietà per piani",
                "name_en": "Flat / condominium",
                "is_active": True,
            },
            {
                "order": 3,
                "name_es": "Edificio residencial",
                "name_fr": "Immeuble résidentiel",
                "name_de": "Wohngebäude",
                "name_it": "Edificio residenziale",
                "name_en": "Residential building",
                "is_active": True,
            },
            {
                "order": 4,
                "name_es": "Comercio",
                "name_fr": "Commerce",
                "name_de": "Geschäftslokal",
                "name_it": "Locale commerciale",
                "name_en": "Commercial premises",
                "is_active": True,
            },
            {
                "order": 5,
                "name_es": "Oficina",
                "name_fr": "Bureau",
                "name_de": "Büroräumlichkeiten",
                "name_it": "Ufficio",
                "name_en": "Office",
                "is_active": True,
            },
            {
                "order": 6,
                "name_es": "Edificio profesional",
                "name_fr": "Bâtiment professionnel",
                "name_de": "Gewerbegebäude",
                "name_it": "Edificio professionale",
                "name_en": "Commercial building",
                "is_active": True,
            },
        ]

        # ==========================================================
        # VALIDACIÓN · PROJECT TYPE
        # ==========================================================

        expected_project_types = {
            item["name_fr"]
            for item in project_types
        }

        existing_project_types = list(
            ProjectType.objects.values_list(
                "name_fr",
                flat=True,
            )
        )

        duplicate_project_types = [
            name
            for name, count in Counter(
                existing_project_types
            ).items()
            if count > 1
        ]

        if duplicate_project_types:
            raise CommandError(
                "Existen ProjectType duplicados: "
                + ", ".join(duplicate_project_types)
                + ". No se modificó nada."
            )

        unexpected_project_types = [
            name
            for name in existing_project_types
            if name not in expected_project_types
        ]

        if unexpected_project_types:
            raise CommandError(
                "Existen tipos de proyecto no reconocidos: "
                + ", ".join(unexpected_project_types)
                + ". No se modificó nada para proteger "
                  "el contenido existente."
            )

        # ==========================================================
        # VALIDACIÓN · BUILDING TYPE
        # ==========================================================

        expected_building_types = {
            item["name_fr"]
            for item in building_types
        }

        existing_building_types = list(
            BuildingType.objects.values_list(
                "name_fr",
                flat=True,
            )
        )

        duplicate_building_types = [
            name
            for name, count in Counter(
                existing_building_types
            ).items()
            if count > 1
        ]

        if duplicate_building_types:
            raise CommandError(
                "Existen BuildingType duplicados: "
                + ", ".join(duplicate_building_types)
                + ". No se modificó nada."
            )

        unexpected_building_types = [
            name
            for name in existing_building_types
            if name not in expected_building_types
        ]

        if unexpected_building_types:
            raise CommandError(
                "Existen tipos de edificio no reconocidos: "
                + ", ".join(unexpected_building_types)
                + ". No se modificó nada para proteger "
                  "el contenido existente."
            )

        # ==========================================================
        # CREAR / ACTUALIZAR
        # ==========================================================

        with transaction.atomic():

            created_projects = 0
            updated_projects = 0

            for item in project_types:
                name_fr = item["name_fr"]

                defaults = item.copy()
                defaults.pop("name_fr")

                obj, created = ProjectType.objects.update_or_create(
                    name_fr=name_fr,
                    defaults=defaults,
                )

                if created:
                    created_projects += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"CREADO ProjectType: {obj.name_fr}"
                        )
                    )
                else:
                    updated_projects += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"ACTUALIZADO ProjectType: {obj.name_fr}"
                        )
                    )

            created_buildings = 0
            updated_buildings = 0

            for item in building_types:
                name_fr = item["name_fr"]

                defaults = item.copy()
                defaults.pop("name_fr")

                obj, created = BuildingType.objects.update_or_create(
                    name_fr=name_fr,
                    defaults=defaults,
                )

                if created:
                    created_buildings += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"CREADO BuildingType: {obj.name_fr}"
                        )
                    )
                else:
                    updated_buildings += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"ACTUALIZADO BuildingType: {obj.name_fr}"
                        )
                    )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "Proceso completado."
            )
        )

        self.stdout.write(
            f"ProjectType creados: {created_projects} | "
            f"actualizados: {updated_projects}"
        )

        self.stdout.write(
            f"BuildingType creados: {created_buildings} | "
            f"actualizados: {updated_buildings}"
        )
