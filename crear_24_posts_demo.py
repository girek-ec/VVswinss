from datetime import timedelta
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.utils import timezone

from blog.models import BlogCategory, BlogTag, Post


# ============================================================
# AUTHOR
# ============================================================

User = get_user_model()

author = (
    User.objects
    .filter(is_superuser=True)
    .order_by("id")
    .first()
)

if not author:
    author = User.objects.order_by("id").first()

if not author:
    raise Exception("No existe ningún usuario para asignar como autor.")


# ============================================================
# CATEGORIES
# ============================================================

categories_data = [
    {
        "name_fr": "Rénovation",
        "slug_fr": "renovation",
        "name_de": "Renovierung",
        "slug_de": "renovierung",
        "name_it": "Ristrutturazione",
        "slug_it": "ristrutturazione",
        "name_en": "Renovation",
        "slug_en": "renovation",
    },
    {
        "name_fr": "Isolation",
        "slug_fr": "isolation",
        "name_de": "Dämmung",
        "slug_de": "daemmung",
        "name_it": "Isolamento",
        "slug_it": "isolamento",
        "name_en": "Insulation",
        "slug_en": "insulation",
    },
    {
        "name_fr": "Peinture et finitions",
        "slug_fr": "peinture-et-finitions",
        "name_de": "Malerarbeiten-und-Ausbau",
        "slug_de": "malerarbeiten-und-ausbau",
        "name_it": "Pittura-e-finiture",
        "slug_it": "pittura-e-finiture",
        "name_en": "Painting-and-finishes",
        "slug_en": "painting-and-finishes",
    },
    {
        "name_fr": "Conseils",
        "slug_fr": "conseils",
        "name_de": "Tipps",
        "slug_de": "tipps",
        "name_it": "Consigli",
        "slug_it": "consigli",
        "name_en": "Advice",
        "slug_en": "advice",
    },
]

categories = []

for data in categories_data:
    category, _ = BlogCategory.objects.update_or_create(
        slug_fr=data["slug_fr"],
        defaults={
            "name_fr": data["name_fr"],
            "name_de": data["name_de"],
            "slug_de": data["slug_de"],
            "name_it": data["name_it"],
            "slug_it": data["slug_it"],
            "name_en": data["name_en"],
            "slug_en": data["slug_en"],
            "is_active": True,
        },
    )

    categories.append(category)


# ============================================================
# TAGS
# ============================================================

tags_data = [
    {
        "name_fr": "Rénovation",
        "slug_fr": "renovation-blog",
        "name_de": "Renovierung",
        "slug_de": "renovierung-blog",
        "name_it": "Ristrutturazione",
        "slug_it": "ristrutturazione-blog",
        "name_en": "Renovation",
        "slug_en": "renovation-blog",
    },
    {
        "name_fr": "Maison",
        "slug_fr": "maison",
        "name_de": "Haus",
        "slug_de": "haus",
        "name_it": "Casa",
        "slug_it": "casa",
        "name_en": "Home",
        "slug_en": "home",
    },
    {
        "name_fr": "Isolation",
        "slug_fr": "isolation-blog",
        "name_de": "Dämmung",
        "slug_de": "daemmung-blog",
        "name_it": "Isolamento",
        "slug_it": "isolamento-blog",
        "name_en": "Insulation",
        "slug_en": "insulation-blog",
    },
    {
        "name_fr": "Peinture",
        "slug_fr": "peinture",
        "name_de": "Malerarbeiten",
        "slug_de": "malerarbeiten",
        "name_it": "Pittura",
        "slug_it": "pittura",
        "name_en": "Painting",
        "slug_en": "painting",
    },
    {
        "name_fr": "Entretien",
        "slug_fr": "entretien",
        "name_de": "Unterhalt",
        "slug_de": "unterhalt",
        "name_it": "Manutenzione",
        "slug_it": "manutenzione",
        "name_en": "Maintenance",
        "slug_en": "maintenance",
    },
    {
        "name_fr": "Conseils",
        "slug_fr": "conseils-blog",
        "name_de": "Tipps",
        "slug_de": "tipps-blog",
        "name_it": "Consigli",
        "slug_it": "consigli-blog",
        "name_en": "Advice",
        "slug_en": "advice-blog",
    },
]

