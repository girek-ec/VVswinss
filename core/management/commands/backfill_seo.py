from django.core.management.base import BaseCommand

from blog.models import Post
from projects.models import Project
from services.models import ServiceCategory


ALL_LANGUAGES = ("es", "fr", "de", "it", "en")
PUBLIC_LANGUAGES = ("fr", "de", "it", "en")


def has_value(value):
    return bool(value and str(value).strip())


def needs_seo_update(
    instance,
    *,
    languages,
    title_source,
    description_sources,
):
    for language in languages:
        source_title = getattr(
            instance,
            f"{title_source}_{language}",
            "",
        )

        seo_title = getattr(
            instance,
            f"seo_title_{language}",
            "",
        )

        if has_value(source_title) and not has_value(seo_title):
            return True

        has_description_source = any(
            has_value(
                getattr(
                    instance,
                    f"{field}_{language}",
                    "",
                )
            )
            for field in description_sources
        )

        meta_description = getattr(
            instance,
            f"meta_description_{language}",
            "",
        )

        if (
            has_description_source
            and not has_value(meta_description)
        ):
            return True

    return False


def needs_category_update(instance):
    if needs_seo_update(
        instance,
        languages=ALL_LANGUAGES,
        title_source="name",
        description_sources=("description",),
    ):
        return True

    if (
        (instance.image or instance.hero_image)
        and not instance.og_image
    ):
        return True

    return False


def needs_post_update(instance):
    if needs_seo_update(
        instance,
        languages=PUBLIC_LANGUAGES,
        title_source="title",
        description_sources=("excerpt", "content"),
    ):
        return True

    if instance.main_image and not instance.og_image:
        return True

    return False


def needs_project_update(instance):
    if needs_seo_update(
        instance,
        languages=ALL_LANGUAGES,
        title_source="title",
        description_sources=("summary", "content"),
    ):
        return True

    if instance.main_image and not instance.og_image:
        return True

    return False


class Command(BaseCommand):
    help = (
        "Completa SEO e imágenes sociales faltantes para "
        "categorías, artículos y proyectos existentes."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Muestra qué registros se actualizarían sin guardarlos.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        configurations = (
            (
                "Categorías de servicios",
                ServiceCategory.objects.all(),
                needs_category_update,
            ),
            (
                "Blog",
                Post.objects.all(),
                needs_post_update,
            ),
            (
                "Proyectos",
                Project.objects.all(),
                needs_project_update,
            ),
        )

        total_scanned = 0
        total_pending = 0
        total_updated = 0

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    "MODO DRY-RUN · No se guardará ningún cambio."
                )
            )

        for label, queryset, checker in configurations:
            scanned = 0
            pending = 0
            updated = 0

            self.stdout.write("")
            self.stdout.write(
                self.style.MIGRATE_HEADING(label)
            )

            for instance in queryset.iterator():
                scanned += 1

                if not checker(instance):
                    continue

                pending += 1

                self.stdout.write(
                    f"  ID {instance.pk} · {instance}"
                )

                if not dry_run:
                    instance.save()
                    updated += 1

            total_scanned += scanned
            total_pending += pending
            total_updated += updated

            self.stdout.write(
                f"  Revisados: {scanned}"
            )
            self.stdout.write(
                f"  Requieren actualización: {pending}"
            )

            if not dry_run:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  Actualizados: {updated}"
                    )
                )

        self.stdout.write("")
        self.stdout.write("=" * 60)
        self.stdout.write(
            f"Total revisados: {total_scanned}"
        )
        self.stdout.write(
            f"Total pendientes: {total_pending}"
        )

        if not dry_run:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Total actualizados: {total_updated}"
                )
            )

        self.stdout.write("=" * 60)