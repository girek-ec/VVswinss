from django.db.models.signals import pre_save
from django.dispatch import receiver

from core.image_utils import optimize_instance_image_fields
from .models import Post, PostSection


@receiver(
    pre_save,
    sender=Post,
    dispatch_uid="optimize_blog_post_images",
)
def optimize_blog_post_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        ("main_image",),
        max_dimension=2200,
        quality=82,
    )


@receiver(
    pre_save,
    sender=PostSection,
    dispatch_uid="optimize_blog_section_images",
)
def optimize_blog_section_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        (
            "image_1",
            "image_2",
        ),
        max_dimension=2200,
        quality=82,
    )