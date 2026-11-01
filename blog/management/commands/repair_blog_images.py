from pathlib import Path

from django.contrib.staticfiles import finders
from django.core.files import File
from django.core.management.base import BaseCommand

from blog.models import BlogPageConfiguration, Post


STATIC_FALLBACK = "antra/assets/img/images/VVS_placeholder_horizontal.webp"


def field_exists(image):
    if not image:
        return False
    try:
        return image.storage.exists(image.name)
    except (AttributeError, OSError, ValueError):
        return False


class Command(BaseCommand):
    help = (
        "Repara referencias de imágenes rotas del Blog, crea la imagen por defecto "
        "desde el placeholder estático y regenera imágenes sociales."
    )

    def handle(self, *args, **options):
        self.stdout.write("\n" + "=" * 68)
        self.stdout.write(" V&V SWISS SERVICES · REPARACIÓN DE IMÁGENES DEL BLOG")
        self.stdout.write("=" * 68 + "\n")

        config = BlogPageConfiguration.objects.order_by("pk").first()
        if config is None:
            config = BlogPageConfiguration.objects.create()
            self.stdout.write(self.style.SUCCESS(f"Configuración creada · ID {config.pk}"))

        config_changed = False

        if config.header_background and not field_exists(config.header_background):
            self.stdout.write(
                self.style.WARNING(
                    f"Referencia rota eliminada · header_background · {config.header_background.name}"
                )
            )
            config.header_background = None
            config_changed = True

        if config.post_default_image and not field_exists(config.post_default_image):
            self.stdout.write(
                self.style.WARNING(
                    f"Referencia rota eliminada · post_default_image · {config.post_default_image.name}"
                )
            )
            config.post_default_image = None
            config_changed = True

        if (
            getattr(config, "post_default_social_image", None)
            and not field_exists(config.post_default_social_image)
        ):
            self.stdout.write(
                self.style.WARNING(
                    "Referencia rota eliminada · post_default_social_image · "
                    f"{config.post_default_social_image.name}"
                )
            )
            config.post_default_social_image = None
            config_changed = True

        if not config.post_default_image:
            static_path = finders.find(STATIC_FALLBACK)
            if static_path:
                static_path = Path(static_path)
                with static_path.open("rb") as source:
                    config.post_default_image.save(
                        "VVS_blog_default.webp",
                        File(source),
                        save=False,
                    )
                config_changed = True
                self.stdout.write(
                    self.style.SUCCESS(
                        "Imagen visual por defecto creada desde VVS_placeholder_horizontal.webp"
                    )
                )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f"No se encontró el fallback estático: {STATIC_FALLBACK}"
                    )
                )

        # Guardar también cuando el social esté vacío para que la señal lo genere.
        if config_changed or not getattr(config, "post_default_social_image", None):
            config.save()
            config.refresh_from_db()

        self.stdout.write(
            f"DEFAULT VISUAL: "
            f"{config.post_default_image.name if config.post_default_image else 'None'}"
        )
        self.stdout.write(
            f"DEFAULT SOCIAL: "
            f"{config.post_default_social_image.name if getattr(config, 'post_default_social_image', None) else 'None'}"
        )

        repaired_main = 0
        repaired_og = 0
        regenerated = 0

        for post in Post.objects.all().iterator():
            changed = False

            if post.main_image and not field_exists(post.main_image):
                self.stdout.write(
                    self.style.WARNING(
                        f"Post {post.pk} · main_image rota: {post.main_image.name}"
                    )
                )
                post.main_image = None
                repaired_main += 1
                changed = True

            if post.og_image and not field_exists(post.og_image):
                self.stdout.write(
                    self.style.WARNING(
                        f"Post {post.pk} · og_image rota: {post.og_image.name}"
                    )
                )
                post.og_image = None
                repaired_og += 1
                changed = True

            # Guardar todos permite generar og_image para los posts con main_image válida.
            post.save()
            regenerated += 1

        self.stdout.write("\n" + "-" * 68)
        self.stdout.write(f"Referencias main_image reparadas: {repaired_main}")
        self.stdout.write(f"Referencias og_image reparadas: {repaired_og}")
        self.stdout.write(f"Posts procesados/regenerados: {regenerated}")
        self.stdout.write("-" * 68)
        self.stdout.write(self.style.SUCCESS("Reparación del Blog finalizada.\n"))
