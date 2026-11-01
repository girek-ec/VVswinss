# -*- coding: utf-8 -*-
"""
V&V Swiss Services · Seed data · Phase 1: Services

EN: Editorial data used by the seed command.
ES: Datos editoriales utilizados por el comando de carga.

Language policy:
- FR: principal, natural wording for Suisse romande.
- DE: Schweizer Hochdeutsch; always "ss", never "ß".
- IT: professional Italian adapted to the Swiss context.
- EN: British English.
- ES: internal administrative reference where the model provides *_es fields.
"""

LANGUAGES = ("es", "fr", "de", "it", "en")


CATEGORY_DATA = [
    {
        "order": 1,
        "icon": "fa-solid fa-house-chimney",
        "name": {
            "es": "Renovación integral",
            "fr": "Rénovation globale",
            "de": "Gesamtrenovation",
            "it": "Ristrutturazione globale",
            "en": "Complete renovation",
        },
        "description": {
            "es": "Renovación coordinada de interiores y exteriores, con un único interlocutor para organizar los distintos trabajos.",
            "fr": "Rénovation coordonnée des espaces intérieurs et extérieurs, avec un interlocuteur unique pour organiser les différents corps de métier.",
            "de": "Koordinierte Innen- und Aussenrenovation mit einer zentralen Ansprechperson für die Organisation der verschiedenen Gewerke.",
            "it": "Ristrutturazione coordinata di interni ed esterni, con un unico referente per organizzare le diverse lavorazioni.",
            "en": "Co-ordinated interior and exterior renovation, with one point of contact to organise the different trades.",
        },
        "detail_lists": {
            "es": ["Renovación de viviendas", "Coordinación de varios oficios", "Reparaciones y acabados", "Preparación para la entrega"],
            "fr": ["Rénovation de logements", "Coordination de plusieurs corps de métier", "Réparations et finitions", "Préparation avant remise"],
            "de": ["Renovation von Wohnräumen", "Koordination mehrerer Gewerke", "Reparaturen und Abschlussarbeiten", "Vorbereitung für die Übergabe"],
            "it": ["Ristrutturazione di abitazioni", "Coordinamento di più mestieri", "Riparazioni e finiture", "Preparazione alla consegna"],
            "en": ["Home renovation", "Multi-trade co-ordination", "Repairs and finishing", "Preparation for handover"],
        },
    },
    {
        "order": 2,
        "icon": "fa-solid fa-trowel-bricks",
        "name": {
            "es": "Albañilería",
            "fr": "Maçonnerie",
            "de": "Maurerarbeiten",
            "it": "Opere murarie",
            "en": "Masonry",
        },
        "description": {
            "es": "Trabajos de albañilería para reformas, reparaciones, tabiques, revoques y fachadas, adaptados al estado del edificio.",
            "fr": "Travaux de maçonnerie pour rénovations, réparations, cloisons, crépis et façades, adaptés à l’état du bâtiment.",
            "de": "Maurerarbeiten für Renovationen, Reparaturen, Trennwände, Verputz und Fassaden, abgestimmt auf den Zustand des Gebäudes.",
            "it": "Opere murarie per ristrutturazioni, riparazioni, pareti, intonaci e facciate, adattate allo stato dell’edificio.",
            "en": "Masonry work for renovations, repairs, partitions, rendering and façades, adapted to the condition of the building.",
        },
        "detail_lists": {
            "es": ["Reparaciones de albañilería", "Muros y tabiques", "Revoques y enlucidos", "Trabajos de fachada"],
            "fr": ["Réparations de maçonnerie", "Murs et cloisons", "Crépis et enduits", "Travaux de façade"],
            "de": ["Mauerwerksreparaturen", "Wände und Trennwände", "Verputz- und Spachtelarbeiten", "Fassadenarbeiten"],
            "it": ["Riparazioni murarie", "Pareti e divisori", "Intonaci e rasature", "Lavori di facciata"],
            "en": ["Masonry repairs", "Walls and partitions", "Rendering and plaster finishes", "Façade works"],
        },
    },
    {
        "order": 3,
        "icon": "fa-solid fa-temperature-half",
        "name": {
            "es": "Aislamiento térmico",
            "fr": "Isolation thermique",
            "de": "Wärmedämmung",
            "it": "Isolamento termico",
            "en": "Thermal insulation",
        },
        "description": {
            "es": "Soluciones de aislamiento para fachadas, áticos, sótanos y cubiertas, orientadas a mejorar el confort y el rendimiento energético.",
            "fr": "Solutions d’isolation pour façades, combles, sous-sols et toitures, afin d’améliorer le confort et la performance énergétique.",
            "de": "Dämmlösungen für Fassaden, Dachräume, Untergeschosse und Dächer zur Verbesserung von Komfort und Energieeffizienz.",
            "it": "Soluzioni di isolamento per facciate, sottotetti, seminterrati e tetti, per migliorare comfort e prestazioni energetiche.",
            "en": "Insulation solutions for façades, lofts, basements and roofs to improve comfort and energy performance.",
        },
        "detail_lists": {
            "es": ["Fachadas e ITE", "Áticos y espacios bajo cubierta", "Sótanos", "Cubiertas y techos"],
            "fr": ["Façades et isolation périphérique", "Combles", "Sous-sols", "Toitures"],
            "de": ["Fassaden und Aussendämmung", "Dachräume", "Untergeschosse", "Dächer"],
            "it": ["Facciate e isolamento esterno", "Sottotetti", "Seminterrati", "Tetti"],
            "en": ["Façades and external insulation", "Lofts", "Basements", "Roofs"],
        },
    },
    {
        "order": 4,
        "icon": "fa-solid fa-border-all",
        "name": {
            "es": "Pladur y yesería",
            "fr": "Plâtrerie",
            "de": "Gipserarbeiten",
            "it": "Opere in cartongesso e gesso",
            "en": "Plastering and drywall",
        },
        "description": {
            "es": "Tabiques, falsos techos, trasdosados y acabados de yesería para redistribuir y renovar espacios interiores.",
            "fr": "Cloisons, faux plafonds, doublages et finitions de plâtrerie pour réorganiser et rénover les espaces intérieurs.",
            "de": "Trennwände, abgehängte Decken, Vorsatzschalen und Gipserarbeiten für die Neugestaltung und Renovation von Innenräumen.",
            "it": "Pareti divisorie, controsoffitti, contropareti e finiture in gesso per riorganizzare e rinnovare gli spazi interni.",
            "en": "Partitions, suspended ceilings, wall linings and plaster finishes for reorganising and renovating interior spaces.",
        },
        "detail_lists": {
            "es": ["Tabiques de pladur", "Falsos techos", "Trasdosados", "Enlucidos y acabados"],
            "fr": ["Cloisons en plaques de plâtre", "Faux plafonds", "Doublages", "Enduits et finitions"],
            "de": ["Gipskarton-Trennwände", "Abgehängte Decken", "Vorsatzschalen", "Spachtel- und Finisharbeiten"],
            "it": ["Pareti in cartongesso", "Controsoffitti", "Contropareti", "Rasature e finiture"],
            "en": ["Plasterboard partitions", "Suspended ceilings", "Wall linings", "Skimming and finishing"],
        },
    },
    {
        "order": 5,
        "icon": "fa-solid fa-paint-roller",
        "name": {
            "es": "Pintura",
            "fr": "Peinture",
            "de": "Malerarbeiten",
            "it": "Pittura",
            "en": "Painting",
        },
        "description": {
            "es": "Pintura interior y exterior, fachadas y acabados decorativos con preparación cuidada de los soportes.",
            "fr": "Peinture intérieure et extérieure, façades et finitions décoratives, avec une préparation soignée des supports.",
            "de": "Malerarbeiten im Innen- und Aussenbereich, Fassaden und dekorative Oberflächen mit sorgfältiger Untergrundvorbereitung.",
            "it": "Pittura interna ed esterna, facciate e finiture decorative con un’accurata preparazione dei supporti.",
            "en": "Interior and exterior painting, façades and decorative finishes with careful preparation of surfaces.",
        },
        "detail_lists": {
            "es": ["Preparación de superficies", "Pintura interior", "Pintura exterior", "Fachadas y acabados"],
            "fr": ["Préparation des supports", "Peinture intérieure", "Peinture extérieure", "Façades et finitions"],
            "de": ["Untergrundvorbereitung", "Innenanstriche", "Aussenanstriche", "Fassaden und Finisharbeiten"],
            "it": ["Preparazione dei supporti", "Pittura interna", "Pittura esterna", "Facciate e finiture"],
            "en": ["Surface preparation", "Interior painting", "Exterior painting", "Façades and finishes"],
        },
    },
    {
        "order": 6,
        "icon": "fa-solid fa-broom",
        "name": {
            "es": "Limpieza de fin de obra",
            "fr": "Nettoyage de fin de chantier",
            "de": "Bauendreinigung",
            "it": "Pulizia di fine cantiere",
            "en": "Post-construction cleaning",
        },
        "description": {
            "es": "Limpieza tras los trabajos y preparación de los espacios para una entrega ordenada y lista para su uso.",
            "fr": "Nettoyage après travaux et préparation des espaces pour une remise propre, ordonnée et prête à l’usage.",
            "de": "Reinigung nach Abschluss der Arbeiten und Vorbereitung der Räume für eine saubere und geordnete Übergabe.",
            "it": "Pulizia dopo i lavori e preparazione degli spazi per una consegna ordinata, pulita e pronta all’uso.",
            "en": "Cleaning after building work and preparation of spaces for a clean, orderly and ready-to-use handover.",
        },
        "detail_lists": {
            "es": ["Retirada de residuos ligeros", "Limpieza de superficies", "Limpieza antes de la entrega", "Preparación de espacios"],
            "fr": ["Évacuation des petits déchets", "Nettoyage des surfaces", "Nettoyage avant remise", "Préparation des espaces"],
            "de": ["Entfernung leichter Bauabfälle", "Reinigung der Oberflächen", "Reinigung vor der Übergabe", "Vorbereitung der Räume"],
            "it": ["Rimozione dei piccoli residui", "Pulizia delle superfici", "Pulizia prima della consegna", "Preparazione degli spazi"],
            "en": ["Removal of light building waste", "Surface cleaning", "Cleaning before handover", "Preparation of spaces"],
        },
    },
    {
        "order": 7,
        "icon": "fa-solid fa-building",
        "name": {
            "es": "Servicios para gerencias inmobiliarias",
            "fr": "Services pour régies immobilières",
            "de": "Dienstleistungen für Liegenschaftsverwaltungen",
            "it": "Servizi per amministrazioni immobiliari",
            "en": "Services for property managers",
        },
        "description": {
            "es": "Mantenimiento, reparaciones y renovación entre inquilinos con coordinación de varios oficios y un único interlocutor.",
            "fr": "Entretien, réparations et remise en état entre deux locataires, avec coordination de plusieurs corps de métier et un interlocuteur unique.",
            "de": "Unterhalt, Reparaturen und Instandstellung zwischen zwei Mietverhältnissen, mit Koordination mehrerer Gewerke und einer zentralen Ansprechperson.",
            "it": "Manutenzione, riparazioni e ripristino tra due locazioni, con coordinamento di più mestieri e un unico referente.",
            "en": "Maintenance, repairs and reinstatement between tenancies, with multi-trade co-ordination and one point of contact.",
        },
        "detail_lists": {
            "es": ["Remise en état entre inquilinos", "Mantenimiento de inmuebles", "Reparaciones corrientes", "Coordinación multi-oficio"],
            "fr": ["Remise en état entre deux locataires", "Entretien d’immeubles", "Réparations courantes", "Coordination multi-métiers"],
            "de": ["Instandstellung zwischen Mietverhältnissen", "Liegenschaftsunterhalt", "Laufende Reparaturen", "Koordination mehrerer Gewerke"],
            "it": ["Ripristino tra due locazioni", "Manutenzione immobiliare", "Riparazioni correnti", "Coordinamento multi-mestiere"],
            "en": ["Reinstatement between tenancies", "Property maintenance", "Routine repairs", "Multi-trade co-ordination"],
        },
    },
]


