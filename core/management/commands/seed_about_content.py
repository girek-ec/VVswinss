from django.core.management.base import BaseCommand, CommandError

from core.models import AboutContent


class Command(BaseCommand):
    help = (
        "Crea o actualiza el contenido corporativo de la página "
        "About / À propos de V&V Swiss Services."
    )

    def handle(self, *args, **options):
        count = AboutContent.objects.count()

        if count > 1:
            raise CommandError(
                "Existen varios registros AboutContent. "
                "No se modificó nada para evitar actualizar el registro equivocado."
            )

        data = {
            # ==========================================================
            # ESPAÑOL · REFERENCIA INTERNA
            # ==========================================================
            "intro_title_es": (
                "Su aliado para proyectos de renovación en la Suiza francófona"
            ),
            "intro_text_es": (
                "V&V Swiss Services acompaña a particulares, propietarios, "
                "gerencias inmobiliarias y profesionales en proyectos de "
                "renovación interior y exterior. Nuestra actividad comprende "
                "albañilería, aislamiento térmico, pladur y yesería, pintura, "
                "acabados, limpieza de fin de obra y trabajos de mantenimiento "
                "y renovación de inmuebles. Nuestro equipo reúne más de 20 años "
                "de experiencia en el sector de la construcción en Suiza, "
                "combinando conocimientos técnicos con una atención cercana, "
                "ágil y adaptada a cada proyecto."
            ),

            "mission_es": (
                "Ofrecer trabajos de renovación con estándares de calidad "
                "suizos, respetando los plazos acordados y manteniendo una "
                "comunicación clara y cercana con cada cliente. Adaptamos "
                "nuestros métodos de trabajo a las nuevas exigencias técnicas, "
                "estructurales, energéticas y medioambientales del sector."
            ),

            "vision_es": (
                "Consolidar V&V Swiss Services como una empresa de referencia "
                "en renovación y aislamiento en la Suiza francófona, reconocida "
                "por la calidad de sus acabados, la fiabilidad de su trabajo y "
                "la confianza establecida con sus clientes y colaboradores."
            ),

            "history_es": (
                "V&V Swiss Services se apoya en un equipo con más de 20 años "
                "de experiencia en el sector de la construcción en Suiza. "
                "Esta trayectoria permite reunir conocimientos técnicos, "
                "experiencia práctica y una forma de trabajar basada en la "
                "proximidad, la flexibilidad y el seguimiento cuidadoso de cada "
                "obra. Al integrar diferentes oficios de la renovación, podemos "
                "ofrecer a particulares, régies y profesionales un interlocutor "
                "único para coordinar sus proyectos."
            ),

            # ==========================================================
            # FRANÇAIS · SUISSE ROMANDE · LANGUE PRINCIPALE
            # ==========================================================
            "intro_title_fr": (
                "Votre partenaire pour vos projets de rénovation en Suisse romande"
            ),
            "intro_text_fr": (
                "V&V Swiss Services accompagne les particuliers, les propriétaires, "
                "les régies immobilières et les professionnels dans leurs projets "
                "de rénovation intérieure et extérieure. Nos prestations couvrent "
                "notamment la maçonnerie, l’isolation thermique, la plâtrerie, "
                "la peinture, les finitions, le nettoyage de fin de chantier ainsi "
                "que l’entretien et la remise en état de biens immobiliers. "
                "Notre équipe bénéficie de plus de 20 ans d’expérience dans le "
                "secteur de la construction en Suisse et associe savoir-faire "
                "technique, proximité, réactivité et flexibilité."
            ),

            "mission_fr": (
                "Réaliser des travaux de rénovation répondant aux standards de "
                "qualité suisses, dans le respect des délais convenus et avec "
                "un accompagnement clair et personnalisé. Nous adaptons en "
                "permanence nos méthodes aux nouvelles exigences techniques, "
                "structurelles, énergétiques et environnementales du secteur."
            ),

            "vision_fr": (
                "Consolider V&V Swiss Services comme une entreprise de référence "
                "dans la rénovation et l’isolation en Suisse romande, reconnue "
                "pour la qualité de ses finitions, la fiabilité de ses prestations "
                "et la confiance durable de ses clients et partenaires."
            ),

            "history_fr": (
                "V&V Swiss Services s’appuie sur une équipe disposant de plus de "
                "20 ans d’expérience dans le secteur de la construction en Suisse. "
                "Cette expérience nous permet d’associer savoir-faire technique, "
                "connaissance du terrain et suivi attentif de chaque chantier. "
                "En réunissant plusieurs métiers de la rénovation, nous pouvons "
                "proposer aux particuliers, aux régies et aux professionnels un "
                "interlocuteur unique capable de coordonner efficacement leurs "
                "projets, de la préparation des travaux jusqu’aux finitions."
            ),

            # ==========================================================
            # DEUTSCH · SCHWEIZER HOCHDEUTSCH
            # ==========================================================
            "intro_title_de": (
                "Ihr Partner für Renovationsprojekte in der Westschweiz"
            ),
            "intro_text_de": (
                "V&V Swiss Services begleitet Privatpersonen, Eigentümer, "
                "Immobilienverwaltungen und Fachpartner bei Renovationsarbeiten "
                "im Innen- und Aussenbereich. Unser Leistungsspektrum umfasst "
                "unter anderem Maurerarbeiten, Wärmedämmung, Gipserarbeiten, "
                "Malerarbeiten, Ausbau und Endreinigung sowie Unterhalts- und "
                "Instandsetzungsarbeiten an Immobilien. Unser Team verfügt über "
                "mehr als 20 Jahre Erfahrung im Schweizer Baugewerbe und verbindet "
                "technisches Fachwissen mit persönlicher Betreuung, Flexibilität "
                "und kurzen Entscheidungswegen."
            ),

            "mission_de": (
                "Renovationsarbeiten nach Schweizer Qualitätsstandards "
                "termingerecht und mit einer klaren, persönlichen Betreuung "
                "auszuführen. Unsere Arbeitsweise wird laufend an die technischen, "
                "baulichen, energetischen und ökologischen Anforderungen der "
                "Branche angepasst."
            ),

            "vision_de": (
                "V&V Swiss Services als verlässlichen Ansprechpartner für "
                "Renovation und Wärmedämmung in der Westschweiz zu etablieren – "
                "bekannt für sorgfältige Ausführung, zuverlässige Leistungen "
                "und langfristiges Vertrauen bei Kunden und Partnern."
            ),

            "history_de": (
                "V&V Swiss Services stützt sich auf ein Team mit mehr als "
                "20 Jahren Erfahrung im Schweizer Baugewerbe. Diese Erfahrung "
                "verbindet fundiertes Fachwissen mit praktischer Kompetenz und "
                "einer persönlichen, flexiblen Arbeitsweise. Durch die Bündelung "
                "verschiedener Renovationsarbeiten bieten wir Privatkunden, "
                "Immobilienverwaltungen und Fachpartnern einen zentralen "
                "Ansprechpartner für die Koordination ihrer Projekte – von der "
                "Vorbereitung bis zur fachgerechten Fertigstellung."
            ),

            # ==========================================================
            # ITALIANO · CONTESTO SVIZZERO
            # ==========================================================
            "intro_title_it": (
                "Il vostro partner per progetti di ristrutturazione "
                "nella Svizzera romanda"
            ),
            "intro_text_it": (
                "V&V Swiss Services affianca privati, proprietari, "
                "amministrazioni immobiliari e professionisti nei progetti di "
                "ristrutturazione interna ed esterna. Le nostre prestazioni "
                "comprendono opere di muratura, isolamento termico, intonacatura "
                "e cartongesso, pittura, finiture, pulizia di fine cantiere, "
                "manutenzione e ripristino di immobili. Il nostro team vanta "
                "oltre 20 anni di esperienza nel settore delle costruzioni in "
                "Svizzera, unendo competenza tecnica, disponibilità, flessibilità "
                "e attenzione alle esigenze di ogni progetto."
            ),

            "mission_it": (
                "Realizzare lavori di ristrutturazione conformi agli standard "
                "di qualità svizzeri, nel rispetto delle tempistiche concordate "
                "e con un accompagnamento chiaro e personalizzato. Adeguiamo "
                "costantemente i nostri metodi alle nuove esigenze tecniche, "
                "strutturali, energetiche e ambientali del settore."
            ),

            "vision_it": (
                "Consolidare V&V Swiss Services come azienda di riferimento "
                "per la ristrutturazione e l’isolamento nella Svizzera romanda, "
                "riconosciuta per la qualità delle finiture, l’affidabilità "
                "del servizio e la fiducia dei propri clienti e partner."
            ),

            "history_it": (
                "V&V Swiss Services si basa su un team con oltre 20 anni di "
                "esperienza nel settore delle costruzioni in Svizzera. "
                "Questa esperienza ci permette di combinare competenza tecnica, "
                "conoscenza pratica e un approccio attento e flessibile. "
                "Riunendo diverse specializzazioni della ristrutturazione, "
                "offriamo a privati, amministrazioni immobiliari e professionisti "
                "un unico interlocutore per coordinare il progetto dalla "
                "preparazione dei lavori fino alle finiture."
            ),

            # ==========================================================
            # ENGLISH · BRITISH ENGLISH
            # ==========================================================
            "intro_title_en": (
                "Your trusted partner for renovation projects "
                "in French-speaking Switzerland"
            ),
            "intro_text_en": (
                "V&V Swiss Services supports private homeowners, property owners, "
                "property managers and construction professionals with interior "
                "and exterior renovation projects. Our services include masonry, "
                "thermal insulation, plastering and dry lining, painting, "
                "finishing works, end-of-build cleaning, property maintenance "
                "and refurbishment. Our team brings more than 20 years of "
                "experience in the Swiss construction sector, combining technical "
                "expertise with responsive, flexible and personalised service."
            ),

            "mission_en": (
                "To deliver renovation work to Swiss quality standards, within "
                "the agreed timescales and with clear, personal communication "
                "throughout each project. We continually adapt our methods to "
                "evolving technical, structural, energy-efficiency and "
                "environmental requirements."
            ),

            "vision_en": (
                "To establish V&V Swiss Services as a trusted reference for "
                "renovation and insulation in French-speaking Switzerland, "
                "recognised for the quality of its finishes, reliable workmanship "
                "and the long-term confidence of its clients and partners."
            ),

            "history_en": (
                "V&V Swiss Services is supported by a team with more than "
                "20 years of experience in the Swiss construction sector. "
                "This experience enables us to combine technical expertise, "
                "practical knowledge and a responsive, flexible approach to "
                "each project. By bringing several renovation trades together, "
                "we provide homeowners, property managers and construction "
                "professionals with a single point of contact from initial "
                "planning through to final finishes."
            ),

            "is_active": True,
        }

        if count == 0:
            obj = AboutContent.objects.create(**data)

            self.stdout.write(
                self.style.SUCCESS(
                    f"AboutContent creado correctamente. ID={obj.pk}"
                )
            )

        else:
            obj = AboutContent.objects.first()

            for field_name, value in data.items():
                setattr(obj, field_name, value)

            obj.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"AboutContent actualizado correctamente. ID={obj.pk}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Contenido cargado en ES, FR, DE, IT y EN."
            )
        )

        self.stdout.write(
            "La imagen existente, si la hubiera, no fue modificada."
        )
