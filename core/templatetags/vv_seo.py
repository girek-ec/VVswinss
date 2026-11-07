"""Etiquetas SEO multilingüe para V&V Swiss Services.
Genera URL alternas válidas sin modificar datos ni el selector de idioma.
"""
from django import template
from django.apps import apps
from django.db.models import Q
from django.urls import NoReverseMatch, resolve, reverse
from django.utils import translation
from django.utils.html import format_html_join

register = template.Library()
LANGUAGES = ("fr", "de", "it", "en")
PUBLIC_APPS = {"core", "professionals", "services", "projects", "blog", "contact"}
EXCLUDED_NAMES = (
    "admin", "inbox", "login", "logout", "success", "design_system",
    "api", "submit", "download", "preview", "webhook", "unsubscribe",
)
DETAIL_MODELS = {
    "services:detail": ("services", "Service"),
    "services:category_detail": ("services", "ServiceCategory"),
    "projects:detail": ("projects", "Project"),
    "blog:detail": ("blog", "Post"),
    "blog:post_detail": ("blog", "Post"),
}


def _get_detail_record(view_name, match):
    """Localiza un registro por el slug de cualquiera de sus idiomas."""
    app_label, model_name = DETAIL_MODELS[view_name]
    model = apps.get_model(app_label, model_name)
    fields = {field.name for field in model._meta.fields}
    slug = next(
        (value for key, value in match.kwargs.items() if "slug" in key and isinstance(value, str)),
        None,
    )
    if slug is None and len(match.args) == 1:
        slug = match.args[0]
    if not slug:
        return None, fields
    current_lang = (translation.get_language() or "fr").split("-")[0]
    preferred = [f"slug_{current_lang}", *(f"slug_{lang}" for lang in LANGUAGES if lang != current_lang), "slug"]
    for field in preferred:
        if field not in fields:
            continue
        record = model._default_manager.filter(**{field: slug}).first()
        if record:
            if "is_active" in fields and not record.is_active:
                return None, fields
            if "is_published" in fields and not record.is_published:
                return None, fields
            if "is_indexable" in fields and not record.is_indexable:
                return None, fields
            return record, fields
    return None, fields


def _translated_detail_paths(view_name, record, fields):
    """Usa los slugs auténticos del registro y omite idiomas sin slug."""
    paths = []
    for lang in LANGUAGES:
        field = f"slug_{lang}"
        slug = getattr(record, field, None) if field in fields else getattr(record, "slug", None)
        if not slug:
            continue
        try:
            with translation.override(lang):
                paths.append((lang, reverse(view_name, args=[slug])))
        except NoReverseMatch:
            continue
    return paths


def _translated_static_paths(view_name):
    """Resuelve la traducción real de cada ruta Django sin alterar su slug."""
    paths = []
    for lang in LANGUAGES:
        try:
            with translation.override(lang):
                paths.append((lang, reverse(view_name)))
        except NoReverseMatch:
            continue
    return paths


@register.simple_tag
def vv_hreflang(request):
    """Enlaza solo URL públicas equivalentes y evita indexar rutas privadas."""
    if request is None:
        return ""
    match = getattr(request, "resolver_match", None)
    if match is None:
        try:
            match = resolve(request.path_info)
        except Exception:
            return ""
    view_name = getattr(match, "view_name", "") or ""
    if not view_name or view_name.split(":", 1)[0] not in PUBLIC_APPS:
        return ""
    if any(token in view_name.lower() for token in EXCLUDED_NAMES):
        return ""
    if view_name in DETAIL_MODELS:
        record, fields = _get_detail_record(view_name, match)
        if record is None:
            return ""
        paths = _translated_detail_paths(view_name, record, fields)
    else:
        # Una ruta pública con argumentos desconocidos podría apuntar al
        # contenido equivocado en otro idioma. Es preferible no anunciarla.
        if match.args or match.kwargs:
            return ""
        paths = _translated_static_paths(view_name)
    if len(paths) < 2:
        return ""
    return format_html_join(
        "\n    ",
        '<link rel="alternate" hreflang="{}" href="{}">',
        ((lang, request.build_absolute_uri(path)) for lang, path in paths),
    )
