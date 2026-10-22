from collections import Counter

from django.core.management.base import BaseCommand, CommandError

from core.models import ProcessStep


class Command(BaseCommand):
    help = "Crea o actualiza el proceso de trabajo de V&V Swiss Services."

    def handle(self, *args, **options):

        steps = [
            {
                "number": 1,

                "title_es": "Solicitud y primer contacto",
                "description_es": (
                    "El cliente nos presenta su proyecto, sus necesidades y, "
                    "cuando es posible, fotografías o información del inmueble. "
                    "Realizamos una primera evaluación para comprender el alcance "
                    "de los trabajos y definir los siguientes pasos."
                ),

                "title_fr": "Demande et premier contact",
                "description_fr": (
                    "Vous nous présentez votre projet, vos besoins et, lorsque "
                    "cela est possible, des photos ou des informations sur le bien. "
                    "Nous effectuons une première analyse afin de comprendre "
                    "l’étendue des travaux et de définir la suite de la démarche."
                ),

                "title_de": "Anfrage und Erstkontakt",
                "description_de": (
                    "Sie stellen uns Ihr Projekt, Ihre Anforderungen und, wenn "
                    "möglich, Fotos oder Informationen zur Immobilie vor. "
                    "Wir nehmen eine erste Einschätzung vor, um den Umfang der "
                    "Arbeiten zu verstehen und die nächsten Schritte festzulegen."
                ),

                "title_it": "Richiesta e primo contatto",
                "description_it": (
                    "Ci presentate il vostro progetto, le vostre esigenze e, "
                    "quando possibile, fotografie o informazioni sull’immobile. "
                    "Effettuiamo una prima valutazione per comprendere l’entità "
                    "dei lavori e definire i passaggi successivi."
                ),

                "title_en": "Enquiry and initial contact",
                "description_en": (
                    "You tell us about your project, requirements and, where "
                    "possible, provide photographs or information about the "
                    "property. We carry out an initial assessment to understand "
                    "the scope of the work and define the next steps."
                ),

                "icon": "",
                "is_active": True,
            },

            {
                "number": 2,

                "title_es": "Evaluación y visita técnica",
                "description_es": (
                    "Cuando el proyecto lo requiere, coordinamos una visita al "
                    "inmueble para evaluar las condiciones existentes, tomar "
                    "medidas y revisar los aspectos técnicos necesarios antes "
                    "de preparar una propuesta."
                ),

                "title_fr": "Évaluation et visite technique",
                "description_fr": (
                    "Lorsque le projet le nécessite, nous organisons une visite "
                    "sur place afin d’évaluer l’état existant, de prendre les "
                    "mesures utiles et d’examiner les aspects techniques avant "
                    "l’établissement de notre proposition."
                ),

                "title_de": "Beurteilung und technische Besichtigung",
                "description_de": (
                    "Wenn es das Projekt erfordert, vereinbaren wir eine "
                    "Besichtigung vor Ort. Dabei beurteilen wir die bestehende "
                    "Situation, nehmen die erforderlichen Masse auf und prüfen "
                    "die technischen Voraussetzungen für die Offerte."
                ),

                "title_it": "Valutazione e sopralluogo tecnico",
                "description_it": (
                    "Quando il progetto lo richiede, organizziamo un sopralluogo "
                    "per valutare la situazione esistente, effettuare le misurazioni "
                    "necessarie e verificare gli aspetti tecnici prima di "
                    "preparare la nostra proposta."
                ),

                "title_en": "Assessment and technical visit",
                "description_en": (
                    "Where required, we arrange a site visit to assess the existing "
                    "conditions, take the necessary measurements and review the "
                    "technical aspects before preparing our proposal."
                ),

                "icon": "",
                "is_active": True,
            },

            {
                "number": 3,

                "title_es": "Presupuesto claro",
                "description_es": (
                    "Preparamos una propuesta adaptada al proyecto, indicando "
                    "los trabajos previstos y las condiciones correspondientes. "
                    "Nuestro objetivo es que el cliente disponga de información "
                    "clara antes de tomar una decisión."
                ),

                "title_fr": "Devis clair et adapté",
                "description_fr": (
                    "Nous préparons une proposition adaptée au projet, avec une "
                    "présentation claire des travaux prévus et des conditions "
                    "correspondantes. Notre objectif est de vous permettre de "
                    "prendre votre décision sur une base transparente."
                ),

                "title_de": "Klare und passende Offerte",
                "description_de": (
                    "Wir erstellen eine auf das Projekt abgestimmte Offerte mit "
                    "einer klaren Beschreibung der vorgesehenen Arbeiten und der "
                    "entsprechenden Bedingungen. So verfügen Sie über eine "
                    "transparente Grundlage für Ihre Entscheidung."
                ),

                "title_it": "Preventivo chiaro e su misura",
                "description_it": (
                    "Prepariamo una proposta adeguata al progetto, indicando in "
                    "modo chiaro i lavori previsti e le relative condizioni. "
                    "Il nostro obiettivo è fornire tutte le informazioni necessarie "
                    "per prendere una decisione consapevole."
                ),

                "title_en": "Clear, tailored quotation",
                "description_en": (
                    "We prepare a proposal tailored to the project, clearly "
                    "setting out the proposed work and relevant conditions. "
                    "Our aim is to give you transparent information before "
                    "you make your decision."
                ),

                "icon": "",
                "is_active": True,
            },

            {
                "number": 4,

                "title_es": "Ejecución de los trabajos",
                "description_es": (
                    "Una vez aprobada la propuesta, organizamos la intervención "
                    "y ejecutamos los trabajos acordados con atención a la calidad, "
                    "la limpieza de la obra y el respeto de la planificación "
                    "establecida."
                ),

                "title_fr": "Réalisation des travaux",
                "description_fr": (
                    "Après validation du devis, nous organisons l’intervention "
                    "et réalisons les travaux convenus avec une attention "
                    "particulière portée à la qualité d’exécution, à la propreté "
                    "du chantier et au respect du planning défini."
                ),

                "title_de": "Ausführung der Arbeiten",
                "description_de": (
                    "Nach Freigabe der Offerte organisieren wir die Ausführung "
                    "und setzen die vereinbarten Arbeiten sorgfältig um. "
                    "Dabei achten wir besonders auf Qualität, Ordnung auf der "
                    "Baustelle und die vereinbarte Terminplanung."
                ),

                "title_it": "Esecuzione dei lavori",
                "description_it": (
                    "Dopo l’approvazione del preventivo, organizziamo l’intervento "
                    "ed eseguiamo i lavori concordati prestando particolare "
                    "attenzione alla qualità, all’ordine del cantiere e al rispetto "
                    "della pianificazione definita."
                ),

                "title_en": "Carrying out the work",
                "description_en": (
                    "Once the quotation has been approved, we organise the work "
                    "and carry out the agreed tasks with particular attention "
                    "to workmanship, site cleanliness and the agreed schedule."
                ),

                "icon": "",
                "is_active": True,
            },

            {
                "number": 5,

                "title_es": "Revisión y entrega",
                "description_es": (
                    "Al finalizar, revisamos los trabajos realizados y dejamos "
                    "el espacio en condiciones para su entrega. Mantenemos una "
                    "comunicación clara hasta el cierre del proyecto."
                ),

                "title_fr": "Contrôle et remise du chantier",
                "description_fr": (
                    "À la fin des travaux, nous contrôlons les prestations "
                    "réalisées et préparons les lieux pour la remise du chantier. "
                    "Nous maintenons une communication claire jusqu’à la clôture "
                    "du projet."
                ),

                "title_de": "Kontrolle und Übergabe",
                "description_de": (
                    "Nach Abschluss kontrollieren wir die ausgeführten Arbeiten "
                    "und bereiten die Räume für die Übergabe vor. Bis zum "
                    "Projektabschluss legen wir Wert auf eine klare Kommunikation."
                ),

                "title_it": "Controllo e consegna",
                "description_it": (
                    "Al termine dei lavori controlliamo gli interventi eseguiti "
                    "e prepariamo gli spazi per la consegna. Manteniamo una "
                    "comunicazione chiara fino alla conclusione del progetto."
                ),

                "title_en": "Final check and handover",
                "description_en": (
                    "At the end of the work, we review the completed services "
                    "and prepare the site for handover. We maintain clear "
                    "communication through to the completion of the project."
                ),

                "icon": "",
                "is_active": True,
            },
        ]

        # ==========================================================
        # SEGURIDAD
        # ==========================================================

        existing_numbers = list(
            ProcessStep.objects.values_list("number", flat=True)
        )

        duplicates = [
            number
            for number, count in Counter(existing_numbers).items()
            if count > 1
        ]

        if duplicates:
            raise CommandError(
                "Existen números de pasos duplicados en la base de datos: "
                + ", ".join(map(str, duplicates))
                + ". No se modificó nada."
            )

        expected_numbers = {item["number"] for item in steps}

        unexpected_numbers = sorted(
            number
            for number in existing_numbers
            if number not in expected_numbers
        )

        if unexpected_numbers:
            raise CommandError(
                "Existen pasos adicionales no reconocidos con los números: "
                + ", ".join(map(str, unexpected_numbers))
                + ". No se modificó nada para evitar sobrescribir contenido."
            )

        created_count = 0
        updated_count = 0

        # ==========================================================
        # CREAR / ACTUALIZAR
        # ==========================================================

        for item in steps:
            number = item["number"]

            defaults = item.copy()
            defaults.pop("number")

            obj, created = ProcessStep.objects.update_or_create(
                number=number,
                defaults=defaults,
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"CREADO: {obj.number}. {obj.title_fr}"
                    )
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"ACTUALIZADO: {obj.number}. {obj.title_fr}"
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
