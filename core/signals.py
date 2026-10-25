from django.db.models.signals import pre_save
from django.dispatch import receiver

from .image_utils import optimize_instance_image_fields
from .models import (
    AboutContent,
    Certification,
    CompanyValue,
    HomeContent,
    Insurance,
    InstitutionalPage,
    ProfessionalBlock,
    ProfessionalPage,
    TeamMember,
    Testimonial,
)


@receiver(
    pre_save,
    sender=AboutContent,
    dispatch_uid="optimize_about_images",
)
def optimize_about_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        (
            "image",
            "video_image",
        ),
        max_dimension=2200,
        quality=82,
    )


@receiver(
    pre_save,
    sender=TeamMember,
    dispatch_uid="optimize_team_images",
)
def optimize_team_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        ("photo",),
        max_dimension=2200,
        quality=82,
    )


@receiver(
    pre_save,
    sender=CompanyValue,
    dispatch_uid="optimize_company_value_images",
)
def optimize_company_value_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        ("image",),
        max_dimension=2200,
        quality=82,
    )


@receiver(
    pre_save,
    sender=Testimonial,
    dispatch_uid="optimize_testimonial_images",
)
def optimize_testimonial_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        ("photo",),
        max_dimension=2200,
        quality=82,
    )


@receiver(
    pre_save,
    sender=InstitutionalPage,
    dispatch_uid="optimize_institutional_page_images",
)
def optimize_institutional_page_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        ("image",),
        max_dimension=2200,
        quality=82,
    )


@receiver(
    pre_save,
    sender=HomeContent,
    dispatch_uid="optimize_home_images",
)
def optimize_home_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        ("hero_image",),
        max_dimension=2200,
        quality=82,
    )


@receiver(
    pre_save,
    sender=ProfessionalPage,
    dispatch_uid="optimize_professional_page_images",
)
def optimize_professional_page_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        ("hero_image",),
        max_dimension=2200,
        quality=82,
    )


@receiver(
    pre_save,
    sender=ProfessionalBlock,
    dispatch_uid="optimize_professional_block_images",
)
def optimize_professional_block_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        ("image",),
        max_dimension=2200,
        quality=82,
    )


@receiver(
    pre_save,
    sender=Insurance,
    dispatch_uid="optimize_insurance_images",
)
def optimize_insurance_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        ("image",),
        max_dimension=2200,
        quality=88,
    )


@receiver(
    pre_save,
    sender=Certification,
    dispatch_uid="optimize_certification_images",
)
def optimize_certification_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        ("image",),
        max_dimension=2200,
        quality=88,
    )