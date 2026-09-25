from django.contrib import admin
from django.utils.html import format_html

from .models import (
    BeforeAfter,
    BuildingType,
    Intervention,
    Project,
    ProjectImage,
    ProjectType,
)


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 0


class BeforeAfterInline(admin.TabularInline):
    model = BeforeAfter
    extra = 0


class InterventionInline(admin.StackedInline):
    model = Intervention
    extra = 0


@admin.register(ProjectType)
class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = (
        "nombre_fr",
        "orden",
        "activo",
    )

    list_editable = (
        "orden",
        "activo",
    )

    search_fields = (
        "nombre_fr",
        "nombre_es",
        "nombre_en",
    )


@admin.register(BuildingType)
class BuildingTypeAdmin(admin.ModelAdmin):
    list_display = (
        "nombre_fr",
        "orden",
        "activo",
    )

    list_editable = (
        "orden",
        "activo",
    )

    search_fields = (
        "nombre_fr",
        "nombre_es",
        "nombre_en",
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "titulo_fr",
        "ubicacion",
        "tipo",
        "imagen_preview",
        "fecha_fin",
        "destacado",
        "publicado",
    )

    list_filter = (
        "tipo",
        "tipo_edificio",
        "destacado",
        "publicado",
        "indexar",
    )

    search_fields = (
        "titulo_fr",
        "titulo_es",
        "titulo_en",
        "ubicacion",
        "cliente",
        "contenido_fr",
    )

    filter_horizontal = ("servicios",)

    readonly_fields = (
        "imagen_preview",
        "created_at",
        "updated_at",
    )

    inlines = [
        ProjectImageInline,
        BeforeAfterInline,
        InterventionInline,
    ]

    @admin.display(description="Imagen")
    def imagen_preview(self, obj):
        if obj.imagen_principal:
            return format_html(
                '<img src="{}" style="height:55px; width:80px; object-fit:cover;" />',
                obj.imagen_principal.url,
            )

        return "—"


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = (
        "proyecto",
        "orden",
    )

    list_filter = ("proyecto",)


@admin.register(BeforeAfter)
class BeforeAfterAdmin(admin.ModelAdmin):
    list_display = (
        "proyecto",
        "titulo_fr",
        "orden",
    )

    list_filter = ("proyecto",)


@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    list_display = (
        "titulo_fr",
        "proyecto",
        "orden",
    )

    list_filter = ("proyecto",)

    search_fields = (
        "titulo_fr",
        "titulo_es",
        "titulo_en",
    )