SERVICE_DATA = [
    # Rénovation globale
    {"category": "Rénovation globale", "order": 1, "featured": True, "names": {"es": "Renovación interior completa", "fr": "Rénovation intérieure complète", "de": "Komplette Innenrenovation", "it": "Ristrutturazione completa degli interni", "en": "Complete interior renovation"}},
    {"category": "Rénovation globale", "order": 2, "featured": True, "names": {"es": "Renovación exterior", "fr": "Rénovation extérieure", "de": "Aussenrenovation", "it": "Ristrutturazione esterna", "en": "Exterior renovation"}},
    {"category": "Rénovation globale", "order": 3, "featured": True, "names": {"es": "Renovación de apartamentos y casas", "fr": "Rénovation d’appartements et de maisons", "de": "Renovation von Wohnungen und Häusern", "it": "Ristrutturazione di appartamenti e case", "en": "Renovation of flats and houses"}},
    {"category": "Rénovation globale", "order": 4, "featured": False, "names": {"es": "Coordinación de varios oficios", "fr": "Coordination multi-métiers", "de": "Koordination mehrerer Gewerke", "it": "Coordinamento multi-mestiere", "en": "Multi-trade co-ordination"}},

    # Maçonnerie
    {"category": "Maçonnerie", "order": 1, "featured": True, "names": {"es": "Trabajos de albañilería", "fr": "Travaux de maçonnerie", "de": "Maurerarbeiten", "it": "Lavori di muratura", "en": "Masonry works"}},
    {"category": "Maçonnerie", "order": 2, "featured": False, "names": {"es": "Reparaciones de albañilería", "fr": "Réparations et reprises de maçonnerie", "de": "Mauerwerksreparaturen und Ausbesserungen", "it": "Riparazioni e riprese murarie", "en": "Masonry repairs and making good"}},
    {"category": "Maçonnerie", "order": 3, "featured": False, "names": {"es": "Muros y tabiques", "fr": "Cloisons et murs", "de": "Wände und Trennwände", "it": "Pareti e divisori", "en": "Walls and partitions"}},
    {"category": "Maçonnerie", "order": 4, "featured": False, "names": {"es": "Revoques y enlucidos", "fr": "Crépis et enduits", "de": "Verputz- und Spachtelarbeiten", "it": "Intonaci e rasature", "en": "Rendering and plaster finishes"}},
    {"category": "Maçonnerie", "order": 5, "featured": False, "names": {"es": "Trabajos de fachada", "fr": "Travaux de façade", "de": "Fassadenarbeiten", "it": "Lavori di facciata", "en": "Façade works"}},

    # Isolation thermique
    {"category": "Isolation thermique", "order": 1, "featured": True, "names": {"es": "Aislamiento térmico de fachadas / ITE", "fr": "Isolation thermique des façades / ITE", "de": "Wärmedämmung von Fassaden / Aussendämmung", "it": "Isolamento termico delle facciate / cappotto esterno", "en": "External wall thermal insulation"}},
    {"category": "Isolation thermique", "order": 2, "featured": False, "names": {"es": "Aislamiento de áticos", "fr": "Isolation des combles", "de": "Dämmung von Dachräumen", "it": "Isolamento dei sottotetti", "en": "Loft insulation"}},
    {"category": "Isolation thermique", "order": 3, "featured": False, "names": {"es": "Aislamiento de sótanos", "fr": "Isolation des sous-sols", "de": "Dämmung von Untergeschossen", "it": "Isolamento dei seminterrati", "en": "Basement insulation"}},
    {"category": "Isolation thermique", "order": 4, "featured": False, "names": {"es": "Aislamiento de cubiertas", "fr": "Isolation des toitures", "de": "Dachdämmung", "it": "Isolamento dei tetti", "en": "Roof insulation"}},

    # Plâtrerie
    {"category": "Plâtrerie", "order": 1, "featured": True, "names": {"es": "Tabiques de pladur", "fr": "Cloisons en plaques de plâtre", "de": "Gipskarton-Trennwände", "it": "Pareti divisorie in cartongesso", "en": "Plasterboard partitions"}},
    {"category": "Plâtrerie", "order": 2, "featured": False, "names": {"es": "Falsos techos", "fr": "Faux plafonds", "de": "Abgehängte Decken", "it": "Controsoffitti", "en": "Suspended ceilings"}},
    {"category": "Plâtrerie", "order": 3, "featured": False, "names": {"es": "Trasdosados", "fr": "Doublages", "de": "Vorsatzschalen", "it": "Contropareti", "en": "Wall linings"}},
    {"category": "Plâtrerie", "order": 4, "featured": False, "names": {"es": "Enlucidos y acabados de yesería", "fr": "Enduits et finitions de plâtrerie", "de": "Spachtel- und Gipser-Finisharbeiten", "it": "Rasature e finiture in gesso", "en": "Plaster skimming and finishes"}},

    # Peinture
    {"category": "Peinture", "order": 1, "featured": True, "names": {"es": "Pintura interior", "fr": "Peinture intérieure", "de": "Innenanstriche", "it": "Pittura interna", "en": "Interior painting"}},
    {"category": "Peinture", "order": 2, "featured": False, "names": {"es": "Pintura exterior", "fr": "Peinture extérieure", "de": "Aussenanstriche", "it": "Pittura esterna", "en": "Exterior painting"}},
    {"category": "Peinture", "order": 3, "featured": False, "names": {"es": "Pintura de fachadas", "fr": "Peinture de façades", "de": "Fassadenanstriche", "it": "Pittura di facciate", "en": "Façade painting"}},
    {"category": "Peinture", "order": 4, "featured": False, "names": {"es": "Acabados decorativos", "fr": "Finitions décoratives", "de": "Dekorative Oberflächen", "it": "Finiture decorative", "en": "Decorative finishes"}},

    # Nettoyage
    {"category": "Nettoyage de fin de chantier", "order": 1, "featured": True, "names": {"es": "Limpieza de fin de obra", "fr": "Nettoyage de fin de chantier", "de": "Bauendreinigung", "it": "Pulizia di fine cantiere", "en": "Post-construction cleaning"}},
    {"category": "Nettoyage de fin de chantier", "order": 2, "featured": False, "names": {"es": "Limpieza antes de la entrega de llaves", "fr": "Nettoyage avant remise des clés", "de": "Reinigung vor der Schlüsselübergabe", "it": "Pulizia prima della consegna delle chiavi", "en": "Cleaning before key handover"}},

    # Régies
    {"category": "Services pour régies immobilières", "order": 1, "featured": True, "names": {"es": "Remise en état entre inquilinos", "fr": "Remise en état entre deux locataires", "de": "Instandstellung zwischen zwei Mietverhältnissen", "it": "Ripristino tra due locazioni", "en": "Reinstatement between tenancies"}},
    {"category": "Services pour régies immobilières", "order": 2, "featured": False, "names": {"es": "Mantenimiento de inmuebles", "fr": "Entretien immobilier", "de": "Liegenschaftsunterhalt", "it": "Manutenzione immobiliare", "en": "Property maintenance"}},
    {"category": "Services pour régies immobilières", "order": 3, "featured": False, "names": {"es": "Reparaciones corrientes", "fr": "Réparations courantes", "de": "Laufende Reparaturen", "it": "Riparazioni correnti", "en": "Routine repairs"}},
    {"category": "Services pour régies immobilières", "order": 4, "featured": False, "names": {"es": "Coordinación multi-oficio para gerencias", "fr": "Coordination multi-métiers pour régies", "de": "Gewerke-Koordination für Liegenschaftsverwaltungen", "it": "Coordinamento multi-mestiere per amministrazioni immobiliari", "en": "Multi-trade co-ordination for property managers"}},
]


BENEFITS = [
    {
        "order": 1,
        "icon": "fa-solid fa-user-check",
        "title": {
            "es": "Un solo interlocutor",
            "fr": "Interlocuteur unique",
            "de": "Eine Ansprechperson",
            "it": "Un unico referente",
            "en": "One point of contact",
        },
        "description": {
            "es": "Un contacto claro para facilitar el seguimiento y la coordinación de los trabajos.",
            "fr": "Un contact clair pour faciliter le suivi et la coordination des travaux.",
            "de": "Eine klare Ansprechperson für eine einfache Koordination und Nachverfolgung der Arbeiten.",
            "it": "Un referente chiaro per facilitare il coordinamento e il monitoraggio dei lavori.",
            "en": "A clear point of contact to simplify co-ordination and follow-up throughout the work.",
        },
    },
    {
        "order": 2,
        "icon": "fa-solid fa-file-signature",
        "title": {
            "es": "Presupuesto claro",
            "fr": "Devis clair",
            "de": "Klare Offerte",
            "it": "Offerta chiara",
            "en": "Clear quotation",
        },
        "description": {
            "es": "Alcance y organización explicados de forma comprensible antes de iniciar la intervención.",
            "fr": "Un périmètre et une organisation expliqués de manière compréhensible avant le début de l’intervention.",
            "de": "Leistungsumfang und Organisation werden vor Beginn der Arbeiten verständlich erläutert.",
            "it": "Ambito e organizzazione vengono spiegati in modo chiaro prima dell’inizio dell’intervento.",
            "en": "Scope and organisation are explained clearly before the work begins.",
        },
    },
    {
        "order": 3,
        "icon": "fa-solid fa-check-double",
        "title": {
            "es": "Acabados cuidados",
            "fr": "Finitions soignées",
            "de": "Sorgfältige Ausführung",
            "it": "Finiture curate",
            "en": "Careful finishing",
        },
        "description": {
            "es": "Atención a la preparación, ejecución y limpieza para obtener un resultado limpio y profesional.",
            "fr": "Une attention portée à la préparation, à l’exécution et à la propreté pour un résultat net et professionnel.",
            "de": "Sorgfalt bei Vorbereitung, Ausführung und Sauberkeit für ein professionelles Ergebnis.",
            "it": "Cura nella preparazione, nell’esecuzione e nella pulizia per un risultato ordinato e professionale.",
            "en": "Attention to preparation, workmanship and cleanliness for a neat, professional result.",
        },
    },
]


# ======================================================================
# PHASE 2 · CORE CONTENT / CONTENIDO CORE
# ======================================================================

SITE_CONTENT = {
    "company_name": "V&V Swiss Services",
    "slogan": {
        "es": "Renovación, coordinación y acabados cuidados en Suiza.",
        "fr": "Rénovation, coordination et finitions soignées en Suisse.",
        "de": "Renovation, Koordination und sorgfältige Ausführung in der Schweiz.",
        "it": "Ristrutturazione, coordinamento e finiture curate in Svizzera.",
        "en": "Renovation, co-ordination and careful finishing in Switzerland.",
    },
    "country": "Switzerland",
    "canton": "Vaud",
}

HOME_CONTENT = {
    "title": {
        "es": "Renovación integral con un solo interlocutor",
        "fr": "La rénovation, avec un seul interlocuteur",
        "de": "Renovation mit einer einzigen Ansprechperson",
        "it": "Ristrutturazione con un unico referente",
        "en": "Renovation with one point of contact",
    },
    "subtitle": {
        "es": "V&V Swiss Services coordina trabajos de renovación interior y exterior para particulares, propietarios, régies, PPE y profesionales de la construcción en el cantón de Vaud y la Suisse romande.",
        "fr": "V&V Swiss Services coordonne vos travaux de rénovation intérieure et extérieure pour particuliers, propriétaires, régies, PPE et professionnels de la construction dans le canton de Vaud et en Suisse romande.",
        "de": "V&V Swiss Services koordiniert Innen- und Aussenrenovationen für Privatpersonen, Eigentümerschaften, Liegenschaftsverwaltungen, Stockwerkeigentum und Baufachleute im Kanton Waadt und in der Romandie.",
        "it": "V&V Swiss Services coordina lavori di ristrutturazione interna ed esterna per privati, proprietari, amministrazioni immobiliari, PPP e professionisti dell’edilizia nel Canton Vaud e nella Svizzera romanda.",
        "en": "V&V Swiss Services co-ordinates interior and exterior renovation work for private clients, property owners, property managers, condominium associations and construction professionals in the canton of Vaud and French-speaking Switzerland.",
    },
}

ABOUT_CONTENT = {
    "intro_title": {
        "es": "Experiencia local, trabajo cuidado",
        "fr": "Une expérience locale, un travail soigné",
        "de": "Lokale Erfahrung, sorgfältige Arbeit",
        "it": "Esperienza locale, lavoro curato",
        "en": "Local experience, careful workmanship",
    },
    "intro_text": {
        "es": "V&V Swiss Services acompaña proyectos de renovación interior y exterior con una organización clara, un trato cercano y una atención constante a la calidad de ejecución. Nuestro enfoque combina experiencia en el sector de la construcción en Suiza con la flexibilidad de un especialista local.",
        "fr": "V&V Swiss Services accompagne des projets de rénovation intérieure et extérieure avec une organisation claire, une relation de proximité et une attention constante portée à la qualité d’exécution. Notre approche associe l’expérience du secteur de la construction en Suisse à la flexibilité d’un spécialiste local.",
        "de": "V&V Swiss Services begleitet Innen- und Aussenrenovationen mit klarer Organisation, persönlicher Betreuung und einem konsequenten Fokus auf die Ausführungsqualität. Unser Ansatz verbindet Erfahrung im Schweizer Bauwesen mit der Flexibilität eines lokalen Spezialisten.",
        "it": "V&V Swiss Services accompagna progetti di ristrutturazione interna ed esterna con un’organizzazione chiara, un rapporto diretto e un’attenzione costante alla qualità dell’esecuzione. Il nostro approccio unisce l’esperienza nel settore edile svizzero alla flessibilità di uno specialista locale.",
        "en": "V&V Swiss Services supports interior and exterior renovation projects with clear organisation, close client contact and consistent attention to workmanship. Our approach combines experience in the Swiss construction sector with the flexibility of a local specialist.",
    },
    "mission": {
        "es": "Ofrecer trabajos de renovación con un nivel de calidad acorde con las exigencias suizas, respetando la planificación acordada y manteniendo una relación cercana con cada cliente. Adaptamos nuestras soluciones a las necesidades técnicas, estructurales, energéticas y medioambientales de cada proyecto.",
        "fr": "Proposer des travaux de rénovation répondant aux exigences de qualité attendues en Suisse, dans le respect de la planification convenue et avec une relation de proximité. Nous adaptons nos solutions aux besoins techniques, structurels, énergétiques et environnementaux de chaque projet.",
        "de": "Renovationsarbeiten anzubieten, die den in der Schweiz erwarteten Qualitätsansprüchen entsprechen, die vereinbarte Planung einzuhalten und eine persönliche Kundenbeziehung zu pflegen. Unsere Lösungen werden auf die technischen, baulichen, energetischen und ökologischen Anforderungen jedes Projekts abgestimmt.",
        "it": "Offrire lavori di ristrutturazione conformi agli standard qualitativi attesi in Svizzera, rispettando la pianificazione concordata e mantenendo un rapporto diretto con il cliente. Adattiamo le nostre soluzioni alle esigenze tecniche, strutturali, energetiche e ambientali di ogni progetto.",
        "en": "To deliver renovation work to the quality standards expected in Switzerland, respecting the agreed programme and maintaining close client contact. We adapt our solutions to the technical, structural, energy and environmental requirements of each project.",
    },
    "vision": {
        "es": "Consolidarnos como una empresa de referencia en renovación y aislamiento en la Suisse romande, reconocida por la calidad de los acabados, la claridad en la coordinación y la confianza de sus clientes.",
        "fr": "Nous consolider comme une entreprise de référence en rénovation et en isolation en Suisse romande, reconnue pour la qualité de ses finitions, la clarté de sa coordination et la confiance de ses clients.",
        "de": "Uns als Referenzunternehmen für Renovation und Dämmung in der Romandie zu etablieren, anerkannt für sorgfältige Ausführung, klare Koordination und das Vertrauen unserer Kundschaft.",
        "it": "Consolidarci come impresa di riferimento per la ristrutturazione e l’isolamento nella Svizzera romanda, riconosciuta per la qualità delle finiture, la chiarezza del coordinamento e la fiducia dei clienti.",
        "en": "To establish ourselves as a reference company for renovation and insulation in French-speaking Switzerland, recognised for the quality of our finishes, clear co-ordination and the trust of our clients.",
    },
    "history": {
        "es": "V&V Swiss Services se apoya en más de 20 años de experiencia en el sector de la construcción en Suiza. Este recorrido aporta conocimiento técnico, comprensión de las exigencias locales y una forma de trabajo orientada a soluciones prácticas, comunicación directa y ejecución cuidada.",
        "fr": "V&V Swiss Services s’appuie sur plus de 20 ans d’expérience dans le secteur de la construction en Suisse. Ce parcours apporte une solide connaissance technique, une bonne compréhension des exigences locales et une manière de travailler fondée sur des solutions pratiques, une communication directe et une exécution soignée.",
        "de": "V&V Swiss Services stützt sich auf mehr als 20 Jahre Erfahrung im Schweizer Bauwesen. Diese Erfahrung bringt technisches Know-how, ein gutes Verständnis der lokalen Anforderungen sowie eine Arbeitsweise mit sich, die auf praktische Lösungen, direkte Kommunikation und sorgfältige Ausführung ausgerichtet ist.",
        "it": "V&V Swiss Services si basa su oltre 20 anni di esperienza nel settore delle costruzioni in Svizzera. Questo percorso porta competenza tecnica, una buona conoscenza delle esigenze locali e un metodo di lavoro orientato a soluzioni pratiche, comunicazione diretta ed esecuzione curata.",
        "en": "V&V Swiss Services draws on more than 20 years of experience in the Swiss construction sector. This background brings technical knowledge, an understanding of local requirements and a way of working based on practical solutions, direct communication and careful execution.",
    },
}

