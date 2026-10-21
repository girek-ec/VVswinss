from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from services.models import Service, ServiceBenefit, ServiceCategory, ServiceImage


# ============================================================
# V&V SWISS SERVICES · SERVICIOS SEGÚN EL BRIEF
# Français = idioma público principal
# Deutsch / Italiano / British English = idiomas públicos secundarios
# Español = referencia interna
# ============================================================

COMMON = {
    "fr": {
        "subtitle": "Travaux soignés, organisation claire et solutions adaptées aux bâtiments en Suisse romande.",
        "detail2_title": "Pourquoi choisir V&V Swiss Services ?",
        "detail2_text": "Nous privilégions la qualité d’exécution, la transparence et la propreté du chantier, avec un interlocuteur unique du début à la fin.",
        "detail2_list": ["Devis clair et détaillé", "Délais convenus respectés", "Chantier protégé et propre", "Finitions soignées", "Un interlocuteur unique"],
        "cta_title": "Parlons de votre projet",
        "cta_button": "Demander un devis gratuit",
        "cta_text": "Décrivez-nous votre projet et recevez une première réponse pour organiser la suite des travaux.",
    },
    "de": {
        "subtitle": "Sorgfältige Arbeiten, klare Organisation und passende Lösungen für Gebäude im Kanton Waadt und in der Westschweiz.",
        "detail2_title": "Warum V&V Swiss Services?",
        "detail2_text": "Wir stehen für sorgfältige Ausführung, transparente Kommunikation und saubere Baustellen – mit einem Ansprechpartner von Anfang bis Ende.",
        "detail2_list": ["Klare und detaillierte Offerte", "Vereinbarte Termine werden eingehalten", "Saubere und geschützte Baustelle", "Sorgfältige Ausführung", "Ein zentraler Ansprechpartner"],
        "cta_title": "Sprechen wir über Ihr Projekt",
        "cta_button": "Kostenlose Offerte anfragen",
        "cta_text": "Beschreiben Sie uns Ihr Projekt und erhalten Sie eine erste Rückmeldung zur weiteren Planung.",
    },
    "it": {
        "subtitle": "Lavori accurati, organizzazione chiara e soluzioni adatte agli edifici del Canton Vaud e della Svizzera romanda.",
        "detail2_title": "Perché scegliere V&V Swiss Services?",
        "detail2_text": "Puntiamo su qualità, trasparenza e pulizia del cantiere, con un unico interlocutore dall’inizio alla fine.",
        "detail2_list": ["Preventivo chiaro e dettagliato", "Rispetto dei tempi concordati", "Cantiere protetto e pulito", "Finiture curate", "Un unico interlocutore"],
        "cta_title": "Parliamo del vostro progetto",
        "cta_button": "Richiedi un preventivo gratuito",
        "cta_text": "Descriveteci il vostro progetto per ricevere una prima risposta e organizzare i lavori.",
    },
    "en": {
        "subtitle": "Careful workmanship, clear organisation and practical solutions for properties in the canton of Vaud and French-speaking Switzerland.",
        "detail2_title": "Why choose V&V Swiss Services?",
        "detail2_text": "We focus on quality workmanship, transparent communication and clean worksites, with one point of contact from start to finish.",
        "detail2_list": ["Clear and detailed quotation", "Agreed timescales respected", "Protected and tidy worksite", "Careful finishes", "One dedicated point of contact"],
        "cta_title": "Let’s discuss your project",
        "cta_button": "Request a free quote",
        "cta_text": "Tell us about your project and receive an initial response so we can plan the next steps.",
    },
}

BENEFITS = [
    {
        "icon": "fa-solid fa-file-invoice-dollar",
        "es": ("Presupuesto claro", "Información clara sobre los trabajos previstos antes de iniciar la obra."),
        "fr": ("Devis clair", "Une proposition compréhensible et détaillée avant le démarrage des travaux."),
        "de": ("Klare Offerte", "Eine verständliche und detaillierte Offerte vor Beginn der Arbeiten."),
        "it": ("Preventivo chiaro", "Una proposta comprensibile e dettagliata prima dell’inizio dei lavori."),
        "en": ("Clear quotation", "A clear and detailed proposal before work begins."),
    },
    {
        "icon": "fa-solid fa-clock",
        "es": ("Plazos respetados", "Planificación y ejecución orientadas al cumplimiento de los plazos acordados."),
        "fr": ("Délais respectés", "Une organisation pensée pour respecter les délais convenus."),
        "de": ("Termintreue", "Planung und Ausführung mit Fokus auf die vereinbarten Termine."),
        "it": ("Tempi rispettati", "Organizzazione e svolgimento orientati al rispetto dei tempi concordati."),
        "en": ("Timescales respected", "Planning and delivery focused on meeting the agreed timescales."),
    },
    {
        "icon": "fa-solid fa-sparkles",
        "es": ("Trabajo limpio", "Protección de las zonas de trabajo y atención a los acabados y la limpieza."),
        "fr": ("Travail soigné", "Protection des zones de travail, attention aux finitions et propreté du chantier."),
        "de": ("Saubere Ausführung", "Schutz der Arbeitsbereiche sowie sorgfältige Ausführung und Sauberkeit."),
        "it": ("Lavoro curato", "Protezione delle aree di lavoro, attenzione alle finiture e pulizia del cantiere."),
        "en": ("Tidy workmanship", "Protection of work areas with close attention to finishes and cleanliness."),
    },
]


def S(category, order, icon, es, fr, de, it, en):
    """Compact service definition.
    Each language tuple: (name, slug, short_focus, list_items)
    """
    return {
        "category": category,
        "order": order,
        "icon": icon,
        "es": es,
        "fr": fr,
        "de": de,
        "it": it,
        "en": en,
    }


