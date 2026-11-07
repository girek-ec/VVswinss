from django.db import models
from .image_utils import optimize_instance_image_fields

# CONFIGURACIÓN VISUAL DE PÁGINAS | PAGE VISUAL CONFIGURATION
class _VisualConfigurationBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @classmethod
    def image_field_names(cls):
        return tuple(field.name for field in cls._meta.fields if isinstance(field, models.ImageField))

    def save(self, *args, **kwargs):
        optimize_instance_image_fields(self, self.image_field_names(), max_dimension=2200, quality=82)
        super().save(*args, **kwargs)


# FOTOGRAFÍAS EXCLUSIVAS DE ABOUT | ABOUT-ONLY SECTION IMAGES
class AboutPageConfiguration(_VisualConfigurationBase):
    header_background = models.ImageField("ABOUT · Encabezado", upload_to="about/page-visuals/header/", blank=True, null=True)
    mission_primary_image = models.ImageField("ABOUT · Misión · Primera imagen", upload_to="about/page-visuals/mission/", blank=True, null=True)
    mission_secondary_image = models.ImageField("ABOUT · Misión · Segunda imagen", upload_to="about/page-visuals/mission/", blank=True, null=True)
    vision_background = models.ImageField("ABOUT · Visión · Fondo", upload_to="about/page-visuals/vision/", blank=True, null=True)
    vision_image = models.ImageField("ABOUT · Visión · Imagen", upload_to="about/page-visuals/vision/", blank=True, null=True)
    projects_background = models.ImageField("ABOUT · Realizaciones · Fondo de sección", upload_to="about/page-visuals/projects/", blank=True, null=True)

    class Meta:
        verbose_name = "004 - About Visual Configuration"
        verbose_name_plural = "004 - About Visual Configuration"

    def __str__(self):
        return "Configuración visual · About"


# COMPATIBILIDAD HISTÓRICA DE PROFESSIONALS | LEGACY PROFESSIONALS SETTINGS
# La página actual usa professionals.ProfessionalVisualSettings; este modelo NO controla sus fichas.
class ProfessionalPageConfiguration(_VisualConfigurationBase):
    turnover_background = models.ImageField("PROFESSIONALS · Remise en état · Fondo", upload_to="professionals/page-visuals/turnover/", blank=True, null=True)
    faq_image = models.ImageField("PROFESSIONALS · Pourquoi V&V · Imagen lateral", upload_to="professionals/page-visuals/faq/", blank=True, null=True)

    class Meta:
        verbose_name = "018 - Professionals Visual Configuration (legacy)"
        verbose_name_plural = "018 - Professionals Visual Configuration (legacy)"

    def __str__(self):
        return "Configuración visual histórica · Professionals"
