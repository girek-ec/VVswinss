from collections import Counter

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.models import FAQ, FAQCategory


class Command(BaseCommand):
    help = "Crea o actualiza las preguntas frecuentes de V&V Swiss Services."

    def handle(self, *args, **options):

        # ==========================================================
        # CATEGORÍAS
        # ==========================================================

        categories = [
            {
                "order": 1,
                "name_es": "Presupuestos y organización",
                "name_fr": "Devis et organisation",
                "name_de": "Offerten und Organisation",
                "name_it": "Preventivi e organizzazione",
                "name_en": "Quotations and organisation",
                "is_active": True,
            },
            {
                "order": 2,
                "name_es": "Renovación y trabajos",
                "name_fr": "Rénovation et travaux",
                "name_de": "Renovation und Bauarbeiten",
                "name_it": "Ristrutturazione e lavori",
                "name_en": "Renovation and building work",
                "is_active": True,
            },
            {
                "order": 3,
                "name_es": "Aislamiento y energía",
                "name_fr": "Isolation et énergie",
                "name_de": "Dämmung und Energie",
                "name_it": "Isolamento ed energia",
                "name_en": "Insulation and energy efficiency",
                "is_active": True,
            },
            {
                "order": 4,
                "name_es": "Profesionales y gerencias",
                "name_fr": "Professionnels et régies",
                "name_de": "Fachpartner und Immobilienverwaltungen",
                "name_it": "Professionisti e amministrazioni immobiliari",
                "name_en": "Professionals and property managers",
                "is_active": True,
            },
        ]

        # ==========================================================
        # FAQ
        # ==========================================================

        faqs = [
            # ------------------------------------------------------
            # DEVIS ET ORGANISATION
            # ------------------------------------------------------
            {
                "category_fr": "Devis et organisation",
                "order": 1,

                "question_fr": "Comment demander un devis pour mon projet ?",
                "answer_fr": (
                    "Vous pouvez nous transmettre votre demande en décrivant les "
                    "travaux souhaités et, si possible, en joignant des photos du "
                    "bien. Ces premières informations nous permettent de mieux "
                    "comprendre votre projet et de déterminer si une visite "
                    "technique est nécessaire avant l’établissement du devis."
                ),

                "question_de": "Wie kann ich eine Offerte für mein Projekt anfragen?",
                "answer_de": (
                    "Sie können uns Ihre Anfrage mit einer Beschreibung der "
                    "gewünschten Arbeiten senden und, wenn möglich, Fotos der "
                    "Immobilie beifügen. Diese ersten Angaben helfen uns, das "
                    "Projekt einzuschätzen und zu bestimmen, ob vor der Erstellung "
                    "der Offerte eine technische Besichtigung erforderlich ist."
                ),

                "question_it": "Come posso richiedere un preventivo per il mio progetto?",
                "answer_it": (
                    "Potete inviarci la vostra richiesta descrivendo i lavori "
                    "desiderati e, se possibile, allegando fotografie dell’immobile. "
                    "Queste prime informazioni ci permettono di comprendere meglio "
                    "il progetto e di stabilire se sia necessario un sopralluogo "
                    "tecnico prima di preparare il preventivo."
                ),

                "question_en": "How can I request a quotation for my project?",
                "answer_en": (
                    "You can send us an enquiry describing the work required and, "
                    "where possible, attach photographs of the property. This "
                    "initial information helps us understand the project and "
                    "determine whether a technical site visit is required before "
                    "we prepare a quotation."
                ),

                "is_active": True,
            },

            {
                "category_fr": "Devis et organisation",
                "order": 2,

                "question_fr": "Une visite technique est-elle toujours nécessaire ?",
                "answer_fr": (
                    "Pas nécessairement. Certains travaux peuvent faire l’objet "
                    "d’une première évaluation sur la base des informations et "
                    "photos transmises. Pour les projets plus complexes ou lorsque "
                    "des mesures et vérifications sont nécessaires, une visite sur "
                    "place permet d’établir une proposition plus précise."
                ),

                "question_de": "Ist eine technische Besichtigung immer erforderlich?",
                "answer_de": (
                    "Nicht unbedingt. Bestimmte Arbeiten können zunächst anhand "
                    "der übermittelten Informationen und Fotos beurteilt werden. "
                    "Bei komplexeren Projekten oder wenn Masse und technische "
                    "Abklärungen erforderlich sind, ermöglicht eine Besichtigung "
                    "vor Ort eine präzisere Offerte."
                ),

                "question_it": "È sempre necessario un sopralluogo tecnico?",
                "answer_it": (
                    "Non necessariamente. Alcuni lavori possono essere valutati "
                    "inizialmente sulla base delle informazioni e delle fotografie "
                    "fornite. Per progetti più complessi, o quando sono necessarie "
                    "misurazioni e verifiche tecniche, un sopralluogo consente di "
                    "preparare una proposta più precisa."
                ),

                "question_en": "Is a technical site visit always required?",
                "answer_en": (
                    "Not necessarily. Some work can initially be assessed from "
                    "the information and photographs provided. For more complex "
                    "projects, or where measurements and technical checks are "
                    "required, a site visit allows us to prepare a more accurate "
                    "quotation."
                ),

                "is_active": True,
            },

            # ------------------------------------------------------
            # RÉNOVATION ET TRAVAUX
            # ------------------------------------------------------
            {
                "category_fr": "Rénovation et travaux",
                "order": 3,

                "question_fr": "Quels types de travaux réalisez-vous ?",
                "answer_fr": (
                    "V&V Swiss Services intervient notamment en maçonnerie, "
                    "isolation thermique, plâtrerie, peinture, finitions, "
                    "nettoyage de fin de chantier, entretien et remise en état "
                    "de biens immobiliers. Nous réalisons des travaux de rénovation "
                    "intérieure et extérieure selon les besoins du projet."
                ),

                "question_de": "Welche Arbeiten führt V&V Swiss Services aus?",
                "answer_de": (
                    "V&V Swiss Services führt unter anderem Maurerarbeiten, "
                    "Wärmedämmungen, Gipserarbeiten, Malerarbeiten, Ausbauarbeiten, "
                    "Endreinigungen sowie Unterhalts- und Instandsetzungsarbeiten "
                    "an Immobilien aus. Wir übernehmen Renovationen im Innen- und "
                    "Aussenbereich entsprechend den Anforderungen des Projekts."
                ),

                "question_it": "Quali tipi di lavori realizzate?",
                "answer_it": (
                    "V&V Swiss Services realizza opere di muratura, isolamento "
                    "termico, intonacatura e cartongesso, pittura, finiture, "
                    "pulizia di fine cantiere, manutenzione e ripristino di "
                    "immobili. Interveniamo su ristrutturazioni interne ed esterne "
                    "in funzione delle esigenze del progetto."
                ),

                "question_en": "What types of work do you undertake?",
                "answer_en": (
                    "V&V Swiss Services undertakes masonry, thermal insulation, "
                    "plastering and dry lining, painting, finishing works, "
                    "end-of-build cleaning, property maintenance and refurbishment. "
                    "We carry out both interior and exterior renovation work "
                    "according to the requirements of each project."
                ),

                "is_active": True,
            },

            {
                "category_fr": "Rénovation et travaux",
                "order": 4,

                "question_fr": "Pouvez-vous coordonner plusieurs corps de métier ?",
                "answer_fr": (
                    "Oui. L’un des avantages de V&V Swiss Services est de réunir "
                    "plusieurs métiers de la rénovation afin de simplifier la "
                    "coordination du chantier. Selon le projet, vous bénéficiez "
                    "ainsi d’un interlocuteur unique pour organiser les différentes "
                    "interventions prévues."
                ),

                "question_de": "Können Sie mehrere Gewerke koordinieren?",
                "answer_de": (
                    "Ja. V&V Swiss Services bündelt mehrere Renovationsbereiche, "
                    "um die Koordination auf der Baustelle zu vereinfachen. "
                    "Je nach Projekt verfügen Sie dadurch über einen zentralen "
                    "Ansprechpartner für die Organisation der verschiedenen "
                    "Arbeitsschritte."
                ),

                "question_it": "Potete coordinare più specializzazioni?",
                "answer_it": (
                    "Sì. Uno dei vantaggi di V&V Swiss Services è riunire diverse "
                    "competenze della ristrutturazione per semplificare il "
                    "coordinamento del cantiere. A seconda del progetto, disponete "
                    "così di un unico interlocutore per organizzare i diversi "
                    "interventi."
                ),

                "question_en": "Can you coordinate several trades within one project?",
                "answer_en": (
                    "Yes. One of the advantages of V&V Swiss Services is that we "
                    "bring several renovation trades together to simplify site "
                    "coordination. Depending on the project, this gives you a "
                    "single point of contact for organising the different stages "
                    "of the work."
                ),

                "is_active": True,
            },

            # ------------------------------------------------------
            # ISOLATION ET ÉNERGIE
            # ------------------------------------------------------
            {
                "category_fr": "Isolation et énergie",
                "order": 5,

                "question_fr": "Quels travaux d’isolation proposez-vous ?",
                "answer_fr": (
                    "Nous intervenons notamment sur l’isolation thermique des "
                    "façades, y compris les systèmes d’isolation thermique par "
                    "l’extérieur, ainsi que sur certains projets concernant "
                    "combles, sous-sols et toitures. La solution adaptée dépend "
                    "toujours de la configuration et de l’état du bâtiment."
                ),

                "question_de": "Welche Dämmarbeiten bieten Sie an?",
                "answer_de": (
                    "Wir führen unter anderem Wärmedämmungen an Fassaden, "
                    "einschliesslich Aussenwärmedämmungen, sowie je nach Projekt "
                    "Arbeiten an Dachräumen, Untergeschossen und Dächern aus. "
                    "Welche Lösung geeignet ist, hängt von der Bauweise und dem "
                    "Zustand des Gebäudes ab."
                ),

                "question_it": "Quali lavori di isolamento proponete?",
                "answer_it": (
                    "Interveniamo in particolare sull’isolamento termico delle "
                    "facciate, compresi i sistemi di isolamento esterno, nonché "
                    "su determinati progetti relativi a sottotetti, cantine e "
                    "coperture. La soluzione appropriata dipende sempre dalla "
                    "configurazione e dallo stato dell’edificio."
                ),

                "question_en": "What insulation work do you provide?",
                "answer_en": (
                    "We undertake thermal insulation work on façades, including "
                    "external wall insulation systems, as well as selected projects "
                    "involving lofts, basements and roofs. The most appropriate "
                    "solution always depends on the construction and condition "
                    "of the building."
                ),

                "is_active": True,
            },

            {
                "category_fr": "Isolation et énergie",
                "order": 6,

                "question_fr": (
                    "Existe-t-il des aides pour les travaux d’isolation dans le canton de Vaud ?"
                ),
                "answer_fr": (
                    "Des programmes d’aide à l’amélioration énergétique des "
                    "bâtiments peuvent être disponibles dans le canton de Vaud. "
                    "Les conditions, montants et critères d’éligibilité dépendent "
                    "du programme et du projet. Il est donc recommandé de vérifier "
                    "les conditions officielles applicables avant le démarrage "
                    "des travaux."
                ),

                "question_de": (
                    "Gibt es im Kanton Waadt Förderbeiträge für Dämmarbeiten?"
                ),
                "answer_de": (
                    "Im Kanton Waadt können Förderprogramme für energetische "
                    "Gebäudesanierungen verfügbar sein. Voraussetzungen, Beiträge "
                    "und Förderkriterien hängen vom jeweiligen Programm und Projekt "
                    "ab. Die aktuellen offiziellen Bedingungen sollten deshalb "
                    "vor Beginn der Arbeiten geprüft werden."
                ),

                "question_it": (
                    "Esistono incentivi per i lavori di isolamento nel Canton Vaud?"
                ),
                "answer_it": (
                    "Nel Canton Vaud possono essere disponibili programmi di "
                    "incentivazione per il miglioramento energetico degli edifici. "
                    "Condizioni, importi e criteri di ammissibilità dipendono dal "
                    "programma e dal progetto. È quindi opportuno verificare le "
                    "condizioni ufficiali applicabili prima dell’inizio dei lavori."
                ),

                "question_en": (
                    "Are grants available for insulation work in the Canton of Vaud?"
                ),
                "answer_en": (
                    "Financial support programmes for improving the energy "
                    "performance of buildings may be available in the Canton of "
                    "Vaud. Eligibility, amounts and conditions depend on the "
                    "programme and the individual project, so the current official "
                    "requirements should be checked before work begins."
                ),

                "is_active": True,
            },

            # ------------------------------------------------------
            # PROFESSIONNELS ET RÉGIES
            # ------------------------------------------------------
            {
                "category_fr": "Professionnels et régies",
                "order": 7,

                "question_fr": "Travaillez-vous avec les régies immobilières ?",
                "answer_fr": (
                    "Oui. V&V Swiss Services intervient pour les régies et les "
                    "administrateurs de biens dans le cadre de travaux d’entretien, "
                    "de rénovation et de remise en état de logements ou locaux, "
                    "notamment lors des changements de locataires."
                ),

                "question_de": "Arbeiten Sie mit Immobilienverwaltungen zusammen?",
                "answer_de": (
                    "Ja. V&V Swiss Services unterstützt Immobilienverwaltungen "
                    "und Bewirtschafter bei Unterhalts-, Renovations- und "
                    "Instandsetzungsarbeiten an Wohnungen und anderen Objekten, "
                    "unter anderem bei Mieterwechseln."
                ),

                "question_it": "Collaborate con amministrazioni immobiliari?",
                "answer_it": (
                    "Sì. V&V Swiss Services collabora con amministrazioni e "
                    "gestori immobiliari per lavori di manutenzione, "
                    "ristrutturazione e ripristino di appartamenti e altri "
                    "immobili, anche in occasione dei cambi di inquilino."
                ),

                "question_en": "Do you work with property management companies?",
                "answer_en": (
                    "Yes. V&V Swiss Services works with property managers and "
                    "property administrators on maintenance, renovation and "
                    "refurbishment projects for residential and other properties, "
                    "including work required between tenancies."
                ),

                "is_active": True,
            },

            {
                "category_fr": "Professionnels et régies",
                "order": 8,

                "question_fr": (
                    "Travaillez-vous également avec les entreprises générales et les architectes ?"
                ),
                "answer_fr": (
                    "Oui. Nous pouvons intervenir comme partenaire pour des travaux "
                    "de rénovation spécifiques ou pour plusieurs prestations, "
                    "selon les besoins du chantier et l’organisation définie avec "
                    "l’entreprise générale, le maître d’œuvre ou l’architecte."
                ),

                "question_de": (
                    "Arbeiten Sie auch mit Generalunternehmen und Architekten zusammen?"
                ),
                "answer_de": (
                    "Ja. Je nach Projekt können wir als Partner für einzelne "
                    "Renovationsarbeiten oder für mehrere Leistungen eingesetzt "
                    "werden. Die Zusammenarbeit richtet sich nach den Anforderungen "
                    "der Baustelle und der mit Generalunternehmen, Bauleitung oder "
                    "Architektur definierten Organisation."
                ),

                "question_it": (
                    "Collaborate anche con imprese generali e architetti?"
                ),
                "answer_it": (
                    "Sì. Possiamo intervenire come partner per specifici lavori "
                    "di ristrutturazione o per più prestazioni, in funzione delle "
                    "esigenze del cantiere e dell’organizzazione concordata con "
                    "l’impresa generale, la direzione lavori o l’architetto."
                ),

                "question_en": (
                    "Do you also work with main contractors and architects?"
                ),
                "answer_en": (
                    "Yes. We can work as a specialist partner for individual "
                    "renovation tasks or several services, depending on the site "
                    "requirements and the arrangements agreed with the main "
                    "contractor, project management team or architect."
                ),

                "is_active": True,
            },
        ]

        # ==========================================================
        # VALIDACIÓN DE SEGURIDAD
        # ==========================================================

        expected_category_names = {
            item["name_fr"]
            for item in categories
        }

        existing_category_names = list(
            FAQCategory.objects.values_list("name_fr", flat=True)
        )

        duplicate_categories = [
            name
            for name, count in Counter(existing_category_names).items()
            if count > 1
        ]

        if duplicate_categories:
            raise CommandError(
                "Existen categorías FAQ duplicadas: "
                + ", ".join(duplicate_categories)
                + ". No se modificó nada."
            )

        unexpected_categories = [
            name
            for name in existing_category_names
            if name not in expected_category_names
        ]

        if unexpected_categories:
            raise CommandError(
                "Existen categorías FAQ no reconocidas: "
                + ", ".join(unexpected_categories)
                + ". No se modificó nada para proteger el contenido existente."
            )

        expected_questions = {
            item["question_fr"]
            for item in faqs
        }

        existing_questions = list(
            FAQ.objects.values_list("question_fr", flat=True)
        )

        duplicate_questions = [
            question
            for question, count in Counter(existing_questions).items()
            if count > 1
        ]

        if duplicate_questions:
            raise CommandError(
                "Existen preguntas FAQ duplicadas. "
                "No se modificó nada."
            )

        unexpected_questions = [
            question
            for question in existing_questions
            if question not in expected_questions
        ]

        if unexpected_questions:
            raise CommandError(
                "Existen preguntas FAQ no reconocidas en la base de datos. "
                "No se modificó nada para proteger el contenido existente."
            )

        # ==========================================================
        # CREACIÓN / ACTUALIZACIÓN
        # ==========================================================

        with transaction.atomic():

            category_map = {}

            for item in categories:
                name_fr = item["name_fr"]

                defaults = item.copy()
                defaults.pop("name_fr")

                obj, created = FAQCategory.objects.update_or_create(
                    name_fr=name_fr,
                    defaults=defaults,
                )

                category_map[name_fr] = obj

                action = "CREADA" if created else "ACTUALIZADA"

                self.stdout.write(
                    f"{action} categoría: {obj.name_fr}"
                )

            created_count = 0
            updated_count = 0

            for item in faqs:
                category_fr = item["category_fr"]
                question_fr = item["question_fr"]

                defaults = item.copy()

                defaults.pop("category_fr")
                defaults.pop("question_fr")

                defaults["category"] = category_map[category_fr]

                obj, created = FAQ.objects.update_or_create(
                    question_fr=question_fr,
                    defaults=defaults,
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"CREADA FAQ: {obj.question_fr}"
                        )
                    )
                else:
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"ACTUALIZADA FAQ: {obj.question_fr}"
                        )
                    )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Proceso completado. "
                f"FAQ creadas: {created_count} | "
                f"FAQ actualizadas: {updated_count}"
            )
        )
