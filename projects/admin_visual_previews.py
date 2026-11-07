# PROJECTS · ADMIN IMAGE PREVIEWS | VISTAS PREVIAS DE IMÁGENES
from django.apps import apps
from django.contrib import admin
from django.db.models import ImageField
from django.templatetags.static import static
from django.utils.html import format_html, format_html_join

ProjectPageConfiguration = apps.get_model("projects", "ProjectPageConfiguration")
_existing_admin = admin.site._registry.get(ProjectPageConfiguration)
_BaseAdmin = type(_existing_admin) if _existing_admin else admin.ModelAdmin
_image_fields = {
    field.name for field in ProjectPageConfiguration._meta.fields
    if isinstance(field, ImageField)
}

# DETECCIÓN DE CAMPOS EXISTENTES | EXISTING FIELD DETECTION
_header_field = next(
    (name for name in ("header_background", "page_header_background", "header_image")
     if name in _image_fields), None
)
_project_field = next(
    (name for name in ("default_image", "project_default_image", "project_fallback_image")
     if name in _image_fields), None
)
_fallbacks = {
    _header_field: "antra/assets/img/bg-img/page-header-bg.webp",
    _project_field: "antra/assets/img/project/VVS_placeholder_cuadrado.webp",
}
_fallbacks.pop(None, None)

class ProjectPageConfigurationImageAdmin(_BaseAdmin):
    # PREVISUALIZACIÓN | UPLOADED IMAGE AND STATIC DEFAULT
    @staticmethod
    def _card(url, label, description):
        return format_html(
            '<div style="display:inline-flex;flex-direction:column;gap:5px;max-width:245px">'
            '<a href="{}" target="_blank" rel="noopener noreferrer" title="{}">'
            '<img src="{}" alt="{}" loading="lazy" style="width:225px;height:145px;'
            'object-fit:cover;border:1px solid #cbd1d8;border-radius:6px;background:#f3f5f7">'
            '</a><strong style="font-size:12px">{}</strong>'
            '<span style="font-size:11px;color:#667085;overflow-wrap:anywhere">{}</span></div>',
            url, label, url, label, label, description,
        )

    def _preview(self, obj, field_name):
        path = _fallbacks.get(field_name)
        if not path:
            return "—"
        fallback = self._card(
            static(path), "Default from static", "static/" + path,
        )
        image = getattr(obj, field_name, None) if obj else None
        if not image:
            return fallback
        try:
            uploaded_url = image.url
        except (ValueError, OSError, AttributeError):
            return fallback
        return format_html(
            '<div style="display:flex;flex-wrap:wrap;align-items:flex-start;gap:16px">{}{}</div>',
            self._card(uploaded_url, "Uploaded image", image.name), fallback,
        )

    @admin.display(description="Header · Uploaded / Static")
    def project_header_preview(self, obj):
        return self._preview(obj, _header_field)

    @admin.display(description="Project fallback · Uploaded / Static")
    def project_default_preview(self, obj):
        return self._preview(obj, _project_field)

    @admin.display(description="Image previews")
    def project_images_list(self, obj):
        cards = []
        for field_name in (_header_field, _project_field):
            if field_name:
                cards.append(self._preview(obj, field_name))
        if not cards:
            return "—"
        return format_html(
            '<div style="display:flex;flex-wrap:wrap;gap:10px">{}</div>',
            format_html_join("", "{}", ((card,) for card in cards)),
        )

    def get_readonly_fields(self, request, obj=None):
        original = tuple(super().get_readonly_fields(request, obj))
        extra = []
        if _header_field:
            extra.append("project_header_preview")
        if _project_field:
            extra.append("project_default_preview")
        return tuple(dict.fromkeys((*original, *extra)))

    def get_fieldsets(self, request, obj=None):
        result = []
        mapping = {
            _header_field: "project_header_preview",
            _project_field: "project_default_preview",
        }
        mapping.pop(None, None)
        preview_names = set(mapping.values())
        for title, options in super().get_fieldsets(request, obj):
            new_options = dict(options)
            fields = []
            for entry in options.get("fields", ()):
                if isinstance(entry, str) and entry in preview_names:
                    continue
                fields.append(entry)
                entry_fields = entry if isinstance(entry, (tuple, list)) else (entry,)
                for name in entry_fields:
                    if name in mapping:
                        fields.append(mapping[name])
            new_options["fields"] = tuple(fields)
            result.append((title, new_options))
        return tuple(result)

    def get_list_display(self, request):
        original = tuple(super().get_list_display(request))
        if "project_images_list" not in original:
            return (*original, "project_images_list")
        return original

# MANTENER ADMIN ORIGINAL Y HEREDAR SUS FUNCIONES | PRESERVE EXISTING ADMIN
if _existing_admin:
    admin.site.unregister(ProjectPageConfiguration)
admin.site.register(ProjectPageConfiguration, ProjectPageConfigurationImageAdmin)
