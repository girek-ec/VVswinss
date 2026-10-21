from django.http import Http404
from django.utils.translation import get_language


# ============================================================
# LANGUAGES
# ============================================================

SUPPORTED_LANGUAGES = (
    "fr",
    "de",
    "it",
    "en",
)

DEFAULT_LANGUAGE = "fr"


# ============================================================
# CURRENT LANGUAGE
# ============================================================

def current_language():
    language = (get_language() or DEFAULT_LANGUAGE).lower().replace("_", "-").split("-")[0]

    if language not in SUPPORTED_LANGUAGES:
        return DEFAULT_LANGUAGE

    return language


# ============================================================
# LOCALIZED VALUE
# ============================================================

def get_localized_value(obj, field_name, language=None):
    if obj is None:
        return ""

    language = language or current_language()

    languages = [
        language,
        "fr",
        "de",
        "it",
        "en",
    ]

    checked = set()

    for lang in languages:
        if lang in checked:
            continue

        checked.add(lang)

        value = getattr(obj, f"{field_name}_{lang}", None)

        if value:
            return value

    return ""


# ============================================================
# LOCALIZED SLUG
# ============================================================

def get_by_localized_slug(model, slug, queryset=None):
    language = current_language()

    if queryset is None:
        queryset = model.objects.all()

    # ========================================================
    # CURRENT LANGUAGE
    # ========================================================

    obj = queryset.filter(**{f"slug_{language}": slug}).first()

    if obj is not None:
        return obj

    # ========================================================
    # FALLBACK TO OTHER LANGUAGES
    # ========================================================

    for fallback_language in SUPPORTED_LANGUAGES:
        if fallback_language == language:
            continue

        obj = queryset.filter(**{f"slug_{fallback_language}": slug}).first()

        if obj is not None:
            return obj

    raise Http404(f"{model.__name__} introuvable.")