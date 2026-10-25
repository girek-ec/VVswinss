import csv
import shutil
from datetime import datetime
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import FileField


EXCLUDED_PREFIXES = (
    "contact/attachments/",
    "site/",
    "seo/",
    "blog/quotes/",
)


def normalize_name(value):
    return str(value).replace("\\", "/").lstrip("/")


class Command(BaseCommand):
    help = (
        "Detecta archivos de MEDIA_ROOT que ya no estan referenciados "
        "por ningun FileField/ImageField. Por defecto solo audita."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--quarantine",
            action="store_true",
            help="Mueve los archivos huerfanos a una carpeta de cuarentena.",
        )

        parser.add_argument(
            "--quarantine-dir",
            type=str,
            default="",
            help="Ruta opcional de cuarentena.",
        )

        parser.add_argument(
            "--limit",
            type=int,
            default=100,
            help="Cantidad maxima de archivos mostrados en pantalla.",
        )

    def handle(self, *args, **options):
        media_root = Path(settings.MEDIA_ROOT).resolve()

        if not media_root.exists():
            raise CommandError(
                f"MEDIA_ROOT no existe: {media_root}"
            )

        references = set()

        # ============================================================
        # REFERENCIAS ACTUALES EN BASE DE DATOS
        # ============================================================

        for model in apps.get_models():
            file_fields = [
                field
                for field in model._meta.fields
                if isinstance(field, FileField)
            ]

            if not file_fields:
                continue

            for instance in model._default_manager.all().iterator():
                for field in file_fields:
                    value = getattr(
                        instance,
                        field.name,
                        None,
                    )

                    name = getattr(
                        value,
                        "name",
                        "",
                    )

                    if name:
                        references.add(
                            normalize_name(name)
                        )

        # ============================================================
        # ARCHIVOS FISICOS
        # ============================================================

        physical_files = [
            path
            for path in media_root.rglob("*")
            if path.is_file()
        ]

        orphan_files = []
        excluded_files = []
        referenced_files = []

        for path in physical_files:
            relative = normalize_name(
                path.relative_to(media_root)
            )

            if relative.startswith(EXCLUDED_PREFIXES):
                excluded_files.append(path)
                continue

            if relative in references:
                referenced_files.append(path)
                continue

            orphan_files.append(path)

        orphan_files.sort(
            key=lambda path: path.stat().st_size,
            reverse=True,
        )

        orphan_size = sum(
            path.stat().st_size
            for path in orphan_files
        )

        referenced_size = sum(
            path.stat().st_size
            for path in referenced_files
        )

        excluded_size = sum(
            path.stat().st_size
            for path in excluded_files
        )

        # ============================================================
        # RESUMEN
        # ============================================================

        self.stdout.write("")
        self.stdout.write("=" * 72)
        self.stdout.write(
            "V&V SWISS SERVICES · AUDITORIA MEDIA"
        )
        self.stdout.write("=" * 72)

        self.stdout.write(
            f"Referencias encontradas en BD: {len(references)}"
        )

        self.stdout.write(
            f"Archivos fisicos en media: {len(physical_files)}"
        )

        self.stdout.write(
            f"Archivos actualmente referenciados: "
            f"{len(referenced_files)}"
        )

        self.stdout.write(
            f"Archivos protegidos/excluidos: "
            f"{len(excluded_files)}"
        )

        self.stdout.write(
            f"Archivos huerfanos candidatos: "
            f"{len(orphan_files)}"
        )

        self.stdout.write(
            f"Peso referenciado: "
            f"{referenced_size / 1024 / 1024:.2f} MB"
        )

        self.stdout.write(
            f"Peso protegido/excluido: "
            f"{excluded_size / 1024 / 1024:.2f} MB"
        )

        self.stdout.write(
            f"Peso recuperable candidato: "
            f"{orphan_size / 1024 / 1024:.2f} MB"
        )

        # ============================================================
        # LISTADO
        # ============================================================

        self.stdout.write("")
        self.stdout.write(
            "ARCHIVOS HUERFANOS MAS PESADOS"
        )
        self.stdout.write("-" * 72)

        limit = max(
            options["limit"],
            0,
        )

        for path in orphan_files[:limit]:
            relative = normalize_name(
                path.relative_to(media_root)
            )

            size_mb = (
                path.stat().st_size
                / 1024
                / 1024
            )

            self.stdout.write(
                f"{size_mb:8.2f} MB | {relative}"
            )

        if len(orphan_files) > limit:
            self.stdout.write(
                f"... y {len(orphan_files) - limit} "
                f"archivos adicionales."
            )

        # ============================================================
        # SOLO AUDITORIA
        # ============================================================

        if not options["quarantine"]:
            self.stdout.write("")
            self.stdout.write(
                self.style.SUCCESS(
                    "DRY-RUN finalizado. "
                    "No se movio ni elimino ningun archivo."
                )
            )
            return

        # ============================================================
        # CUARENTENA
        # ============================================================

        if options["quarantine_dir"]:
            quarantine_root = Path(
                options["quarantine_dir"]
            ).resolve()
        else:
            stamp = datetime.now().strftime(
                "%Y%m%d-%H%M%S"
            )

            quarantine_root = (
                media_root.parent.parent
                / f"VVswinss_media_quarantine_{stamp}"
            ).resolve()

        try:
            quarantine_root.relative_to(
                media_root
            )

            raise CommandError(
                "La cuarentena no puede estar dentro de MEDIA_ROOT."
            )

        except ValueError:
            pass

        quarantine_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        manifest_path = (
            quarantine_root
            / "manifest.csv"
        )

        moved = 0
        moved_size = 0

        with manifest_path.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as csv_file:
            writer = csv.writer(
                csv_file
            )

            writer.writerow(
                [
                    "relative_path",
                    "size_bytes",
                ]
            )

            for source in orphan_files:
                relative_path = source.relative_to(
                    media_root
                )

                destination = (
                    quarantine_root
                    / relative_path
                )

                destination.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                size = source.stat().st_size

                writer.writerow(
                    [
                        normalize_name(relative_path),
                        size,
                    ]
                )

                shutil.move(
                    str(source),
                    str(destination),
                )

                moved += 1
                moved_size += size

        self.stdout.write("")
        self.stdout.write("=" * 72)

        self.stdout.write(
            self.style.SUCCESS(
                f"Archivos movidos: {moved}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Peso movido: "
                f"{moved_size / 1024 / 1024:.2f} MB"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Cuarentena: {quarantine_root}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Manifest: {manifest_path}"
            )
        )

        self.stdout.write("")
        self.stdout.write(
            "No se elimino definitivamente ningun archivo."
        )
