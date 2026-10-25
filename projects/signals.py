from django.db.models.signals import pre_save
from django.dispatch import receiver

from core.image_utils import optimize_instance_image_fields
from .models import BeforeAfter, Project, ProjectImage


@receiver(
    pre_save,
    sender=Project,
    dispatch_uid="optimize_project_images",
)
def optimize_project_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        ("main_image",),
        max_dimension=2200,
        quality=82,
    )


@receiver(
    pre_save,
    sender=ProjectImage,
    dispatch_uid="optimize_project_gallery_images",
)
def optimize_project_gallery_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        ("image",),
        max_dimension=2200,
        quality=82,
    )


@receiver(
    pre_save,
    sender=BeforeAfter,
    dispatch_uid="optimize_before_after_images",
)
def optimize_before_after_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        (
            "before_image",
            "after_image",
        ),
        max_dimension=2200,
        quality=82,
    )