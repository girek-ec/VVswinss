from django.db.models.signals import pre_save
from django.dispatch import receiver

from core.image_utils import optimize_instance_image_fields, sync_social_image

from .models import Post, PostSection
from .visual_config import BlogPageConfiguration


@receiver(
    pre_save,
    sender=BlogPageConfiguration,
    dispatch_uid="optimize_blog_page_configuration_images",
)
def optimize_blog_page_configuration_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        (
            "header_background",
            "post_default_image",
        ),
        max_dimension=2200,
        quality=82,
    )

    sync_social_image(
        instance,
        "post_default_image",
        target_field_name="post_default_social_image",
    )


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

    sync_social_image(
        instance,
        "main_image",
        target_field_name="og_image",
    )


@receiver(
    pre_save,
    sender=PostSection,
    dispatch_uid="optimize_blog_post_section_images",
)
def optimize_blog_post_section_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        (
            "image_1",
            "image_2",
            "quote_icon",
        ),
        max_dimension=2200,
        quality=82,
    )