COMPANY_VALUES = [
    {
        "order": 1,
        "title": {"es": "Calidad", "fr": "Qualité", "de": "Qualität", "it": "Qualità", "en": "Quality"},
        "description": {
            "es": "Trabajo bien ejecutado, atención a los detalles y acabados limpios en cada etapa.",
            "fr": "Un travail bien réalisé, une attention portée aux détails et des finitions propres à chaque étape.",
            "de": "Sorgfältige Arbeit, Aufmerksamkeit für Details und saubere Abschlüsse in jeder Etappe.",
            "it": "Lavoro ben eseguito, attenzione ai dettagli e finiture pulite in ogni fase.",
            "en": "Well-executed work, attention to detail and neat finishes at every stage.",
        },
    },
    {
        "order": 2,
        "title": {"es": "Honestidad", "fr": "Honnêteté", "de": "Ehrlichkeit", "it": "Onestà", "en": "Honesty"},
        "description": {
            "es": "Información clara sobre el alcance del trabajo, las necesidades del proyecto y la organización prevista.",
            "fr": "Des informations claires sur l’étendue des travaux, les besoins du projet et l’organisation prévue.",
            "de": "Klare Informationen zu Leistungsumfang, Projektanforderungen und geplanter Organisation.",
            "it": "Informazioni chiare sull’ambito dei lavori, sulle esigenze del progetto e sull’organizzazione prevista.",
            "en": "Clear information about the scope of work, project requirements and the planned organisation.",
        },
    },
    {
        "order": 3,
        "title": {"es": "Confianza", "fr": "Confiance", "de": "Vertrauen", "it": "Fiducia", "en": "Trust"},
        "description": {
            "es": "Compromiso con lo acordado, comunicación directa y seguimiento responsable de los trabajos.",
            "fr": "Respect des engagements, communication directe et suivi responsable des travaux.",
            "de": "Verlässlichkeit bei Vereinbarungen, direkte Kommunikation und verantwortungsvolle Begleitung der Arbeiten.",
            "it": "Rispetto degli impegni, comunicazione diretta e monitoraggio responsabile dei lavori.",
            "en": "Commitment to what has been agreed, direct communication and responsible follow-up of the work.",
        },
    },
    {
        "order": 4,
        "title": {"es": "Tradición e innovación", "fr": "Tradition et innovation", "de": "Tradition und Innovation", "it": "Tradizione e innovazione", "en": "Tradition and innovation"},
        "description": {
            "es": "Respeto por el oficio y las buenas prácticas, combinados con soluciones técnicas actuales.",
            "fr": "Le respect du métier et des bonnes pratiques, associé à des solutions techniques actuelles.",
            "de": "Respekt für das Handwerk und bewährte Praktiken, kombiniert mit zeitgemässen technischen Lösungen.",
            "it": "Rispetto per il mestiere e per le buone pratiche, unito a soluzioni tecniche attuali.",
            "en": "Respect for the craft and sound practice, combined with current technical solutions.",
        },
    },
    {
        "order": 5,
        "title": {"es": "Respeto por el entorno", "fr": "Respect de l’environnement", "de": "Respekt für die Umwelt", "it": "Rispetto per l’ambiente", "en": "Respect for the environment"},
        "description": {
            "es": "Obras ordenadas y soluciones orientadas a mejorar el uso de los recursos y el rendimiento energético.",
            "fr": "Des chantiers organisés et des solutions visant une meilleure utilisation des ressources et une performance énergétique améliorée.",
            "de": "Geordnete Baustellen und Lösungen für einen bewussteren Ressourceneinsatz und eine bessere Energieeffizienz.",
            "it": "Cantieri ordinati e soluzioni orientate a un uso più efficiente delle risorse e a migliori prestazioni energetiche.",
            "en": "Well-organised sites and solutions aimed at better use of resources and improved energy performance.",
        },
    },
]

PROCESS_STEPS = [
    {
        "number": 1,
        "icon": "fa-solid fa-comments",
        "title": {"es": "Primer contacto", "fr": "Premier échange", "de": "Erstes Gespräch", "it": "Primo contatto", "en": "Initial discussion"},
        "description": {
            "es": "Escuchamos sus necesidades, el tipo de inmueble, el alcance previsto y las prioridades del proyecto.",
            "fr": "Nous prenons connaissance de vos besoins, du type de bâtiment, de l’étendue envisagée et des priorités du projet.",
            "de": "Wir klären Ihre Bedürfnisse, die Gebäudeart, den vorgesehenen Umfang und die Prioritäten des Projekts.",
            "it": "Raccogliamo le vostre esigenze, il tipo di immobile, l’ambito previsto e le priorità del progetto.",
            "en": "We discuss your requirements, the type of property, the intended scope and the project priorities.",
        },
    },
    {
        "number": 2,
        "icon": "fa-solid fa-ruler-combined",
        "title": {"es": "Evaluación", "fr": "Évaluation", "de": "Beurteilung", "it": "Valutazione", "en": "Assessment"},
        "description": {
            "es": "Cuando el proyecto lo requiere, revisamos el lugar, los soportes existentes y las condiciones técnicas antes de definir la intervención.",
            "fr": "Lorsque le projet le nécessite, nous examinons les lieux, les supports existants et les contraintes techniques avant de définir l’intervention.",
            "de": "Wenn es das Projekt erfordert, prüfen wir die Situation vor Ort, bestehende Untergründe und technische Rahmenbedingungen.",
            "it": "Quando il progetto lo richiede, valutiamo gli spazi, i supporti esistenti e i vincoli tecnici prima di definire l’intervento.",
            "en": "Where required, we assess the site, existing surfaces and technical constraints before defining the work.",
        },
    },
    {
        "number": 3,
        "icon": "fa-solid fa-file-lines",
        "title": {"es": "Propuesta y planificación", "fr": "Offre et planification", "de": "Offerte und Planung", "it": "Offerta e pianificazione", "en": "Quotation and planning"},
        "description": {
            "es": "Definimos el alcance de los trabajos y organizamos las etapas necesarias para una ejecución clara y coordinada.",
            "fr": "Nous définissons l’étendue des travaux et organisons les étapes nécessaires à une réalisation claire et coordonnée.",
            "de": "Wir definieren den Leistungsumfang und organisieren die notwendigen Etappen für eine klare und koordinierte Ausführung.",
            "it": "Definiamo l’ambito dei lavori e organizziamo le fasi necessarie per un’esecuzione chiara e coordinata.",
            "en": "We define the scope of work and organise the stages required for clear and co-ordinated delivery.",
        },
    },
    {
        "number": 4,
        "icon": "fa-solid fa-person-digging",
        "title": {"es": "Ejecución", "fr": "Réalisation", "de": "Ausführung", "it": "Esecuzione", "en": "Delivery"},
        "description": {
            "es": "Coordinamos los trabajos, protegemos las zonas de intervención y hacemos seguimiento de la calidad durante la ejecución.",
            "fr": "Nous coordonnons les travaux, protégeons les zones d’intervention et suivons la qualité tout au long de l’exécution.",
            "de": "Wir koordinieren die Arbeiten, schützen die Arbeitsbereiche und begleiten die Qualität während der Ausführung.",
            "it": "Coordiniamo i lavori, proteggiamo le aree di intervento e monitoriamo la qualità durante l’esecuzione.",
            "en": "We co-ordinate the work, protect the work areas and monitor quality throughout delivery.",
        },
    },
    {
        "number": 5,
        "icon": "fa-solid fa-circle-check",
        "title": {"es": "Control y entrega", "fr": "Contrôle et remise", "de": "Kontrolle und Übergabe", "it": "Controllo e consegna", "en": "Final check and handover"},
        "description": {
            "es": "Revisamos el trabajo realizado y preparamos los espacios para una entrega limpia y ordenada.",
            "fr": "Nous vérifions les travaux réalisés et préparons les espaces pour une remise propre et ordonnée.",
            "de": "Wir prüfen die ausgeführten Arbeiten und bereiten die Räume für eine saubere und geordnete Übergabe vor.",
            "it": "Verifichiamo i lavori eseguiti e prepariamo gli spazi per una consegna pulita e ordinata.",
            "en": "We review the completed work and prepare the spaces for a clean and orderly handover.",
        },
    },
]

SERVICE_AREAS = [
    {
        "name": "Canton de Vaud",
        "canton": "Vaud",
        "order": 1,
        "description": {
            "es": "Intervenciones de renovación y mantenimiento en el cantón de Vaud.",
            "fr": "Interventions de rénovation et d’entretien dans le canton de Vaud.",
            "de": "Renovations- und Unterhaltsarbeiten im Kanton Waadt.",
            "it": "Interventi di ristrutturazione e manutenzione nel Canton Vaud.",
            "en": "Renovation and maintenance work throughout the canton of Vaud.",
        },
    },
    {
        "name": "Lausanne et environs",
        "canton": "Vaud",
        "order": 2,
        "description": {
            "es": "Atención a proyectos en Lausanne y sus alrededores, según disponibilidad y alcance.",
            "fr": "Prise en charge de projets à Lausanne et dans ses environs, selon disponibilité et étendue des travaux.",
            "de": "Projekte in Lausanne und Umgebung, je nach Verfügbarkeit und Leistungsumfang.",
            "it": "Progetti a Losanna e dintorni, in base alla disponibilità e all’entità dei lavori.",
            "en": "Projects in Lausanne and the surrounding area, subject to availability and scope of work.",
        },
    },
    {
        "name": "Suisse romande",
        "canton": "",
        "order": 3,
        "description": {
            "es": "Estudio de proyectos en la Suisse romande según ubicación, alcance y planificación.",
            "fr": "Étude de projets en Suisse romande selon la localisation, l’étendue et la planification.",
            "de": "Prüfung von Projekten in der Romandie je nach Standort, Umfang und Terminplanung.",
            "it": "Valutazione di progetti nella Svizzera romanda in funzione della località, dell’ambito e della pianificazione.",
            "en": "Projects in French-speaking Switzerland can be considered depending on location, scope and programme.",
        },
    },
]

STATISTICS = [
    {
        "value": "20+",
        "order": 1,
        "title": {
            "es": "años de experiencia en construcción en Suiza",
            "fr": "ans d’expérience dans la construction en Suisse",
            "de": "Jahre Erfahrung im Schweizer Bauwesen",
            "it": "anni di esperienza nell’edilizia in Svizzera",
            "en": "years of experience in Swiss construction",
        },
    },
]

FAQ_CATEGORIES = [
    {"order": 1, "name": {"es": "Presupuesto y proyecto", "fr": "Devis et projet", "de": "Offerte und Projekt", "it": "Offerta e progetto", "en": "Quotation and project"}},
    {"order": 2, "name": {"es": "Renovación", "fr": "Rénovation", "de": "Renovation", "it": "Ristrutturazione", "en": "Renovation"}},
    {"order": 3, "name": {"es": "Aislamiento térmico", "fr": "Isolation thermique", "de": "Wärmedämmung", "it": "Isolamento termico", "en": "Thermal insulation"}},
    {"order": 4, "name": {"es": "Régies y PPE", "fr": "Régies et PPE", "de": "Liegenschaftsverwaltungen und STWE", "it": "Amministrazioni e PPP", "en": "Property managers and condominiums"}},
    {"order": 5, "name": {"es": "Organización de obra", "fr": "Organisation des travaux", "de": "Arbeitsorganisation", "it": "Organizzazione dei lavori", "en": "Work organisation"}},
]