tags = []

for data in tags_data:
    tag, _ = BlogTag.objects.update_or_create(
        slug_fr=data["slug_fr"],
        defaults={
            "name_fr": data["name_fr"],
            "name_de": data["name_de"],
            "slug_de": data["slug_de"],
            "name_it": data["name_it"],
            "slug_it": data["slug_it"],
            "name_en": data["name_en"],
            "slug_en": data["slug_en"],
            "is_active": True,
        },
    )

    tags.append(tag)


# ============================================================
# STATIC BLOG IMAGES
# ============================================================

static_blog_path = (
    Path(settings.BASE_DIR)
    / "static"
    / "antra"
    / "assets"
    / "img"
    / "blog"
)

image_names = [
    "post-1.jpg",
    "post-2.png",
    "post-3.png",
    "post-4.png",
    "post-5.png",
    "post-6.png",
    "post-7.png",
    "post-8.png",
]


# ============================================================
# DEMO POSTS
# ============================================================

titles_fr = [
    "Comment préparer correctement un projet de rénovation",
    "5 erreurs à éviter avant de commencer des travaux",
    "Comment choisir les bonnes couleurs pour votre intérieur",
    "Pourquoi améliorer l’isolation de votre logement",
    "Rénover une pièce sans perdre sa fonctionnalité",
    "Comment reconnaître des murs qui nécessitent une rénovation",
    "Les étapes essentielles d’une rénovation intérieure",
    "Comment entretenir une façade extérieure",
    "Quels travaux réaliser avant de repeindre un mur",
    "Comment améliorer le confort thermique de votre maison",
    "Rénovation complète ou travaux par étapes : que choisir ?",
    "Comment moderniser un intérieur sans tout remplacer",
    "Pourquoi la préparation des surfaces est essentielle",
    "Comment protéger durablement les murs contre l’humidité",
    "Les avantages d’un interlocuteur unique pour vos travaux",
    "Comment organiser un chantier de rénovation",
    "Peinture intérieure : comment obtenir une finition soignée",
    "Quand faut-il rénover une façade ?",
    "Comment valoriser un bien immobilier grâce à la rénovation",
    "Isolation intérieure ou extérieure : quelles différences ?",
    "Comment préparer un logement avant des travaux de peinture",
    "Les finitions qui font la différence dans une rénovation",
    "Comment planifier efficacement plusieurs corps de métier",
    "Conseils pour conserver votre logement en bon état",
]

titles_de = [
    "Wie man ein Renovierungsprojekt richtig vorbereitet",
    "5 Fehler, die Sie vor Renovierungsarbeiten vermeiden sollten",
    "Wie Sie die richtigen Farben für Ihre Innenräume wählen",
    "Warum Sie die Dämmung Ihrer Wohnung verbessern sollten",
    "Einen Raum renovieren, ohne seine Funktionalität zu verlieren",
    "Wie Sie renovierungsbedürftige Wände erkennen",
    "Die wichtigsten Schritte einer Innenrenovierung",
    "Wie Sie eine Aussenfassade richtig pflegen",
    "Welche Arbeiten vor dem Neuanstrich einer Wand nötig sind",
    "Wie Sie den Wärmekomfort Ihres Hauses verbessern",
    "Komplettrenovierung oder Arbeiten in Etappen?",
    "Wie Sie Innenräume modernisieren, ohne alles zu ersetzen",
    "Warum eine sorgfältige Oberflächenvorbereitung wichtig ist",
    "Wie Sie Wände dauerhaft vor Feuchtigkeit schützen",
    "Die Vorteile eines einzigen Ansprechpartners für Bauarbeiten",
    "Wie Sie eine Renovierungsbaustelle organisieren",
    "Innenanstrich: So erzielen Sie ein sauberes Ergebnis",
    "Wann sollte eine Fassade renoviert werden?",
    "Wie Renovierungsarbeiten den Immobilienwert steigern",
    "Innen- oder Aussendämmung: Was sind die Unterschiede?",
    "Wie Sie eine Wohnung vor Malerarbeiten vorbereiten",
    "Details und Ausführungen, die eine Renovierung aufwerten",
    "Wie mehrere Gewerke effizient koordiniert werden",
    "Tipps für die langfristige Pflege Ihrer Immobilie",
]

