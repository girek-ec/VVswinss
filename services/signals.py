from django.db.models.signals import pre_save
from django.dispatch import receiver

from core.image_utils import optimize_instance_image_fields, sync_social_image
from .models import (
    Service,
    ServiceCategory,
    ServiceImage,
    ServicePageConfiguration,
)


# CONFIGURACIÓN VISUAL · OPTIMIZACIÓN / VISUAL CONFIGURATION · OPTIMIZATION
@receiver(
    pre_save,
    sender=ServicePageConfiguration,
    dispatch_uid="optimize_service_page_configuration_images",
)
def optimize_service_page_configuration_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        (
            "category_default_image",
            "list_cta_background",
            "method_background",
            "page_header_background",
            "sidebar_cta_background",
            "detail_default_image",
            "secondary_default_image",
            "third_default_image",
            "gallery_default_image",
        ),
        max_dimension=2200,
        quality=82,
    )

    sync_social_image(
        instance,
        "category_default_image",
        target_field_name="category_default_social_image",
    )


# CATEGORÍA · OPTIMIZACIÓN DE IMÁGENES / CATEGORY · IMAGE OPTIMIZATION
@receiver(
    pre_save,
    sender=ServiceCategory,
    dispatch_uid="optimize_service_category_images",
)
def optimize_service_category_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        ("hero_image", "image"),
        max_dimension=2200,
        quality=82,
    )


# SERVICIO · OPTIMIZACIÓN DE IMÁGENES / SERVICE · IMAGE OPTIMIZATION
@receiver(
    pre_save,
    sender=Service,
    dispatch_uid="optimize_service_images",
)
def optimize_service_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        (
            "hero_image",
            "main_image",
            "secondary_image",
            "third_image",
        ),
        max_dimension=2200,
        quality=82,
    )


# GALERÍA DE SERVICIO · OPTIMIZACIÓN / SERVICE GALLERY · OPTIMIZATION
@receiver(
    pre_save,
    sender=ServiceImage,
    dispatch_uid="optimize_service_gallery_images",
)
def optimize_service_gallery_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        ("image",),
        max_dimension=2200,
        quality=82,
    )


# CATEGORÍA · IMAGEN SOCIAL / CATEGORY · SOCIAL IMAGE
@receiver(
    pre_save,
    sender=ServiceCategory,
    dispatch_uid="sync_service_category_social_image",
)
def sync_service_category_social_image(sender, instance, **kwargs):
    if instance.image:
        source_field = "image"
    elif instance.hero_image:
        source_field = "hero_image"
    else:
        return

    sync_social_image(
        instance,
        source_field,
    )
