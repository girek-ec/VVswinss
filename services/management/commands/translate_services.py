from django.core.management.base import BaseCommand

from services.models import Service


# ============================================================
# TRADUCCIONES LOCALES
# ============================================================
# IMPORTANTE:
# - No utiliza Internet.
# - No utiliza OpenAI.
# - No utiliza ninguna API.
# - Solo contiene textos preparados manualmente.
#
# Cada servicio puede tener su propio bloque de contenido.
# ============================================================

SERVICE_TRANSLATIONS = {

    # ========================================================
    # SERVICE ID 1
    # Isolation thermique extérieure
    # ========================================================

    1: {

        # ----------------------------------------------------
        # FRANÇAIS
        # Idioma principal
        # ----------------------------------------------------

        "fr": {
            "name": "Isolation thermique extérieure",

            "hero_title_prefix": "Isolation thermique",
            "hero_title_suffix": "extérieure",

            "subtitle": (
                "Améliorez le confort et la performance énergétique "
                "de votre bâtiment."
            ),

            "summary": (
                "Isolation extérieure destinée à réduire les pertes "
                "thermiques, améliorer le confort et augmenter "
                "l’efficacité énergétique du bâtiment."
            ),

            "content": (
                "Nous réalisons des solutions d’isolation thermique "
                "extérieure adaptées aux bâtiments existants comme aux "
                "nouvelles constructions. Une enveloppe thermique "
                "correctement réalisée permet de limiter les pertes de "
                "chaleur, d’améliorer le confort intérieur et d’optimiser "
                "les performances énergétiques du bâtiment."
            ),

            "detail_1_title": "Une isolation performante et durable",

            "detail_1_text": (
                "L’isolation thermique extérieure permet d’améliorer "
                "l’enveloppe du bâtiment tout en limitant les ponts "
                "thermiques et les déperditions de chaleur."
            ),

            "detail_1_list": (
                "Réduction des pertes thermiques\n"
                "Amélioration du confort intérieur\n"
                "Réduction des ponts thermiques\n"
                "Protection durable des façades"
            ),

            "detail_2_title": "Une solution adaptée à votre bâtiment",

            "detail_2_text": (
                "Chaque projet est étudié selon les caractéristiques "
                "du bâtiment afin de proposer une solution d’isolation "
                "adaptée, efficace et durable."
            ),

            "detail_2_list": (
                "Analyse des besoins du bâtiment\n"
                "Choix de matériaux adaptés\n"
                "Mise en œuvre soignée\n"
                "Finitions adaptées à la façade"
            ),

            "cta_title": "Améliorez l’efficacité énergétique de votre bâtiment",

            "cta_text": (
                "Contactez-nous pour étudier votre projet d’isolation "
                "thermique extérieure et obtenir une solution adaptée "
                "à votre bâtiment."
            ),
        },

        # ----------------------------------------------------
        # DEUTSCH
        # ----------------------------------------------------

        "de": {
            "name": "Aussendämmung",

            "hero_title_prefix": "Thermische",
            "hero_title_suffix": "Aussendämmung",

            "subtitle": (
                "Verbessern Sie den Komfort und die Energieeffizienz "
                "Ihres Gebäudes."
            ),

            "summary": (
                "Aussendämmung zur Reduzierung von Wärmeverlusten, "
                "Verbesserung des Komforts und Steigerung der "
                "Energieeffizienz des Gebäudes."
            ),

            "content": (
                "Wir realisieren Lösungen für die Aussendämmung von "
                "bestehenden Gebäuden und Neubauten. Eine fachgerecht "
                "ausgeführte thermische Gebäudehülle reduziert "
                "Wärmeverluste, verbessert den Innenkomfort und optimiert "
                "die Energieeffizienz des Gebäudes."
            ),

            "detail_1_title": "Leistungsfähige und dauerhafte Wärmedämmung",

            "detail_1_text": (
                "Eine Aussendämmung verbessert die Gebäudehülle und "
                "reduziert gleichzeitig Wärmebrücken und Wärmeverluste."
            ),

            "detail_1_list": (
                "Reduzierung von Wärmeverlusten\n"
                "Verbesserung des Innenkomforts\n"
                "Reduzierung von Wärmebrücken\n"
                "Dauerhafter Schutz der Fassaden"
            ),

            "detail_2_title": "Eine passende Lösung für Ihr Gebäude",

            "detail_2_text": (
                "Jedes Projekt wird entsprechend den Eigenschaften des "
                "Gebäudes geprüft, um eine geeignete, effiziente und "
                "dauerhafte Dämmung zu realisieren."
            ),

            "detail_2_list": (
                "Analyse der Gebäudeanforderungen\n"
                "Auswahl geeigneter Materialien\n"
                "Sorgfältige Ausführung\n"
                "Passende Fassadenoberflächen"
            ),

            "cta_title": "Verbessern Sie die Energieeffizienz Ihres Gebäudes",

            "cta_text": (
                "Kontaktieren Sie uns, um Ihr Projekt für eine "
                "Aussendämmung zu besprechen und eine passende Lösung "
                "für Ihr Gebäude zu erhalten."
            ),
        },

        # ----------------------------------------------------
        # ITALIANO
        # ----------------------------------------------------

        "it": {
            "name": "Isolamento termico esterno",

            "hero_title_prefix": "Isolamento termico",
            "hero_title_suffix": "esterno",

            "subtitle": (
                "Migliorate il comfort e l’efficienza energetica "
                "del vostro edificio."
            ),

            "summary": (
                "Isolamento esterno progettato per ridurre le dispersioni "
                "termiche, migliorare il comfort e aumentare l’efficienza "
                "energetica dell’edificio."
            ),

            "content": (
                "Realizziamo soluzioni di isolamento termico esterno "
                "adatte sia agli edifici esistenti sia alle nuove "
                "costruzioni. Un involucro termico realizzato correttamente "
                "consente di limitare le dispersioni di calore, migliorare "
                "il comfort interno e ottimizzare le prestazioni "
                "energetiche dell’edificio."
            ),

            "detail_1_title": "Un isolamento efficiente e duraturo",

            "detail_1_text": (
                "L’isolamento termico esterno migliora l’involucro "
                "dell’edificio riducendo al tempo stesso i ponti termici "
                "e le dispersioni di calore."
            ),

            "detail_1_list": (
                "Riduzione delle dispersioni termiche\n"
                "Miglioramento del comfort interno\n"
                "Riduzione dei ponti termici\n"
                "Protezione duratura delle facciate"
            ),

            "detail_2_title": "Una soluzione adatta al vostro edificio",

            "detail_2_text": (
                "Ogni progetto viene studiato in base alle caratteristiche "
                "dell’edificio per proporre una soluzione di isolamento "
                "adeguata, efficiente e duratura."
            ),

            "detail_2_list": (
                "Analisi delle esigenze dell’edificio\n"
                "Scelta dei materiali adeguati\n"
                "Esecuzione accurata\n"
                "Finiture adatte alla facciata"
            ),

            "cta_title": "Migliorate l’efficienza energetica del vostro edificio",

            "cta_text": (
                "Contattateci per valutare il vostro progetto di "
                "isolamento termico esterno e ottenere una soluzione "
                "adatta al vostro edificio."
            ),
        },

        # ----------------------------------------------------
        # ENGLISH
        # ----------------------------------------------------

        "en": {
            "name": "External thermal insulation",

            "hero_title_prefix": "External thermal",
            "hero_title_suffix": "insulation",

            "subtitle": (
                "Improve the comfort and energy efficiency "
                "of your building."
            ),

            "summary": (
                "External insulation designed to reduce heat loss, "
                "improve comfort and increase the energy efficiency "
                "of the building."
            ),

            "content": (
                "We provide external thermal insulation solutions for "
                "both existing buildings and new constructions. A properly "
                "installed thermal envelope helps reduce heat loss, improve "
                "indoor comfort and optimise the building’s energy "
                "performance."
            ),

            "detail_1_title": "Efficient and durable thermal insulation",

            "detail_1_text": (
                "External thermal insulation improves the building "
                "envelope while reducing thermal bridges and heat loss."
            ),

            "detail_1_list": (
                "Reduced heat loss\n"
                "Improved indoor comfort\n"
                "Reduced thermal bridges\n"
                "Long-lasting façade protection"
            ),

            "detail_2_title": "A solution adapted to your building",

            "detail_2_text": (
                "Each project is assessed according to the characteristics "
                "of the building in order to provide a suitable, efficient "
                "and durable insulation solution."
            ),

            "detail_2_list": (
                "Assessment of building requirements\n"
                "Selection of suitable materials\n"
                "Careful installation\n"
                "Finishes adapted to the façade"
            ),

            "cta_title": "Improve your building’s energy efficiency",

            "cta_text": (
                "Contact us to discuss your external thermal insulation "
                "project and receive a solution adapted to your building."
            ),
        },
    },
}


