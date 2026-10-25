from django.db.models.signals import pre_save
from django.dispatch import receiver

from core.image_utils import optimize_instance_image_fields
from .models import Service, ServiceCategory, ServiceImage


@receiver(
    pre_save,
    sender=ServiceCategory,
    dispatch_uid="optimize_service_category_images",
)
def optimize_service_category_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        ("image",),
        max_dimension=2200,
        quality=82,
    )


@receiver(
    pre_save,
    sender=Service,
    dispatch_uid="optimize_service_images",
)
def optimize_service_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        (
            "main_image",
            "secondary_image",
            "third_image",
        ),
        max_dimension=2200,
        quality=82,
    )


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