from django.db import models

from .image_utils import optimize_instance_image_fields


class _VisualConfigurationBase(models.Model):
    """
    EN: Base model for single-record visual page configuration.
    ES: Modelo base para configuración visual de una sola instancia.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @classmethod
    def image_field_names(cls):
        return tuple(
            field.name
            for field in cls._meta.fields
            if isinstance(field, models.ImageField)
        )

    def save(self, *args, **kwargs):
        optimize_instance_image_fields(
            self,
            self.image_field_names(),
            max_dimension=2200,
            quality=82,
        )
        super().save(*args, **kwargs)


class AboutPageConfiguration(_VisualConfigurationBase):
    """
    EN: Visual images used by the About page when a more specific image is not available.
    ES: Imágenes visuales de About usadas cuando no existe una imagen más específica.
    """

    header_background = models.ImageField(
        "ABOUT · Header / Encabezado",
        upload_to="about/page-visuals/header/",
        blank=True,
        null=True,
        help_text=(
            "ES: Fondo del encabezado. Si está vacío se usa static "
            "antra/assets/img/bg-img/page-header-bg.webp. "
            "EN: Header background. If empty, the original static image is used."
        ),
    )
    intro_image = models.ImageField(
        "ABOUT · Introduction / Presentación",
        upload_to="about/page-visuals/intro/",
        blank=True,
        null=True,
        help_text=(
            "ES: Respaldo para la imagen de presentación. AboutContent.image tiene prioridad. "
            "EN: Fallback for the introduction image. AboutContent.image has priority."
        ),
    )
    team_default_image = models.ImageField(
        "ABOUT · Team fallback / Respaldo de equipo",
        upload_to="about/page-visuals/team/",
        blank=True,
        null=True,
        help_text=(
            "ES: Se usa cuando un miembro no tiene foto. "
            "EN: Used when a team member does not have a photo."
        ),
    )
    video_background = models.ImageField(
        "ABOUT · Video background / Fondo de vídeo",
        upload_to="about/page-visuals/video/",
        blank=True,
        null=True,
        help_text=(
            "ES: Respaldo del bloque de vídeo. AboutContent.video_image tiene prioridad. "
            "EN: Video section fallback. AboutContent.video_image has priority."
        ),
    )
    mission_primary_image = models.ImageField(
        "ABOUT · Mission primary / Misión principal",
        upload_to="about/page-visuals/mission/",
        blank=True,
        null=True,
        help_text="ES: Imagen principal de la misión. EN: Primary mission image.",
    )
    mission_secondary_image = models.ImageField(
        "ABOUT · Mission secondary / Misión secundaria",
        upload_to="about/page-visuals/mission/",
        blank=True,
        null=True,
        help_text="ES: Imagen secundaria de la misión. EN: Secondary mission image.",
    )
    vision_background = models.ImageField(
        "ABOUT · Vision background / Fondo de visión",
        upload_to="about/page-visuals/vision/",
        blank=True,
        null=True,
        help_text="ES: Fondo de la sección de visión. EN: Vision section background.",
    )
    vision_image = models.ImageField(
        "ABOUT · Vision image / Imagen de visión",
        upload_to="about/page-visuals/vision/",
        blank=True,
        null=True,
        help_text="ES: Imagen principal de la visión. EN: Main vision image.",
    )
    value_default_image = models.ImageField(
        "ABOUT · Values fallback / Respaldo de valores",
        upload_to="about/page-visuals/values/",
        blank=True,
        null=True,
        help_text="ES: Respaldo visual de valores. EN: Default visual for values.",
    )

    insurance_default_image = models.ImageField(
        "ABOUT · Insurance fallback / Respaldo de seguros",
        upload_to="about/page-visuals/insurances/",
        blank=True,
        null=True,
        help_text=(
            "ES: Se usa cuando un seguro no dispone de imagen. "
            "EN: Used when an insurance item does not have an image."
        ),
    )

    certification_default_image = models.ImageField(
        "ABOUT · Certifications fallback / Respaldo de certificaciones",
        upload_to="about/page-visuals/certifications/",
        blank=True,
        null=True,
        help_text=(
            "ES: Se usa cuando una certificación no dispone de imagen. "
            "EN: Used when a certification does not have an image."
        ),
    )
    certification_default_image = models.ImageField(
        "ABOUT · Certifications fallback / Respaldo de certificaciones",
        upload_to="about/page-visuals/certifications/",
        blank=True,
        null=True,
        help_text=(
            "ES: Se usa cuando una certificación no dispone de imagen. "
            "EN: Used when a certification does not have an image."
        ),
    )


    projects_background = models.ImageField(
        "ABOUT · Projects background / Fondo de realizaciones",
        upload_to="about/page-visuals/projects/",
        blank=True,
        null=True,
        help_text="ES: Fondo del bloque de realizaciones. EN: Projects section background.",
    )
    project_default_image = models.ImageField(
        "ABOUT · Project fallback / Respaldo de proyecto",
        upload_to="about/page-visuals/projects/",
        blank=True,
        null=True,
        help_text=(
            "ES: Se usa cuando un proyecto destacado no tiene main_image. "
            "EN: Used when a featured project has no main_image."
        ),
    )

    class Meta:
        verbose_name = '004 - About Visual Configuration'
        verbose_name_plural = '004 - About Visual Configuration'

    def __str__(self):
        return "Configuración visual · About"


class ProfessionalPageConfiguration(_VisualConfigurationBase):
    """
    EN: Static-image replacements and visual fallbacks for Professionals.
    ES: Reemplazos administrables y respaldos visuales para Professionals.
    """

    hero_default_image = models.ImageField(
        "PROFESSIONALS · Hero fallback / Respaldo del hero",
        upload_to="professionals/page-visuals/hero/",
        blank=True,
        null=True,
        help_text=(
            "ES: Se usa si ProfessionalPage.hero_image está vacío. "
            "EN: Used when ProfessionalPage.hero_image is empty."
        ),
    )
    need_coordination_image = models.ImageField(
        "PROFESSIONALS · Need 01 / Necesidad 01 · Coordinación",
        upload_to="professionals/page-visuals/needs/",
        blank=True,
        null=True,
    )
    need_planning_image = models.ImageField(
        "PROFESSIONALS · Need 02 / Necesidad 02 · Planificación",
        upload_to="professionals/page-visuals/needs/",
        blank=True,
        null=True,
    )
    need_turnover_image = models.ImageField(
        "PROFESSIONALS · Need 03 / Necesidad 03 · Remise en état",
        upload_to="professionals/page-visuals/needs/",
        blank=True,
        null=True,
    )
    need_maintenance_image = models.ImageField(
        "PROFESSIONALS · Need 04 / Necesidad 04 · Mantenimiento",
        upload_to="professionals/page-visuals/needs/",
        blank=True,
        null=True,
    )
    need_occupancy_image = models.ImageField(
        "PROFESSIONALS · Need 05 / Necesidad 05 · Nueva ocupación",
        upload_to="professionals/page-visuals/needs/",
        blank=True,
        null=True,
    )
    turnover_background = models.ImageField(
        "PROFESSIONALS · Turnover background / Fondo Remise en état",
        upload_to="professionals/page-visuals/turnover/",
        blank=True,
        null=True,
    )
    evaluation_image = models.ImageField(
        "PROFESSIONALS · Process 01 / Proceso 01 · Évaluation",
        upload_to="professionals/page-visuals/process/",
        blank=True,
        null=True,
    )
    planning_image = models.ImageField(
        "PROFESSIONALS · Process 02 / Proceso 02 · Planification",
        upload_to="professionals/page-visuals/process/",
        blank=True,
        null=True,
    )
    intervention_image = models.ImageField(
        "PROFESSIONALS · Process 03 / Proceso 03 · Intervention",
        upload_to="professionals/page-visuals/process/",
        blank=True,
        null=True,
    )
    control_image = models.ImageField(
        "PROFESSIONALS · Process 04 / Proceso 04 · Contrôle",
        upload_to="professionals/page-visuals/process/",
        blank=True,
        null=True,
    )
    faq_image = models.ImageField(
        "PROFESSIONALS · Why V&V / Pourquoi V&V · Imagen lateral",
        upload_to="professionals/page-visuals/faq/",
        blank=True,
        null=True,
    )
    service_default_image = models.ImageField(
        "PROFESSIONALS · Services fallback / Respaldo de servicios",
        upload_to="professionals/page-visuals/services/",
        blank=True,
        null=True,
        help_text=(
            "ES: Se usa cuando un servicio no tiene main_image. "
            "EN: Used when a service has no main_image."
        ),
    )
    project_default_image = models.ImageField(
        "PROFESSIONALS · Projects fallback / Respaldo de proyectos",
        upload_to="professionals/page-visuals/projects/",
        blank=True,
        null=True,
        help_text=(
            "ES: Se usa cuando un proyecto no tiene main_image. "
            "EN: Used when a project has no main_image."
        ),
    )

    class Meta:
        verbose_name = '018 - Professionals Visual Configuration'
        verbose_name_plural = '018 - Professionals Visual Configuration'

    def __str__(self):
        return "Configuración visual · Professionals"
