from django.contrib import admin

from .visual_config import ProjectPageConfiguration


@admin.register(ProjectPageConfiguration)
class ProjectPageConfigurationAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("PROJECTS · Images / Imágenes", {
            "fields": ("header_background", "default_image"),
            "description": (
                "ES: Si un campo está vacío, la web vuelve al archivo static original. "
                "EN: If a field is empty, the website falls back to the original static file."
            ),
        }),
        ("System / Sistema", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at"),
        }),
    )

    def has_add_permission(self, request):
        if ProjectPageConfiguration.objects.exists():
            return False
        return super().has_add_permission(request)
