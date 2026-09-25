from django.shortcuts import get_object_or_404
from django.utils.translation import get_language


SUPPORTED_LANGUAGES = ("fr", "es", "en")


def current_language():
    language = (get_language() or "fr").split("-")[0]

    if language not in SUPPORTED_LANGUAGES:
        return "fr"

    return language


def get_by_localized_slug(model, slug, queryset=None):
    language = current_language()
    slug_field = f"slug_{language}"

    if queryset is None:
        queryset = model.objects.all()

    return get_object_or_404(
        queryset,
        **{slug_field: slug},
    )