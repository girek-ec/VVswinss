from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.utils import timezone

from blog.models import BlogCategory, Post


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
# CATEGORY · EXTERIORS
# ============================================================

category, _ = BlogCategory.objects.get_or_create(
    slug_fr="exterieurs",
    defaults={
        "name_fr": "Extérieurs",
        "name_de": "Aussenbereiche",
        "slug_de": "aussenbereiche",
        "name_it": "Esterni",
        "slug_it": "esterni",
        "name_en": "Exteriors",
        "slug_en": "exteriors",
        "is_active": True,
    },
)


# ============================================================
# DEMO POSTS
# ============================================================

posts_data = [
    {
        "title_fr": "5 conseils pour réussir la rénovation de votre intérieur",
        "slug_fr": "5-conseils-pour-reussir-la-renovation-de-votre-interieur",
        "excerpt_fr": "Découvrez les points essentiels à considérer avant de commencer vos travaux de rénovation intérieure.",
        "content_fr": "Une rénovation bien préparée permet d’améliorer le confort, la fonctionnalité et la valeur de votre logement. Voici quelques conseils pour organiser votre projet efficacement.",

        "title_de": "5 Tipps für eine erfolgreiche Innenrenovierung",
        "slug_de": "5-tipps-fuer-eine-erfolgreiche-innenrenovierung",
        "excerpt_de": "Entdecken Sie die wichtigsten Punkte, die Sie vor Beginn Ihrer Innenrenovierung berücksichtigen sollten.",
        "content_de": "Eine gut geplante Renovierung verbessert Komfort, Funktionalität und den Wert Ihrer Immobilie.",

        "title_it": "5 consigli per una ristrutturazione interna di successo",
        "slug_it": "5-consigli-per-una-ristrutturazione-interna-di-successo",
        "excerpt_it": "Scoprite gli aspetti essenziali da considerare prima di iniziare i lavori di ristrutturazione interna.",
        "content_it": "Una ristrutturazione ben pianificata permette di migliorare il comfort, la funzionalità e il valore dell'immobile.",

        "title_en": "5 tips for a successful interior renovation",
        "slug_en": "5-tips-for-a-successful-interior-renovation",
        "excerpt_en": "Discover the key points to consider before starting your interior renovation project.",
        "content_en": "A well-planned renovation can improve the comfort, functionality and value of your property.",

        "image": "post-1.jpg",
    },
    {
        "title_fr": "Comment améliorer l’isolation thermique de votre logement ?",
        "slug_fr": "comment-ameliorer-isolation-thermique-logement",
        "excerpt_fr": "Une bonne isolation permet d’améliorer le confort intérieur et de réduire les pertes énergétiques.",
        "content_fr": "Murs, façades, plafonds et autres zones sensibles peuvent être responsables d’importantes pertes de chaleur. Une intervention adaptée améliore durablement les performances du bâtiment.",

        "title_de": "Wie lässt sich die Wärmedämmung einer Wohnung verbessern?",
        "slug_de": "waermedaemmung-einer-wohnung-verbessern",
        "excerpt_de": "Eine gute Wärmedämmung verbessert den Wohnkomfort und reduziert Energieverluste.",
        "content_de": "Wände, Fassaden und Decken können erhebliche Wärmeverluste verursachen. Eine geeignete Dämmung verbessert die Energieeffizienz nachhaltig.",

        "title_it": "Come migliorare l’isolamento termico della propria abitazione?",
        "slug_it": "come-migliorare-isolamento-termico-abitazione",
        "excerpt_it": "Un buon isolamento migliora il comfort interno e contribuisce a ridurre le dispersioni energetiche.",
        "content_it": "Pareti, facciate e soffitti possono causare importanti dispersioni di calore. Un intervento adeguato migliora l'efficienza energetica dell'edificio.",

        "title_en": "How to improve the thermal insulation of your home",
        "slug_en": "how-to-improve-the-thermal-insulation-of-your-home",
        "excerpt_en": "Good insulation improves indoor comfort and helps reduce energy loss.",
        "content_en": "Walls, façades and ceilings can account for significant heat loss. Suitable insulation can improve a building's long-term energy performance.",

        "image": "post-2.png",
    },
    {
        "title_fr": "Quand faut-il rénover les murs et repeindre un logement ?",
        "slug_fr": "quand-renover-murs-repeindre-logement",
        "excerpt_fr": "Fissures, traces d’humidité et peinture dégradée sont quelques signes indiquant qu’une remise en état peut être nécessaire.",
        "content_fr": "L’état des murs influence directement l’apparence et la qualité d’un intérieur. Une préparation correcte des surfaces est essentielle avant toute nouvelle peinture.",

        "title_de": "Wann sollten Wände renoviert und neu gestrichen werden?",
        "slug_de": "wann-waende-renovieren-und-neu-streichen",
        "excerpt_de": "Risse, Feuchtigkeitsspuren und beschädigte Farbe können darauf hinweisen, dass eine Instandsetzung notwendig ist.",
        "content_de": "Der Zustand der Wände beeinflusst das Erscheinungsbild eines Innenraums wesentlich. Eine sorgfältige Vorbereitung ist vor jedem neuen Anstrich entscheidend.",

        "title_it": "Quando è necessario rinnovare le pareti e ritinteggiare?",
        "slug_it": "quando-rinnovare-pareti-e-ritinteggiare",
        "excerpt_it": "Crepe, tracce di umidità e pittura deteriorata possono indicare la necessità di un intervento.",
        "content_it": "Lo stato delle pareti influisce direttamente sull'aspetto degli ambienti. Una corretta preparazione delle superfici è fondamentale prima della tinteggiatura.",

        "title_en": "When should walls be renovated and repainted?",
        "slug_en": "when-should-walls-be-renovated-and-repainted",
        "excerpt_en": "Cracks, damp marks and deteriorated paint are common signs that repair work may be required.",
        "content_en": "The condition of walls directly affects the appearance of an interior. Proper surface preparation is essential before repainting.",

        "image": "post-3.png",
    },
]


# ============================================================
# CREATE / UPDATE POSTS
# ============================================================

static_blog_path = (
    Path(settings.BASE_DIR)
    / "static"
    / "antra"
    / "assets"
    / "img"
    / "blog"
)

for data in posts_data:

    image_name = data.pop("image")

    post, created = Post.objects.update_or_create(
        slug_fr=data["slug_fr"],
        defaults={
            "category": category,
            "author": author,

            "title_fr": data["title_fr"],
            "slug_fr": data["slug_fr"],
            "excerpt_fr": data["excerpt_fr"],
            "content_fr": data["content_fr"],

            "title_de": data["title_de"],
            "slug_de": data["slug_de"],
            "excerpt_de": data["excerpt_de"],
            "content_de": data["content_de"],

            "title_it": data["title_it"],
            "slug_it": data["slug_it"],
            "excerpt_it": data["excerpt_it"],
            "content_it": data["content_it"],

            "title_en": data["title_en"],
            "slug_en": data["slug_en"],
            "excerpt_en": data["excerpt_en"],
            "content_en": data["content_en"],

            "published_at": timezone.now(),
            "is_published": True,
            "is_featured": True,
        },
    )

    image_path = static_blog_path / image_name

    if image_path.exists():
        with image_path.open("rb") as image_file:
            post.main_image.save(
                image_name,
                File(image_file),
                save=True,
            )

    print(
        "CREADO" if created else "ACTUALIZADO",
        "·",
        post.title_fr,
    )


print("")
print("========================================")
print("3 PUBLICACIONES DEMO CREADAS")
print("========================================")