# ============================================================
# COMANDO DJANGO
# ============================================================

class Command(BaseCommand):

    help = "Completa localmente los campos vacíos de los servicios."

    def add_arguments(self, parser):

        parser.add_argument(
            "--service",
            type=int,
            required=True,
            help="ID del servicio que se desea completar.",
        )

    def handle(self, *args, **options):

        service_id = options["service"]

        # ========================================================
        # COMPROBAR QUE TENEMOS DATOS LOCALES PARA ESE SERVICIO
        # ========================================================

        if service_id not in SERVICE_TRANSLATIONS:

            self.stdout.write(
                self.style.ERROR(
                    f"No existen traducciones locales configuradas "
                    f"para el servicio ID {service_id}."
                )
            )
            return

        # ========================================================
        # BUSCAR SERVICIO EN LA BASE DE DATOS
        # ========================================================

        try:
            service = Service.objects.get(pk=service_id)

        except Service.DoesNotExist:

            self.stdout.write(
                self.style.ERROR(
                    f"No existe el servicio ID {service_id}."
                )
            )
            return

        self.stdout.write("")
        self.stdout.write("=" * 70)

        self.stdout.write(
            self.style.SUCCESS(
                f"Procesando: {service.name_fr}"
            )
        )

        self.stdout.write("=" * 70)
        self.stdout.write("")

        translations = SERVICE_TRANSLATIONS[service_id]

        updated_fields = []
        preserved_fields = []

        # ========================================================
        # RECORRER LOS 4 IDIOMAS
        # ========================================================

        for language, fields in translations.items():

            self.stdout.write(
                self.style.HTTP_INFO(
                    f"IDIOMA: {language.upper()}"
                )
            )

            for field, new_value in fields.items():

                field_name = f"{field}_{language}"

                current_value = getattr(
                    service,
                    field_name,
                    "",
                )

                # =================================================
                # SOLO COMPLETAR SI EL CAMPO ESTÁ VACÍO
                # =================================================

                if not current_value or not str(current_value).strip():

                    setattr(
                        service,
                        field_name,
                        new_value,
                    )

                    updated_fields.append(field_name)

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  COMPLETADO: {field_name}"
                        )
                    )

                else:

                    preserved_fields.append(field_name)

                    self.stdout.write(
                        f"  CONSERVADO: {field_name}"
                    )

            self.stdout.write("")

        # ========================================================
        # GUARDAR
        # ========================================================

        if updated_fields:

            service.save()

            self.stdout.write(
                self.style.SUCCESS(
                    "Los nuevos datos fueron guardados."
                )
            )

        else:

            self.stdout.write(
                self.style.WARNING(
                    "No había campos vacíos para completar."
                )
            )

        # ========================================================
        # RESUMEN
        # ========================================================

        self.stdout.write("")
        self.stdout.write("=" * 70)

        self.stdout.write(
            self.style.SUCCESS(
                f"CAMPOS COMPLETADOS: {len(updated_fields)}"
            )
        )

        self.stdout.write(
            f"CAMPOS CONSERVADOS: {len(preserved_fields)}"
        )

        self.stdout.write("=" * 70)
        self.stdout.write("")

        # ========================================================
        # MOSTRAR LOS CAMPOS QUE SE MODIFICARON
        # ========================================================

        if updated_fields:

            self.stdout.write(
                self.style.SUCCESS(
                    "Campos nuevos:"
                )
            )

            for field_name in updated_fields:
                self.stdout.write(
                    f"  - {field_name}"
                )

        self.stdout.write("")