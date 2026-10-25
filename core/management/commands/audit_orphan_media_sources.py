from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import FileField


EXCLUDED_PREFIXES = (
    "contact/attachments/",
    "site/",
    "seo/",
    "blog/quotes/",
)

SOURCE_EXTENSIONS = {
    ".html",
    ".css",
    ".js",
    ".py",
    ".json",
    ".txt",
    ".md",
}

SCAN_DIRECTORIES = (
    "templates",
    "static",
    "core",
    "services",
    "projects",
    "blog",
    "contact",
    "vvswinss",
)


def normalize_name(value):
    return str(value).replace("\\", "/").lstrip("/")


class Command(BaseCommand):
    help = (
        "Comprueba si archivos aparentemente huerfanos de media "
        "estan referenciados directamente en plantillas, CSS, JS o Python."
    )

    def handle(self, *args, **options):
        base_dir = Path(settings.BASE_DIR).resolve()
        media_root = Path(settings.MEDIA_ROOT).resolve()

        # ============================================================
        # REFERENCIAS DE BASE DE DATOS
        # ============================================================

        database_references = set()

        for model in apps.get_models():
            fields = [
                field
                for field in model._meta.fields
                if isinstance(field, FileField)
            ]

            if not fields:
                continue

            for instance in model._default_manager.all().iterator():
                for field in fields:
                    value = getattr(instance, field.name, None)
                    name = getattr(value, "name", "")

                    if name:
                        database_references.add(
                            normalize_name(name)
                        )

        # ============================================================
        # CANDIDATOS HUERFANOS
        # ============================================================

        candidates = []

        for path in media_root.rglob("*"):
            if not path.is_file():
                continue

            relative = normalize_name(
                path.relative_to(media_root)
            )

            if relative.startswith(EXCLUDED_PREFIXES):
                continue

            if relative in database_references:
                continue

            candidates.append(
                (
                    path,
                    relative,
                )
            )

        # ============================================================
        # CARGAR ARCHIVOS FUENTE
        # ============================================================

        source_documents = []

        for directory_name in SCAN_DIRECTORIES:
            directory = base_dir / directory_name

            if not directory.exists():
                continue

            for source_path in directory.rglob("*"):
                if not source_path.is_file():
                    continue

                if source_path.suffix.lower() not in SOURCE_EXTENSIONS:
                    continue

                try:
                    content = source_path.read_text(
                        encoding="utf-8",
                        errors="ignore",
                    ).lower()
                except OSError:
                    continue

                source_documents.append(
                    (
                        source_path,
                        content,
                    )
                )

        # ============================================================
        # BUSCAR REFERENCIAS DIRECTAS
        # ============================================================

        source_referenced = []
        safe_candidates = []

        for physical_path, relative in candidates:
            relative_lower = relative.lower()
            basename_lower = physical_path.name.lower()

            matches = []

            for source_path, content in source_documents:
                if (
                    relative_lower in content
                    or basename_lower in content
                ):
                    matches.append(source_path)

            if matches:
                source_referenced.append(
                    (
                        physical_path,
                        relative,
                        matches,
                    )
                )
            else:
                safe_candidates.append(
                    (
                        physical_path,
                        relative,
                    )
                )

        # ============================================================
        # RESUMEN
        # ============================================================

        candidate_size = sum(
            path.stat().st_size
            for path, _ in candidates
        )

        protected_size = sum(
            path.stat().st_size
            for path, _, _ in source_referenced
        )

        safe_size = sum(
            path.stat().st_size
            for path, _ in safe_candidates
        )

        self.stdout.write("")
        self.stdout.write("=" * 72)
        self.stdout.write(
            "V&V SWISS SERVICES · AUDITORIA DE REFERENCIAS EN CODIGO"
        )
        self.stdout.write("=" * 72)

        self.stdout.write(
            f"Candidatos huerfanos segun BD: {len(candidates)}"
        )

        self.stdout.write(
            f"Encontrados en plantillas/codigo: {len(source_referenced)}"
        )

        self.stdout.write(
            f"Candidatos sin referencia detectada: {len(safe_candidates)}"
        )

        self.stdout.write(
            f"Peso total candidato: "
            f"{candidate_size / 1024 / 1024:.2f} MB"
        )

        self.stdout.write(
            f"Peso protegido por referencia en codigo: "
            f"{protected_size / 1024 / 1024:.2f} MB"
        )

        self.stdout.write(
            f"Peso potencialmente recuperable: "
            f"{safe_size / 1024 / 1024:.2f} MB"
        )

        # ============================================================
        # ARCHIVOS ENCONTRADOS EN CODIGO
        # ============================================================

        if source_referenced:
            self.stdout.write("")
            self.stdout.write(
                "ARCHIVOS QUE NO DEBEMOS MOVER TODAVIA"
            )
            self.stdout.write("-" * 72)

            for physical_path, relative, matches in source_referenced:
                size_mb = (
                    physical_path.stat().st_size
                    / 1024
                    / 1024
                )

                self.stdout.write(
                    f"{size_mb:8.2f} MB | {relative}"
                )

                for match in matches[:5]:
                    try:
                        shown_path = match.relative_to(base_dir)
                    except ValueError:
                        shown_path = match

                    self.stdout.write(
                        f"           -> {shown_path}"
                    )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "Auditoria finalizada. No se modifico ningun archivo."
            )
        )
