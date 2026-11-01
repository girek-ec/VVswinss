from django.contrib import admin
from django.templatetags.static import static
from django.utils.html import format_html

from .visual_config import BlogPageConfiguration


BLOG_STATIC_FALLBACK = "antra/assets/img/images/VVS_placeholder_horizontal.webp"
HEADER_STATIC_FALLBACK = "antra/assets/img/bg-img/page-header-bg.webp"


def image_url_if_exists(image):
    if not image:
        return None
    try:
        if image.storage.exists(image.name):
            return image.url
    except (AttributeError, OSError, ValueError):
        return None
    return None


def preview_card(url, label, width=500, height=240):
    return format_html(
        '<div style="max-width:{}px;">'
        '<img src="{}" style="width:100%;height:{}px;object-fit:cover;border-radius:8px;display:block;" />'
        '<div style="margin-top:7px;color:#666;font-size:12px;">{}</div>'
        '</div>',
        width,
        url,
        height,
        label,
    )


@admin.register(BlogPageConfiguration)
class BlogPageConfigurationAdmin(admin.ModelAdmin):
    readonly_fields = (
        "header_background_preview",
        "post_default_image_preview",
        "post_default_social_image",
        "post_default_social_image_preview",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Encabezado del Blog",
            {
                "fields": (
                    "header_background",
                    "header_background_preview",
                ),
            },
        ),
        (
            "Imagen por defecto · publicaciones",
            {
                "description": (
                    "Se utiliza automáticamente cuando un artículo no tiene imagen propia. "
                    "Si se deja vacía, el sitio utiliza el placeholder estático del Blog."
                ),
                "fields": (
                    "post_default_image",
                    "post_default_image_preview",
                ),
            },
        ),
        (
            "SEO social · Open Graph / X",
            {
                "description": (
                    "La imagen social se genera automáticamente en JPEG 1200 × 630 "
                    "desde la imagen por defecto de publicaciones."
                ),
                "fields": (
                    "post_default_social_image",
                    "post_default_social_image_preview",
                ),
            },
        ),
        (
            "Sistema",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    def has_add_permission(self, request):
        if BlogPageConfiguration.objects.exists():
            return False
        return super().has_add_permission(request)

    @admin.display(description="Vista previa · encabezado")
    def header_background_preview(self, obj):
        url = image_url_if_exists(obj.header_background) if obj else None
        if url:
            return preview_card(url, "Imagen configurada")
        return preview_card(static(HEADER_STATIC_FALLBACK), "Fallback estático")

    @admin.display(description="Vista previa · imagen por defecto")
    def post_default_image_preview(self, obj):
        url = image_url_if_exists(obj.post_default_image) if obj else None
        if url:
            return preview_card(url, "Imagen por defecto configurada")
        return preview_card(static(BLOG_STATIC_FALLBACK), "Fallback estático")

    @admin.display(description="Vista previa · imagen social 1200 × 630")
    def post_default_social_image_preview(self, obj):
        url = image_url_if_exists(obj.post_default_social_image) if obj else None
        if url:
            return preview_card(url, "JPEG social automático · 1200 × 630", 500, 263)

        normal_url = image_url_if_exists(obj.post_default_image) if obj else None
        if normal_url:
            return preview_card(
                normal_url,
                "Pendiente de regeneración · guarde nuevamente esta configuración",
                500,
                263,
            )

        return preview_card(
            static(BLOG_STATIC_FALLBACK),
            "Fallback estático · ejecute repair_blog_images para crear el social automático",
            500,
            263,
        )
