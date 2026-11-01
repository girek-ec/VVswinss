from django.db import models

from core.image_utils import optimize_instance_image_fields


class ProjectPageConfiguration(models.Model):
    """
    EN: Visual configuration for the Projects section.
    ES: Configuración visual de la sección Projects.
    """

    header_background = models.ImageField(
        "PROJECTS · Header / Encabezado",
        upload_to="projects/page-visuals/header/",
        blank=True,
        null=True,
        help_text=(
            "ES: Fondo general del encabezado. Si está vacío se usa static "
            "antra/assets/img/bg-img/page-header-bg.webp. "
            "EN: General header background. If empty, the static fallback is used."
        ),
    )
    default_image = models.ImageField(
        "PROJECTS · Project fallback / Respaldo de proyecto",
        upload_to="projects/page-visuals/fallback/",
        blank=True,
        null=True,
        help_text=(
            "ES: Se usa cuando Project.main_image está vacío. "
            "EN: Used when Project.main_image is empty."
        ),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '001 - Projects Visual Configuration'
        verbose_name_plural = '001 - Projects Visual Configuration'

    def __str__(self):
        return "Configuración visual · Projects"

    def save(self, *args, **kwargs):
        optimize_instance_image_fields(
            self,
            ("header_background", "default_image"),
            max_dimension=2200,
            quality=82,
        )
        super().save(*args, **kwargs)
