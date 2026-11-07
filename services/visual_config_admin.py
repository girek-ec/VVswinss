
# SERVICES · VISUAL ADMIN | ADMINISTRACIÓN VISUAL Y RESPALDOS
from django.contrib import admin
from django.templatetags.static import static
from django.utils.html import format_html, format_html_join
from .visual_config import (
    SERVICE_STATIC_FALLBACKS,
    ServicePageVisualConfiguration,
    resolved_service_image_url,
    uploaded_service_image_url,
)

@admin.register(ServicePageVisualConfiguration)
class ServicePageVisualConfigurationAdmin(admin.ModelAdmin):
    list_display = ("__str__", "image_thumbnails")

    # CATEGORY FALLBACK FIXED IN STATIC | RESPALDO DE CATEGORÍAS FIJO EN STATIC
    fields = (
        "category_static_preview",
        "cta_background", "cta_background_preview",
        "work_method_image", "work_method_image_preview",
        "social_default_image", "social_default_image_preview",
    )

    readonly_fields = (
        "category_static_preview",
        "cta_background_preview",
        "work_method_image_preview",
        "social_default_image_preview",
    )

    class Media:
        js = ("services/admin/service_visual_previews.js",)

    def has_add_permission(self, request):
        return super().has_add_permission(request) and not ServicePageVisualConfiguration.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    # IMAGE PREVIEW CARD | TARJETA DE VISTA PREVIA
    @staticmethod
    def _card(url, label, source, path=None):
        path_html = format_html(
            '<span style="font-size:11px;color:#777;overflow-wrap:anywhere">{}</span>',
            path,
        ) if path else ""
        return format_html(
            '<div style="display:inline-flex;flex-direction:column;gap:5px;max-width:240px">'
            '<a href="{}" target="_blank" rel="noopener noreferrer" title="{}">'
            '<img src="{}" alt="{}" loading="lazy" '
            'style="display:block;width:220px;height:135px;object-fit:cover;'
            'border:1px solid #ced4db;border-radius:6px;background:#f5f7fa"></a>'
            '<strong style="font-size:12px">{}</strong>{}</div>',
            url, source, url, label, source, path_html,
        )

    # CATEGORY · ALWAYS STATIC | CATEGORÍA · SIEMPRE STATIC
    @admin.display(description="Category default image · Static only")
    def category_static_preview(self, obj):
        path = SERVICE_STATIC_FALLBACKS["category_default_image"]
        return self._card(
            static(path),
            "Category default image",
            "Always used when a category has no image · STATIC",
            "static/" + path,
        )

    # CONFIGURABLE IMAGE PREVIEWS | VISTAS PREVIAS ADMINISTRABLES
    def _preview(self, obj, field_name):
        image_url = uploaded_service_image_url(obj, field_name)
        fallback_path = SERVICE_STATIC_FALLBACKS[field_name]

        static_card = self._card(
            static(fallback_path),
            field_name,
            "Static default" if image_url else "Currently displayed · Static default",
            "static/" + fallback_path,
        )

        if not image_url:
            cards = static_card
        else:
            uploaded = getattr(obj, field_name)
            cards = format_html(
                "{}{}",
                self._card(
                    image_url,
                    field_name,
                    "Currently displayed · Uploaded",
                    uploaded.name,
                ),
                static_card,
            )

        return format_html(
            '<div id="vv-services-preview-{}" '
            'style="display:flex;flex-wrap:wrap;gap:15px;align-items:flex-start">{}</div>',
            field_name,
            cards,
        )

    # QUOTE REQUEST BACKGROUND | FONDO DE PRESUPUESTO
    @admin.display(description="Image preview · Uploaded / Static")
    def cta_background_preview(self, obj):
        return self._preview(obj, "cta_background")

    # WORK METHOD IMAGE | IMAGEN DE METODOLOGÍA
    @admin.display(description="Image preview · Uploaded / Static")
    def work_method_image_preview(self, obj):
        return self._preview(obj, "work_method_image")

    # SOCIAL SHARING IMAGE | IMAGEN SOCIAL
    @admin.display(description="Image preview · Uploaded / Static")
    def social_default_image_preview(self, obj):
        return self._preview(obj, "social_default_image")

    # IMAGE THUMBNAILS | MINIATURAS DEL LISTADO
    @admin.display(description="Image thumbnails")
    def image_thumbnails(self, obj):
        entries = []

        for name in SERVICE_STATIC_FALLBACKS:
            if name == "category_default_image":
                url = static(SERVICE_STATIC_FALLBACKS[name])
                source = "Static · Fixed"
            else:
                url = resolved_service_image_url(obj, name)
                source = (
                    "Uploaded"
                    if uploaded_service_image_url(obj, name)
                    else "Static default"
                )

            entries.append((url, name.replace("_", " "), source))

        return format_html_join(
            " ",
            '<a href="{}" target="_blank" rel="noopener noreferrer" title="{} · {}">'
            '<img src="{}" alt="{}" loading="lazy" '
            'style="width:85px;height:56px;object-fit:cover;'
            'border-radius:5px;border:1px solid #ddd"></a>',
            (
                (url, label, source, url, label)
                for url, label, source in entries
            ),
        )

# CATEGORY · FIXED STATIC FALLBACK | RESPALDO FIJO DE CATEGORÍA
def current_category_fallback_url():
    return static(SERVICE_STATIC_FALLBACKS["category_default_image"])

# SOCIAL · CONFIGURABLE FALLBACK | RESPALDO SOCIAL ADMINISTRABLE
def current_social_fallback_url():
    config = ServicePageVisualConfiguration.objects.order_by("pk").first()
    return resolved_service_image_url(config, "social_default_image")