FAQS = [
    {
        "category": "Devis et projet",
        "order": 1,
        "question": {
            "fr": "Comment demander un devis ?",
            "de": "Wie kann ich eine Offerte anfordern?",
            "it": "Come posso richiedere un’offerta?",
            "en": "How can I request a quotation?",
        },
        "answer": {
            "fr": "Vous pouvez nous transmettre votre demande via le formulaire de contact en décrivant le type de travaux, la localisation et vos principales attentes. Des photos peuvent également aider à préparer le premier échange.",
            "de": "Sie können Ihre Anfrage über das Kontaktformular senden und die Art der Arbeiten, den Standort sowie Ihre wichtigsten Anforderungen beschreiben. Fotos können für die erste Einschätzung ebenfalls hilfreich sein.",
            "it": "Potete inviare la richiesta tramite il modulo di contatto indicando il tipo di lavori, la località e le principali esigenze. Anche alcune foto possono facilitare una prima valutazione.",
            "en": "You can send your enquiry through the contact form, describing the type of work, location and main requirements. Photos can also help with the initial assessment.",
        },
    },
    {
        "category": "Devis et projet",
        "order": 2,
        "question": {
            "fr": "Une visite technique est-elle toujours nécessaire ?",
            "de": "Ist eine technische Besichtigung immer erforderlich?",
            "it": "È sempre necessario un sopralluogo tecnico?",
            "en": "Is a technical visit always required?",
        },
        "answer": {
            "fr": "Pas nécessairement. Pour certains travaux simples, un premier échange détaillé peut suffire. Pour les rénovations plus importantes ou lorsque l’état des supports doit être vérifié, une visite sur place est recommandée.",
            "de": "Nicht immer. Bei einfachen Arbeiten kann ein ausführliches Erstgespräch ausreichen. Bei grösseren Renovationen oder wenn bestehende Untergründe beurteilt werden müssen, ist eine Besichtigung empfehlenswert.",
            "it": "Non sempre. Per lavori semplici può essere sufficiente un primo scambio dettagliato. Per ristrutturazioni più importanti o quando occorre verificare i supporti esistenti, è consigliato un sopralluogo.",
            "en": "Not always. For straightforward work, a detailed initial discussion may be sufficient. For larger renovations or where existing surfaces need to be assessed, a site visit is recommended.",
        },
    },
    {
        "category": "Rénovation",
        "order": 1,
        "question": {
            "fr": "Pouvez-vous coordonner plusieurs corps de métier ?",
            "de": "Können Sie mehrere Gewerke koordinieren?",
            "it": "Potete coordinare più mestieri?",
            "en": "Can you co-ordinate several trades?",
        },
        "answer": {
            "fr": "Oui. La coordination multi-métiers fait partie de notre approche pour les projets qui réunissent plusieurs interventions, avec un interlocuteur unique pour faciliter le suivi.",
            "de": "Ja. Die Koordination mehrerer Gewerke gehört bei Projekten mit verschiedenen Arbeiten zu unserem Ansatz. Eine zentrale Ansprechperson vereinfacht dabei die Abstimmung.",
            "it": "Sì. Il coordinamento di più mestieri fa parte del nostro approccio nei progetti che richiedono interventi diversi, con un unico referente per semplificare il monitoraggio.",
            "en": "Yes. Multi-trade co-ordination forms part of our approach for projects involving several types of work, with one point of contact to simplify follow-up.",
        },
    },
    {
        "category": "Rénovation",
        "order": 2,
        "question": {
            "fr": "Intervenez-vous sur des appartements et des maisons ?",
            "de": "Arbeiten Sie in Wohnungen und Häusern?",
            "it": "Intervenite in appartamenti e case?",
            "en": "Do you work on both flats and houses?",
        },
        "answer": {
            "fr": "Oui. Nous étudions les projets de rénovation d’appartements, de maisons et d’autres bâtiments selon les travaux à réaliser, l’état existant et la localisation.",
            "de": "Ja. Wir prüfen Renovationsprojekte für Wohnungen, Häuser und weitere Gebäude je nach Umfang, bestehendem Zustand und Standort.",
            "it": "Sì. Valutiamo progetti di ristrutturazione di appartamenti, case e altri edifici in funzione dei lavori, dello stato esistente e della località.",
            "en": "Yes. We consider renovation projects for flats, houses and other buildings according to the work required, the existing condition and the location.",
        },
    },
    {
        "category": "Isolation thermique",
        "order": 1,
        "question": {
            "fr": "Quels éléments peuvent être isolés ?",
            "de": "Welche Gebäudeteile können gedämmt werden?",
            "it": "Quali parti dell’edificio possono essere isolate?",
            "en": "Which parts of a building can be insulated?",
        },
        "answer": {
            "fr": "Selon le bâtiment, l’isolation peut concerner les façades, les combles, les sous-sols ou les toitures. Le choix dépend de l’état existant et des objectifs du projet.",
            "de": "Je nach Gebäude können Fassaden, Dachräume, Untergeschosse oder Dächer gedämmt werden. Die geeignete Lösung hängt vom Bestand und den Projektzielen ab.",
            "it": "A seconda dell’edificio, l’isolamento può interessare facciate, sottotetti, seminterrati o tetti. La soluzione dipende dallo stato esistente e dagli obiettivi del progetto.",
            "en": "Depending on the building, insulation may be applied to façades, lofts, basements or roofs. The appropriate solution depends on the existing condition and project objectives.",
        },
    },
    {
        "category": "Isolation thermique",
        "order": 2,
        "question": {
            "fr": "L’isolation thermique peut-elle améliorer le confort du logement ?",
            "de": "Kann Wärmedämmung den Wohnkomfort verbessern?",
            "it": "L’isolamento termico può migliorare il comfort dell’abitazione?",
            "en": "Can thermal insulation improve comfort?",
        },
        "answer": {
            "fr": "Une isolation adaptée peut contribuer à réduire les pertes de chaleur et à améliorer le confort thermique. Une évaluation du bâtiment permet de déterminer les zones pertinentes.",
            "de": "Eine geeignete Dämmung kann Wärmeverluste reduzieren und den thermischen Komfort verbessern. Eine Beurteilung des Gebäudes hilft, die relevanten Bereiche zu bestimmen.",
            "it": "Un isolamento adeguato può contribuire a ridurre le dispersioni di calore e a migliorare il comfort termico. Una valutazione dell’edificio aiuta a individuare le zone più pertinenti.",
            "en": "Suitable insulation can help reduce heat loss and improve thermal comfort. An assessment of the building helps identify the most relevant areas.",
        },
    },
    {
        "category": "Régies et PPE",
        "order": 1,
        "question": {
            "fr": "Proposez-vous des remises en état entre deux locataires ?",
            "de": "Bieten Sie Instandstellungen zwischen zwei Mietverhältnissen an?",
            "it": "Offrite ripristini tra due locazioni?",
            "en": "Do you provide reinstatement between tenancies?",
        },
        "answer": {
            "fr": "Oui. Nous pouvons organiser les travaux nécessaires entre deux occupations, notamment réparations, peinture, plâtrerie, petites interventions de maçonnerie et nettoyage de fin de chantier.",
            "de": "Ja. Wir können die notwendigen Arbeiten zwischen zwei Nutzungen organisieren, darunter Reparaturen, Maler- und Gipserarbeiten, kleinere Maurerarbeiten sowie Bauendreinigung.",
            "it": "Sì. Possiamo organizzare i lavori necessari tra due occupazioni, tra cui riparazioni, pittura, cartongesso, piccoli lavori murari e pulizia di fine cantiere.",
            "en": "Yes. We can organise the work required between occupancies, including repairs, painting, plastering, minor masonry and post-construction cleaning.",
        },
    },
    {
        "category": "Régies et PPE",
        "order": 2,
        "question": {
            "fr": "Travaillez-vous avec les régies immobilières et les administrateurs PPE ?",
            "de": "Arbeiten Sie mit Liegenschaftsverwaltungen und STWE-Verwaltungen zusammen?",
            "it": "Lavorate con amministrazioni immobiliari e amministratori PPP?",
            "en": "Do you work with property managers and condominium administrators?",
        },
        "answer": {
            "fr": "Oui. Nous proposons un accompagnement adapté aux besoins des régies et des administrateurs PPE, notamment pour l’entretien, les réparations, les remises en état et la coordination de plusieurs corps de métier.",
            "de": "Ja. Wir unterstützen Liegenschaftsverwaltungen und STWE-Verwaltungen bei Unterhalt, Reparaturen, Instandstellungen und der Koordination mehrerer Gewerke.",
            "it": "Sì. Offriamo un supporto adatto alle amministrazioni immobiliari e agli amministratori PPP per manutenzione, riparazioni, ripristini e coordinamento di più mestieri.",
            "en": "Yes. We support property managers and condominium administrators with maintenance, repairs, reinstatement and the co-ordination of several trades.",
        },
    },
    {
        "category": "Organisation des travaux",
        "order": 1,
        "question": {
            "fr": "Comment protégez-vous les zones de travail ?",
            "de": "Wie schützen Sie die Arbeitsbereiche?",
            "it": "Come proteggete le aree di lavoro?",
            "en": "How do you protect work areas?",
        },
        "answer": {
            "fr": "La protection est adaptée au type d’intervention et aux surfaces existantes. L’objectif est de limiter les salissures, de maintenir un chantier organisé et de faciliter la remise en état finale.",
            "de": "Der Schutz wird an die Art der Arbeiten und die vorhandenen Oberflächen angepasst. Ziel ist es, Verschmutzungen zu begrenzen, die Baustelle geordnet zu halten und die abschliessende Reinigung zu erleichtern.",
            "it": "La protezione viene adattata al tipo di intervento e alle superfici esistenti. L’obiettivo è limitare lo sporco, mantenere il cantiere ordinato e facilitare la pulizia finale.",
            "en": "Protection is adapted to the type of work and the existing surfaces. The aim is to limit dirt, keep the site organised and make final cleaning easier.",
        },
    },
    {
        "category": "Organisation des travaux",
        "order": 2,
        "question": {
            "fr": "Comment suivez-vous l’avancement d’un projet ?",
            "de": "Wie wird der Projektfortschritt begleitet?",
            "it": "Come viene seguito l’avanzamento del progetto?",
            "en": "How is project progress monitored?",
        },
        "answer": {
            "fr": "Le suivi repose sur une organisation claire, un interlocuteur identifié et une communication régulière sur les principales étapes du chantier.",
            "de": "Die Begleitung basiert auf einer klaren Organisation, einer definierten Ansprechperson und regelmässiger Kommunikation zu den wichtigsten Projektetappen.",
            "it": "Il monitoraggio si basa su un’organizzazione chiara, un referente definito e una comunicazione regolare sulle principali fasi del cantiere.",
            "en": "Progress is managed through clear organisation, an identified point of contact and regular communication on the main stages of the work.",
        },
    },
]

INSTITUTIONAL_PAGES = [
    {
        "slug_fr": "entreprise",
        "title": {
            "es": "Empresa",
            "fr": "Entreprise",
            "de": "Unternehmen",
            "it": "Azienda",
            "en": "Company",
        },
        "content": {
            "es": "V&V Swiss Services acompaña proyectos de renovación interior y exterior en el cantón de Vaud y la Suisse romande. Nuestro enfoque combina experiencia en el sector de la construcción en Suiza, coordinación clara y atención personalizada.",
            "fr": "V&V Swiss Services accompagne des projets de rénovation intérieure et extérieure dans le canton de Vaud et en Suisse romande. Notre approche associe l’expérience du secteur de la construction en Suisse, une coordination claire et un accompagnement personnalisé.",
            "de": "V&V Swiss Services begleitet Innen- und Aussenrenovationen im Kanton Waadt und in der Romandie. Unser Ansatz verbindet Erfahrung im Schweizer Bauwesen mit klarer Koordination und persönlicher Betreuung.",
            "it": "V&V Swiss Services accompagna progetti di ristrutturazione interna ed esterna nel Canton Vaud e nella Svizzera romanda. Il nostro approccio unisce esperienza nel settore edile svizzero, coordinamento chiaro e assistenza personalizzata.",
            "en": "V&V Swiss Services supports interior and exterior renovation projects in the canton of Vaud and French-speaking Switzerland. Our approach combines experience in the Swiss construction sector with clear co-ordination and personal service.",
        },
    },
    {
        "slug_fr": "mentions-legales",
        "title": {
            "es": "Aviso legal",
            "fr": "Mentions légales",
            "de": "Impressum",
            "it": "Note legali",
            "en": "Legal notice",
        },
        "content": {
            "es": "Esta página reúne la información legal vinculada a V&V Swiss Services y al uso del sitio web. Los datos jurídicos oficiales, la identificación de la empresa y los datos de contacto deben mantenerse actualizados desde la configuración del sitio.",
            "fr": "Cette page regroupe les informations légales liées à V&V Swiss Services et à l’utilisation du site. Les données juridiques officielles, l’identification de l’entreprise et les coordonnées doivent être tenues à jour depuis la configuration du site.",
            "de": "Diese Seite enthält die rechtlichen Informationen zu V&V Swiss Services und zur Nutzung der Website. Offizielle Unternehmensangaben, rechtliche Identifikationsdaten und Kontaktdaten müssen in der Website-Konfiguration aktuell gehalten werden.",
            "it": "Questa pagina raccoglie le informazioni legali relative a V&V Swiss Services e all’utilizzo del sito. I dati giuridici ufficiali, l’identificazione dell’azienda e i contatti devono essere mantenuti aggiornati nella configurazione del sito.",
            "en": "This page contains legal information relating to V&V Swiss Services and the use of this website. Official company details, legal identification and contact information must be kept up to date in the site configuration.",
        },
    },
    {
        "slug_fr": "protection-des-donnees",
        "title": {
            "es": "Protección de datos",
            "fr": "Protection des données",
            "de": "Datenschutz",
            "it": "Protezione dei dati",
            "en": "Data protection",
        },
        "content": {
            "es": "Los datos transmitidos mediante los formularios del sitio se utilizan para responder a solicitudes, preparar contactos comerciales y organizar, cuando corresponda, una visita o propuesta. La información debe tratarse únicamente durante el tiempo necesario para la finalidad correspondiente y conforme a las obligaciones aplicables.",
            "fr": "Les données transmises via les formulaires du site sont utilisées pour répondre aux demandes, préparer les échanges commerciaux et organiser, le cas échéant, une visite ou une proposition. Les informations doivent être traitées uniquement pendant la durée nécessaire à la finalité concernée et conformément aux obligations applicables.",
            "de": "Die über die Formulare der Website übermittelten Daten werden verwendet, um Anfragen zu beantworten, geschäftliche Kontakte vorzubereiten und gegebenenfalls eine Besichtigung oder Offerte zu organisieren. Die Informationen sollen nur so lange bearbeitet werden, wie dies für den jeweiligen Zweck erforderlich ist und den anwendbaren Vorgaben entspricht.",
            "it": "I dati trasmessi tramite i moduli del sito vengono utilizzati per rispondere alle richieste, preparare i contatti commerciali e, se necessario, organizzare un sopralluogo o un’offerta. Le informazioni devono essere trattate solo per il tempo necessario allo scopo previsto e nel rispetto degli obblighi applicabili.",
            "en": "Data submitted through the website forms is used to respond to enquiries, prepare commercial discussions and, where relevant, organise a visit or quotation. Information should only be processed for as long as necessary for the relevant purpose and in accordance with applicable obligations.",
        },
    },
]

PROFESSIONAL_PAGE = {
    "hero_title": {
        "es": "Un socio fiable para sus inmuebles y proyectos",
        "fr": "Un partenaire fiable pour vos biens et vos projets",
        "de": "Ein zuverlässiger Partner für Ihre Liegenschaften und Projekte",
        "it": "Un partner affidabile per i vostri immobili e progetti",
        "en": "A reliable partner for your properties and projects",
    },
    "hero_text": {
        "es": "Acompañamos a régies inmobiliarias, administradores PPE, empresas generales, constructores y arquitectos con intervenciones coordinadas, mantenimiento, reparaciones y remise en état.",
        "fr": "Nous accompagnons les régies immobilières, administrateurs PPE, entreprises générales, constructeurs et architectes avec des interventions coordonnées, de l’entretien, des réparations et des remises en état.",
        "de": "Wir unterstützen Liegenschaftsverwaltungen, STWE-Verwaltungen, Generalunternehmen, Bauunternehmen und Architekturbüros mit koordinierten Arbeiten, Unterhalt, Reparaturen und Instandstellungen.",
        "it": "Affianchiamo amministrazioni immobiliari, amministratori PPP, imprese generali, costruttori e architetti con interventi coordinati, manutenzione, riparazioni e ripristini.",
        "en": "We support property managers, condominium administrators, general contractors, builders and architects with co-ordinated work, maintenance, repairs and reinstatement.",
    },
}

