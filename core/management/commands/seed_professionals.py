from django.core.management.base import BaseCommand

from core.models import (
    ProfessionalPage,
    ProfessionalAudience,
    ProfessionalBenefit,
)

from services.models import Service


class Command(BaseCommand):
    help = "Carga o actualiza el contenido inicial de la página Professionnels."

    def handle(self, *args, **options):

        self.stdout.write("")
        self.stdout.write(
            self.style.MIGRATE_HEADING(
                "=============================================="
            )
        )
        self.stdout.write(
            self.style.MIGRATE_HEADING(
                " V&V SWISS SERVICES · PROFESSIONNELS"
            )
        )
        self.stdout.write(
            self.style.MIGRATE_HEADING(
                "=============================================="
            )
        )

        # ====================================================
        # PROFESSIONAL PAGE
        # ====================================================

        page = ProfessionalPage.objects.order_by("pk").first()

        if page is None:
            page = ProfessionalPage()
            created = True
        else:
            created = False

        # ====================================================
        # HERO
        # ====================================================

        page.hero_label_es = "PARA PROFESIONALES"
        page.hero_label_fr = "POUR LES PROFESSIONNELS"
        page.hero_label_de = "FÜR PROFESSIONELLE"
        page.hero_label_it = "PER I PROFESSIONISTI"
        page.hero_label_en = "FOR PROFESSIONALS"

        page.hero_title_es = (
            "Un socio fiable para sus proyectos de renovación"
        )

        page.hero_title_fr = (
            "Un partenaire fiable pour vos travaux de rénovation"
        )

        page.hero_title_de = (
            "Ein zuverlässiger Partner für Ihre Renovationsarbeiten"
        )

        page.hero_title_it = (
            "Un partner affidabile per i vostri lavori di ristrutturazione"
        )

        page.hero_title_en = (
            "A reliable partner for your renovation projects"
        )

        page.hero_text_es = (
            "V&V Swiss Services acompaña a administraciones inmobiliarias, "
            "administradores de PPE, empresas generales, constructoras y "
            "arquitectos en trabajos de renovación, mantenimiento y puesta "
            "a punto de inmuebles."
        )

        page.hero_text_fr = (
            "V&V Swiss Services accompagne les régies immobilières, "
            "administrateurs PPE, entreprises générales, constructeurs et "
            "architectes dans leurs travaux de rénovation, d’entretien et "
            "de remise en état."
        )

        page.hero_text_de = (
            "V&V Swiss Services unterstützt Immobilienverwaltungen, "
            "STWE-Verwaltungen, Generalunternehmen, Bauunternehmen und "
            "Architekturbüros bei Renovations-, Unterhalts- und "
            "Instandsetzungsarbeiten."
        )

        page.hero_text_it = (
            "V&V Swiss Services affianca amministrazioni immobiliari, "
            "amministratori di proprietà per piani, imprese generali, "
            "imprese di costruzione e studi di architettura nei lavori "
            "di ristrutturazione, manutenzione e ripristino."
        )

        page.hero_text_en = (
            "V&V Swiss Services supports property managers, condominium "
            "administrators, general contractors, construction companies "
            "and architects with renovation, maintenance and property "
            "reinstatement works."
        )

        # ====================================================
        # INTRODUCTION
        # ====================================================

        page.intro_title_es = (
            "Un solo interlocutor para varios oficios"
        )

        page.intro_title_fr = (
            "Un seul interlocuteur pour plusieurs corps de métier"
        )

        page.intro_title_de = (
            "Ein Ansprechpartner für mehrere Gewerke"
        )

        page.intro_title_it = (
            "Un unico interlocutore per diverse lavorazioni"
        )

        page.intro_title_en = (
            "One point of contact for multiple trades"
        )

        page.intro_text_es = (
            "La gestión de un inmueble o de una obra exige capacidad de "
            "respuesta, coordinación y respeto de los plazos. V&V Swiss "
            "Services centraliza diferentes prestaciones para simplificar "
            "las intervenciones y reducir la necesidad de coordinar varios "
            "proveedores. Albañilería, aislamiento, yesería, pintura o "
            "limpieza de fin de obra: intervenimos según las necesidades "
            "del proyecto con una organización clara y un seguimiento "
            "profesional."
        )

        page.intro_text_fr = (
            "La gestion d’un bien immobilier ou d’un chantier exige "
            "réactivité, coordination et respect des délais. V&V Swiss "
            "Services centralise plusieurs prestations afin de simplifier "
            "vos interventions et de limiter la multiplication des "
            "prestataires. Maçonnerie, isolation, plâtrerie, peinture ou "
            "nettoyage de fin de chantier : nous intervenons selon les "
            "besoins du projet avec une organisation claire et un suivi "
            "professionnel."
        )

        page.intro_text_de = (
            "Die Bewirtschaftung einer Immobilie oder die Koordination "
            "einer Baustelle erfordern Reaktionsfähigkeit, Organisation "
            "und Termintreue. V&V Swiss Services bündelt verschiedene "
            "Leistungen, um Einsätze zu vereinfachen und die Anzahl der "
            "zu koordinierenden Anbieter zu reduzieren."
        )

        page.intro_text_it = (
            "La gestione di un immobile o di un cantiere richiede "
            "rapidità, coordinamento e rispetto delle scadenze. V&V Swiss "
            "Services riunisce diverse prestazioni per semplificare gli "
            "interventi e ridurre il numero di fornitori da coordinare."
        )

        page.intro_text_en = (
            "Managing a property or construction project requires "
            "responsiveness, coordination and respect for deadlines. "
            "V&V Swiss Services brings several trades together to simplify "
            "interventions and reduce the number of contractors you need "
            "to coordinate."
        )

        # ====================================================
        # AUDIENCES
        # ====================================================

        page.audiences_title_es = (
            "Soluciones para clientes profesionales"
        )

        page.audiences_title_fr = (
            "Nos solutions pour les professionnels"
        )

        page.audiences_title_de = (
            "Unsere Lösungen für professionelle Auftraggeber"
        )

        page.audiences_title_it = (
            "Le nostre soluzioni per i professionisti"
        )

        page.audiences_title_en = (
            "Solutions for professional clients"
        )

        # ====================================================
        # TURNOVER / ENTRE LOCATAIRES
        # ====================================================

        page.turnover_title_es = (
            "Puesta a punto entre dos inquilinos"
        )

        page.turnover_title_fr = (
            "Remise en état entre deux locataires"
        )

        page.turnover_title_de = (
            "Instandsetzung zwischen zwei Mietverhältnissen"
        )

        page.turnover_title_it = (
            "Ripristino tra un inquilino e l’altro"
        )

        page.turnover_title_en = (
            "Property reinstatement between tenancies"
        )

        page.turnover_text_es = (
            "Cuando cambia un inquilino, los plazos suelen ser reducidos. "
            "Podemos coordinar varias intervenciones necesarias para poner "
            "a punto la vivienda y facilitar su preparación antes de la "
            "siguiente ocupación."
        )

        page.turnover_text_fr = (
            "Lors d’un changement de locataire, les délais sont souvent "
            "courts. Nous pouvons coordonner plusieurs interventions "
            "nécessaires à la remise en état du logement afin de faciliter "
            "sa préparation avant la prochaine occupation."
        )

        page.turnover_text_de = (
            "Bei einem Mieterwechsel sind die verfügbaren Zeitfenster oft "
            "kurz. Wir können mehrere notwendige Arbeiten koordinieren, "
            "damit die Wohnung effizient für die nächste Vermietung "
            "vorbereitet werden kann."
        )

        page.turnover_text_it = (
            "In occasione di un cambio di inquilino, i tempi sono spesso "
            "ridotti. Possiamo coordinare diversi interventi necessari al "
            "ripristino dell’alloggio prima della successiva occupazione."
        )

        page.turnover_text_en = (
            "When tenants change, turnaround times are often short. "
            "We can coordinate several works required to reinstate the "
            "property and prepare it efficiently for its next occupancy."
        )

        # ====================================================
        # SERVICES
        # ====================================================

        page.services_title_es = (
            "Varios oficios, un solo socio"
        )

        page.services_title_fr = (
            "Plusieurs métiers, un seul partenaire"
        )

        page.services_title_de = (
            "Mehrere Gewerke, ein Partner"
        )

        page.services_title_it = (
            "Diverse competenze, un unico partner"
        )

        page.services_title_en = (
            "Multiple trades, one partner"
        )

        # ====================================================
        # BENEFITS
        # ====================================================

        page.benefits_title_es = (
            "Un socio pensado para las exigencias profesionales"
        )

        page.benefits_title_fr = (
            "Un partenaire pensé pour les exigences des professionnels"
        )

        page.benefits_title_de = (
            "Ein Partner für die Anforderungen professioneller Auftraggeber"
        )

        page.benefits_title_it = (
            "Un partner pensato per le esigenze dei professionisti"
        )

        page.benefits_title_en = (
            "A partner for professional requirements"
        )

        # ====================================================
        # CTA
        # ====================================================

        page.cta_title_es = (
            "¿Busca un socio para sus próximos trabajos?"
        )

        page.cta_title_fr = (
            "Vous recherchez un partenaire pour vos prochains travaux ?"
        )

        page.cta_title_de = (
            "Suchen Sie einen Partner für Ihre nächsten Arbeiten?"
        )

        page.cta_title_it = (
            "Cercate un partner per i vostri prossimi lavori?"
        )

        page.cta_title_en = (
            "Looking for a partner for your next project?"
        )

        page.cta_text_es = (
            "Preséntenos su proyecto o sus necesidades recurrentes. "
            "Nuestro equipo analizará los trabajos necesarios para "
            "organizar las siguientes etapas de la intervención."
        )

        page.cta_text_fr = (
            "Présentez-nous votre projet ou vos besoins récurrents. "
            "Notre équipe vous répondra afin d’évaluer les travaux et "
            "d’organiser la suite de l’intervention."
        )

        page.cta_text_de = (
            "Stellen Sie uns Ihr Projekt oder Ihren wiederkehrenden Bedarf "
            "vor. Unser Team prüft die erforderlichen Arbeiten und "
            "organisiert die nächsten Schritte."
        )

        page.cta_text_it = (
            "Presentateci il vostro progetto o le vostre esigenze "
            "ricorrenti. Il nostro team valuterà i lavori necessari e "
            "organizzerà le fasi successive."
        )

        page.cta_text_en = (
            "Tell us about your project or recurring requirements. "
            "Our team will assess the work required and organise the "
            "next steps."
        )

        page.cta_button_es = "Presentar un proyecto"
        page.cta_button_fr = "Nous soumettre un projet"
        page.cta_button_de = "Projekt anfragen"
        page.cta_button_it = "Sottoporre un progetto"
        page.cta_button_en = "Submit a project"

        # ====================================================
        # SEO
        # ====================================================

        page.seo_title_es = (
            "Servicios para profesionales | V&V Swiss Services"
        )

        page.seo_title_fr = (
            "Travaux pour professionnels | V&V Swiss Services"
        )

        page.seo_title_de = (
            "Arbeiten für professionelle Auftraggeber | V&V Swiss Services"
        )

        page.seo_title_it = (
            "Lavori per professionisti | V&V Swiss Services"
        )

        page.seo_title_en = (
            "Services for professionals | V&V Swiss Services"
        )

        page.meta_description_es = (
            "Soluciones de renovación y mantenimiento para administraciones "
            "inmobiliarias, PPE, constructoras, empresas generales y "
            "arquitectos."
        )

        page.meta_description_fr = (
            "Solutions de rénovation, d’entretien et de remise en état "
            "pour régies immobilières, PPE, entreprises générales, "
            "constructeurs et architectes."
        )

        page.meta_description_de = (
            "Renovations-, Unterhalts- und Instandsetzungslösungen für "
            "Immobilienverwaltungen, STWE-Verwaltungen, Generalunternehmen, "
            "Bauunternehmen und Architekten."
        )

        page.meta_description_it = (
            "Soluzioni di ristrutturazione, manutenzione e ripristino per "
            "amministrazioni immobiliari, proprietà per piani, imprese "
            "generali, costruttori e architetti."
        )

        page.meta_description_en = (
            "Renovation, maintenance and reinstatement solutions for "
            "property managers, condominium administrators, contractors, "
            "construction companies and architects."
        )

        page.is_indexable = True
        page.is_active = True

        page.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    "✓ Página Professionnels creada."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "✓ Página Professionnels actualizada."
                )
            )

        # ====================================================
        # PROFESSIONAL AUDIENCES
        # ====================================================

        audiences = [

            {
                "title_fr": "Régies immobilières",
                "title_es": "Administraciones inmobiliarias",
                "title_de": "Immobilienverwaltungen",
                "title_it": "Amministrazioni immobiliari",
                "title_en": "Property managers",

                "description_fr":
                    "Entretien, rénovation et remise en état de logements "
                    "et d’immeubles locatifs.",

                "description_es":
                    "Mantenimiento, renovación y puesta a punto de viviendas "
                    "e inmuebles de alquiler.",

                "description_de":
                    "Unterhalt, Renovation und Instandsetzung von Wohnungen "
                    "und Mietliegenschaften.",

                "description_it":
                    "Manutenzione, ristrutturazione e ripristino di alloggi "
                    "e immobili locativi.",

                "description_en":
                    "Maintenance, renovation and reinstatement of rental "
                    "properties and residential buildings.",

                "icon": "fa-solid fa-building",
                "order": 1,
            },

            {
                "title_fr": "Administrateurs PPE",
                "title_es": "Administradores PPE",
                "title_de": "STWE-Verwaltungen",
                "title_it": "Amministratori di proprietà per piani",
                "title_en": "Condominium administrators",

                "description_fr":
                    "Travaux dans les parties communes et interventions "
                    "planifiées sur les bâtiments.",

                "description_es":
                    "Trabajos en zonas comunes e intervenciones planificadas "
                    "en los edificios.",

                "description_de":
                    "Arbeiten in gemeinschaftlichen Bereichen und geplante "
                    "Einsätze an Gebäuden.",

                "description_it":
                    "Lavori nelle parti comuni e interventi pianificati "
                    "sugli edifici.",

                "description_en":
                    "Works in communal areas and planned building "
                    "interventions.",

                "icon": "fa-solid fa-building-user",
                "order": 2,
            },

            {
                "title_fr": "Entreprises générales et constructeurs",
                "title_es": "Empresas generales y constructoras",
                "title_de": "General- und Bauunternehmen",
                "title_it": "Imprese generali e costruttori",
                "title_en": "General contractors and builders",

                "description_fr":
                    "Un partenaire opérationnel pour la réalisation de "
                    "travaux spécifiques dans le cadre de vos chantiers.",

                "description_es":
                    "Un socio operativo para ejecutar trabajos específicos "
                    "dentro de sus proyectos de construcción.",

                "description_de":
                    "Ein operativer Partner für die Ausführung spezifischer "
                    "Arbeiten innerhalb Ihrer Bauprojekte.",

                "description_it":
                    "Un partner operativo per l’esecuzione di lavori "
                    "specifici nell’ambito dei vostri cantieri.",

                "description_en":
                    "An operational partner for specific works within your "
                    "construction projects.",

                "icon": "fa-solid fa-helmet-safety",
                "order": 3,
            },

            {
                "title_fr": "Architectes",
                "title_es": "Arquitectos",
                "title_de": "Architekturbüros",
                "title_it": "Architetti",
                "title_en": "Architects",

                "description_fr":
                    "Exécution de travaux de rénovation et de finition "
                    "selon les exigences et la planification du projet.",

                "description_es":
                    "Ejecución de trabajos de renovación y acabado según "
                    "las exigencias y planificación del proyecto.",

                "description_de":
                    "Ausführung von Renovations- und Fertigstellungsarbeiten "
                    "gemäss Projektanforderungen und Terminplanung.",

                "description_it":
                    "Esecuzione di lavori di ristrutturazione e finitura "
                    "secondo le esigenze e la pianificazione del progetto.",

                "description_en":
                    "Renovation and finishing works carried out according "
                    "to project requirements and schedules.",

                "icon": "fa-solid fa-compass-drafting",
                "order": 4,
            },
        ]

        for data in audiences:

            audience, audience_created = (
                ProfessionalAudience.objects.update_or_create(
                    page=page,
                    order=data["order"],
                    defaults={
                        **data,
                        "is_active": True,
                    },
                )
            )

            action = (
                "creado"
                if audience_created
                else "actualizado"
            )

            self.stdout.write(
                f"  ✓ Cliente profesional {action}: "
                f"{audience.title_fr}"
            )

        # ====================================================
        # PROFESSIONAL BENEFITS
        # ====================================================

        benefits = [

            {
                "title_fr": "Interlocuteur unique",
                "title_es": "Interlocutor único",
                "title_de": "Ein Ansprechpartner",
                "title_it": "Un unico interlocutore",
                "title_en": "Single point of contact",

                "description_fr":
                    "Un seul contact pour coordonner plusieurs prestations.",

                "description_es":
                    "Un solo contacto para coordinar varias prestaciones.",

                "description_de":
                    "Ein Ansprechpartner für die Koordination mehrerer "
                    "Leistungen.",

                "description_it":
                    "Un unico contatto per coordinare diverse prestazioni.",

                "description_en":
                    "One point of contact to coordinate multiple services.",

                "icon": "fa-solid fa-user-check",
                "order": 1,
            },

            {
                "title_fr": "Réactivité",
                "title_es": "Capacidad de respuesta",
                "title_de": "Reaktionsfähigkeit",
                "title_it": "Rapidità",
                "title_en": "Responsiveness",

                "description_fr":
                    "Une organisation adaptée aux interventions et aux "
                    "délais du projet.",

                "description_es":
                    "Una organización adaptada a las intervenciones y "
                    "plazos del proyecto.",

                "description_de":
                    "Eine Organisation, die auf Einsätze und Projekttermine "
                    "abgestimmt ist.",

                "description_it":
                    "Un’organizzazione adattata agli interventi e alle "
                    "tempistiche del progetto.",

                "description_en":
                    "An organisation adapted to project requirements and "
                    "deadlines.",

                "icon": "fa-solid fa-clock",
                "order": 2,
            },

            {
                "title_fr": "Devis clairs",
                "title_es": "Presupuestos claros",
                "title_de": "Klare Offerten",
                "title_it": "Preventivi chiari",
                "title_en": "Clear quotations",

                "description_fr":
                    "Des prestations définies clairement avant le démarrage "
                    "des travaux.",

                "description_es":
                    "Prestaciones claramente definidas antes del inicio "
                    "de los trabajos.",

                "description_de":
                    "Klar definierte Leistungen vor Beginn der Arbeiten.",

                "description_it":
                    "Prestazioni definite chiaramente prima dell’inizio "
                    "dei lavori.",

                "description_en":
                    "Clearly defined services before work begins.",

                "icon": "fa-solid fa-file-signature",
                "order": 3,
            },

            {
                "title_fr": "Finitions soignées",
                "title_es": "Acabados cuidados",
                "title_de": "Sorgfältige Ausführung",
                "title_it": "Finiture curate",
                "title_en": "Careful finishing",

                "description_fr":
                    "Une attention particulière portée à la qualité "
                    "d’exécution et à la propreté.",

                "description_es":
                    "Especial atención a la calidad de ejecución y a "
                    "la limpieza.",

                "description_de":
                    "Besonderes Augenmerk auf Ausführungsqualität und "
                    "Sauberkeit.",

                "description_it":
                    "Particolare attenzione alla qualità dell’esecuzione "
                    "e alla pulizia.",

                "description_en":
                    "Particular attention to workmanship and cleanliness.",

                "icon": "fa-solid fa-circle-check",
                "order": 4,
            },

            {
                "title_fr": "Flexibilité",
                "title_es": "Flexibilidad",
                "title_de": "Flexibilität",
                "title_it": "Flessibilità",
                "title_en": "Flexibility",

                "description_fr":
                    "Des interventions adaptées aux besoins du bâtiment "
                    "et à la planification du chantier.",

                "description_es":
                    "Intervenciones adaptadas a las necesidades del "
                    "inmueble y a la planificación de la obra.",

                "description_de":
                    "Einsätze abgestimmt auf die Anforderungen des Gebäudes "
                    "und die Bauplanung.",

                "description_it":
                    "Interventi adattati alle esigenze dell’edificio e "
                    "alla pianificazione del cantiere.",

                "description_en":
                    "Works adapted to the building's requirements and "
                    "project schedule.",

                "icon": "fa-solid fa-arrows-rotate",
                "order": 5,
            },

            {
                "title_fr": "Expérience en Suisse",
                "title_es": "Experiencia en Suiza",
                "title_de": "Erfahrung in der Schweiz",
                "title_it": "Esperienza in Svizzera",
                "title_en": "Experience in Switzerland",

                "description_fr":
                    "Une équipe disposant de plus de 20 ans d’expérience "
                    "dans le secteur de la construction en Suisse.",

                "description_es":
                    "Un equipo con más de 20 años de experiencia en el "
                    "sector de la construcción en Suiza.",

                "description_de":
                    "Ein Team mit über 20 Jahren Erfahrung im Schweizer "
                    "Bausektor.",

                "description_it":
                    "Un team con oltre 20 anni di esperienza nel settore "
                    "delle costruzioni in Svizzera.",

                "description_en":
                    "A team with more than 20 years of experience in the "
                    "Swiss construction sector.",

                "icon": "fa-solid fa-award",
                "order": 6,
            },
        ]

        for data in benefits:

            benefit, benefit_created = (
                ProfessionalBenefit.objects.update_or_create(
                    page=page,
                    order=data["order"],
                    defaults={
                        **data,
                        "is_active": True,
                    },
                )
            )

            action = (
                "creado"
                if benefit_created
                else "actualizado"
            )

            self.stdout.write(
                f"  ✓ Ventaja {action}: "
                f"{benefit.title_fr}"
            )

        # ====================================================
        # SERVICES
        #
        # Relacionamos automáticamente TODOS los servicios
        # actualmente activos.
        # ====================================================

        active_services = (
            Service.objects
            .filter(is_active=True)
            .order_by("order", "name_fr")
        )

        page.services.set(active_services)

        service_count = active_services.count()

        self.stdout.write(
            self.style.SUCCESS(
                f"✓ {service_count} servicios activos relacionados."
            )
        )

        # ====================================================
        # FIN
        # ====================================================

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "=============================================="
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                " PROFESSIONNELS CARGADO CORRECTAMENTE"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                "=============================================="
            )
        )
        self.stdout.write("")