from django.contrib import admin
from django.db import models
from .visual_config import BlogPageConfiguration

# IMÁGENES DE SECCIONES DE ACTUALIDAD | BLOG-ONLY PAGE IMAGES
@admin.register(BlogPageConfiguration)
class BlogPageConfigurationAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")

    def get_fields(self, request, obj=None):
        return tuple(
            field.name for field in self.model._meta.fields
            if isinstance(field, models.ImageField) and field.editable
        ) + ("created_at", "updated_at")

    def has_add_permission(self, request):
        return not self.model.objects.exists() and super().has_add_permission(request)