titles_it = [
    "Come preparare correttamente un progetto di ristrutturazione",
    "5 errori da evitare prima di iniziare i lavori",
    "Come scegliere i colori giusti per gli interni",
    "Perché migliorare l’isolamento della propria abitazione",
    "Ristrutturare un ambiente senza perdere funzionalità",
    "Come riconoscere pareti che necessitano di interventi",
    "Le fasi essenziali di una ristrutturazione interna",
    "Come mantenere correttamente una facciata esterna",
    "Quali lavori eseguire prima di ridipingere una parete",
    "Come migliorare il comfort termico della casa",
    "Ristrutturazione completa o lavori a tappe?",
    "Come modernizzare un interno senza sostituire tutto",
    "Perché la preparazione delle superfici è fondamentale",
    "Come proteggere le pareti dall’umidità",
    "I vantaggi di un unico interlocutore per i lavori",
    "Come organizzare un cantiere di ristrutturazione",
    "Pittura interna: come ottenere una finitura accurata",
    "Quando è necessario ristrutturare una facciata?",
    "Come valorizzare un immobile attraverso la ristrutturazione",
    "Isolamento interno o esterno: quali differenze?",
    "Come preparare un’abitazione prima della pittura",
    "Le finiture che fanno la differenza in una ristrutturazione",
    "Come coordinare efficacemente diverse attività",
    "Consigli per mantenere l’abitazione in buone condizioni",
]

titles_en = [
    "How to prepare a renovation project properly",
    "5 mistakes to avoid before starting renovation work",
    "How to choose the right colours for your interior",
    "Why improving your home's insulation matters",
    "How to renovate a room without losing functionality",
    "How to recognise walls that need renovation",
    "The essential stages of an interior renovation",
    "How to maintain an exterior façade",
    "What should be done before repainting a wall",
    "How to improve thermal comfort in your home",
    "Complete renovation or work in stages?",
    "How to modernise an interior without replacing everything",
    "Why surface preparation is essential",
    "How to protect walls against damp",
    "The benefits of having one point of contact for your project",
    "How to organise a renovation project",
    "Interior painting: how to achieve a quality finish",
    "When should a façade be renovated?",
    "How renovation can increase property value",
    "Internal or external insulation: what is the difference?",
    "How to prepare a property before painting work",
    "Finishing details that make a difference in renovation",
    "How to coordinate several trades efficiently",
    "Advice for keeping your property in good condition",
]


# ============================================================
# CREATE POSTS
# ============================================================

created_count = 0
updated_count = 0

