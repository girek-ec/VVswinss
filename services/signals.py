from django.db.models.signals import pre_save
from django.dispatch import receiver
from core.image_utils import optimize_instance_image_fields, sync_social_image
from .models import Service, ServiceCategory

# CATEGORÍAS · OPTIMIZACIÓN AUTOMÁTICA | CATEGORY IMAGE OPTIMIZATION
@receiver(pre_save, sender=ServiceCategory, dispatch_uid="optimize_service_category_images")
def optimize_service_category_images(sender, instance, **kwargs):
    optimize_instance_image_fields(instance, ("hero_image", "image"), max_dimension=2200, quality=82)

# SERVICIOS · OPTIMIZACIÓN AUTOMÁTICA | SERVICE IMAGE OPTIMIZATION

# GALERÍA · OPTIMIZACIÓN AUTOMÁTICA | GALLERY IMAGE OPTIMIZATION

# CATEGORÍAS · IMAGEN SOCIAL | CATEGORY SOCIAL IMAGE
@receiver(pre_save, sender=ServiceCategory, dispatch_uid="sync_service_category_social_image")
def sync_service_category_social_image(sender, instance, **kwargs):
    source_field = "image" if instance.image else "hero_image" if instance.hero_image else None
    if source_field:
        sync_social_image(instance, source_field)

# SERVICES PAGE · WEBP OPTIMIZATION | OPTIMIZAR IMÁGENES CONFIGURADAS
from .visual_config import ServicePageVisualConfiguration

@receiver(pre_save, sender=ServicePageVisualConfiguration, dispatch_uid="optimize_service_page_visual_images")
def optimize_service_page_visual_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        ("category_default_image", "cta_background", "work_method_image", "social_default_image"),
        max_dimension=2200,
        quality=82,
    )
