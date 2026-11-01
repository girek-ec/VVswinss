from django.db import models

from core.image_utils import optimize_instance_image_fields


class ContactPageConfiguration(models.Model):
    """
    EN: Visual configuration for the Contact page.
    ES: Configuración visual de la página Contact.
    """

    header_background = models.ImageField(
        "CONTACT · Header / Encabezado",
        upload_to="contact/page-visuals/header/",
        blank=True,
        null=True,
        help_text=(
            "ES: Fondo del encabezado. Si está vacío se usa el static original. "
            "EN: Header background. If empty, the original static image is used."
        ),
    )
    main_image = models.ImageField(
        "CONTACT · Main image / Imagen principal",
        upload_to="contact/page-visuals/main/",
        blank=True,
        null=True,
        help_text=(
            "ES: Imagen principal de la página Contact. "
            "EN: Main image shown on the Contact page."
        ),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '001 - Contact Visual Configuration'
        verbose_name_plural = '001 - Contact Visual Configuration'

    def __str__(self):
        return "Configuración visual · Contact"

    def save(self, *args, **kwargs):
        optimize_instance_image_fields(
            self,
            ("header_background", "main_image"),
            max_dimension=2200,
            quality=82,
        )
        super().save(*args, **kwargs)
