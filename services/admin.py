from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Service,
    ServiceBenefit,
    ServiceCategory,
    ServiceImage,
)


class ServiceBenefitInline(admin.TabularInline):
    model = ServiceBenefit
    extra = 0
    fields = (
        "titulo_fr",
        "titulo_es",
        "titulo_en",
        "orden",
    )


class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 0
    fields = (
        "imagen",
        "alt_fr",
        "alt_es",
        "alt_en",
        "orden",
    )


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "nombre_fr",
        "orden",
        "activo",
    )

    list_editable = (
        "orden",
        "activo",
    )

    list_filter = ("activo",)

    search_fields = (
        "nombre_fr",
        "nombre_es",
        "nombre_en",
    )

    ordering = ("orden",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "nombre_fr",
        "categoria",
        "imagen_preview",
        "destacado",
        "orden",
        "activo",
    )

    list_filter = (
        "categoria",
        "destacado",
        "activo",
        "indexar",
    )

    list_editable = (
        "destacado",
        "orden",
        "activo",
    )

    search_fields = (
        "nombre_fr",
        "nombre_es",
        "nombre_en",
        "resumen_fr",
        "contenido_fr",
    )

    readonly_fields = (
        "imagen_preview",
        "created_at",
        "updated_at",
    )

    inlines = [
        ServiceBenefitInline,
        ServiceImageInline,
    ]

    fieldsets = (
        (
            "Categoría",
            {
                "fields": (
                    "categoria",
                    "icono",
                )
            },
        ),
        (
            "Francés",
            {
                "fields": (
                    "nombre_fr",
                    "slug_fr",
                    "resumen_fr",
                    "contenido_fr",
                )
            },
        ),
        (
            "Español",
            {
                "fields": (
                    "nombre_es",
                    "slug_es",
                    "resumen_es",
                    "contenido_es",
                )
            },
        ),
        (
            "English",
            {
                "fields": (
                    "nombre_en",
                    "slug_en",
                    "resumen_en",
                    "contenido_en",
                )
            },
        ),
        (
            "Imagen",
            {
                "fields": (
                    "imagen_principal",
                    "imagen_preview",
                )
            },
        ),
        (
            "SEO",
            {
                "fields": (
                    "seo_titulo_fr",
                    "seo_titulo_es",
                    "seo_titulo_en",
                    "meta_descripcion_fr",
                    "meta_descripcion_es",
                    "meta_descripcion_en",
                    "og_imagen",
                    "indexar",
                )
            },
        ),
        (
            "Publicación",
            {
                "fields": (
                    "destacado",
                    "orden",
                    "activo",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    @admin.display(description="Imagen")
    def imagen_preview(self, obj):
        if obj.imagen_principal:
            return format_html(
                '<img src="{}" style="height:55px; width:80px; object-fit:cover;" />',
                obj.imagen_principal.url,
            )

        return "—"