PROFESSIONAL_BLOCKS = [
    {
        "order": 1,
        "layout": "card",
        "icon": "fa-solid fa-diagram-project",
        "title": {
            "es": "Coordinación multi-oficio",
            "fr": "Coordination multi-métiers",
            "de": "Koordination mehrerer Gewerke",
            "it": "Coordinamento multi-mestiere",
            "en": "Multi-trade co-ordination",
        },
        "text": {
            "es": "Un único interlocutor para organizar intervenciones que requieren varios oficios y facilitar el seguimiento del proyecto.",
            "fr": "Un interlocuteur unique pour organiser les interventions nécessitant plusieurs corps de métier et faciliter le suivi du projet.",
            "de": "Eine zentrale Ansprechperson zur Organisation von Arbeiten mit mehreren Gewerken und für eine einfachere Projektbegleitung.",
            "it": "Un unico referente per organizzare interventi che richiedono più mestieri e semplificare il monitoraggio del progetto.",
            "en": "One point of contact to organise work involving several trades and simplify project follow-up.",
        },
    },
    {
        "order": 2,
        "layout": "card",
        "icon": "fa-solid fa-key",
        "title": {
            "es": "Remise en état entre inquilinos",
            "fr": "Remise en état entre deux locataires",
            "de": "Instandstellung zwischen Mietverhältnissen",
            "it": "Ripristino tra due locazioni",
            "en": "Reinstatement between tenancies",
        },
        "text": {
            "es": "Organización de reparaciones, pintura, plâtrerie, albañilería ligera y limpieza para preparar el inmueble antes de una nueva ocupación.",
            "fr": "Organisation des réparations, travaux de peinture, plâtrerie, petite maçonnerie et nettoyage afin de préparer le bien avant une nouvelle occupation.",
            "de": "Organisation von Reparaturen, Maler- und Gipserarbeiten, kleineren Maurerarbeiten und Reinigung zur Vorbereitung der Liegenschaft auf eine neue Nutzung.",
            "it": "Organizzazione di riparazioni, pittura, cartongesso, piccoli lavori murari e pulizia per preparare l’immobile a una nuova occupazione.",
            "en": "Organisation of repairs, painting, plastering, minor masonry and cleaning to prepare the property for new occupancy.",
        },
    },
    {
        "order": 3,
        "layout": "card",
        "icon": "fa-solid fa-screwdriver-wrench",
        "title": {
            "es": "Mantenimiento y reparaciones",
            "fr": "Entretien et réparations",
            "de": "Unterhalt und Reparaturen",
            "it": "Manutenzione e riparazioni",
            "en": "Maintenance and repairs",
        },
        "text": {
            "es": "Intervenciones planificadas para mantener el inmueble, corregir daños y preparar actuaciones de renovación cuando sea necesario.",
            "fr": "Des interventions planifiées pour entretenir le bien, corriger les dégradations et préparer des travaux de rénovation lorsque cela est nécessaire.",
            "de": "Geplante Arbeiten für den Unterhalt der Liegenschaft, zur Behebung von Schäden und zur Vorbereitung von Renovationen bei Bedarf.",
            "it": "Interventi pianificati per mantenere l’immobile, correggere i danni e preparare lavori di ristrutturazione quando necessario.",
            "en": "Planned work to maintain the property, address defects and prepare renovation work where required.",
        },
    },
    {
        "order": 4,
        "layout": "cta",
        "icon": "fa-solid fa-envelope-open-text",
        "title": {
            "es": "¿Necesita un interlocutor para sus intervenciones?",
            "fr": "Besoin d’un interlocuteur pour vos interventions ?",
            "de": "Benötigen Sie eine Ansprechperson für Ihre Arbeiten?",
            "it": "Avete bisogno di un referente per i vostri interventi?",
            "en": "Need one point of contact for your works?",
        },
        "text": {
            "es": "Preséntenos sus necesidades de mantenimiento, remise en état o renovación. Revisaremos el alcance para organizar una intervención adecuada.",
            "fr": "Présentez-nous vos besoins d’entretien, de remise en état ou de rénovation. Nous examinerons l’étendue des travaux afin d’organiser une intervention adaptée.",
            "de": "Schildern Sie uns Ihren Bedarf an Unterhalt, Instandstellung oder Renovation. Wir prüfen den Umfang und organisieren eine passende Ausführung.",
            "it": "Presentateci le vostre esigenze di manutenzione, ripristino o ristrutturazione. Valuteremo l’ambito per organizzare un intervento adeguato.",
            "en": "Tell us about your maintenance, reinstatement or renovation requirements. We will review the scope and organise an appropriate response.",
        },
    },
]


# ======================================================================
# PHASE 3 · PROJECTS / RÉALISATIONS
# ======================================================================

PROJECT_TYPES = [
    {"order": 1, "name": {"es": "Renovación completa", "fr": "Rénovation complète", "de": "Komplette Renovation", "it": "Ristrutturazione completa", "en": "Complete renovation"}},
    {"order": 2, "name": {"es": "Renovación interior", "fr": "Rénovation intérieure", "de": "Innenrenovation", "it": "Ristrutturazione interna", "en": "Interior renovation"}},
    {"order": 3, "name": {"es": "Renovación exterior", "fr": "Rénovation extérieure", "de": "Aussenrenovation", "it": "Ristrutturazione esterna", "en": "Exterior renovation"}},
    {"order": 4, "name": {"es": "Aislamiento térmico", "fr": "Isolation thermique", "de": "Wärmedämmung", "it": "Isolamento termico", "en": "Thermal insulation"}},
    {"order": 5, "name": {"es": "Remise en état", "fr": "Remise en état", "de": "Instandstellung", "it": "Ripristino", "en": "Reinstatement"}},
    {"order": 6, "name": {"es": "Mantenimiento inmobiliario", "fr": "Entretien immobilier", "de": "Liegenschaftsunterhalt", "it": "Manutenzione immobiliare", "en": "Property maintenance"}},
]

BUILDING_TYPES = [
    {"order": 1, "name": {"es": "Apartamento", "fr": "Appartement", "de": "Wohnung", "it": "Appartamento", "en": "Flat"}},
    {"order": 2, "name": {"es": "Casa unifamiliar", "fr": "Maison individuelle", "de": "Einfamilienhaus", "it": "Casa unifamiliare", "en": "Detached house"}},
    {"order": 3, "name": {"es": "Edificio residencial", "fr": "Immeuble résidentiel", "de": "Wohngebäude", "it": "Edificio residenziale", "en": "Residential building"}},
    {"order": 4, "name": {"es": "PPE", "fr": "PPE", "de": "Stockwerkeigentum", "it": "PPP", "en": "Condominium property"}},
    {"order": 5, "name": {"es": "Local comercial", "fr": "Local commercial", "de": "Gewerbefläche", "it": "Locale commerciale", "en": "Commercial premises"}},
    {"order": 6, "name": {"es": "Oficina", "fr": "Bureau", "de": "Büro", "it": "Ufficio", "en": "Office"}},
]

