from django.contrib import admin

from .visual_config import ContactPageConfiguration


@admin.register(ContactPageConfiguration)
class ContactPageConfigurationAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("CONTACT · Images / Imágenes", {
            "fields": ("header_background", "main_image"),
            "description": (
                "ES: Si no se sube una imagen, se conserva el static actual. "
                "EN: If no image is uploaded, the current static fallback remains."
            ),
        }),
        ("System / Sistema", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at"),
        }),
    )

    def has_add_permission(self, request):
        if ContactPageConfiguration.objects.exists():
            return False
        return super().has_add_permission(request)
