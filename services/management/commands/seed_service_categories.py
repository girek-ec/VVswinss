from django.core.management.base import BaseCommand

from services.models import ServiceCategory


CATEGORIES = [
    # ================================================================
    # 01 · ALBAÑILERÍA / MAÇONNERIE
    # ================================================================
    {
        "name_es": "Albañilería",
        "description_es": (
            "Obra menor y mayor, reparaciones, tabiques, revoques y fachadas."
        ),

        "name_fr": "Maçonnerie",
        "slug_fr": "maconnerie",
        "description_fr": (
            "Travaux de maçonnerie pour rénovations et transformations : "
            "petits et gros travaux, réparations, cloisons, crépis, "
            "reprises de maçonnerie et façades."
        ),

        "name_de": "Maurerarbeiten",
        "slug_de": "maurerarbeiten",
        "description_de": (
            "Maurerarbeiten für Renovierungen und Umbauten: kleinere und "
            "grössere Arbeiten, Reparaturen, Trennwände, Verputzarbeiten "
            "und Fassaden."
        ),

        "name_it": "Opere murarie",
        "slug_it": "opere-murarie",
        "description_it": (
            "Opere murarie per ristrutturazioni: lavori di piccola e grande "
            "entità, riparazioni, pareti divisorie, intonaci e facciate."
        ),

        "name_en": "Masonry",
        "slug_en": "masonry",
        "description_en": (
            "Minor and major masonry works, repairs, partitions, rendering "
            "and façade work for renovation and refurbishment projects."
        ),

        "icon": "fa-solid fa-trowel-bricks",
        "order": 1,
        "is_active": True,
    },

    # ================================================================
    # 02 · AISLAMIENTO TÉRMICO / ISOLATION THERMIQUE
    # ================================================================
    {
        "name_es": "Aislamiento térmico",
        "description_es": (
            "Aislamiento de fachadas mediante ITE o crépi aislante, áticos, "
            "sótanos y techos para mejorar la eficiencia energética."
        ),

        "name_fr": "Isolation thermique",
        "slug_fr": "isolation-thermique",
        "description_fr": (
            "Isolation thermique des façades, notamment par systèmes ITE "
            "et crépis isolants, ainsi que des combles, sous-sols et "
            "toitures afin d’améliorer la performance énergétique du bâtiment."
        ),

        "name_de": "Wärmedämmung",
        "slug_de": "waermedaemmung",
        "description_de": (
            "Wärmedämmung von Fassaden, Dachgeschossen, Kellern und Dächern "
            "zur Verbesserung der Energieeffizienz und des Wohnkomforts."
        ),

        "name_it": "Isolamento termico",
        "slug_it": "isolamento-termico",
        "description_it": (
            "Isolamento termico di facciate, sottotetti, cantine e coperture "
            "per migliorare l'efficienza energetica e il comfort dell'edificio."
        ),

        "name_en": "Thermal insulation",
        "slug_en": "thermal-insulation",
        "description_en": (
            "Thermal insulation for façades, including external wall "
            "insulation systems, lofts, basements and roofs to improve "
            "energy efficiency and indoor comfort."
        ),

        "icon": "fa-solid fa-temperature-half",
        "order": 2,
        "is_active": True,
    },

    # ================================================================
    # 03 · PLADUR / PLÂTRERIE
    # ================================================================
    {
        "name_es": "Pladur",
        "description_es": (
            "Tabiques, falsos techos, trasdosados y acabados interiores."
        ),

        "name_fr": "Plâtrerie",
        "slug_fr": "platrerie",
        "description_fr": (
            "Travaux de plâtrerie comprenant cloisons, faux plafonds, "
            "doublages et finitions intérieures pour les projets "
            "de rénovation et d’aménagement."
        ),

        "name_de": "Trockenbau & Gipserarbeiten",
        "slug_de": "trockenbau-gipserarbeiten",
        "description_de": (
            "Trockenbau- und Gipserarbeiten mit Trennwänden, abgehängten "
            "Decken, Wandverkleidungen und sauberen Innenausbauten."
        ),

        "name_it": "Cartongesso e gessatura",
        "slug_it": "cartongesso-gessatura",
        "description_it": (
            "Pareti divisorie, controsoffitti, contropareti e finiture "
            "interne in cartongesso e gesso."
        ),

        "name_en": "Plasterboard & dry lining",
        "slug_en": "plasterboard-dry-lining",
        "description_en": (
            "Plasterboard partitions, suspended ceilings, dry lining "
            "and interior finishing for renovation projects."
        ),

        "icon": "fa-solid fa-border-all",
        "order": 3,
        "is_active": True,
    },

    # ================================================================
    # 04 · PINTURA / PEINTURE
    # ================================================================
    {
        "name_es": "Pintura",
        "description_es": (
            "Pintura interior, exterior, fachadas y acabados decorativos."
        ),

        "name_fr": "Peinture",
        "slug_fr": "peinture",
        "description_fr": (
            "Travaux de peinture intérieure et extérieure, peinture de "
            "façades et finitions décoratives avec préparation soignée "
            "des supports."
        ),

        "name_de": "Malerarbeiten",
        "slug_de": "malerarbeiten",
        "description_de": (
            "Malerarbeiten im Innen- und Aussenbereich, Fassadenanstriche "
            "und dekorative Oberflächen."
        ),

        "name_it": "Pittura",
        "slug_it": "pittura",
        "description_it": (
            "Pittura interna ed esterna, facciate e finiture decorative."
        ),

        "name_en": "Painting & decorating",
        "slug_en": "painting-decorating",
        "description_en": (
            "Interior and exterior painting, façade painting and decorative "
            "finishes with careful surface preparation."
        ),

        "icon": "fa-solid fa-paint-roller",
        "order": 4,
        "is_active": True,
    },

    # ================================================================
    # 05 · LIMPIEZA DE OBRA
    # ================================================================
    {
        "name_es": "Limpieza de obra",
        "description_es": (
            "Limpieza de fin de obra y preparación del inmueble "
            "para la entrega de llaves."
        ),

        "name_fr": "Nettoyage de fin de chantier",
        "slug_fr": "nettoyage-fin-chantier",
        "description_fr": (
            "Nettoyage complet après travaux ou rénovation, élimination "
            "des poussières et résidus et préparation du bien avant "
            "la remise des clés."
        ),

        "name_de": "Bauendreinigung",
        "slug_de": "bauendreinigung",
        "description_de": (
            "Endreinigung nach Bau- oder Renovierungsarbeiten und "
            "Vorbereitung der Immobilie für die Schlüsselübergabe."
        ),

        "name_it": "Pulizia di fine cantiere",
        "slug_it": "pulizia-fine-cantiere",
        "description_it": (
            "Pulizia completa dopo lavori o ristrutturazioni e preparazione "
            "dell'immobile per la consegna delle chiavi."
        ),

        "name_en": "Post-construction cleaning",
        "slug_en": "post-construction-cleaning",
        "description_en": (
            "Thorough cleaning after building or renovation work, preparing "
            "the property for final handover and key collection."
        ),

        "icon": "fa-solid fa-broom",
        "order": 5,
        "is_active": True,
    },

    # ================================================================
    # 06 · SERVICIOS PARA RÉGIES
    # ================================================================
    {
        "name_es": "Servicios a gerencias inmobiliarias",
        "description_es": (
            "Mantenimiento y renovación de inmuebles en alquiler, incluida "
            "la renovación y puesta a punto entre inquilinos."
        ),

        "name_fr": "Services pour régies immobilières",
        "slug_fr": "services-regies-immobilieres",
        "description_fr": (
            "Services pour régies immobilières comprenant l’entretien, "
            "les réparations, la rénovation de biens locatifs et la remise "
            "en état rapide entre deux locataires."
        ),

        "name_de": "Dienstleistungen für Immobilienverwaltungen",
        "slug_de": "dienstleistungen-immobilienverwaltungen",
        "description_de": (
            "Unterhalt und Renovierung von Mietobjekten für "
            "Immobilienverwaltungen, einschliesslich schneller "
            "Instandsetzung bei Mieterwechsel."
        ),

        "name_it": "Servizi per amministrazioni immobiliari",
        "slug_it": "servizi-amministrazioni-immobiliari",
        "description_it": (
            "Manutenzione e ristrutturazione di immobili in locazione, "
            "compreso il ripristino tra un inquilino e l'altro."
        ),

        "name_en": "Services for property managers",
        "slug_en": "services-property-managers",
        "description_en": (
            "Maintenance and refurbishment of rental properties for property "
            "managers, including rapid renovation between tenancies."
        ),

        "icon": "fa-solid fa-building",
        "order": 6,
        "is_active": True,
    },
]