DEMO_PROJECTS = [
    {
        "key": "demo-lausanne-appartement",
        "project_type": "Rénovation intérieure",
        "building_type": "Appartement",
        "location": "Lausanne, VD",
        "featured": True,
        "services_fr": ["Rénovation intérieure complète", "Peinture intérieure", "Cloisons en plaques de plâtre", "Nettoyage de fin de chantier"],
        "title": {
            "es": "Renovación interior de un apartamento en Lausanne",
            "fr": "Rénovation intérieure d’un appartement à Lausanne",
            "de": "Innenrenovation einer Wohnung in Lausanne",
            "it": "Ristrutturazione interna di un appartamento a Losanna",
            "en": "Interior renovation of a flat in Lausanne",
        },
        "summary": {
            "es": "Ejemplo de una renovación interior coordinada con trabajos de plâtrerie, pintura y limpieza final antes de la entrega.",
            "fr": "Exemple de rénovation intérieure coordonnée avec travaux de plâtrerie, peinture et nettoyage final avant remise.",
            "de": "Beispiel einer koordinierten Innenrenovation mit Gipserarbeiten, Malerarbeiten und abschliessender Reinigung vor der Übergabe.",
            "it": "Esempio di ristrutturazione interna coordinata con lavori in cartongesso, pittura e pulizia finale prima della consegna.",
            "en": "Example of a co-ordinated interior renovation including plastering, painting and final cleaning before handover.",
        },
        "content": {
            "es": "Este proyecto demostrativo presenta cómo puede organizarse la renovación de un apartamento cuando intervienen varios oficios. La planificación contempla preparación de superficies, ajustes interiores, pintura y limpieza final, manteniendo una coordinación clara entre las distintas etapas.",
            "fr": "Ce projet de démonstration illustre l’organisation possible d’une rénovation d’appartement lorsque plusieurs corps de métier interviennent. La planification comprend la préparation des supports, les adaptations intérieures, la peinture et le nettoyage final, avec une coordination claire entre les différentes étapes.",
            "de": "Dieses Demonstrationsprojekt zeigt, wie eine Wohnungsrenovation mit mehreren Gewerken organisiert werden kann. Die Planung umfasst Untergrundvorbereitung, Innenanpassungen, Malerarbeiten und Schlussreinigung mit klarer Koordination der einzelnen Etappen.",
            "it": "Questo progetto dimostrativo illustra come può essere organizzata la ristrutturazione di un appartamento con il coinvolgimento di più mestieri. La pianificazione comprende preparazione dei supporti, adattamenti interni, pittura e pulizia finale, con un coordinamento chiaro tra le varie fasi.",
            "en": "This demonstration project shows how a flat renovation involving several trades can be organised. The plan includes surface preparation, internal alterations, painting and final cleaning, with clear co-ordination between each stage.",
        },
        "interventions": [
            {"es": "Preparación y protección de las zonas de trabajo", "fr": "Préparation et protection des zones de travail", "de": "Vorbereitung und Schutz der Arbeitsbereiche", "it": "Preparazione e protezione delle aree di lavoro", "en": "Preparation and protection of work areas"},
            {"es": "Ajustes de plâtrerie y tabiques", "fr": "Adaptations de plâtrerie et cloisons", "de": "Gipserarbeiten und Anpassung von Trennwänden", "it": "Adattamenti in cartongesso e divisori", "en": "Plastering and partition alterations"},
            {"es": "Pintura interior y acabados", "fr": "Peinture intérieure et finitions", "de": "Innenanstriche und Finisharbeiten", "it": "Pittura interna e finiture", "en": "Interior painting and finishes"},
            {"es": "Limpieza final antes de la entrega", "fr": "Nettoyage final avant remise", "de": "Schlussreinigung vor der Übergabe", "it": "Pulizia finale prima della consegna", "en": "Final cleaning before handover"},
        ],
    },
    {
        "key": "demo-renens-remise-etat",
        "project_type": "Remise en état",
        "building_type": "Appartement",
        "location": "Renens, VD",
        "featured": True,
        "services_fr": ["Remise en état entre deux locataires", "Réparations courantes", "Peinture intérieure", "Nettoyage avant remise des clés"],
        "title": {
            "es": "Remise en état entre inquilinos en Renens",
            "fr": "Remise en état entre deux locataires à Renens",
            "de": "Instandstellung zwischen zwei Mietverhältnissen in Renens",
            "it": "Ripristino tra due locazioni a Renens",
            "en": "Reinstatement between tenancies in Renens",
        },
        "summary": {
            "es": "Ejemplo de remise en état con reparaciones, pintura y limpieza coordinadas para preparar una vivienda antes de una nueva ocupación.",
            "fr": "Exemple de remise en état avec réparations, peinture et nettoyage coordonnés afin de préparer un logement avant une nouvelle occupation.",
            "de": "Beispiel einer Instandstellung mit koordinierten Reparaturen, Malerarbeiten und Reinigung zur Vorbereitung einer Wohnung auf eine neue Nutzung.",
            "it": "Esempio di ripristino con riparazioni, pittura e pulizia coordinate per preparare un’abitazione a una nuova occupazione.",
            "en": "Example of reinstatement with co-ordinated repairs, painting and cleaning to prepare a home for new occupancy.",
        },
        "content": {
            "es": "Este escenario demostrativo está pensado para régies y propietarios que necesitan intervenir en un plazo controlado entre dos ocupaciones. Agrupa pequeñas reparaciones, preparación de superficies, pintura y limpieza final bajo una misma coordinación.",
            "fr": "Ce scénario de démonstration s’adresse aux régies et propriétaires qui doivent intervenir dans un délai maîtrisé entre deux occupations. Il regroupe petites réparations, préparation des supports, peinture et nettoyage final sous une même coordination.",
            "de": "Dieses Demonstrationsszenario richtet sich an Liegenschaftsverwaltungen und Eigentümerschaften, die zwischen zwei Nutzungen innerhalb eines klaren Zeitrahmens Arbeiten organisieren müssen. Kleinere Reparaturen, Untergrundvorbereitung, Malerarbeiten und Schlussreinigung werden koordiniert zusammengeführt.",
            "it": "Questo scenario dimostrativo è pensato per amministrazioni immobiliari e proprietari che devono intervenire in tempi controllati tra due occupazioni. Riunisce piccole riparazioni, preparazione dei supporti, pittura e pulizia finale sotto un unico coordinamento.",
            "en": "This demonstration scenario is intended for property managers and owners who need work completed within a controlled period between occupancies. It brings together minor repairs, surface preparation, painting and final cleaning under one co-ordinated programme.",
        },
        "interventions": [
            {"es": "Revisión de daños y reparaciones necesarias", "fr": "Contrôle des dégradations et réparations nécessaires", "de": "Kontrolle von Schäden und notwendigen Reparaturen", "it": "Controllo dei danni e delle riparazioni necessarie", "en": "Assessment of damage and required repairs"},
            {"es": "Reparaciones corrientes", "fr": "Réparations courantes", "de": "Laufende Reparaturen", "it": "Riparazioni correnti", "en": "Routine repairs"},
            {"es": "Repintado de las zonas previstas", "fr": "Remise en peinture des zones prévues", "de": "Neuanstrich der vorgesehenen Bereiche", "it": "Ritinteggiatura delle aree previste", "en": "Repainting of agreed areas"},
            {"es": "Limpieza y preparación para la entrega", "fr": "Nettoyage et préparation avant remise", "de": "Reinigung und Vorbereitung für die Übergabe", "it": "Pulizia e preparazione alla consegna", "en": "Cleaning and preparation for handover"},
        ],
    },
    {
        "key": "demo-pully-ppe",
        "project_type": "Rénovation intérieure",
        "building_type": "PPE",
        "location": "Pully, VD",
        "featured": True,
        "services_fr": ["Coordination multi-métiers pour régies", "Peinture intérieure", "Réparations et reprises de maçonnerie", "Nettoyage de fin de chantier"],
        "title": {
            "es": "Renovación de espacios comunes de una PPE en Pully",
            "fr": "Rénovation des espaces communs d’une PPE à Pully",
            "de": "Renovation der Gemeinschaftsbereiche eines Stockwerkeigentums in Pully",
            "it": "Ristrutturazione degli spazi comuni di una PPP a Pully",
            "en": "Renovation of condominium common areas in Pully",
        },
        "summary": {
            "es": "Ejemplo de intervención en zonas comunes con coordinación de reparaciones, preparación, pintura y limpieza.",
            "fr": "Exemple d’intervention dans des espaces communs avec coordination des réparations, de la préparation, de la peinture et du nettoyage.",
            "de": "Beispiel für Arbeiten in Gemeinschaftsbereichen mit Koordination von Reparaturen, Vorbereitung, Malerarbeiten und Reinigung.",
            "it": "Esempio di intervento negli spazi comuni con coordinamento di riparazioni, preparazione, pittura e pulizia.",
            "en": "Example of work in common areas with co-ordinated repairs, preparation, painting and cleaning.",
        },
        "content": {
            "es": "Este proyecto demostrativo representa una intervención en zonas comunes donde es importante organizar los trabajos por etapas y mantener los accesos lo más ordenados posible. La coordinación permite agrupar reparaciones y acabados bajo un mismo seguimiento.",
            "fr": "Ce projet de démonstration représente une intervention dans des espaces communs où il est important d’organiser les travaux par étapes et de maintenir les accès aussi ordonnés que possible. La coordination permet de regrouper réparations et finitions sous un même suivi.",
            "de": "Dieses Demonstrationsprojekt zeigt Arbeiten in Gemeinschaftsbereichen, bei denen eine etappenweise Organisation und möglichst geordnete Zugänge wichtig sind. Durch die Koordination können Reparaturen und Finisharbeiten gemeinsam begleitet werden.",
            "it": "Questo progetto dimostrativo rappresenta un intervento negli spazi comuni, dove è importante organizzare i lavori per fasi e mantenere gli accessi il più ordinati possibile. Il coordinamento consente di riunire riparazioni e finiture sotto un unico monitoraggio.",
            "en": "This demonstration project represents work in common areas where phased organisation and keeping access routes as orderly as possible are important. Co-ordination allows repairs and finishing work to be managed together.",
        },
        "interventions": [
            {"es": "Protección de circulaciones y accesos", "fr": "Protection des circulations et des accès", "de": "Schutz von Verkehrswegen und Zugängen", "it": "Protezione dei passaggi e degli accessi", "en": "Protection of circulation routes and access points"},
            {"es": "Reparaciones y preparación de soportes", "fr": "Réparations et préparation des supports", "de": "Reparaturen und Untergrundvorbereitung", "it": "Riparazioni e preparazione dei supporti", "en": "Repairs and surface preparation"},
            {"es": "Pintura de espacios comunes", "fr": "Peinture des espaces communs", "de": "Malerarbeiten in Gemeinschaftsbereichen", "it": "Pittura degli spazi comuni", "en": "Painting of common areas"},
            {"es": "Control final y limpieza", "fr": "Contrôle final et nettoyage", "de": "Schlusskontrolle und Reinigung", "it": "Controllo finale e pulizia", "en": "Final inspection and cleaning"},
        ],
    },
    {
        "key": "demo-morges-isolation",
        "project_type": "Isolation thermique",
        "building_type": "Immeuble résidentiel",
        "location": "Morges, VD",
        "featured": True,
        "services_fr": ["Isolation thermique des façades / ITE", "Travaux de façade", "Peinture de façades", "Nettoyage de fin de chantier"],
        "title": {
            "es": "Aislamiento térmico y renovación de fachada en Morges",
            "fr": "Isolation thermique et rénovation de façade à Morges",
            "de": "Wärmedämmung und Fassadenrenovation in Morges",
            "it": "Isolamento termico e ristrutturazione della facciata a Morges",
            "en": "Thermal insulation and façade renovation in Morges",
        },
        "summary": {
            "es": "Ejemplo de renovación exterior orientada a la envolvente del edificio, combinando aislamiento, reparación y acabado de fachada.",
            "fr": "Exemple de rénovation extérieure centrée sur l’enveloppe du bâtiment, combinant isolation, réparation et finition de façade.",
            "de": "Beispiel einer Aussenrenovation der Gebäudehülle mit Dämmung, Reparatur und Fassadenfinish.",
            "it": "Esempio di ristrutturazione esterna dell’involucro edilizio, con isolamento, riparazione e finitura della facciata.",
            "en": "Example of exterior renovation focused on the building envelope, combining insulation, repairs and façade finishing.",
        },
        "content": {
            "es": "Este ejemplo muestra cómo puede estructurarse una intervención exterior cuando se combinan trabajos de aislamiento y renovación de fachada. La secuencia considera evaluación del soporte, preparación, ejecución del sistema previsto y acabado exterior.",
            "fr": "Cet exemple montre comment structurer une intervention extérieure lorsque des travaux d’isolation et de rénovation de façade sont combinés. La séquence tient compte de l’évaluation du support, de la préparation, de la mise en œuvre du système prévu et de la finition extérieure.",
            "de": "Dieses Beispiel zeigt, wie eine Aussenmassnahme mit Dämm- und Fassadenrenovationsarbeiten aufgebaut werden kann. Der Ablauf berücksichtigt die Beurteilung des Untergrunds, die Vorbereitung, die Ausführung des vorgesehenen Systems und das Fassadenfinish.",
            "it": "Questo esempio mostra come può essere strutturato un intervento esterno quando si combinano isolamento e ristrutturazione della facciata. La sequenza comprende valutazione del supporto, preparazione, esecuzione del sistema previsto e finitura esterna.",
            "en": "This example shows how an exterior project can be structured when insulation and façade renovation are combined. The sequence considers assessment of the substrate, preparation, installation of the planned system and the exterior finish.",
        },
        "interventions": [
            {"es": "Evaluación y preparación de la fachada", "fr": "Évaluation et préparation de la façade", "de": "Beurteilung und Vorbereitung der Fassade", "it": "Valutazione e preparazione della facciata", "en": "Assessment and preparation of the façade"},
            {"es": "Trabajos de aislamiento previstos", "fr": "Travaux d’isolation prévus", "de": "Vorgesehene Dämmarbeiten", "it": "Lavori di isolamento previsti", "en": "Planned insulation work"},
            {"es": "Reparaciones y acabado exterior", "fr": "Réparations et finition extérieure", "de": "Reparaturen und Aussenfinish", "it": "Riparazioni e finitura esterna", "en": "Repairs and exterior finishing"},
            {"es": "Control final y limpieza de obra", "fr": "Contrôle final et nettoyage de chantier", "de": "Schlusskontrolle und Baustellenreinigung", "it": "Controllo finale e pulizia del cantiere", "en": "Final inspection and site cleaning"},
        ],
    },
    {
        "key": "demo-nyon-maison",
        "project_type": "Rénovation complète",
        "building_type": "Maison individuelle",
        "location": "Nyon, VD",
        "featured": True,
        "services_fr": ["Rénovation d’appartements et de maisons", "Travaux de maçonnerie", "Peinture intérieure", "Coordination multi-métiers"],
        "title": {
            "es": "Renovación completa de una vivienda en Nyon",
            "fr": "Rénovation complète d’un logement à Nyon",
            "de": "Komplette Renovation eines Wohnhauses in Nyon",
            "it": "Ristrutturazione completa di un’abitazione a Nyon",
            "en": "Complete renovation of a home in Nyon",
        },
        "summary": {
            "es": "Ejemplo de proyecto global con coordinación de varios oficios y una secuencia de trabajos desde la preparación hasta los acabados.",
            "fr": "Exemple de projet global avec coordination de plusieurs corps de métier et une séquence de travaux allant de la préparation aux finitions.",
            "de": "Beispiel eines Gesamtprojekts mit Koordination mehrerer Gewerke und einem Ablauf von der Vorbereitung bis zu den Finisharbeiten.",
            "it": "Esempio di progetto globale con coordinamento di più mestieri e una sequenza di lavori dalla preparazione alle finiture.",
            "en": "Example of a complete project involving several trades, with work sequenced from preparation through to finishing.",
        },
        "content": {
            "es": "Este proyecto demostrativo representa una renovación global en la que distintas intervenciones deben coordinarse para mantener una secuencia lógica. El objetivo es organizar los trabajos, evitar solapamientos innecesarios y preparar cada fase para la siguiente.",
            "fr": "Ce projet de démonstration représente une rénovation globale dans laquelle plusieurs interventions doivent être coordonnées afin de conserver une séquence logique. L’objectif est d’organiser les travaux, d’éviter les chevauchements inutiles et de préparer chaque étape pour la suivante.",
            "de": "Dieses Demonstrationsprojekt steht für eine Gesamtrenovation, bei der mehrere Arbeiten in einer logischen Reihenfolge koordiniert werden. Ziel ist es, die Abläufe zu organisieren, unnötige Überschneidungen zu vermeiden und jede Etappe für die nächste vorzubereiten.",
            "it": "Questo progetto dimostrativo rappresenta una ristrutturazione globale in cui diversi interventi devono essere coordinati secondo una sequenza logica. L’obiettivo è organizzare i lavori, evitare sovrapposizioni inutili e preparare ogni fase per quella successiva.",
            "en": "This demonstration project represents a complete renovation in which several types of work need to be co-ordinated in a logical sequence. The aim is to organise the work, avoid unnecessary overlap and prepare each stage for the next.",
        },
        "interventions": [
            {"es": "Planificación general de la intervención", "fr": "Planification générale de l’intervention", "de": "Gesamtplanung der Arbeiten", "it": "Pianificazione generale dell’intervento", "en": "Overall planning of the work"},
            {"es": "Trabajos de albañilería y ajustes", "fr": "Travaux de maçonnerie et adaptations", "de": "Maurerarbeiten und Anpassungen", "it": "Lavori murari e adattamenti", "en": "Masonry works and alterations"},
            {"es": "Preparación y acabados interiores", "fr": "Préparation et finitions intérieures", "de": "Vorbereitung und Innenausbau", "it": "Preparazione e finiture interne", "en": "Preparation and interior finishes"},
            {"es": "Control final y preparación para la entrega", "fr": "Contrôle final et préparation avant remise", "de": "Schlusskontrolle und Vorbereitung für die Übergabe", "it": "Controllo finale e preparazione alla consegna", "en": "Final inspection and preparation for handover"},
        ],
    },
]


# ======================================================================
# PHASE 4 · BLOG / ACTUALITÉS & CONSEILS
# ======================================================================

BLOG_CATEGORIES = [
    {"order": 1, "name": {"fr": "Rénovation", "de": "Renovation", "it": "Ristrutturazione", "en": "Renovation"}},
    {"order": 2, "name": {"fr": "Isolation thermique", "de": "Wärmedämmung", "it": "Isolamento termico", "en": "Thermal insulation"}},
    {"order": 3, "name": {"fr": "Conseils pratiques", "de": "Praktische Tipps", "it": "Consigli pratici", "en": "Practical advice"}},
    {"order": 4, "name": {"fr": "Entretien immobilier", "de": "Liegenschaftsunterhalt", "it": "Manutenzione immobiliare", "en": "Property maintenance"}},
    {"order": 5, "name": {"fr": "Régies & PPE", "de": "Liegenschaftsverwaltungen & STWE", "it": "Amministrazioni & PPP", "en": "Property managers & condominiums"}},
]

BLOG_TAGS = [
    {"name": {"fr": "Rénovation", "de": "Renovation", "it": "Ristrutturazione", "en": "Renovation"}},
    {"name": {"fr": "Planification", "de": "Planung", "it": "Pianificazione", "en": "Planning"}},
    {"name": {"fr": "Isolation", "de": "Dämmung", "it": "Isolamento", "en": "Insulation"}},
    {"name": {"fr": "Façade", "de": "Fassade", "it": "Facciata", "en": "Façade"}},
    {"name": {"fr": "Régie immobilière", "de": "Liegenschaftsverwaltung", "it": "Amministrazione immobiliare", "en": "Property management"}},
    {"name": {"fr": "PPE", "de": "Stockwerkeigentum", "it": "PPP", "en": "Condominium"}},
    {"name": {"fr": "Entretien", "de": "Unterhalt", "it": "Manutenzione", "en": "Maintenance"}},
    {"name": {"fr": "Travaux", "de": "Bauarbeiten", "it": "Lavori", "en": "Building work"}},
]

