from django.contrib import admin

from .visual_config import AboutPageConfiguration, ProfessionalPageConfiguration


class _SingleVisualConfigurationAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(AboutPageConfiguration)
class AboutPageConfigurationAdmin(_SingleVisualConfigurationAdmin):
    fieldsets = (
        ("ABOUT · General / General", {
            "fields": (
                "header_background",
                "intro_image",
                "team_default_image",
                "video_background",
            ),
            "description": (
                "ES: Imágenes generales y respaldos de la parte superior de About. "
                "EN: General images and fallbacks for the upper part of About."
            ),
        }),
        ("ABOUT · Mission & Vision / Misión y visión", {
            "fields": (
                "mission_primary_image",
                "mission_secondary_image",
                "vision_background",
                "vision_image",
            ),
        }),
        ("ABOUT · Values, certifications & projects / Valores, certificaciones y proyectos", {
            "fields": (
                "value_default_image",
                "certification_default_image",
                "projects_background",
                "project_default_image",
            ),
        }),
        ("System / Sistema", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at"),
        }),
    )


@admin.register(ProfessionalPageConfiguration)
class ProfessionalPageConfigurationAdmin(_SingleVisualConfigurationAdmin):
    fieldsets = (
        ("PROFESSIONALS · Hero / Hero", {
            "fields": ("hero_default_image",),
            "description": (
                "ES: ProfessionalPage.hero_image mantiene prioridad. "
                "EN: ProfessionalPage.hero_image keeps priority."
            ),
        }),
        ("PROFESSIONALS · Needs / Necesidades", {
            "fields": (
                "need_coordination_image",
                "need_planning_image",
                "need_turnover_image",
                "need_maintenance_image",
                "need_occupancy_image",
            ),
        }),
        ("PROFESSIONALS · Turnover process / Proceso Remise en état", {
            "fields": (
                "turnover_background",
                "evaluation_image",
                "planning_image",
                "intervention_image",
                "control_image",
            ),
        }),
        ("PROFESSIONALS · Other fallbacks / Otros respaldos", {
            "fields": (
                "faq_image",
                "service_default_image",
                "project_default_image",
            ),
        }),
        ("System / Sistema", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at"),
        }),
    )
