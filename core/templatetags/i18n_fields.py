from django import template
from django.utils.translation import get_language

register = template.Library()


@register.filter
def localized(obj, field_name):
    """
    Devuelve automáticamente el campo correspondiente
    al idioma activo.

    Ejemplo:
        {{ servicio|localized:"nombre" }}

    Buscará:
        nombre_fr
        nombre_es
        nombre_en
    """
    if obj is None:
        return ""

    language = (get_language() or "fr").split("-")[0]

    languages = [language, "fr", "es", "en"]

    for lang in languages:
        value = getattr(obj, f"{field_name}_{lang}", None)

        if value:
            return value

    return ""