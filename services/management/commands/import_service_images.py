# CARGA SEGURA DE FOTOGRAFÍAS WEBP DE SERVICIOS | SAFE SERVICE WEBP IMPORT
from pathlib import Path
from django.contrib.staticfiles import finders
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from services.models import Service
from services.service_image_catalog import SERVICE_SLUGS, service_image_static_path


class Command(BaseCommand):
    help = "Vincula las 37 imágenes WebP estáticas a Service.image sin sobrescribir fotos existentes."

    def add_arguments(self, parser):
        parser.add_argument("--apply", action="store_true", help="Importar archivos en MEDIA y guardar referencias en PostgreSQL.")

    def handle(self, *args, **options):
        apply = options["apply"]
        found = missing = occupied = imported = errors = 0
        self.stdout.write("V&V SWISS SERVICES · CATÁLOGO DE IMÁGENES")
        self.stdout.write("MODO: " + ("IMPORTAR" if apply else "VISTA PREVIA (no modifica nada)"))
        for slug in sorted(SERVICE_SLUGS):
            service = Service.objects.filter(slug_fr=slug).first()
            if service is None:
                missing += 1
                self.stdout.write(self.style.WARNING("SIN SERVICIO: " + slug))
                continue
            found += 1
            if service.image:
                occupied += 1
                self.stdout.write("CONSERVAR IMAGEN EXISTENTE: " + service.name_fr)
                continue
            source_path = service_image_static_path(slug)
            file_path = finders.find(source_path)
            if not file_path or not Path(file_path).is_file():
                errors += 1
                self.stdout.write(self.style.ERROR("NO EXISTE WEBP: " + source_path))
                continue
            if not apply:
                self.stdout.write("PREPARADO: " + service.name_fr)
                continue
            try:
                with open(file_path, "rb") as fp:
                    service.image.save(f"{slug}.webp", ContentFile(fp.read()), save=True)
                imported += 1
                self.stdout.write(self.style.SUCCESS("IMPORTADO: " + service.name_fr))
            except Exception as exc:
                errors += 1
                self.stdout.write(self.style.ERROR(f"ERROR: {service.name_fr}: {exc}"))
        self.stdout.write(f"Serv. encontrados: {found} | No encontrados: {missing} | "
                          f"Ya tenían imagen: {occupied} | Nuevas importaciones: {imported} | Errores: {errors}")
        if not apply:
            self.stdout.write("Para aplicar: python manage.py import_service_images --apply")
        if errors:
            self.stdout.write(self.style.WARNING("Revisar archivos ausentes o permisos antes de continuar."))
