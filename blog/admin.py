from django.contrib import admin
from django.utils.html import format_html

from .models import BlogCategory, Post


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "nombre_fr",
        "slug_fr",
        "activo",
    )

    list_editable = ("activo",)

    search_fields = (
        "nombre_fr",
        "nombre_es",
        "nombre_en",
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "titulo_fr",
        "categoria",
        "autor",
        "imagen_preview",
        "fecha_publicacion",
        "destacado",
        "publicado",
    )

    list_filter = (
        "categoria",
        "destacado",
        "publicado",
        "indexar",
        "fecha_publicacion",
    )

    search_fields = (
        "titulo_fr",
        "titulo_es",
        "titulo_en",
        "extracto_fr",
        "contenido_fr",
    )

    date_hierarchy = "fecha_publicacion"

    readonly_fields = (
        "imagen_preview",
        "created_at",
        "updated_at",
    )

    @admin.display(description="Imagen")
    def imagen_preview(self, obj):
        if obj.imagen_principal:
            return format_html(
                '<img src="{}" style="height:55px; width:80px; object-fit:cover;" />',
                obj.imagen_principal.url,
            )

        return "—"