SERVICES = [
    # --------------------------------------------------------
    # 01 · MAÇONNERIE
    # --------------------------------------------------------
    S("maconnerie", 11, "fa-solid fa-trowel-bricks", "Trabajos de albañilería",
      ("Travaux de maçonnerie", "travaux-maconnerie", "petits et gros travaux de maçonnerie pour rénovations et transformations", ["Petits travaux de maçonnerie", "Travaux de transformation", "Création et modification de murs", "Reprises de maçonnerie", "Travaux intérieurs et extérieurs"]),
      ("Maurerarbeiten", "maurerarbeiten", "kleinere und grössere Maurerarbeiten für Renovierungen und Umbauten", ["Kleinere Maurerarbeiten", "Umbauarbeiten", "Erstellung und Änderung von Mauern", "Ausbesserung von Mauerwerk", "Innen- und Aussenarbeiten"]),
      ("Opere murarie", "opere-murarie", "lavori murari di piccola e grande entità per ristrutturazioni e trasformazioni", ["Piccoli lavori murari", "Lavori di trasformazione", "Realizzazione e modifica di muri", "Ripristini murari", "Lavori interni ed esterni"]),
      ("Masonry works", "masonry-works", "minor and major masonry works for renovation and alteration projects", ["Minor masonry work", "Alteration work", "Construction and alteration of walls", "Masonry repairs", "Interior and exterior work"])),

    S("maconnerie", 12, "fa-solid fa-screwdriver-wrench", "Reparaciones de albañilería",
      ("Réparations de maçonnerie", "reparations-maconnerie", "réparations ciblées et remises en état des éléments maçonnés", ["Réparation de fissures", "Reprises de murs endommagés", "Réparation de surfaces maçonnées", "Petites interventions", "Remise en état"]),
      ("Mauerwerksreparaturen", "mauerwerksreparaturen", "gezielte Reparaturen und Instandsetzung von Mauerwerk", ["Rissreparaturen", "Ausbesserung beschädigter Mauern", "Reparatur gemauerter Flächen", "Kleinere Reparaturen", "Instandsetzung"]),
      ("Riparazioni murarie", "riparazioni-murarie", "riparazioni mirate e ripristino di elementi in muratura", ["Riparazione di crepe", "Ripristino di muri danneggiati", "Riparazione di superfici murarie", "Piccoli interventi", "Ripristino"]),
      ("Masonry repairs", "masonry-repairs", "targeted repairs and making good of masonry elements", ["Crack repairs", "Repairs to damaged walls", "Masonry surface repairs", "Minor remedial works", "General making good"])),

    S("maconnerie", 13, "fa-solid fa-grip-lines-vertical", "Tabiques de albañilería",
      ("Cloisons maçonnées", "cloisons-maconnees", "création et modification de cloisons maçonnées pour redistribuer les espaces", ["Création de cloisons", "Modification de distributions", "Séparation de pièces", "Murs en blocs", "Adaptation d’espaces existants"]),
      ("Gemauerte Trennwände", "gemauerte-trennwaende", "gemauerte Trennwände zur Anpassung und Neuaufteilung von Räumen", ["Neue Trennwände", "Änderung von Raumaufteilungen", "Raumtrennungen", "Mauern aus Mauersteinen", "Anpassung bestehender Räume"]),
      ("Pareti divisorie in muratura", "pareti-divisorie-muratura", "pareti divisorie in muratura per ridistribuire e adattare gli spazi", ["Realizzazione di pareti divisorie", "Modifica degli spazi", "Separazione di ambienti", "Pareti in blocchi", "Adattamento di spazi esistenti"]),
      ("Masonry partitions", "masonry-partitions", "masonry partition walls for adapting and reorganising internal spaces", ["New partition walls", "Alteration of room layouts", "Room separation", "Blockwork walls", "Adaptation of existing spaces"])),

    S("maconnerie", 14, "fa-solid fa-layer-group", "Revoques y revestimientos",
      ("Crépis et enduits", "crepis-enduits", "crépis, enduits et préparation des supports intérieurs et extérieurs", ["Crépis intérieurs", "Crépis extérieurs", "Enduits de finition", "Réparation de supports", "Préparation avant peinture"]),
      ("Verputzarbeiten", "verputzarbeiten", "Innen- und Aussenputz sowie Vorbereitung der Untergründe", ["Innenputz", "Aussenputz", "Feinputz und Oberflächen", "Untergrundreparaturen", "Vorbereitung für Malerarbeiten"]),
      ("Intonaci e rasature", "intonaci-rasature", "intonaci, rasature e preparazione dei supporti interni ed esterni", ["Intonaci interni", "Intonaci esterni", "Rasature di finitura", "Ripristino dei supporti", "Preparazione alla pittura"]),
      ("Rendering and coatings", "rendering-coatings", "interior and exterior rendering, coatings and substrate preparation", ["Interior rendering", "Exterior rendering", "Finishing coats", "Substrate repairs", "Preparation before painting"])),

    S("maconnerie", 15, "fa-solid fa-building", "Renovación de fachadas",
      ("Rénovation de façades", "renovation-facades", "réparation et remise en état des façades avant finition", ["Réparation de façades", "Reprises de crépi", "Traitement des fissures", "Préparation des supports", "Rénovation des surfaces extérieures"]),
      ("Fassadensanierung", "fassadensanierung", "Reparatur und Instandsetzung von Fassaden vor der Endbeschichtung", ["Fassadenreparaturen", "Putzsanierungen", "Rissbehandlung", "Untergrundvorbereitung", "Sanierung von Aussenflächen"]),
      ("Risanamento facciate", "risanamento-facciate", "riparazione e ripristino delle facciate prima della finitura", ["Riparazione facciate", "Ripristino intonaci", "Trattamento delle crepe", "Preparazione dei supporti", "Risanamento delle superfici esterne"]),
      ("Façade renovation", "facade-renovation", "repair and refurbishment of façades before final finishing", ["Façade repairs", "Render repairs", "Crack treatment", "Surface preparation", "Renovation of external surfaces"])),

    # --------------------------------------------------------
    # 02 · ISOLATION THERMIQUE
    # --------------------------------------------------------
    S("isolation-thermique", 21, "fa-solid fa-temperature-half", "Aislamiento térmico exterior ITE",
      ("Isolation thermique extérieure (ITE)", "isolation-thermique-exterieure-ite", "isolation des façades par l’extérieur pour améliorer la performance énergétique", ["Isolation extérieure des façades", "Pose de panneaux isolants", "Fixation mécanique", "Treillis d’armature", "Crépi de finition"]),
      ("Aussenwärmedämmung", "aussenwaermedaemmung", "Aussendämmung von Fassaden zur Verbesserung der Energieeffizienz", ["Aussendämmung von Fassaden", "Montage von Dämmplatten", "Mechanische Befestigung", "Armierungsgewebe", "Deckputz"]),
      ("Isolamento termico a cappotto", "isolamento-termico-cappotto", "isolamento esterno delle facciate per migliorare l’efficienza energetica", ["Isolamento esterno delle facciate", "Posa di pannelli isolanti", "Fissaggio meccanico", "Rete di armatura", "Intonaco di finitura"]),
      ("External wall insulation", "external-wall-insulation", "external façade insulation to improve the energy performance of the building", ["External façade insulation", "Installation of insulation boards", "Mechanical fixings", "Reinforcement mesh", "Finishing render"])),

    S("isolation-thermique", 22, "fa-solid fa-layer-group", "Revoco aislante",
      ("Crépi isolant", "crepi-isolant", "système de crépi isolant pour améliorer la protection thermique des façades", ["Préparation du support", "Application du système isolant", "Couche d’armature", "Crépi de finition", "Traitement des détails de façade"]),
      ("Wärmedämmputz", "waermedaemmputz", "Wärmedämmputz zur Verbesserung des thermischen Schutzes der Fassade", ["Untergrundvorbereitung", "Aufbringen des Dämmsystems", "Armierungsschicht", "Deckputz", "Bearbeitung der Fassadendetails"]),
      ("Intonaco termoisolante", "intonaco-termoisolante", "intonaco termoisolante per migliorare la protezione termica della facciata", ["Preparazione del supporto", "Applicazione del sistema isolante", "Strato di armatura", "Intonaco di finitura", "Trattamento dei dettagli della facciata"]),
      ("Insulating render", "insulating-render", "insulating render system for improved thermal protection of façades", ["Surface preparation", "Application of the insulation system", "Reinforcement layer", "Finishing render", "Treatment of façade details"])),

    S("isolation-thermique", 23, "fa-solid fa-house", "Aislamiento de áticos",
      ("Isolation des combles", "isolation-combles", "isolation des combles pour limiter les pertes de chaleur par la toiture", ["Isolation entre chevrons", "Isolation sous toiture", "Isolation des planchers de combles", "Pare-vapeur", "Traitement des ponts thermiques"]),
      ("Dachbodendämmung", "dachbodendaemmung", "Dämmung von Dachräumen zur Reduzierung von Wärmeverlusten über das Dach", ["Dämmung zwischen Sparren", "Dämmung unter dem Dach", "Dämmung von Dachböden", "Dampfbremse", "Behandlung von Wärmebrücken"]),
      ("Isolamento sottotetti", "isolamento-sottotetti", "isolamento dei sottotetti per ridurre le dispersioni termiche attraverso la copertura", ["Isolamento tra le travi", "Isolamento sotto copertura", "Isolamento del solaio", "Barriera al vapore", "Riduzione dei ponti termici"]),
      ("Loft insulation", "loft-insulation", "loft insulation to reduce heat loss through the roof", ["Insulation between rafters", "Under-roof insulation", "Loft floor insulation", "Vapour control layer", "Reduction of thermal bridging"])),

    S("isolation-thermique", 24, "fa-solid fa-warehouse", "Aislamiento de sótanos",
      ("Isolation des sous-sols", "isolation-sous-sols", "isolation des caves et sous-sols pour réduire les pertes de chaleur", ["Isolation des plafonds de caves", "Isolation des murs", "Traitement des zones froides", "Réduction des pertes thermiques", "Amélioration du confort"]),
      ("Kellerdämmung", "kellerdaemmung", "Dämmung von Kellern zur Reduzierung von Wärmeverlusten", ["Dämmung von Kellerdecken", "Wanddämmung", "Behandlung kalter Bereiche", "Reduzierung von Wärmeverlusten", "Verbesserung des Wohnkomforts"]),
      ("Isolamento cantine", "isolamento-cantine", "isolamento di cantine e seminterrati per ridurre le dispersioni termiche", ["Isolamento dei soffitti delle cantine", "Isolamento delle pareti", "Trattamento delle zone fredde", "Riduzione delle dispersioni termiche", "Miglioramento del comfort"]),
      ("Basement insulation", "basement-insulation", "basement and cellar insulation to reduce heat loss", ["Basement ceiling insulation", "Wall insulation", "Treatment of cold areas", "Reduction of heat loss", "Improved indoor comfort"])),

    S("isolation-thermique", 25, "fa-solid fa-house-chimney", "Aislamiento de techos",
      ("Isolation des toitures", "isolation-toitures", "isolation des toitures pour améliorer le confort et la performance énergétique", ["Isolation de toitures inclinées", "Isolation sous chevrons", "Isolation entre chevrons", "Pare-vapeur", "Amélioration de la performance énergétique"]),
      ("Dachdämmung", "dachdaemmung", "Dachdämmung zur Verbesserung von Wohnkomfort und Energieeffizienz", ["Dämmung von Steildächern", "Untersparrendämmung", "Zwischensparrendämmung", "Dampfbremse", "Verbesserung der Energieeffizienz"]),
      ("Isolamento tetti", "isolamento-tetti", "isolamento delle coperture per migliorare comfort ed efficienza energetica", ["Isolamento di tetti inclinati", "Isolamento sotto le travi", "Isolamento tra le travi", "Barriera al vapore", "Miglioramento dell’efficienza energetica"]),
      ("Roof insulation", "roof-insulation", "roof insulation to improve comfort and energy performance", ["Pitched roof insulation", "Insulation below rafters", "Insulation between rafters", "Vapour control layer", "Improved energy performance"])),

    # --------------------------------------------------------
    # 03 · PLÂTRERIE
    # --------------------------------------------------------
    S("platrerie", 31, "fa-solid fa-border-all", "Tabiques de pladur",
      ("Cloisons en plaques de plâtre", "cloisons-plaques-platre", "cloisons légères en plaques de plâtre pour créer ou redistribuer les espaces", ["Création de cloisons", "Ossatures métalliques", "Pose de plaques de plâtre", "Isolation intégrée", "Joints et finitions"]),
      ("Trockenbauwände", "trockenbauwaende", "leichte Trockenbauwände zur Gestaltung und Neuaufteilung von Räumen", ["Neue Trennwände", "Metallunterkonstruktionen", "Montage von Gipskartonplatten", "Integrierte Dämmung", "Fugen und Oberflächen"]),
      ("Pareti in cartongesso", "pareti-cartongesso", "pareti leggere in cartongesso per creare o ridistribuire gli spazi", ["Realizzazione di pareti divisorie", "Strutture metalliche", "Posa di lastre in cartongesso", "Isolamento integrato", "Giunti e finiture"]),
      ("Plasterboard partitions", "plasterboard-partitions", "lightweight plasterboard partitions for creating and reorganising spaces", ["New partition walls", "Metal framing", "Plasterboard installation", "Integrated insulation", "Jointing and finishing"])),

    S("platrerie", 32, "fa-solid fa-square", "Falsos techos",
      ("Faux plafonds", "faux-plafonds", "faux plafonds en plaques de plâtre pour intégrer techniques et éclairage", ["Faux plafonds en plaques de plâtre", "Plafonds suspendus", "Intégration de spots", "Création de décrochés", "Finitions des joints"]),
      ("Abgehängte Decken", "abgehaengte-decken", "abgehängte Decken für Technik, Beleuchtung und saubere Raumgestaltung", ["Gipskartondecken", "Abgehängte Deckensysteme", "Integration von Einbauspots", "Deckenabstufungen", "Fugenbearbeitung"]),
      ("Controsoffitti", "controsoffitti", "controsoffitti in cartongesso per integrare impianti e illuminazione", ["Controsoffitti in cartongesso", "Sistemi sospesi", "Integrazione di faretti", "Velette e ribassamenti", "Finitura dei giunti"]),
      ("Suspended ceilings", "suspended-ceilings", "suspended plasterboard ceilings for services, lighting and clean interior lines", ["Plasterboard ceilings", "Suspended ceiling systems", "Integration of recessed lighting", "Ceiling drops and features", "Joint finishing"])),

    S("platrerie", 33, "fa-solid fa-layer-group", "Trasdosados interiores",
      ("Doublages intérieurs", "doublages-interieurs", "doublages et habillages intérieurs pour corriger, isoler ou finir les parois", ["Doublage de murs", "Habillage de parois", "Ossatures métalliques", "Intégration d’isolant", "Préparation avant peinture"]),
      ("Innenwandverkleidungen", "innenwandverkleidungen", "Innenwandverkleidungen zum Ausgleichen, Dämmen und Fertigstellen von Wänden", ["Wandverkleidungen", "Vorsatzschalen", "Metallunterkonstruktionen", "Integration von Dämmung", "Vorbereitung für Malerarbeiten"]),
      ("Contropareti interne", "contropareti-interne", "contropareti e rivestimenti per correggere, isolare e rifinire le pareti", ["Rivestimento di pareti", "Contropareti", "Strutture metalliche", "Inserimento di isolante", "Preparazione alla pittura"]),
      ("Dry lining", "dry-lining", "dry lining systems to straighten, insulate and finish internal walls", ["Wall lining systems", "Independent wall linings", "Metal framing", "Integrated insulation", "Preparation before painting"])),

    S("platrerie", 34, "fa-solid fa-fill-drip", "Acabados de pladur",
      ("Finitions de plâtrerie", "finitions-platrerie", "joints, enduits et ponçage pour obtenir des surfaces prêtes à peindre", ["Bandes et joints", "Enduisage", "Ponçage", "Correction des surfaces", "Préparation avant peinture"]),
      ("Gipserarbeiten und Oberflächen", "gipserarbeiten-oberflaechen", "Fugen, Spachtel- und Schleifarbeiten für streichfertige Oberflächen", ["Fugen und Bänder", "Spachtelarbeiten", "Schleifarbeiten", "Ausbesserung von Oberflächen", "Vorbereitung für Malerarbeiten"]),
      ("Finiture in gesso", "finiture-gesso", "giunti, rasature e carteggiatura per superfici pronte alla pittura", ["Nastri e giunti", "Rasatura", "Carteggiatura", "Correzione delle superfici", "Preparazione alla pittura"]),
      ("Plastering finishes", "plastering-finishes", "jointing, skimming and sanding for surfaces ready to paint", ["Taping and jointing", "Skimming", "Sanding", "Surface corrections", "Preparation before painting"])),

    # --------------------------------------------------------
    # 04 · PEINTURE
    # --------------------------------------------------------
    S("peinture", 41, "fa-solid fa-paint-roller", "Pintura interior",
      ("Peinture intérieure", "peinture-interieure", "peinture des murs, plafonds et éléments intérieurs avec préparation soignée", ["Murs", "Plafonds", "Portes et encadrements", "Préparation des supports", "Finitions propres et uniformes"]),
      ("Innenanstriche", "innenanstriche", "Anstrich von Wänden, Decken und Innenelementen mit sorgfältiger Vorbereitung", ["Wände", "Decken", "Türen und Rahmen", "Untergrundvorbereitung", "Saubere und gleichmässige Oberflächen"]),
      ("Pittura interna", "pittura-interna", "pittura di pareti, soffitti ed elementi interni con preparazione accurata", ["Pareti", "Soffitti", "Porte e telai", "Preparazione dei supporti", "Finiture pulite e uniformi"]),
      ("Interior painting", "interior-painting", "painting of walls, ceilings and interior elements with careful preparation", ["Walls", "Ceilings", "Doors and frames", "Surface preparation", "Clean and even finishes"])),

    S("peinture", 42, "fa-solid fa-brush", "Pintura exterior",
      ("Peinture extérieure", "peinture-exterieure", "mise en peinture des surfaces extérieures avec produits adaptés aux intempéries", ["Surfaces extérieures", "Boiseries", "Éléments de façade", "Préparation et protection", "Peintures adaptées à l’extérieur"]),
      ("Aussenanstriche", "aussenanstriche", "Anstrich von Aussenflächen mit für Witterung geeigneten Beschichtungen", ["Aussenflächen", "Holzbauteile", "Fassadenelemente", "Vorbereitung und Schutz", "Geeignete Aussenbeschichtungen"]),
      ("Pittura esterna", "pittura-esterna", "pittura delle superfici esterne con prodotti adatti agli agenti atmosferici", ["Superfici esterne", "Elementi in legno", "Elementi di facciata", "Preparazione e protezione", "Pitture per esterni"]),
      ("Exterior painting", "exterior-painting", "painting of external surfaces using coatings suitable for weather exposure", ["External surfaces", "Exterior timber", "Façade elements", "Preparation and protection", "Exterior-grade coatings"])),

    S("peinture", 43, "fa-solid fa-building", "Pintura de fachadas",
      ("Peinture de façades", "peinture-facades", "préparation et mise en peinture des façades pour une finition uniforme et durable", ["Préparation de façade", "Nettoyage du support", "Réparations locales", "Application de peinture", "Finition homogène"]),
      ("Fassadenanstriche", "fassadenanstriche", "Vorbereitung und Anstrich von Fassaden für ein gleichmässiges und dauerhaftes Ergebnis", ["Fassadenvorbereitung", "Reinigung des Untergrunds", "Lokale Reparaturen", "Beschichtungsarbeiten", "Gleichmässige Oberfläche"]),
      ("Pittura facciate", "pittura-facciate", "preparazione e pittura delle facciate per una finitura uniforme e durevole", ["Preparazione della facciata", "Pulizia del supporto", "Riparazioni locali", "Applicazione della pittura", "Finitura uniforme"]),
      ("Façade painting", "facade-painting", "preparation and painting of façades for a uniform and durable finish", ["Façade preparation", "Surface cleaning", "Localised repairs", "Paint application", "Uniform finish"])),

    S("peinture", 44, "fa-solid fa-palette", "Acabados decorativos",
      ("Finitions décoratives", "finitions-decoratives", "finitions décoratives et choix de teintes pour personnaliser les espaces", ["Murs d’accent", "Effets décoratifs", "Choix de teintes", "Finitions mates ou satinées", "Détails personnalisés"]),
      ("Dekorative Oberflächen", "dekorative-oberflaechen", "dekorative Oberflächen und Farbkonzepte zur individuellen Raumgestaltung", ["Akzentwände", "Dekorative Effekte", "Farbgestaltung", "Matte oder seidenglänzende Oberflächen", "Individuelle Details"]),
      ("Finiture decorative", "finiture-decorative", "finiture decorative e scelta dei colori per personalizzare gli ambienti", ["Pareti d’accento", "Effetti decorativi", "Scelta dei colori", "Finiture opache o satinate", "Dettagli personalizzati"]),
      ("Decorative finishes", "decorative-finishes", "decorative finishes and colour choices to personalise interior spaces", ["Feature walls", "Decorative effects", "Colour selection", "Matt or satin finishes", "Bespoke details"])),

    # --------------------------------------------------------
    # 05 · NETTOYAGE DE FIN DE CHANTIER
    # --------------------------------------------------------
    S("nettoyage-fin-chantier", 51, "fa-solid fa-broom", "Limpieza de fin de obra",
      ("Nettoyage de fin de chantier", "nettoyage-fin-chantier", "nettoyage complet après travaux afin de rendre le bien propre et prêt à l’usage", ["Élimination des poussières", "Nettoyage des sols", "Nettoyage des surfaces", "Retrait des résidus de chantier", "Préparation du bien pour utilisation"]),
      ("Bauendreinigung", "bauendreinigung", "gründliche Reinigung nach Bau- oder Renovierungsarbeiten", ["Entfernung von Baustaub", "Bodenreinigung", "Oberflächenreinigung", "Entfernung von Baurückständen", "Vorbereitung für die Nutzung"]),
      ("Pulizia di fine cantiere", "pulizia-fine-cantiere", "pulizia completa dopo i lavori per lasciare l’immobile pronto all’uso", ["Rimozione della polvere", "Pulizia dei pavimenti", "Pulizia delle superfici", "Rimozione dei residui di cantiere", "Preparazione dell’immobile all’uso"]),
      ("Post-construction cleaning", "post-construction-cleaning", "thorough cleaning after building or renovation work so the property is ready to use", ["Removal of building dust", "Floor cleaning", "Surface cleaning", "Removal of construction residues", "Preparation for occupation"])),

    S("nettoyage-fin-chantier", 52, "fa-solid fa-key", "Limpieza antes de entrega de llaves",
      ("Nettoyage avant remise des clés", "nettoyage-remise-cles", "nettoyage final et préparation du logement avant sa remise au client ou au locataire", ["Nettoyage final", "Contrôle des surfaces", "Nettoyage des pièces", "Nettoyage cuisine et sanitaires", "Préparation pour la remise des clés"]),
      ("Reinigung vor Schlüsselübergabe", "reinigung-schluesseluebergabe", "Endreinigung und Vorbereitung der Wohnung für die Übergabe", ["Endreinigung", "Kontrolle der Oberflächen", "Reinigung der Räume", "Reinigung von Küche und Sanitärbereichen", "Vorbereitung für die Schlüsselübergabe"]),
      ("Pulizia prima della consegna chiavi", "pulizia-consegna-chiavi", "pulizia finale e preparazione dell’alloggio prima della consegna", ["Pulizia finale", "Controllo delle superfici", "Pulizia degli ambienti", "Pulizia di cucina e sanitari", "Preparazione alla consegna delle chiavi"]),
      ("Pre-handover cleaning", "pre-handover-cleaning", "final cleaning and preparation of the property before handover", ["Final cleaning", "Surface checks", "Room cleaning", "Kitchen and bathroom cleaning", "Preparation for key handover"])),

    # --------------------------------------------------------
    # 06 · RÉGIES
    # --------------------------------------------------------
    S("services-regies-immobilieres", 61, "fa-solid fa-building", "Mantenimiento de inmuebles en alquiler",
      ("Entretien d’immeubles locatifs", "entretien-immeubles-locatifs", "entretien courant et petites interventions pour biens locatifs gérés par des régies", ["Petites réparations", "Travaux d’entretien", "Interventions dans les logements", "Remise en état", "Coordination de plusieurs travaux"]),
      ("Unterhalt von Mietliegenschaften", "unterhalt-mietliegenschaften", "Unterhalt und kleinere Arbeiten an Mietobjekten für Immobilienverwaltungen", ["Kleinreparaturen", "Unterhaltsarbeiten", "Arbeiten in Mietwohnungen", "Instandsetzung", "Koordination mehrerer Arbeiten"]),
      ("Manutenzione immobili in locazione", "manutenzione-immobili-locazione", "manutenzione ordinaria e piccoli interventi per immobili gestiti da amministrazioni", ["Piccole riparazioni", "Lavori di manutenzione", "Interventi negli appartamenti", "Ripristino", "Coordinamento di più lavori"]),
      ("Rental property maintenance", "rental-property-maintenance", "routine maintenance and minor works for rental properties managed by property managers", ["Minor repairs", "General maintenance", "Work within rental properties", "Making good", "Coordination of multiple trades"])),

    S("services-regies-immobilieres", 62, "fa-solid fa-house", "Renovación de inmuebles en alquiler",
      ("Rénovation de logements en location", "renovation-logements-location", "rénovation et remise en état de logements locatifs avec plusieurs corps de métier", ["Rénovation intérieure", "Réparations", "Plâtrerie", "Peinture", "Nettoyage final"]),
      ("Renovierung von Mietwohnungen", "renovierung-mietwohnungen", "Renovierung und Instandsetzung von Mietwohnungen mit mehreren Gewerken", ["Innenrenovierung", "Reparaturen", "Trockenbau und Gipserarbeiten", "Malerarbeiten", "Endreinigung"]),
      ("Ristrutturazione immobili in locazione", "ristrutturazione-immobili-locazione", "ristrutturazione e ripristino di immobili in locazione con più lavorazioni", ["Ristrutturazione interna", "Riparazioni", "Cartongesso e gessatura", "Pittura", "Pulizia finale"]),
      ("Rental property refurbishment", "rental-property-refurbishment", "refurbishment and making good of rental properties using multiple trades", ["Interior refurbishment", "Repairs", "Plasterboard and plastering", "Painting", "Final cleaning"])),

    S("services-regies-immobilieres", 63, "fa-solid fa-key", "Renovación entre inquilinos",
      ("Rénovation entre deux locataires", "renovation-entre-locataires", "remise en état rapide d’un logement entre le départ d’un locataire et l’arrivée du suivant", ["État des lieux des travaux nécessaires", "Petites réparations", "Remise en état des murs", "Peinture", "Nettoyage avant nouvel occupant"]),
      ("Renovierung bei Mieterwechsel", "renovierung-mieterwechsel", "schnelle Instandsetzung einer Wohnung zwischen Auszug und Neubezug", ["Beurteilung der notwendigen Arbeiten", "Kleinreparaturen", "Instandsetzung der Wände", "Malerarbeiten", "Reinigung vor dem neuen Bezug"]),
      ("Ristrutturazione tra un inquilino e l’altro", "ristrutturazione-tra-inquilini", "ripristino rapido dell’alloggio tra l’uscita di un inquilino e l’ingresso del successivo", ["Valutazione dei lavori necessari", "Piccole riparazioni", "Ripristino delle pareti", "Pittura", "Pulizia prima del nuovo inquilino"]),
      ("Between-tenancy refurbishment", "between-tenancy-refurbishment", "rapid refurbishment between one tenancy ending and the next beginning", ["Assessment of required works", "Minor repairs", "Making good walls", "Painting", "Cleaning before the new tenancy"])),
]


