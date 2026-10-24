from django import template
from django.urls import translate_url

register = template.Library()


@register.simple_tag(takes_context=True)
def switch_language_url(context, language_code):
    """Return the current URL translated to the requested public language."""
    request = context.get("request")

    if request is None:
        return "/"

    current_url = request.get_full_path()
    return translate_url(current_url, language_code)
