# CONTACT · VISUAL CONFIGURATION ADMIN | ADMINISTRACIÓN DE IMÁGENES
from django.contrib import admin
from django.templatetags.static import static
from django.utils.html import format_html, format_html_join

from .visual_config import ContactPageConfiguration

# CONTACT · ORIGINAL STATIC FALLBACKS | RESPALDOS DEL HTML ORIGINAL
CONTACT_STATIC_FALLBACKS = {
    "header_background": "antra/assets/img/bg-img/page-header-bg.webp",
    "main_image": "antra/assets/img/images/contact-img-1.png",
}


@admin.register(ContactPageConfiguration)
class ContactPageConfigurationAdmin(admin.ModelAdmin):
    list_display = ("__str__", "image_thumbnails", "updated_at")
    readonly_fields = (
        "header_background_preview",
        "main_image_preview",
        "created_at",
        "updated_at",
    )
    fieldsets = (
        ("CONTACT · Header / Encabezado", {
            "description": (
                "ES: Sube una imagen para reemplazar el encabezado; siempre puedes "
                "consultar el respaldo original de static. "
                "EN: Upload an image to replace the header; the original static "
                "fallback is always visible."
            ),
            "fields": ("header_background", "header_background_preview"),
        }),
        ("CONTACT · Main image / Imagen principal", {
            "description": (
                "ES: Imagen principal de la sección de contacto. Cuando no hay una "
                "imagen subida, se utiliza el archivo original de static. "
                "EN: Contact section image. When no image is uploaded, "
                "the original static file is used."
            ),
            "fields": ("main_image", "main_image_preview"),
        }),
        ("System / Sistema", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at"),
        }),
    )

    class Media:
        js = ("contact/admin/contact_visual_previews.js",)

    def has_add_permission(self, request):
        if ContactPageConfiguration.objects.exists():
            return False
        return super().has_add_permission(request)

    # CONTACT · UPLOADED URL | URL DE IMAGEN GUARDADA
    @staticmethod
    def _uploaded_url(obj, field_name):
        image = getattr(obj, field_name, None) if obj else None
        if not image:
            return None
        try:
            return image.url
        except (ValueError, OSError, AttributeError):
            return None

    # CONTACT · PREVIEW CARD | TARJETA DE VISTA PREVIA
    @staticmethod
    def _card(url, label, source, path):
        return format_html(
            '<div style="display:inline-flex;flex-direction:column;gap:5px;max-width:235px">'
            '<a href="{}" target="_blank" rel="noopener noreferrer" title="{}">'
            '<img src="{}" alt="{}" loading="lazy" '
            'style="display:block;width:220px;height:140px;object-fit:cover;'
            'border:1px solid #cbd5e1;border-radius:7px;background:#f3f4f6"></a>'
            '<strong style="font-size:12px">{}</strong>'
            '<span style="font-size:11px;color:#667085">{}</span>'
            '<span style="font-size:11px;color:#667085;overflow-wrap:anywhere">{}</span>'
            '</div>',
            url, label, url, label, label, source, path,
        )

    # CONTACT · IMAGE AND STATIC PREVIEW | IMAGEN CARGADA Y RESPALDO
    def _preview(self, obj, field_name):
        static_path = CONTACT_STATIC_FALLBACKS[field_name]
        uploaded_url = self._uploaded_url(obj, field_name)
        fallback_card = self._card(
            static(static_path),
            "Default from static",
            "Static fallback" if uploaded_url else "Currently displayed · Static fallback",
            "static/" + static_path,
        )
        if uploaded_url:
            uploaded_field = getattr(obj, field_name)
            cards = format_html(
                "{}{}",
                self._card(
                    uploaded_url, "Uploaded image", "Currently displayed · Uploaded",
                    uploaded_field.name,
                ),
                fallback_card,
            )
        else:
            cards = fallback_card
        return format_html(
            '<div id="vv-contact-preview-{}" '
            'style="display:flex;flex-wrap:wrap;gap:16px;align-items:flex-start">{}</div>',
            field_name, cards,
        )

    @admin.display(description="Header · Uploaded / Static")
    def header_background_preview(self, obj):
        return self._preview(obj, "header_background")

    @admin.display(description="Main image · Uploaded / Static")
    def main_image_preview(self, obj):
        return self._preview(obj, "main_image")

    # CONTACT · CHANGE LIST THUMBNAILS | MINIATURAS DEL LISTADO
    @admin.display(description="Image thumbnails")
    def image_thumbnails(self, obj):
        items = []
        for field_name, path in CONTACT_STATIC_FALLBACKS.items():
            uploaded_url = self._uploaded_url(obj, field_name)
            items.append((
                uploaded_url or static(path),
                "Header" if field_name == "header_background" else "Main image",
                "Uploaded image" if uploaded_url else "Static fallback",
            ))
        return format_html_join(
            " ",
            '<a href="{}" target="_blank" rel="noopener noreferrer" title="{} · {}">'
            '<img src="{}" alt="{}" loading="lazy" '
            'style="width:85px;height:58px;object-fit:cover;'
            'border:1px solid #cbd5e1;border-radius:5px"></a>',
            ((url, label, source, url, label) for url, label, source in items),
        )