CATEGORY_LABELS_ES = {
    "maconnerie": "Albañilería",
    "isolation-thermique": "Aislamiento térmico",
    "platrerie": "Pladur",
    "peinture": "Pintura",
    "nettoyage-fin-chantier": "Limpieza de obra",
    "services-regies-immobilieres": "Servicios a gerencias inmobiliarias",
}


def lines(values):
    return "\n".join(values)


def model_field_names(model):
    return {f.name for f in model._meta.get_fields() if getattr(f, "concrete", False)}


def set_if_exists(values, model, **kwargs):
    allowed = model_field_names(model)
    for key, value in kwargs.items():
        if key in allowed:
            values[key] = value


def build_language(service, lang):
    name, slug, focus, items = service[lang]
    common = COMMON[lang]

    if lang == "fr":
        prefix = "Spécialistes en"
        suffix = "Travail soigné et durable"
        summary = f"{name} dans le canton de Vaud et en Suisse romande : {focus}."
        content = (
            f"V&V Swiss Services réalise des travaux de {name.lower()} pour les particuliers, propriétaires, "
            f"régies immobilières et professionnels. Notre intervention couvre {focus}.\n\n"
            "Chaque chantier est préparé selon l’état du support, les contraintes du bâtiment et le résultat attendu. "
            "Nous accordons une attention particulière à la protection des lieux, à la coordination des travaux et à la qualité des finitions."
        )
        detail1_title = "Ce que comprend notre intervention"
        detail1_text = "Selon le projet, nous pouvons prendre en charge notamment les travaux suivants :"
        whatsapp = f"Bonjour V&V Swiss Services, je souhaite demander un devis pour le service « {name} ». Merci."
        seo_title = f"{name} dans le canton de Vaud | V&V Swiss Services"
        meta = f"{name} dans le canton de Vaud et en Suisse romande. {focus.capitalize()}. Demandez un devis à V&V Swiss Services."
    elif lang == "de":
        prefix = "Spezialisten für"
        suffix = "Sorgfältig und dauerhaft"
        summary = f"{name} im Kanton Waadt und in der Westschweiz: {focus}."
        content = (
            f"V&V Swiss Services führt {name} für Privatkunden, Eigentümer, Immobilienverwaltungen und Geschäftskunden aus. "
            f"Unser Leistungsbereich umfasst {focus}.\n\n"
            "Jede Baustelle wird auf den Zustand des Untergrunds, die Gebäudesituation und das gewünschte Ergebnis abgestimmt. "
            "Besonderen Wert legen wir auf Schutz, Koordination und saubere Ausführung."
        )
        detail1_title = "Unsere Leistungen"
        detail1_text = "Je nach Projekt übernehmen wir unter anderem folgende Arbeiten:"
        whatsapp = f"Guten Tag V&V Swiss Services, ich möchte eine Offerte für « {name} » anfragen. Vielen Dank."
        seo_title = f"{name} im Kanton Waadt | V&V Swiss Services"
        meta = f"{name} im Kanton Waadt und in der Westschweiz. {focus.capitalize()}. Kostenlose Offerte bei V&V Swiss Services anfragen."
    elif lang == "it":
        prefix = "Specialisti in"
        suffix = "Lavori curati e durevoli"
        summary = f"{name} nel Canton Vaud e nella Svizzera romanda: {focus}."
        content = (
            f"V&V Swiss Services realizza interventi di {name.lower()} per privati, proprietari, amministrazioni immobiliari e professionisti. "
            f"Il servizio comprende {focus}.\n\n"
            "Ogni cantiere viene organizzato in funzione dello stato dei supporti, delle caratteristiche dell’edificio e del risultato richiesto. "
            "Prestiamo particolare attenzione alla protezione degli ambienti, al coordinamento e alla qualità delle finiture."
        )
        detail1_title = "Cosa comprende il servizio"
        detail1_text = "In base al progetto possiamo occuparci, tra l’altro, dei seguenti lavori:"
        whatsapp = f"Buongiorno V&V Swiss Services, vorrei richiedere un preventivo per « {name} ». Grazie."
        seo_title = f"{name} nel Canton Vaud | V&V Swiss Services"
        meta = f"{name} nel Canton Vaud e nella Svizzera romanda. {focus.capitalize()}. Richiedete un preventivo a V&V Swiss Services."
    else:
        prefix = "Specialists in"
        suffix = "Careful, lasting workmanship"
        summary = f"{name} in the canton of Vaud and French-speaking Switzerland: {focus}."
        content = (
            f"V&V Swiss Services provides {name.lower()} for homeowners, landlords, property managers and professional clients. "
            f"Our work covers {focus}.\n\n"
            "Each job is planned according to the condition of the surfaces, the property constraints and the required result. "
            "We pay particular attention to protecting the premises, coordinating the work and delivering careful finishes."
        )
        detail1_title = "What the service includes"
        detail1_text = "Depending on the project, our work may include:"
        whatsapp = f"Hello V&V Swiss Services, I would like to request a quote for “{name}”. Thank you."
        seo_title = f"{name} in Vaud | V&V Swiss Services"
        meta = f"{name} in the canton of Vaud and French-speaking Switzerland. {focus.capitalize()}. Request a quote from V&V Swiss Services."

    values = {
        f"name_{lang}": name,
        f"hero_title_prefix_{lang}": prefix,
        f"hero_title_suffix_{lang}": suffix,
        f"subtitle_{lang}": common["subtitle"],
        f"slug_{lang}": slug,
        f"summary_{lang}": summary,
        f"content_{lang}": content,
        f"detail_1_title_{lang}": detail1_title,
        f"detail_1_text_{lang}": detail1_text,
        f"detail_1_list_{lang}": lines(items),
        f"detail_2_title_{lang}": common["detail2_title"],
        f"detail_2_text_{lang}": common["detail2_text"],
        f"detail_2_list_{lang}": lines(common["detail2_list"]),
        f"cta_title_{lang}": common["cta_title"],
        f"cta_text_{lang}": common["cta_text"],
        f"cta_button_{lang}": common["cta_button"],
        f"whatsapp_message_{lang}": whatsapp,
        f"seo_title_{lang}": seo_title,
        f"meta_description_{lang}": meta,
    }
    return values


