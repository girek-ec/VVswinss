import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from core.models import SiteConfiguration


class Command(BaseCommand):
    help = (
        "Crea o actualiza la configuración general "
        "de V&V Swiss Services."
    )

    def handle(self, *args, **options):

        # ==========================================================
        # LOGO PRINCIPAL
        # ==========================================================

        logo_name = "site/logo-vvswiss-services.png"

        media_logo_path = (
            Path(settings.MEDIA_ROOT)
            / logo_name
        )

        source_logo_path = (
            Path(settings.BASE_DIR)
            / "static"
            / "antra"
            / "assets"
            / "img"
            / "logo"
            / "logo-2.png"
        )

        # Si el logo todavía no existe en MEDIA,
        # se copia desde el archivo estático versionado.
        #
        # Nunca sobrescribimos un logo existente en MEDIA.
        if not media_logo_path.exists():

            if not source_logo_path.exists():
                raise CommandError(
                    "No existe el logo en MEDIA y tampoco se encontró "
                    f"el logo fuente en: {source_logo_path}"
                )

            media_logo_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            shutil.copy2(
                source_logo_path,
                media_logo_path,
            )

            self.stdout.write(
                self.style.SUCCESS(
                    "Logo copiado a MEDIA: "
                    f"{media_logo_path}"
                )
            )

        if not media_logo_path.is_file():
            raise CommandError(
                "La ruta esperada para el logo no corresponde "
                f"a un archivo: {media_logo_path}"
            )

        # ==========================================================
        # SEGURIDAD · SINGLETON
        # ==========================================================

        count = SiteConfiguration.objects.count()

        if count > 1:
            raise CommandError(
                "Existen varios registros SiteConfiguration. "
                "No se modificó nada para evitar actualizar "
                "el registro equivocado."
            )

        # ==========================================================
        # DATOS CONFIRMADOS
        # ==========================================================

        data = {
            "company_name": "V&V Swiss Services",

            "slogan_es": (
                "Renovación, aislamiento y trabajos del edificio "
                "en la Suiza francófona"
            ),

            "slogan_fr": (
                "Rénovation, isolation et travaux du bâtiment "
                "en Suisse romande"
            ),

            "slogan_de": (
                "Renovation, Wärmedämmung und Bauarbeiten "
                "in der Westschweiz"
            ),

            "slogan_it": (
                "Ristrutturazione, isolamento e lavori edili "
                "nella Svizzera romanda"
            ),

            "slogan_en": (
                "Renovation, insulation and building works "
                "in French-speaking Switzerland"
            ),

            "country": "Switzerland",
            "is_active": True,
        }

        # ==========================================================
        # CREAR
        # ==========================================================

        if count == 0:

            obj = SiteConfiguration.objects.create(
                logo=logo_name,
                **data,
            )

            self.stdout.write(
                self.style.SUCCESS(
                    "SiteConfiguration creado correctamente. "
                    f"ID={obj.pk}"
                )
            )

        # ==========================================================
        # ACTUALIZAR
        # ==========================================================

        else:

            obj = SiteConfiguration.objects.first()

            for field_name, value in data.items():
                setattr(
                    obj,
                    field_name,
                    value,
                )

            # Conservamos un logo ya configurado.
            # Solo asignamos el logo estándar si está vacío.
            if not obj.logo:
                obj.logo.name = logo_name

            obj.save()

            self.stdout.write(
                self.style.SUCCESS(
                    "SiteConfiguration actualizado correctamente. "
                    f"ID={obj.pk}"
                )
            )

        # ==========================================================
        # RESULTADO
        # ==========================================================

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                f"Empresa: {obj.company_name}"
            )
        )

        self.stdout.write(
            f"Logo: {obj.logo.name}"
        )

        self.stdout.write(
            f"País: {obj.country}"
        )

        self.stdout.write(
            f"Activo: {obj.is_active}"
        )

        self.stdout.write("")

        self.stdout.write(
            "Los datos de teléfono, WhatsApp, correo, dirección, "
            "IDE/UID, TVA y demás información legal no fueron "
            "inventados ni modificados."
        )
