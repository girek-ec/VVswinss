"""Auditoría V2 de Professionals sin modificar datos existentes.

Uso:
    python manage.py audit_professionals_v2
    python manage.py audit_professionals_v2 --probe-upload
"""
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand, CommandError
from django.contrib.staticfiles import finders
from django.db import models
from django.template.loader import get_template
from PIL import Image

from professionals.models import (
    ProfessionalSitePage,
    ProfessionalNeedItem,
    ProfessionalProcessItem,
    ProfessionalAdvantageItem,
    ProfessionalProjectItem,
    ProfessionalExtraBlock,
    ProfessionalVisualSettings,
)

PAGE_MODELS = (
    (ProfessionalSitePage, "Página / Hero", "professional_page"),
    (ProfessionalNeedItem, "Necesidades", "professional_needs"),
    (ProfessionalProcessItem, "Etapas", "professional_processes"),
    (ProfessionalAdvantageItem, "Ventajas", "professional_advantages"),
    (ProfessionalProjectItem, "Proyectos vinculados", "featured_projects"),
    (ProfessionalExtraBlock, "Bloques adicionales", "professional_blocks"),
    (ProfessionalVisualSettings, "Imágenes de sección", "professional_visuals"),
)
FALLBACK = "antra/assets/img/professionals/professionals_default.webp"
IMAGE_FIELDS = (
    (ProfessionalSitePage, ("hero_image",)),
    (ProfessionalVisualSettings, ("hero_default_image", "turnover_background", "faq_image")),
    (ProfessionalNeedItem, ("image",)),
    (ProfessionalProcessItem, ("image",)),
    (ProfessionalExtraBlock, ("image",)),
)