def build_spanish_reference(service):
    return {
        "name_es": service["es"],
        "hero_title_prefix_es": "Servicio de",
        "hero_title_suffix_es": "Trabajo profesional y duradero",
        "subtitle_es": "Contenido interno de referencia. No se publica como idioma del sitio.",
        "summary_es": f"Servicio de {service['es'].lower()} de V&V Swiss Services.",
        "content_es": f"Referencia interna para el servicio de {service['es'].lower()}.",
        "detail_1_title_es": "Trabajos incluidos",
        "detail_1_text_es": "Consultar el contenido público en francés como referencia principal.",
        "detail_1_list_es": "",
        "detail_2_title_es": "Compromiso de servicio",
        "detail_2_text_es": "Presupuesto claro, plazos acordados, obra protegida y acabados cuidados.",
        "detail_2_list_es": "Presupuesto claro\nPlazos acordados\nTrabajo limpio\nAcabados cuidados",
        "cta_title_es": "Solicitar presupuesto",
        "cta_text_es": "Referencia interna.",
        "cta_button_es": "Solicitar presupuesto",
        "whatsapp_message_es": "",
    }


def sync_benefits(service):
    valid_orders = []
    for idx, benefit in enumerate(BENEFITS, start=1):
        valid_orders.append(idx)
        obj, _ = ServiceBenefit.objects.update_or_create(
            service=service,
            order=idx,
            defaults={
                "title_es": benefit["es"][0],
                "description_es": benefit["es"][1],
                "title_fr": benefit["fr"][0],
                "description_fr": benefit["fr"][1],
                "title_de": benefit["de"][0],
                "description_de": benefit["de"][1],
                "title_it": benefit["it"][0],
                "description_it": benefit["it"][1],
                "title_en": benefit["en"][0],
                "description_en": benefit["en"][1],
                "icon": benefit["icon"],
            },
        )
    service.benefits.exclude(order__in=valid_orders).delete()