BLOG_POSTS = [
    {
        "category": "Rénovation",
        "tags": ["Rénovation", "Planification", "Travaux"],
        "featured": True,
        "title": {
            "fr": "Bien préparer un projet de rénovation",
            "de": "Ein Renovationsprojekt gut vorbereiten",
            "it": "Come preparare bene un progetto di ristrutturazione",
            "en": "How to prepare a renovation project",
        },
        "excerpt": {
            "fr": "Une préparation claire permet de mieux définir les priorités, les travaux nécessaires et l’organisation du chantier avant de commencer.",
            "de": "Eine klare Vorbereitung hilft, Prioritäten, notwendige Arbeiten und die Organisation der Baustelle vor Beginn besser festzulegen.",
            "it": "Una preparazione chiara aiuta a definire meglio priorità, lavori necessari e organizzazione del cantiere prima di iniziare.",
            "en": "Clear preparation helps define priorities, required work and site organisation before work begins.",
        },
        "content": {
            "fr": "Un projet de rénovation commence bien avant le premier coup de marteau. Il est utile de définir les objectifs, d’identifier les zones concernées, de hiérarchiser les priorités et de préciser le niveau de finition attendu. Une visite technique peut ensuite aider à vérifier l’état des supports et les contraintes existantes. Cette préparation facilite la coordination, limite les imprévus et permet d’établir une planification plus réaliste.",
            "de": "Ein Renovationsprojekt beginnt lange vor dem ersten Arbeitsschritt. Ziele, betroffene Bereiche, Prioritäten und der gewünschte Ausführungsstandard sollten frühzeitig definiert werden. Eine technische Besichtigung kann anschliessend helfen, den Zustand der Untergründe und bestehende Rahmenbedingungen zu beurteilen. Diese Vorbereitung erleichtert die Koordination, reduziert Überraschungen und ermöglicht eine realistischere Planung.",
            "it": "Un progetto di ristrutturazione inizia ben prima del primo intervento. È utile definire gli obiettivi, identificare le aree interessate, stabilire le priorità e chiarire il livello di finitura desiderato. Un sopralluogo tecnico può poi aiutare a verificare lo stato dei supporti e i vincoli esistenti. Questa preparazione facilita il coordinamento, riduce gli imprevisti e consente una pianificazione più realistica.",
            "en": "A renovation project begins well before the first physical work starts. It helps to define the objectives, identify the areas concerned, set priorities and clarify the required standard of finish. A technical visit can then help assess existing surfaces and constraints. This preparation makes co-ordination easier, reduces surprises and supports a more realistic programme.",
        },
        "sections": [
            {
                "title": {
                    "fr": "Définir les priorités",
                    "de": "Prioritäten festlegen",
                    "it": "Definire le priorità",
                    "en": "Define the priorities",
                },
                "text": {
                    "fr": "Commencez par distinguer les travaux indispensables des améliorations souhaitées. Cette hiérarchisation aide à organiser le budget et les étapes.",
                    "de": "Unterscheiden Sie zunächst notwendige Arbeiten von gewünschten Verbesserungen. Diese Priorisierung hilft bei Budget und Ablaufplanung.",
                    "it": "Iniziate distinguendo i lavori indispensabili dai miglioramenti desiderati. Questa priorità aiuta a organizzare budget e fasi.",
                    "en": "Start by separating essential work from desirable improvements. This helps organise the budget and the sequence of work.",
                },
            },
            {
                "title": {
                    "fr": "Vérifier l’existant",
                    "de": "Bestehenden Zustand prüfen",
                    "it": "Verificare lo stato esistente",
                    "en": "Assess the existing condition",
                },
                "text": {
                    "fr": "L’état des murs, plafonds, façades ou autres supports influence directement les solutions techniques et la préparation nécessaire.",
                    "de": "Der Zustand von Wänden, Decken, Fassaden und anderen Untergründen beeinflusst die technischen Lösungen und den Vorbereitungsaufwand.",
                    "it": "Lo stato di pareti, soffitti, facciate e altri supporti influenza direttamente le soluzioni tecniche e la preparazione necessaria.",
                    "en": "The condition of walls, ceilings, façades and other surfaces directly affects the technical solutions and preparation required.",
                },
            },
            {
                "title": {
                    "fr": "Planifier les étapes",
                    "de": "Etappen planen",
                    "it": "Pianificare le fasi",
                    "en": "Plan the stages",
                },
                "text": {
                    "fr": "Lorsque plusieurs corps de métier interviennent, l’ordre des travaux doit être cohérent afin d’éviter des reprises inutiles.",
                    "de": "Wenn mehrere Gewerke beteiligt sind, sollte die Reihenfolge logisch geplant werden, um unnötige Nacharbeiten zu vermeiden.",
                    "it": "Quando intervengono più mestieri, l’ordine dei lavori deve essere coerente per evitare riprese inutili.",
                    "en": "Where several trades are involved, the order of work should be logical to avoid unnecessary rework.",
                },
            },
        ],
    },
    {
        "category": "Isolation thermique",
        "tags": ["Isolation", "Planification", "Travaux"],
        "featured": True,
        "title": {
            "fr": "Isolation thermique : les points à vérifier avant les travaux",
            "de": "Wärmedämmung: Was vor den Arbeiten geprüft werden sollte",
            "it": "Isolamento termico: cosa verificare prima dei lavori",
            "en": "Thermal insulation: what to check before work begins",
        },
        "excerpt": {
            "fr": "Avant d’isoler, il faut comprendre l’état du bâtiment, les zones de déperdition et les contraintes techniques propres à l’enveloppe.",
            "de": "Vor einer Dämmung sollten der Zustand des Gebäudes, mögliche Wärmeverluste und die technischen Rahmenbedingungen der Gebäudehülle geprüft werden.",
            "it": "Prima di isolare è importante comprendere lo stato dell’edificio, le dispersioni e i vincoli tecnici dell’involucro.",
            "en": "Before insulating, it is important to understand the building condition, heat-loss areas and technical constraints affecting the envelope.",
        },
        "content": {
            "fr": "L’isolation thermique peut concerner les façades, les combles, les sous-sols ou les toitures. Le choix dépend du bâtiment, de son état et des objectifs recherchés. Avant les travaux, il est important d’examiner les supports, les raccords, les zones sensibles à l’humidité et la continuité de l’enveloppe. Une bonne préparation permet de choisir une solution cohérente et d’éviter de traiter un seul point sans tenir compte du comportement global du bâtiment.",
            "de": "Wärmedämmung kann Fassaden, Dachräume, Untergeschosse oder Dächer betreffen. Die geeignete Lösung hängt vom Gebäudezustand und den Projektzielen ab. Vor Beginn sollten Untergründe, Anschlüsse, feuchteempfindliche Bereiche und die Kontinuität der Gebäudehülle geprüft werden. Eine gute Vorbereitung hilft, eine stimmige Lösung zu wählen und verhindert, dass nur ein Einzelpunkt betrachtet wird.",
            "it": "L’isolamento termico può riguardare facciate, sottotetti, seminterrati o tetti. La soluzione dipende dall’edificio, dal suo stato e dagli obiettivi. Prima dei lavori è importante esaminare supporti, raccordi, zone sensibili all’umidità e continuità dell’involucro. Una buona preparazione aiuta a scegliere una soluzione coerente e a evitare interventi isolati senza considerare il comportamento complessivo dell’edificio.",
            "en": "Thermal insulation may involve façades, lofts, basements or roofs. The appropriate solution depends on the building, its condition and the project objectives. Before work begins, it is important to examine substrates, junctions, moisture-sensitive areas and the continuity of the building envelope. Good preparation helps select a coherent solution rather than treating one area in isolation.",
        },
        "sections": [
            {
                "title": {
                    "fr": "Observer l’enveloppe du bâtiment",
                    "de": "Gebäudehülle beurteilen",
                    "it": "Valutare l’involucro edilizio",
                    "en": "Assess the building envelope",
                },
                "text": {
                    "fr": "Les façades, toitures, combles et sous-sols doivent être considérés comme des éléments liés entre eux.",
                    "de": "Fassaden, Dächer, Dachräume und Untergeschosse sollten als zusammenhängende Bauteile betrachtet werden.",
                    "it": "Facciate, tetti, sottotetti e seminterrati vanno considerati come elementi collegati tra loro.",
                    "en": "Façades, roofs, lofts and basements should be considered as connected parts of the building envelope.",
                },
            },
            {
                "title": {
                    "fr": "Vérifier les supports",
                    "de": "Untergründe prüfen",
                    "it": "Verificare i supporti",
                    "en": "Check the substrates",
                },
                "text": {
                    "fr": "Un support dégradé, fissuré ou humide peut nécessiter une préparation spécifique avant la pose d’un système d’isolation.",
                    "de": "Geschädigte, gerissene oder feuchte Untergründe können vor der Dämmung besondere Vorarbeiten erfordern.",
                    "it": "Un supporto degradato, fessurato o umido può richiedere una preparazione specifica prima dell’isolamento.",
                    "en": "Damaged, cracked or damp substrates may require specific preparation before an insulation system is installed.",
                },
            },
            {
                "title": {
                    "fr": "Penser à la performance globale",
                    "de": "Gesamtleistung berücksichtigen",
                    "it": "Considerare la prestazione complessiva",
                    "en": "Consider overall performance",
                },
                "text": {
                    "fr": "Une intervention cohérente tient compte des raccords et des continuités pour limiter les points faibles de l’enveloppe.",
                    "de": "Eine stimmige Lösung berücksichtigt Anschlüsse und Übergänge, um Schwachstellen in der Gebäudehülle zu reduzieren.",
                    "it": "Un intervento coerente considera raccordi e continuità per ridurre i punti deboli dell’involucro.",
                    "en": "A coherent approach considers junctions and continuity to reduce weak points in the building envelope.",
                },
            },
        ],
    },
    {
        "category": "Entretien immobilier",
        "tags": ["Façade", "Entretien", "Travaux"],
        "featured": False,
        "title": {
            "fr": "Quand envisager la rénovation d’une façade ?",
            "de": "Wann sollte eine Fassadenrenovation in Betracht gezogen werden?",
            "it": "Quando valutare la ristrutturazione di una facciata?",
            "en": "When should a façade renovation be considered?",
        },
        "excerpt": {
            "fr": "Fissures, décollements, salissures persistantes ou finitions dégradées peuvent indiquer qu’une façade mérite une évaluation.",
            "de": "Risse, Ablösungen, hartnäckige Verschmutzungen oder beschädigte Beschichtungen können darauf hinweisen, dass eine Fassade beurteilt werden sollte.",
            "it": "Fessure, distacchi, sporco persistente o finiture deteriorate possono indicare che una facciata necessita di una valutazione.",
            "en": "Cracks, flaking, persistent staining or deteriorated finishes can indicate that a façade should be assessed.",
        },
        "content": {
            "fr": "La façade protège le bâtiment tout en participant à son aspect général. Avec le temps, les finitions peuvent se dégrader et certains défauts devenir visibles. Une rénovation ne signifie pas toujours une intervention lourde : selon l’état, il peut s’agir de réparations localisées, de reprises d’enduit, de peinture ou d’un projet plus global incluant l’isolation. Une inspection permet de mieux déterminer la nature et l’étendue des travaux.",
            "de": "Die Fassade schützt das Gebäude und prägt gleichzeitig sein Erscheinungsbild. Mit der Zeit können Beschichtungen altern und Schäden sichtbar werden. Eine Renovation bedeutet nicht immer eine umfassende Massnahme: Je nach Zustand können lokale Reparaturen, Verputzarbeiten, ein neuer Anstrich oder ein umfassenderes Projekt mit Dämmung sinnvoll sein. Eine Beurteilung hilft, Art und Umfang der Arbeiten festzulegen.",
            "it": "La facciata protegge l’edificio e contribuisce al suo aspetto generale. Con il tempo, le finiture possono deteriorarsi e alcuni difetti diventare visibili. Una ristrutturazione non implica sempre un intervento importante: a seconda dello stato, possono bastare riparazioni localizzate, riprese d’intonaco, pittura oppure un progetto più ampio che includa l’isolamento. Un’ispezione aiuta a definire meglio natura ed entità dei lavori.",
            "en": "A façade protects the building while also contributing to its overall appearance. Over time, finishes can deteriorate and defects may become visible. Renovation does not always mean major work: depending on the condition, it may involve local repairs, rendering repairs, painting or a wider project including insulation. An inspection helps determine the nature and extent of the work required.",
        },
        "sections": [
            {
                "title": {"fr": "Signes visibles", "de": "Sichtbare Anzeichen", "it": "Segnali visibili", "en": "Visible signs"},
                "text": {
                    "fr": "Fissures, décollements, cloques ou zones très encrassées peuvent justifier une vérification plus approfondie.",
                    "de": "Risse, Ablösungen, Blasen oder stark verschmutzte Bereiche können eine genauere Prüfung erforderlich machen.",
                    "it": "Fessure, distacchi, bolle o zone molto sporche possono giustificare una verifica più approfondita.",
                    "en": "Cracks, flaking, blistering or heavily soiled areas may justify closer inspection.",
                },
            },
            {
                "title": {"fr": "Réparer avant de finir", "de": "Vor dem Finish reparieren", "it": "Riparare prima della finitura", "en": "Repair before finishing"},
                "text": {
                    "fr": "Une peinture ou un nouvel enduit doit être appliqué sur un support correctement préparé pour obtenir un résultat durable.",
                    "de": "Ein neuer Anstrich oder Verputz sollte auf einem korrekt vorbereiteten Untergrund ausgeführt werden, damit das Ergebnis dauerhaft ist.",
                    "it": "Pittura o nuovo intonaco devono essere applicati su un supporto correttamente preparato per ottenere un risultato duraturo.",
                    "en": "Paint or a new render should be applied to a properly prepared substrate to achieve a durable result.",
                },
            },
            {
                "title": {"fr": "Profiter d’une rénovation globale", "de": "Gesamtrenovation mitdenken", "it": "Valutare una ristrutturazione globale", "en": "Consider a wider renovation"},
                "text": {
                    "fr": "Lorsque des travaux importants sont prévus, il peut être pertinent d’étudier en même temps l’isolation et les autres éléments de l’enveloppe.",
                    "de": "Bei grösseren Arbeiten kann es sinnvoll sein, gleichzeitig Dämmung und weitere Elemente der Gebäudehülle zu prüfen.",
                    "it": "Quando sono previsti lavori importanti, può essere utile valutare contemporaneamente l’isolamento e gli altri elementi dell’involucro.",
                    "en": "Where substantial work is planned, it can be useful to consider insulation and other parts of the building envelope at the same time.",
                },
            },
        ],
    },
    {
        "category": "Régies & PPE",
        "tags": ["Régie immobilière", "PPE", "Entretien", "Planification"],
        "featured": True,
        "title": {
            "fr": "Remise en état entre deux locataires : comment bien s’organiser ?",
            "de": "Instandstellung zwischen zwei Mietverhältnissen: Wie organisiert man die Arbeiten?",
            "it": "Ripristino tra due locazioni: come organizzarsi bene?",
            "en": "Reinstatement between tenancies: how to organise the work",
        },
        "excerpt": {
            "fr": "Entre deux occupations, les délais sont souvent courts. Une coordination claire permet de regrouper réparations, peinture et nettoyage.",
            "de": "Zwischen zwei Mietverhältnissen sind die Zeitfenster oft kurz. Eine klare Koordination hilft, Reparaturen, Malerarbeiten und Reinigung zusammenzuführen.",
            "it": "Tra due occupazioni i tempi sono spesso brevi. Un coordinamento chiaro permette di riunire riparazioni, pittura e pulizia.",
            "en": "The period between tenancies is often short. Clear co-ordination helps bring together repairs, painting and cleaning.",
        },
        "content": {
            "fr": "Une remise en état efficace commence par un constat clair des travaux nécessaires. Les réparations doivent être identifiées avant la peinture et les finitions, puis le nettoyage final doit intervenir lorsque les autres travaux sont terminés. Pour une régie ou un propriétaire, disposer d’un interlocuteur capable de coordonner plusieurs interventions simplifie le suivi et réduit les pertes de temps entre les étapes.",
            "de": "Eine effiziente Instandstellung beginnt mit einer klaren Bestandsaufnahme der notwendigen Arbeiten. Reparaturen sollten vor Maler- und Finisharbeiten definiert werden; die Schlussreinigung erfolgt nach Abschluss der übrigen Arbeiten. Für eine Liegenschaftsverwaltung oder Eigentümerschaft vereinfacht eine zentrale Ansprechperson für mehrere Arbeiten die Begleitung und reduziert Zeitverluste zwischen den Etappen.",
            "it": "Un ripristino efficace inizia con una verifica chiara dei lavori necessari. Le riparazioni devono essere individuate prima della pittura e delle finiture, mentre la pulizia finale va eseguita al termine degli altri interventi. Per un’amministrazione o un proprietario, avere un unico referente capace di coordinare più lavorazioni semplifica il monitoraggio e riduce i tempi morti.",
            "en": "Efficient reinstatement starts with a clear assessment of the work required. Repairs should be identified before painting and finishing, with final cleaning carried out once the other work is complete. For a property manager or owner, having one point of contact capable of co-ordinating several types of work simplifies follow-up and reduces downtime between stages.",
        },
        "sections": [
            {
                "title": {"fr": "Faire un état des lieux des travaux", "de": "Arbeitsumfang erfassen", "it": "Definire i lavori necessari", "en": "Assess the work required"},
                "text": {
                    "fr": "Identifier les réparations, les surfaces à reprendre et les zones à nettoyer permet d’établir une séquence cohérente.",
                    "de": "Die Erfassung von Reparaturen, zu bearbeitenden Flächen und Reinigungsbereichen ermöglicht einen logischen Ablauf.",
                    "it": "Individuare riparazioni, superfici da riprendere e aree da pulire permette di definire una sequenza coerente.",
                    "en": "Identifying repairs, surfaces requiring attention and areas to clean helps establish a logical sequence.",
                },
            },
            {
                "title": {"fr": "Coordonner les corps de métier", "de": "Gewerke koordinieren", "it": "Coordinare i mestieri", "en": "Co-ordinate the trades"},
                "text": {
                    "fr": "Une bonne coordination évite que certaines finitions soient réalisées trop tôt ou doivent être reprises après une autre intervention.",
                    "de": "Eine gute Koordination verhindert, dass Finisharbeiten zu früh ausgeführt und nach anderen Arbeiten erneut bearbeitet werden müssen.",
                    "it": "Un buon coordinamento evita che alcune finiture vengano eseguite troppo presto e debbano essere rifatte dopo altri interventi.",
                    "en": "Good co-ordination helps avoid finishing work being completed too early and then needing to be redone after another trade.",
                },
            },
            {
                "title": {"fr": "Terminer par le nettoyage", "de": "Mit der Reinigung abschliessen", "it": "Concludere con la pulizia", "en": "Finish with cleaning"},
                "text": {
                    "fr": "Le nettoyage final prépare le logement pour la remise et permet de vérifier les derniers détails avant la nouvelle occupation.",
                    "de": "Die Schlussreinigung bereitet die Wohnung für die Übergabe vor und ermöglicht eine letzte Kontrolle vor der neuen Nutzung.",
                    "it": "La pulizia finale prepara l’abitazione alla consegna e permette di verificare gli ultimi dettagli prima della nuova occupazione.",
                    "en": "Final cleaning prepares the home for handover and provides an opportunity to check the last details before new occupancy.",
                },
            },
        ],
    },
    {
        "category": "Conseils pratiques",
        "tags": ["Planification", "Travaux", "Rénovation"],
        "featured": False,
        "title": {
            "fr": "Plusieurs corps de métier, un seul interlocuteur : quels avantages ?",
            "de": "Mehrere Gewerke, eine Ansprechperson: Welche Vorteile bietet das?",
            "it": "Più mestieri, un unico referente: quali vantaggi?",
            "en": "Several trades, one point of contact: what are the benefits?",
        },
        "excerpt": {
            "fr": "Lorsque plusieurs interventions se suivent, une coordination centralisée facilite la planification, la communication et le contrôle du chantier.",
            "de": "Wenn mehrere Arbeiten aufeinander folgen, erleichtert eine zentrale Koordination Planung, Kommunikation und Baustellenkontrolle.",
            "it": "Quando si susseguono più interventi, un coordinamento centralizzato facilita pianificazione, comunicazione e controllo del cantiere.",
            "en": "Where several types of work follow one another, central co-ordination simplifies planning, communication and site control.",
        },
        "content": {
            "fr": "Un projet de rénovation peut réunir maçonnerie, plâtrerie, peinture, isolation et nettoyage. Lorsque chaque intervention est organisée séparément, les délais et les interfaces deviennent plus difficiles à suivre. Un interlocuteur unique peut aider à structurer l’ordre des travaux, centraliser les informations et résoudre plus rapidement les ajustements nécessaires. Cette approche est particulièrement utile pour les rénovations complètes et les remises en état gérées dans des délais courts.",
            "de": "Ein Renovationsprojekt kann Maurer-, Gipser-, Maler-, Dämm- und Reinigungsarbeiten umfassen. Werden alle Arbeiten separat organisiert, werden Termine und Schnittstellen schwieriger zu steuern. Eine zentrale Ansprechperson kann helfen, die Reihenfolge zu strukturieren, Informationen zu bündeln und notwendige Anpassungen schneller zu lösen. Dieser Ansatz ist besonders bei Gesamtrenovationen und Instandstellungen mit engem Zeitfenster hilfreich.",
            "it": "Un progetto di ristrutturazione può comprendere muratura, cartongesso, pittura, isolamento e pulizia. Se ogni intervento viene organizzato separatamente, tempi e interfacce diventano più difficili da gestire. Un unico referente può aiutare a strutturare l’ordine dei lavori, centralizzare le informazioni e risolvere più rapidamente gli adeguamenti necessari. Questo approccio è particolarmente utile nelle ristrutturazioni complete e nei ripristini con tempi brevi.",
            "en": "A renovation project may involve masonry, plastering, painting, insulation and cleaning. When each activity is organised separately, timescales and interfaces become harder to manage. One point of contact can help structure the order of work, centralise information and resolve necessary adjustments more quickly. This approach is particularly useful for complete renovations and reinstatement projects with tight timescales.",
        },
        "sections": [
            {
                "title": {"fr": "Une meilleure visibilité", "de": "Bessere Übersicht", "it": "Maggiore visibilità", "en": "Better visibility"},
                "text": {
                    "fr": "Une planification centralisée permet de mieux comprendre ce qui doit être réalisé, dans quel ordre et à quel moment.",
                    "de": "Eine zentrale Planung erleichtert den Überblick darüber, was in welcher Reihenfolge und zu welchem Zeitpunkt ausgeführt werden soll.",
                    "it": "Una pianificazione centralizzata permette di capire meglio cosa deve essere fatto, in quale ordine e in quale momento.",
                    "en": "Central planning makes it easier to understand what needs to be done, in what order and at what point.",
                },
            },
            {
                "title": {"fr": "Moins d’interfaces à gérer", "de": "Weniger Schnittstellen", "it": "Meno interfacce da gestire", "en": "Fewer interfaces to manage"},
                "text": {
                    "fr": "Le client, la régie ou l’administrateur PPE dispose d’un contact principal pour le suivi des différentes interventions.",
                    "de": "Kundschaft, Liegenschaftsverwaltung oder STWE-Verwaltung hat eine zentrale Ansprechperson für die Begleitung der verschiedenen Arbeiten.",
                    "it": "Cliente, amministrazione immobiliare o amministratore PPP dispone di un referente principale per seguire i diversi interventi.",
                    "en": "The client, property manager or condominium administrator has one main contact for following the different activities.",
                },
            },
            {
                "title": {"fr": "Une remise plus simple", "de": "Einfachere Übergabe", "it": "Una consegna più semplice", "en": "A simpler handover"},
                "text": {
                    "fr": "Lorsque les dernières finitions et le nettoyage sont intégrés à la planification, la préparation de la remise devient plus fluide.",
                    "de": "Wenn Finisharbeiten und Schlussreinigung in die Planung integriert sind, lässt sich die Übergabe einfacher vorbereiten.",
                    "it": "Quando finiture e pulizia finale sono integrate nella pianificazione, la preparazione della consegna diventa più fluida.",
                    "en": "When final finishes and cleaning are included in the programme, preparation for handover becomes smoother.",
                },
            },
        ],
    },
]


