from pathlib import PurePosixPath

from django.apps import apps
from django.core.management.base import BaseCommand

from core.image_utils import optimize_uploaded_image


IMAGE_FIELDS = {
    # CORE
    "core.AboutContent": (
        "image",
        "video_image",
    ),
    "core.TeamMember": (
        "photo",
    ),
    "core.Insurance": (
        "image",
    ),
    "core.Certification": (
        "image",
    ),
    "core.CompanyValue": (
        "image",
    ),
    "core.Testimonial": (
        "photo",
    ),
    "core.InstitutionalPage": (
        "image",
    ),
    "core.HomeContent": (
        "hero_image",
    ),
    "core.ProfessionalPage": (
        "hero_image",
    ),
    "core.ProfessionalBlock": (
        "image",
    ),

    # SERVICES
    "services.ServiceCategory": (
        "image",
    ),
    "services.Service": (
        "main_image",
        "secondary_image",
        "third_image",
    ),

    # PROJECTS
    "projects.Project": (
        "main_image",
    ),
    "projects.ProjectImage": (
        "image",
    ),
    "projects.BeforeAfter": (
        "before_image",
        "after_image",
    ),

    # BLOG
    "blog.Post": (
        "main_image",
    ),
    "blog.PostSection": (
        "image_1",
        "image_2",
    ),
}


SUPPORTED_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
}


class Command(BaseCommand):
    help = (
        "Convierte imagenes existentes PNG/JPG/JPEG a WebP. "
        "Por defecto funciona en modo dry-run."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Guarda los WebP y actualiza las referencias en la base de datos.",
        )

    def handle(self, *args, **options):
        apply_changes = options["apply"]

        total_files = 0
        converted_files = 0
        missing_files = 0

        original_total = 0
        optimized_total = 0

        self.stdout.write("")
        self.stdout.write("=" * 72)

        if apply_changes:
            self.stdout.write(
                self.style.WARNING(
                    "V&V SWISS SERVICES · OPTIMIZACION MEDIA · APPLY"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "V&V SWISS SERVICES · OPTIMIZACION MEDIA · DRY-RUN"
                )
            )

        self.stdout.write("=" * 72)
        self.stdout.write("")

        for model_label, field_names in IMAGE_FIELDS.items():
            app_label, model_name = model_label.split(".", 1)

            model = apps.get_model(
                app_label,
                model_name,
            )

            self.stdout.write(
                f"\n[{model_label}]"
            )

            for instance in model.objects.all().iterator():
                for field_name in field_names:
                    field_file = getattr(
                        instance,
                        field_name,
                        None,
                    )

                    if not field_file:
                        continue

                    old_name = field_file.name

                    if not old_name:
                        continue

                    extension = PurePosixPath(
                        old_name
                    ).suffix.lower()

                    # Los WebP existentes se dejan intactos
                    # en esta primera migracion.
                    if extension not in SUPPORTED_EXTENSIONS:
                        continue

                    storage = field_file.storage

                    if not storage.exists(old_name):
                        missing_files += 1

                        self.stdout.write(
                            self.style.WARNING(
                                f"  FALTA | "
                                f"ID {instance.pk} | "
                                f"{field_name} | "
                                f"{old_name}"
                            )
                        )
                        continue

                    total_files += 1

                    original_size = storage.size(
                        old_name
                    )

                    try:
                        with storage.open(
                            old_name,
                            "rb",
                        ) as source:
                            quality = (
                                88
                                if model_label in {
                                    "core.Insurance",
                                    "core.Certification",
                                }
                                else 82
                            )

                            optimized = optimize_uploaded_image(
                                source,
                                max_dimension=2200,
                                quality=quality,
                            )

                    except Exception as exc:
                        self.stdout.write(
                            self.style.ERROR(
                                f"  ERROR | "
                                f"ID {instance.pk} | "
                                f"{field_name} | "
                                f"{old_name} | "
                                f"{exc}"
                            )
                        )
                        continue

                    optimized_size = optimized.size

                    original_total += original_size
                    optimized_total += optimized_size

                    saving_percent = 0

                    if original_size:
                        saving_percent = (
                            1
                            - (
                                optimized_size
                                / original_size
                            )
                        ) * 100

                    new_name = str(
                        PurePosixPath(
                            old_name
                        ).with_suffix(".webp")
                    )

                    self.stdout.write(
                        f"  OK | "
                        f"ID {instance.pk} | "
                        f"{field_name} | "
                        f"{original_size / 1024 / 1024:.2f} MB"
                        f" -> "
                        f"{optimized_size / 1024 / 1024:.2f} MB"
                        f" | ahorro {saving_percent:.1f}%"
                        f" | {new_name}"
                    )

                    if not apply_changes:
                        continue

                    # Evita sobreescribir accidentalmente un
                    # WebP que ya exista.
                    db_field = model._meta.get_field(
                        field_name
                    )

                    max_length = (
                            db_field.max_length
                            or 100
                    )

                    optimized.seek(0)

                    saved_name = storage.save(
                        new_name,
                        optimized,
                        max_length=max_length,
                    )

                    try:
                        updated = (
                            model.objects
                            .filter(pk=instance.pk)
                            .update(
                                **{
                                    field_name: saved_name,
                                }
                            )
                        )

                        if updated != 1:
                            raise RuntimeError(
                                "No se pudo actualizar "
                                "la referencia en la base de datos."
                            )

                    except Exception:
                        # Si falla la BD, elimina el WebP nuevo.
                        if storage.exists(saved_name):
                            storage.delete(saved_name)

                        raise

                    converted_files += 1

                    # IMPORTANTE:
                    # No eliminamos el PNG/JPG original todavía.
                    # Se conservará hasta verificar toda la web.

        self.stdout.write("")
        self.stdout.write("=" * 72)
        self.stdout.write("RESUMEN")
        self.stdout.write("=" * 72)

        self.stdout.write(
            f"Imagenes analizadas: {total_files}"
        )

        if apply_changes:
            self.stdout.write(
                f"Imagenes convertidas: {converted_files}"
            )

        self.stdout.write(
            f"Archivos faltantes: {missing_files}"
        )

        self.stdout.write(
            f"Peso original: "
            f"{original_total / 1024 / 1024:.2f} MB"
        )

        self.stdout.write(
            f"Peso WebP estimado: "
            f"{optimized_total / 1024 / 1024:.2f} MB"
        )

        if original_total:
            total_saving = (
                1
                - (
                    optimized_total
                    / original_total
                )
            ) * 100

            self.stdout.write(
                f"Ahorro estimado: "
                f"{total_saving:.1f}%"
            )

        self.stdout.write("")

        if apply_changes:
            self.stdout.write(
                self.style.SUCCESS(
                    "Proceso APPLY finalizado. "
                    "Los originales se conservaron."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "DRY-RUN finalizado. "
                    "No se modifico ningun archivo ni la base de datos."
                )
            )