def save_image_field(instance, field_name, path, overwrite=False):
    field = getattr(instance, field_name, None)
    if field is None or not path.exists():
        return False
    if field and not overwrite:
        return False
    with path.open("rb") as fh:
        getattr(instance, field_name).save(path.name, File(fh), save=False)
    return True


def sync_media(service, images_root, overwrite=False):
    """
    Expected optional structure:

      <images_root>/<service.slug_fr>/
          main.webp
          secondary.webp
          third.webp
          og.webp                 (optional)
          gallery/
              01.webp
              02.webp
              ...

    If a file/folder is missing, it is simply skipped.
    """
    if not images_root:
        return 0

    folder = Path(images_root) / service.slug_fr
    if not folder.exists():
        return 0

    changed = False
    for field_name, filename in (
        ("main_image", "main.webp"),
        ("secondary_image", "secondary.webp"),
        ("third_image", "third.webp"),
    ):
        changed |= save_image_field(service, field_name, folder / filename, overwrite=overwrite)

    # MultilingualSEOModel is external to this file. If og_image exists, use it.
    service_fields = model_field_names(Service)
    if "og_image" in service_fields:
        og_path = folder / "og.webp"
        if og_path.exists():
            changed |= save_image_field(service, "og_image", og_path, overwrite=overwrite)
        elif getattr(service, "main_image", None) and not getattr(service, "og_image", None):
            service.og_image = service.main_image.name
            changed = True

    if changed:
        service.save()

    gallery = folder / "gallery"
    gallery_count = 0
    if gallery.exists():
        files = sorted(
            p for p in gallery.iterdir()
            if p.is_file() and p.suffix.lower() in {".webp", ".jpg", ".jpeg", ".png"}
        )
        if overwrite:
            service.images.all().delete()

        for idx, path in enumerate(files, start=1):
            if not overwrite and service.images.filter(order=idx).exists():
                continue
            image = ServiceImage(
                service=service,
                order=idx,
                alt_es=service.name_es,
                alt_fr=service.name_fr,
                alt_de=service.name_de,
                alt_it=service.name_it,
                alt_en=service.name_en,
            )
            with path.open("rb") as fh:
                image.image.save(path.name, File(fh), save=False)
            image.save()
            gallery_count += 1

    return gallery_count


