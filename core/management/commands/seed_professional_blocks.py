from django.core.management.base import BaseCommand, CommandError

from core.models import ProfessionalBlock, ProfessionalPage


class Command(BaseCommand):
    help = "Create or update the default content blocks for the Professionals page."

    def handle(self, *args, **options):
        page = (
            ProfessionalPage.objects
            .filter(is_active=True)
            .order_by("id")
            .first()
        )

        if not page:
            raise CommandError(
                "No active ProfessionalPage was found. Create or activate one first."
            )

        blocks = [
            {
                "layout": ProfessionalBlock.LAYOUT_IMAGE_RIGHT,
                "title_fr": "À qui s’adressent nos services ?",
                "text_fr": (
                    "V&V Swiss Services accompagne les régies immobilières, "
                    "administrateurs PPE, entreprises générales, constructeurs, "
                    "architectes et autres professionnels ayant besoin d’un partenaire "
                    "fiable pour leurs travaux de rénovation, d’entretien et de remise en état."
                ),
                "title_de": "Für wen sind unsere Dienstleistungen gedacht?",
                "text_de": (
                    "V&V Swiss Services unterstützt Immobilienverwaltungen, "
                    "Stockwerkeigentümergemeinschaften, Generalunternehmen, Bauunternehmen, "
                    "Architekten und weitere Fachkunden, die einen zuverlässigen Partner "
                    "für Renovationen, Unterhalt und Instandsetzungen benötigen."
                ),
                "title_it": "A chi sono rivolti i nostri servizi?",
                "text_it": (
                    "V&V Swiss Services affianca amministrazioni immobiliari, "
                    "proprietà per piani, imprese generali, costruttori, architetti "
                    "e altri professionisti che cercano un partner affidabile per lavori "
                    "di ristrutturazione, manutenzione e ripristino."
                ),
                "title_en": "Who are our professional services for?",
                "text_en": (
                    "V&V Swiss Services works with property managers, condominium "
                    "administrators, general contractors, builders, architects and other "
                    "professionals looking for a reliable partner for renovation, maintenance "
                    "and refurbishment work."
                ),
                "title_es": "¿A quiénes están dirigidos nuestros servicios?",
                "text_es": (
                    "V&V Swiss Services acompaña a administradores inmobiliarios, "
                    "administraciones de propiedad horizontal, empresas generales, constructores, "
                    "arquitectos y otros profesionales que necesitan un socio fiable para trabajos "
                    "de renovación, mantenimiento y puesta a punto."
                ),
                "icon": "fa-solid fa-building",
                "order": 1,
                "is_active": True,
            },
            {
                "layout": ProfessionalBlock.LAYOUT_IMAGE_LEFT,
                "title_fr": "Remise en état entre locataires",
                "text_fr": (
                    "Lors d’un changement de locataire, nous pouvons coordonner les travaux "
                    "nécessaires pour remettre rapidement le logement ou le local en état. "
                    "L’intervention est organisée selon les priorités du bien, les délais "
                    "disponibles et les prestations requises afin de préparer efficacement "
                    "la prochaine occupation."
                ),
                "title_de": "Instandsetzung zwischen zwei Mietverhältnissen",
                "text_de": (
                    "Bei einem Mieterwechsel können wir die notwendigen Arbeiten koordinieren, "
                    "damit Wohnung oder Objekt rasch wieder bezugsbereit sind. Die Arbeiten "
                    "werden nach den Prioritäten des Objekts, den verfügbaren Fristen und den "
                    "erforderlichen Leistungen organisiert."
                ),
                "title_it": "Ripristino tra un inquilino e l’altro",
                "text_it": (
                    "In occasione di un cambio di inquilino possiamo coordinare i lavori "
                    "necessari per ripristinare rapidamente l’abitazione o il locale. "
                    "L’intervento viene organizzato in funzione delle priorità dell’immobile, "
                    "delle tempistiche disponibili e delle prestazioni richieste."
                ),
                "title_en": "Refurbishment between tenancies",
                "text_en": (
                    "When tenants change, we can coordinate the work required to prepare "
                    "the property efficiently for its next occupation. The intervention is "
                    "organised around the property's priorities, available timeframes and "
                    "the services required."
                ),
                "title_es": "Puesta a punto entre arrendamientos",
                "text_es": (
                    "Cuando cambia un inquilino, podemos coordinar los trabajos necesarios "
                    "para preparar rápidamente la vivienda o el local para su próxima ocupación. "
                    "La intervención se organiza según las prioridades del inmueble, los plazos "
                    "disponibles y los trabajos requeridos."
                ),
                "icon": "fa-solid fa-key",
                "order": 2,
                "is_active": True,
            },
            {
                "layout": ProfessionalBlock.LAYOUT_CARD,
                "title_fr": "Un interlocuteur unique",
                "text_fr": (
                    "Un seul point de contact simplifie le suivi de vos travaux. "
                    "Nous coordonnons les différentes interventions afin de faciliter "
                    "les échanges, le suivi de l’avancement et l’organisation générale "
                    "du projet."
                ),
                "title_de": "Ein zentraler Ansprechpartner",
                "text_de": (
                    "Ein zentraler Ansprechpartner vereinfacht die Betreuung Ihrer Arbeiten. "
                    "Wir koordinieren die verschiedenen Einsätze und erleichtern damit "
                    "die Kommunikation, die Fortschrittskontrolle und die gesamte "
                    "Projektorganisation."
                ),
                "title_it": "Un unico interlocutore",
                "text_it": (
                    "Un unico punto di contatto semplifica la gestione dei lavori. "
                    "Coordiniamo i diversi interventi per facilitare la comunicazione, "
                    "il controllo dell’avanzamento e l’organizzazione generale del progetto."
                ),
                "title_en": "One dedicated point of contact",
                "text_en": (
                    "A single point of contact makes your work easier to manage. "
                    "We coordinate the different interventions to simplify communication, "
                    "progress monitoring and the overall organisation of the project."
                ),
                "title_es": "Un único interlocutor",
                "text_es": (
                    "Un solo punto de contacto simplifica el seguimiento de los trabajos. "
                    "Coordinamos las diferentes intervenciones para facilitar la comunicación, "
                    "el control del avance y la organización general del proyecto."
                ),
                "icon": "fa-solid fa-handshake",
                "order": 3,
                "is_active": True,
            },
            {
                "layout": ProfessionalBlock.LAYOUT_TEXT,
                "title_fr": "Réactivité, clarté et qualité d’exécution",
                "text_fr": (
                    "Nous privilégions une organisation claire, des échanges simples et "
                    "un suivi professionnel à chaque étape. Notre objectif est de faciliter "
                    "la gestion de vos interventions tout en maintenant une exécution soignée "
                    "et adaptée aux exigences du projet."
                ),
                "title_de": "Reaktionsfähigkeit, Klarheit und Ausführungsqualität",
                "text_de": (
                    "Wir setzen auf eine klare Organisation, einfache Kommunikation und "
                    "eine professionelle Begleitung in jeder Phase. Unser Ziel ist es, "
                    "die Verwaltung Ihrer Arbeiten zu erleichtern und gleichzeitig eine "
                    "sorgfältige, projektgerechte Ausführung sicherzustellen."
                ),
                "title_it": "Reattività, chiarezza e qualità di esecuzione",
                "text_it": (
                    "Privilegiamo un’organizzazione chiara, una comunicazione semplice e "
                    "un monitoraggio professionale in ogni fase. Il nostro obiettivo è "
                    "facilitare la gestione degli interventi mantenendo un’esecuzione curata "
                    "e adeguata alle esigenze del progetto."
                ),
                "title_en": "Responsiveness, clarity and quality of execution",
                "text_en": (
                    "We favour clear organisation, straightforward communication and "
                    "professional follow-up at every stage. Our aim is to make your work "
                    "easier to manage while maintaining careful execution suited to the "
                    "requirements of each project."
                ),
                "title_es": "Rapidez, claridad y calidad de ejecución",
                "text_es": (
                    "Priorizamos una organización clara, una comunicación sencilla y un "
                    "seguimiento profesional en cada etapa. Nuestro objetivo es facilitar "
                    "la gestión de las intervenciones manteniendo una ejecución cuidada y "
                    "adaptada a las necesidades de cada proyecto."
                ),
                "icon": "fa-solid fa-circle-check",
                "order": 4,
                "is_active": True,
            },
            {
                "layout": ProfessionalBlock.LAYOUT_CTA,
                "title_fr": "Un partenaire fiable pour vos projets immobiliers",
                "text_fr": (
                    "Vous recherchez un partenaire pour une intervention ponctuelle ou "
                    "une collaboration régulière ? Présentez-nous votre projet et vos besoins. "
                    "Nous vous répondrons avec une approche adaptée à votre organisation "
                    "et à votre bien immobilier."
                ),
                "title_de": "Ein zuverlässiger Partner für Ihre Immobilienprojekte",
                "text_de": (
                    "Suchen Sie einen Partner für einen einzelnen Auftrag oder eine regelmässige "
                    "Zusammenarbeit? Stellen Sie uns Ihr Projekt und Ihre Anforderungen vor. "
                    "Wir schlagen Ihnen eine Lösung vor, die zu Ihrer Organisation und Ihrem "
                    "Objekt passt."
                ),
                "title_it": "Un partner affidabile per i vostri progetti immobiliari",
                "text_it": (
                    "Cercate un partner per un intervento puntuale o per una collaborazione "
                    "continuativa? Presentateci il vostro progetto e le vostre esigenze. "
                    "Vi proporremo un approccio adatto alla vostra organizzazione e al vostro immobile."
                ),
                "title_en": "A reliable partner for your property projects",
                "text_en": (
                    "Looking for a partner for a one-off intervention or an ongoing collaboration? "
                    "Tell us about your project and requirements. We will propose an approach "
                    "suited to your organisation and your property."
                ),
                "title_es": "Un socio fiable para sus proyectos inmobiliarios",
                "text_es": (
                    "¿Busca un socio para una intervención puntual o para una colaboración continua? "
                    "Cuéntenos su proyecto y sus necesidades. Le propondremos un enfoque adaptado "
                    "a su organización y a su inmueble."
                ),
                "icon": "fa-solid fa-arrow-right",
                "order": 5,
                "is_active": True,
            },
        ]

        created_count = 0
        updated_count = 0

        for data in blocks:
            title_fr = data["title_fr"]

            defaults = {
                key: value
                for key, value in data.items()
                if key != "title_fr"
            }

            block, created = ProfessionalBlock.objects.update_or_create(
                page=page,
                title_fr=title_fr,
                defaults=defaults,
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"CREATED: {block.title_fr}"
                    )
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"UPDATED: {block.title_fr}"
                    )
                )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Completed: {created_count} created, {updated_count} updated."
            )
        )