# ======================================================================
# PHASE 5 · DEMO / SUPPORT CONTENT
# Models that require real company/client data are created only with
# --with-demo. They are clearly marked and can be removed with --reset-demo.
# ======================================================================

DEMO_SOCIAL_LINKS = [
    {"name": "Instagram · DEMO", "url": "https://example.com/vv-instagram-demo", "icon": "fa-brands fa-instagram", "order": 1},
    {"name": "Facebook · DEMO", "url": "https://example.com/vv-facebook-demo", "icon": "fa-brands fa-facebook-f", "order": 2},
    {"name": "LinkedIn · DEMO", "url": "https://example.com/vv-linkedin-demo", "icon": "fa-brands fa-linkedin-in", "order": 3},
]

DEMO_BUSINESS_HOURS = [
    {"order": 1, "day_fr": "Lundi – vendredi · DÉMO", "day_de": "Montag – Freitag · DEMO", "day_it": "Lunedì – venerdì · DEMO", "day_en": "Monday – Friday · DEMO", "hours": "08:00 – 17:30"},
    {"order": 2, "day_fr": "Samedi · DÉMO", "day_de": "Samstag · DEMO", "day_it": "Sabato · DEMO", "day_en": "Saturday · DEMO", "hours": "Sur rendez-vous / Nach Vereinbarung / Su appuntamento / By appointment"},
]

DEMO_TEAM = [
    {
        "name": "Équipe V&V · DÉMONSTRATION",
        "position": {
            "fr": "Coordination des travaux",
            "de": "Koordination der Arbeiten",
            "it": "Coordinamento dei lavori",
            "en": "Works co-ordination",
        },
        "biography": {
            "fr": "Profil de démonstration utilisé uniquement pour vérifier l’affichage de la section Équipe. Remplacer par les informations réelles avant publication.",
            "de": "Demoprofil zur Prüfung der Teamdarstellung. Vor der Veröffentlichung durch reale Angaben ersetzen.",
            "it": "Profilo dimostrativo utilizzato solo per verificare la sezione Team. Sostituire con dati reali prima della pubblicazione.",
            "en": "Demonstration profile used only to check the Team section. Replace with real information before publication.",
        },
        "order": 1,
    },
]

DEMO_INSURANCES = [
    {
        "name": {
            "es": "Seguro de responsabilidad civil · DEMO",
            "fr": "Assurance responsabilité civile · DÉMONSTRATION",
            "de": "Betriebshaftpflichtversicherung · DEMO",
            "it": "Assicurazione responsabilità civile · DEMO",
            "en": "Public liability insurance · DEMO",
        },
        "description": {
            "es": "Registro de demostración. Sustituir por la póliza y documentación oficial de la empresa antes de publicar.",
            "fr": "Enregistrement de démonstration. À remplacer par la police et les documents officiels de l’entreprise avant publication.",
            "de": "Demoeintrag. Vor der Veröffentlichung durch die offizielle Police und Unternehmensunterlagen ersetzen.",
            "it": "Voce dimostrativa. Sostituire con la polizza e i documenti ufficiali dell’azienda prima della pubblicazione.",
            "en": "Demonstration record. Replace with the company’s official policy and documents before publication.",
        },
        "order": 1,
    },
]

DEMO_CERTIFICATIONS = [
    {
        "name": "DÉMONSTRATION · Document professionnel à confirmer",
        "issuer": "À remplacer par l’émetteur officiel",
        "order": 1,
    },
]

DEMO_TESTIMONIALS = [
    {
        "name": "Client démonstration",
        "company": "DÉMONSTRATION",
        "rating": 5,
        "order": 1,
        "text": {
            "es": "Testimonio de demostración para validar el diseño. Debe reemplazarse por una reseña real antes de publicar.",
            "fr": "Témoignage de démonstration destiné à valider la mise en page. À remplacer par un avis réel avant publication.",
            "de": "Demotestimonial zur Prüfung des Layouts. Vor der Veröffentlichung durch eine echte Bewertung ersetzen.",
            "it": "Testimonianza dimostrativa per verificare il layout. Sostituire con una recensione reale prima della pubblicazione.",
            "en": "Demonstration testimonial used to check the layout. Replace with a genuine review before publication.",
        },
    },
    {
        "name": "Régie démonstration",
        "company": "DÉMONSTRATION",
        "rating": 5,
        "order": 2,
        "text": {
            "es": "Ejemplo de reseña profesional para probar el carrusel de testimonios. No representa un cliente real.",
            "fr": "Exemple d’avis professionnel destiné à tester le carrousel de témoignages. Il ne représente pas un client réel.",
            "de": "Beispiel einer professionellen Bewertung zum Testen des Testimonials-Karussells. Sie stellt keine reale Kundschaft dar.",
            "it": "Esempio di recensione professionale per testare il carosello delle testimonianze. Non rappresenta un cliente reale.",
            "en": "Example professional review used to test the testimonial carousel. It does not represent a real client.",
        },
    },
]

DEMO_CONTACT = {
    "name": "Demande de démonstration",
    "company": "DÉMONSTRATION",
    "email": "demo-contact@example.com",
    "phone": "+41 00 000 00 00",
    "project_location": "Lausanne, VD",
    "message": "DEMO · Demande fictive utilisée uniquement pour vérifier le traitement d’une demande de contact dans l’administration.",
    "language": "fr",
    "internal_notes": "DÉMONSTRATION · Peut être supprimée avec python manage.py seed_vv_content --reset-demo",
}