# Categorías antiguas que ya NO corresponden a la estructura definitiva.
OBSOLETE_NAMES_FR = [
    "Rénovation globale",
    "Maçonnerie & isolation",
    "Aménagement intérieur & finitions",
    "Entretien & gestion immobilière",
]


class Command(BaseCommand):
    help = (
        "Sincroniza las categorías de servicios de V&V Swiss Services "
        "con el brief definitivo."
    )

    def handle(self, *args, **options):

        self.stdout.write("")
        self.stdout.write("=" * 78)
        self.stdout.write(
            " V&V SWISS SERVICES · SINCRONIZACIÓN DE CATEGORÍAS"
        )
        self.stdout.write("=" * 78)
        self.stdout.write("")

        # ------------------------------------------------------------
        # DESACTIVAR CATEGORÍAS ANTIGUAS
        # ------------------------------------------------------------
        obsolete = ServiceCategory.objects.filter(
            name_fr__in=OBSOLETE_NAMES_FR
        )

        disabled_count = obsolete.update(is_active=False)

        if disabled_count:
            self.stdout.write(
                self.style.WARNING(
                    f"[DESACTIVADAS] {disabled_count} categorías antiguas"
                )
            )
            self.stdout.write("")

        created_count = 0
        updated_count = 0

        # ------------------------------------------------------------
        # CREAR / ACTUALIZAR LAS 6 CATEGORÍAS CORRECTAS
        # ------------------------------------------------------------
        for data in CATEGORIES:

            defaults = {
                "name_es": data["name_es"],
                "description_es": data["description_es"],

                "name_fr": data["name_fr"],
                "slug_fr": data["slug_fr"],
                "description_fr": data["description_fr"],

                "name_de": data["name_de"],
                "slug_de": data["slug_de"],
                "description_de": data["description_de"],

                "name_it": data["name_it"],
                "slug_it": data["slug_it"],
                "description_it": data["description_it"],

                "name_en": data["name_en"],
                "slug_en": data["slug_en"],
                "description_en": data["description_en"],

                "icon": data["icon"],
                "order": data["order"],
                "is_active": data["is_active"],
            }

            category, created = ServiceCategory.objects.update_or_create(
                name_fr=data["name_fr"],
                defaults=defaults,
            )

            if created:
                created_count += 1
                status = self.style.SUCCESS("CREADA")
            else:
                updated_count += 1
                status = self.style.WARNING("ACTUALIZADA")

            self.stdout.write(
                f"[{status}] "
                f"{category.order:02d} · "
                f"{category.name_fr}"
            )

        self.stdout.write("")
        self.stdout.write("-" * 78)

        self.stdout.write(
            self.style.SUCCESS(
                f"Proceso completado · "
                f"{created_count} creadas · "
                f"{updated_count} actualizadas · "
                f"{disabled_count} antiguas desactivadas."
            )
        )

        self.stdout.write("-" * 78)
        self.stdout.write("")