class Command(BaseCommand):
    help = "Audita modelos V2, plantilla, archivos y prueba WebP en memoria (opcional) sin modificar la base de datos."

    def add_arguments(self, parser):
        parser.add_argument("--probe-upload", action="store_true", help="Simula una carga PNG/JPEG sin guardar registros ni imágenes en MEDIA_ROOT.")
        parser.add_argument("--limit", type=int, default=30, help="Máximo de imágenes existentes inspeccionadas.")

    def handle(self, *args, **options):
        self.stdout.write("=" * 64)
        self.stdout.write("V&V · AUDITORÍA PROFESSIONALS V2")
        self.stdout.write("=" * 64)
        self._check_template()
        self._check_records()
        self._check_stored_images(max(0, options["limit"]))
        if options["probe_upload"]:
            self._probe_upload()
        self.stdout.write(self.style.SUCCESS("Auditoría finalizada. No se modificaron registros de la base de datos."))

    def _check_template(self):
        template = get_template("professionals/index.html")
        origin = getattr(template, "origin", None)
        source_path = getattr(origin, "name", None)
        if not source_path or not Path(source_path).is_file():
            self.stdout.write(self.style.WARNING("PLANTILLA: no se pudo leer el código de origen para cotejar las variables."))
        else:
            source = Path(source_path).read_text(encoding="utf-8")
            for _, title, context_name in PAGE_MODELS:
                used = context_name in source
                self.stdout.write(("[OK]" if used else "[REVISAR]") + f" Plantilla usa {context_name}: {title}")
            if "block.icon" not in source:
                self.stdout.write(self.style.WARNING("[PENDIENTE] El campo icon de ProfessionalExtraBlock no se muestra en el HTML."))
            if "block.layout == 'card'" not in source and 'block.layout == "card"' not in source:
                self.stdout.write(self.style.WARNING("[PENDIENTE] El layout 'card' no tiene tratamiento específico en el HTML."))
        fallback_path = finders.find(FALLBACK)
        if fallback_path:
            self.stdout.write(f"[OK] Respaldo estático existente: {fallback_path}")
        else:
            self.stdout.write(self.style.ERROR(f"[FALTA] Static fallback: {FALLBACK}. Copiarlo desde el ZIP V2 y ejecutar collectstatic en producción."))

    def _check_records(self):
        page = ProfessionalSitePage.objects.filter(slug="main", is_active=True).first()
        if page is None:
            self.stdout.write(self.style.WARNING("[PENDIENTE] No se encontró ProfessionalSitePage(slug='main', is_active=True)."))
            return
        self.stdout.write(f"[OK] Página principal: ID {page.pk} | servicios vinculados: {page.services.count()}")
        for model, title, _ in PAGE_MODELS[1:]:
            qs = model.objects.filter(page=page)
            if model is ProfessionalVisualSettings:
                count = qs.count()
                active = count
            else:
                count = qs.count()
                active = qs.filter(is_active=True).count()
            self.stdout.write(f"{title}: {active} activos / {count} registros")
        selected = ProfessionalProjectItem.objects.filter(page=page, is_active=True, project__is_published=True).count()
        self.stdout.write(f"Proyectos publicados seleccionados: {selected} (si 0, la vista usa los destacados globales).")

    def _check_stored_images(self, limit):
        self.stdout.write("-- Imágenes previamente guardadas en los modelos V2 --")
        checked = 0
        for model, field_names in IMAGE_FIELDS:
            for obj in model.objects.all().iterator():
                for name in field_names:
                    file_field = getattr(obj, name)
                    if not file_field:
                        continue
                    if checked >= limit:
                        self.stdout.write("Límite de inspección alcanzado.")
                        return
                    checked += 1
                    try:
                        if not file_field.storage.exists(file_field.name):
                            self.stdout.write(self.style.ERROR(f"[NO EXISTE] {model.__name__} #{obj.pk}.{name}: {file_field.name}"))
                            continue
                        length = file_field.size
                        with file_field.storage.open(file_field.name, "rb") as uploaded:
                            with Image.open(uploaded) as image:
                                format_name, width, height = image.format, image.width, image.height
                        good = format_name == "WEBP" and max(width, height) <= 2200
                        msg = f"{model.__name__} #{obj.pk}.{name}: {format_name}, {width}x{height}, {length / 1024:.1f} KB · {file_field.name}"
                        self.stdout.write(("[OK] " if good else "[REVISAR] ") + msg)
                    except Exception as exc:
                        self.stdout.write(self.style.ERROR(f"[ERROR] {model.__name__} #{obj.pk}.{name}: {type(exc).__name__}: {exc}"))
        if checked == 0:
            self.stdout.write("No hay imágenes V2 cargadas todavía. Use --probe-upload para probar el optimizador.")

    @staticmethod
    def _make_upload(kind):
        image = Image.new("RGB", (2600, 1400), (194, 197, 195))
        out = BytesIO()
        if kind == "PNG":
            image.save(out, format="PNG")
            return SimpleUploadedFile("prueba_professionals.png", out.getvalue(), content_type="image/png")
        image.save(out, format="JPEG", quality=92)
        return SimpleUploadedFile("prueba_professionals.jpg", out.getvalue(), content_type="image/jpeg")

    def _probe_upload(self):
        # Se reemplaza temporalmente el storage de los ImageField por un directorio efímero.
        # Se intercepta Model.save: no escribe ninguna fila ni toca MEDIA_ROOT.
        self.stdout.write("-- Prueba temporal de JPG/PNG -> WebP, sin guardar en BD --")
        try:
            from core.image_utils import optimize_instance_image_fields  # noqa: F401
        except Exception as exc:
            raise CommandError(f"No se pudo importar el optimizador común core.image_utils: {exc}") from exc
        from professionals.models import ProfessionalSitePage as Page
        with TemporaryDirectory(prefix="vv_prof_audit_") as temp_dir:
            for model, names in IMAGE_FIELDS:
                for name in names:
                    field = model._meta.get_field(name)
                    if not isinstance(field, models.ImageField):
                        continue
                    for kind in ("PNG", "JPEG"):
                        try:
                            # Se construye un modelo V2 sin guardar y se utiliza su save() real
                            # para comprobar la llamada al optimizador configurada en el modelo.
                            tmp_storage = FileSystemStorage(location=temp_dir)
                            with patch.object(field, "storage", tmp_storage), patch.object(models.Model, "save", return_value=None):
                                obj = model()
                                setattr(obj, name, self._make_upload(kind))
                                obj.save()
                                result = getattr(obj, name)
                                with result.open("rb") as uploaded:
                                    with Image.open(uploaded) as image:
                                        actual_format, w, h = image.format, image.width, image.height
                                expected = result.name.lower().endswith(".webp") and actual_format == "WEBP" and max(w, h) <= 2200
                                label = f"{model.__name__}.{name} / {kind} -> {result.name} | {actual_format} {w}x{h}"
                                self.stdout.write(("[OK] " if expected else "[FALLO] ") + label)
                        except Exception as exc:
                            self.stdout.write(self.style.ERROR(f"[ERROR] {model.__name__}.{name} / {kind}: {type(exc).__name__}: {exc}"))
        self.stdout.write("La prueba usa un directorio temporal y simula Model.save sin escribir registros.")
