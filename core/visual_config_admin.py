from django.contrib import admin
from .visual_config import AboutPageConfiguration

# IMÁGENES DE SECCIONES DE ABOUT | ABOUT PAGE SECTION IMAGES
@admin.register(AboutPageConfiguration)
class AboutPageConfigurationAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("ABOUT · Encabezado", {"fields": ("header_background",)}),
        ("ABOUT · Misión", {"fields": ("mission_primary_image", "mission_secondary_image")}),
        ("ABOUT · Visión", {"fields": ("vision_background", "vision_image")}),
        ("ABOUT · Realizaciones", {"fields": ("projects_background",)}),
        ("Sistema", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )

    def has_add_permission(self, request):
        return not self.model.objects.exists() and super().has_add_permission(request)
