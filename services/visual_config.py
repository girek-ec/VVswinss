# SERVICES · VISUAL CONFIGURATION | CONFIGURACIÓN VISUAL DE SERVICIOS
from django.db import models
from django.templatetags.static import static

# SERVICES · STATIC FALLBACKS | RESPALDOS EXACTOS DE SERVICE_LIST.HTML
SERVICE_STATIC_FALLBACKS = {
    "category_default_image": "antra/assets/img/service/VVS_service.webp",
    "cta_background": "antra/assets/img/service/terraza_minimalista_frente_al_lago_alpino.webp",
    "work_method_image": "antra/assets/img/service/interior_alpino_en_renovacion.webp",
    "social_default_image": "antra/assets/img/service/VVS_service.webp",
}


class ServicePageVisualConfiguration(models.Model):
    category_default_image = models.ImageField(
        "Category default image",
        upload_to="services/page/category/",
        blank=True,
        null=True,
        help_text="Used when a service category has no own image. Default shown below.",
    )
    cta_background = models.ImageField(
        "Quote request background",
        upload_to="services/page/cta/",
        blank=True,
        null=True,
        help_text="Background for the Request a quote section. Default shown below.",
    )
    work_method_image = models.ImageField(
        "Work method image",
        upload_to="services/page/work-method/",
        blank=True,
        null=True,
        help_text="Photo for Our way of working. Default shown below.",
    )
    social_default_image = models.ImageField(
        "Social sharing default image",
        upload_to="services/page/social/",
        blank=True,
        null=True,
        help_text="Open Graph / Twitter image for the Services listing. Default shown below.",
    )

    class Meta:
        verbose_name = "001 - Services Visual Configuration"
        verbose_name_plural = "001 - Services Visual Configuration"

    def __str__(self):
        return "Services · Visual Configuration"


def uploaded_service_image_url(configuration, field_name):
    """Return the uploaded URL only; do not hide the fallback status."""
    if configuration is None:
        return None
    image = getattr(configuration, field_name, None)
    if not image:
        return None
    try:
        return image.url
    except (ValueError, AttributeError, OSError):
        return None


def resolved_service_image_url(configuration, field_name):
    """Uploaded image -> matching static fallback. Never returns an empty URL."""
    return uploaded_service_image_url(configuration, field_name) or static(
        SERVICE_STATIC_FALLBACKS[field_name]
    )
