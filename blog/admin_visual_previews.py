# BLOG · ADMIN IMAGE PREVIEWS | VISTAS PREVIAS DEL ADMIN
# Preserva el administrador original y su configuración | Preserve existing ModelAdmin behaviour.
from django.contrib import admin
from django.db.models import ImageField
from django.templatetags.static import static
from django.utils.html import format_html, format_html_join
from .visual_config import BlogPageConfiguration
from . import visual_config_admin  # noqa: F401 · Register original admin first

# ROUTES · ORIGINAL STATIC FALLBACKS | RESPALDOS STATIC ORIGINALES
BLOG_IMAGE_FALLBACKS = {
    "header_background": "antra/assets/img/bg-img/page-header-bg.webp",
    "post_default_image": "antra/assets/img/images/VVS_placeholder_horizontal.webp",
}
_available_fields = {
    field.name for field in BlogPageConfiguration._meta.fields
    if isinstance(field, ImageField)
}
_image_fields = {
    name: path for name, path in BLOG_IMAGE_FALLBACKS.items()
    if name in _available_fields
}
_existing_admin = admin.site._registry.get(BlogPageConfiguration)
if _existing_admin is None:
    raise RuntimeError("BlogPageConfiguration must be registered in blog.visual_config_admin first.")

class BlogPageConfigurationPreviewAdmin(type(_existing_admin)):
    # THUMBNAIL CARD | MINIATURA CLICABLE
    @staticmethod
    def _card(url, title, source, path):
        return format_html(
            '<div style="display:inline-flex;flex-direction:column;gap:5px;max-width:230px">'
            '<a href="{}" target="_blank" rel="noopener noreferrer" title="{}">'
            '<img src="{}" alt="{}" loading="lazy" '
            'style="width:220px;height:135px;object-fit:cover;display:block;'
            'border:1px solid #cbd5e1;border-radius:7px;background:#f3f4f6"></a>'
            '<strong style="font-size:12px">{}</strong>'
            '<small style="font-size:11px;color:#667085;overflow-wrap:anywhere">{}</small>'
            '</div>', url, source, url, title, source, path,
        )

    # FILE URL | URL DE ARCHIVO SUBIDO
    @staticmethod
    def _image_url(obj, field_name):
        image = getattr(obj, field_name, None) if obj else None
        if not image:
            return None
        try:
            return image.url
        except (OSError, ValueError, AttributeError):
            return None

    # UPLOADED + STATIC | IMAGEN CARGADA MÁS RESPALDO
    def _preview(self, obj, field_name):
        path = _image_fields.get(field_name)
        if path is None:
            return "—"
        url = self._image_url(obj, field_name)
        default_card = self._card(
            static(path), field_name.replace("_", " ").title(),
            "STATIC · Default image" if url else "Currently displayed · STATIC default",
            "static/" + path,
        )
        if not url:
            return default_card
        image = getattr(obj, field_name)
        return format_html(
            '<div style="display:flex;gap:16px;flex-wrap:wrap">{}{}</div>',
            self._card(url, field_name, "Currently displayed · Uploaded image", image.name),
            default_card,
        )

    @admin.display(description="Header · Uploaded / Static")
    def blog_header_preview(self, obj):
        return self._preview(obj, "header_background")

    @admin.display(description="Post fallback · Uploaded / Static")
    def blog_default_image_preview(self, obj):
        return self._preview(obj, "post_default_image")

    @admin.display(description="Images")
    def blog_image_thumbnails(self, obj):
        rows = []
        for name, path in _image_fields.items():
            uploaded = self._image_url(obj, name)
            rows.append((uploaded or static(path), name.replace("_", " "),
                         "Uploaded" if uploaded else "STATIC default"))
        return format_html_join(
            " ",
            '<a href="{}" target="_blank" rel="noopener noreferrer" title="{} · {}">'
            '<img src="{}" alt="{}" loading="lazy" '
            'style="width:85px;height:58px;object-fit:cover;border:1px solid #ddd;'
            'border-radius:5px"></a>',
            ((url, label, source, url, label) for url, label, source in rows),
        ) if rows else "—"

    # RETAIN EXISTING READONLY FIELDS | CONSERVAR CAMPOS SOLO LECTURA
    def get_readonly_fields(self, request, obj=None):
        original = tuple(super().get_readonly_fields(request, obj))
        additions = []
        if "header_background" in _image_fields:
            additions.append("blog_header_preview")
        if "post_default_image" in _image_fields:
            additions.append("blog_default_image_preview")
        return tuple(dict.fromkeys((*original, *additions)))

    # INSERT PREVIEWS NEXT TO UPLOAD FIELDS | MINIATURAS DEBAJO DE CADA CAMPO
    def get_fieldsets(self, request, obj=None):
        mapping = {
            "header_background": "blog_header_preview",
            "post_default_image": "blog_default_image_preview",
        }
        original = super().get_fieldsets(request, obj)
        result = []
        found = set()
        preview_names = set(mapping.values())
        for title, options in original:
            fields = []
            for entry in options.get("fields", ()):
                names = entry if isinstance(entry, (tuple, list)) else (entry,)
                # Avoid duplicated previews if default ModelAdmin already included them.
                if len(names) == 1 and names[0] in preview_names:
                    continue
                fields.append(entry)
                for name in names:
                    if name in mapping and name in _image_fields:
                        found.add(name)
                        fields.append(mapping[name])
            new_options = dict(options)
            new_options["fields"] = tuple(fields)
            result.append((title, new_options))
        # In case the original admin hid a field, add the supported upload controls.
        missing = [name for name in _image_fields if name not in found]
        if missing:
            result.append(("BLOG · Images / Imágenes", {
                "fields": tuple(item for name in missing for item in (name, mapping[name])),
            }))
        return tuple(result)

    # PRESERVE EXISTING CHANGE LIST | CONSERVAR LISTADO ACTUAL
    def get_list_display(self, request):
        existing = tuple(super().get_list_display(request))
        return existing if "blog_image_thumbnails" in existing else (*existing, "blog_image_thumbnails")

# ONE REGISTRATION ONLY | UN SOLO REGISTRO, DESPUÉS DEL ADMIN ORIGINAL
admin.site.unregister(BlogPageConfiguration)
admin.site.register(BlogPageConfiguration, BlogPageConfigurationPreviewAdmin)