for index in range(24):

    number = index + 1

    slug_fr = f"article-demo-renovation-{number:02d}"
    slug_de = f"demo-renovierung-{number:02d}"
    slug_it = f"articolo-demo-ristrutturazione-{number:02d}"
    slug_en = f"renovation-demo-article-{number:02d}"

    category = categories[index % len(categories)]

    excerpt_fr = (
        "Découvrez des conseils pratiques pour mieux préparer, organiser "
        "et réaliser vos travaux de rénovation avec des solutions adaptées "
        "aux besoins de votre bâtiment."
    )

    excerpt_de = (
        "Praktische Tipps zur Planung, Organisation und Durchführung "
        "von Renovierungsarbeiten mit passenden Lösungen für Ihre Immobilie."
    )

    excerpt_it = (
        "Consigli pratici per preparare, organizzare e realizzare "
        "i lavori di ristrutturazione con soluzioni adatte all’immobile."
    )

    excerpt_en = (
        "Practical advice to help you plan, organise and carry out renovation "
        "work with solutions suited to the needs of your property."
    )

    content_fr = (
        f"{titles_fr[index]}. "
        "Une bonne préparation permet de mieux maîtriser les différentes étapes "
        "du chantier, d’anticiper les interventions nécessaires et d’obtenir "
        "un résultat cohérent et durable. Chaque bâtiment possède ses propres "
        "caractéristiques : il est donc important d’adapter les travaux à son état, "
        "à son usage et aux objectifs du projet."
    )

    content_de = (
        f"{titles_de[index]}. "
        "Eine sorgfältige Planung hilft dabei, die einzelnen Arbeitsschritte "
        "besser zu koordinieren und ein dauerhaft gutes Ergebnis zu erzielen. "
        "Jede Immobilie hat ihre eigenen Anforderungen, deshalb sollten die "
        "Arbeiten immer an Zustand, Nutzung und Projektziele angepasst werden."
    )

    content_it = (
        f"{titles_it[index]}. "
        "Una buona pianificazione permette di coordinare meglio le diverse fasi "
        "del lavoro e di ottenere un risultato duraturo. Ogni immobile presenta "
        "caratteristiche specifiche, per questo gli interventi devono essere "
        "adattati allo stato dell’edificio e agli obiettivi del progetto."
    )

    content_en = (
        f"{titles_en[index]}. "
        "Careful planning helps coordinate each stage of the work and achieve "
        "a consistent, long-lasting result. Every property has its own "
        "characteristics, so renovation work should be adapted to its condition, "
        "use and the objectives of the project."
    )

    post, created = Post.objects.update_or_create(
        slug_fr=slug_fr,
        defaults={
            "category": category,
            "author": author,

            "title_fr": titles_fr[index],
            "slug_fr": slug_fr,
            "excerpt_fr": excerpt_fr,
            "content_fr": content_fr,

            "title_de": titles_de[index],
            "slug_de": slug_de,
            "excerpt_de": excerpt_de,
            "content_de": content_de,

            "title_it": titles_it[index],
            "slug_it": slug_it,
            "excerpt_it": excerpt_it,
            "content_it": content_it,

            "title_en": titles_en[index],
            "slug_en": slug_en,
            "excerpt_en": excerpt_en,
            "content_en": content_en,

            "published_at": timezone.now() - timedelta(days=index + 1),

            "is_published": True,
            "is_featured": index < 6,
        },
    )

    if created:
        created_count += 1
    else:
        updated_count += 1

    # ========================================================
    # TAGS
    # ========================================================

    post.tags.set(
        [
            tags[index % len(tags)],
            tags[(index + 1) % len(tags)],
        ]
    )

    # ========================================================
    # IMAGE
    # ========================================================

    image_name = image_names[index % len(image_names)]
    image_path = static_blog_path / image_name

    if image_path.exists():

        with image_path.open("rb") as image_file:

            post.main_image.save(
                f"demo-{number:02d}-{image_name}",
                File(image_file),
                save=True,
            )

    print(
        f"{number:02d}",
        "·",
        "CREADO" if created else "ACTUALIZADO",
        "·",
        post.title_fr,
    )


# ============================================================
# RESULT
# ============================================================

print("")
print("============================================================")
print("PROCESO FINALIZADO")
print("============================================================")
print("Nuevos posts:", created_count)
print("Posts actualizados:", updated_count)
print("Total de posts en la base de datos:", Post.objects.count())
print("============================================================")