class Command(BaseCommand):
    help = "Crea o actualiza los servicios de V&V Swiss Services según el brief, con traducciones, SEO, beneficios y multimedia opcional."

    def add_arguments(self, parser):
        parser.add_argument(
            "--images-dir",
            type=str,
            default=None,
            help="Carpeta raíz opcional con imágenes organizadas por slug_fr del servicio.",
        )
        parser.add_argument(
            "--overwrite-images",
            action="store_true",
            help="Reemplaza main/secondary/third/og y recrea la galería si existen archivos locales.",
        )
        parser.add_argument(
            "--deactivate-obsolete",
            action="store_true",
            help="Desactiva servicios existentes que no estén en esta estructura.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("\n" + "=" * 88)
        self.stdout.write(" V&V SWISS SERVICES · SINCRONIZACIÓN COMPLETA DE SERVICIOS")
        self.stdout.write("=" * 88 + "\n")

        # Validate categories first.
        category_slugs = sorted({s["category"] for s in SERVICES})
        categories = {
            c.slug_fr: c
            for c in ServiceCategory.objects.filter(slug_fr__in=category_slugs, is_active=True)
        }
        missing = [slug for slug in category_slugs if slug not in categories]
        if missing:
            raise CommandError(
                "Faltan categorías activas con estos slug_fr: " + ", ".join(missing) +
                ". Ejecuta primero seed_service_categories."
            )

        service_fields = model_field_names(Service)
        created_count = updated_count = gallery_count = 0
        valid_slugs = []

        for spec in SERVICES:
            defaults = {
                "category": categories[spec["category"]],
                "icon": spec["icon"],
                "order": spec["order"],
                "is_featured": spec["order"] % 10 == 1,
                "is_active": True,
                "whatsapp_enabled": True,
            }
            defaults.update(build_spanish_reference(spec))
            for lang in ("fr", "de", "it", "en"):
                defaults.update(build_language(spec, lang))

            # SEO fields come from MultilingualSEOModel. Keep only fields that really exist.
            defaults = {k: v for k, v in defaults.items() if k in service_fields}
            set_if_exists(defaults, Service, is_indexable=True)

            slug_fr = spec["fr"][1]
            valid_slugs.append(slug_fr)

            service, created = Service.objects.update_or_create(
                slug_fr=slug_fr,
                defaults=defaults,
            )
            sync_benefits(service)
            gallery_count += sync_media(
                service,
                options["images_dir"],
                overwrite=options["overwrite_images"],
            )

            if created:
                created_count += 1
                status = self.style.SUCCESS("CREADO")
            else:
                updated_count += 1
                status = self.style.WARNING("ACTUALIZADO")

            self.stdout.write(
                f"[{status}] {service.order:02d} · {service.category.name_fr} → {service.name_fr}"
            )

        disabled_count = 0
        if options["deactivate_obsolete"]:
            disabled_count = Service.objects.exclude(slug_fr__in=valid_slugs).filter(is_active=True).update(is_active=False)

        self.stdout.write("\n" + "-" * 88)
        self.stdout.write(self.style.SUCCESS(
            f"Proceso completado · {created_count} creados · {updated_count} actualizados · "
            f"{disabled_count} antiguos desactivados · {gallery_count} imágenes de galería añadidas."
        ))
        self.stdout.write("-" * 88 + "\n")
