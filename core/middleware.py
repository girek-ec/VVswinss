"""Middleware de caché para archivos MEDIA de V&V Swiss Services."""

from django.conf import settings


class MediaCacheControlMiddleware:
    """Añade Cache-Control a respuestas /media/ sin marcar MEDIA como immutable."""

    def __init__(self, get_response):
        self.get_response = get_response
        self.media_url = getattr(settings, "MEDIA_URL", "/media/")
        self.max_age = int(getattr(settings, "MEDIA_CACHE_MAX_AGE", 604800))
        self.stale_while_revalidate = int(
            getattr(settings, "MEDIA_CACHE_STALE_WHILE_REVALIDATE", 86400)
        )

    def __call__(self, request):
        response = self.get_response(request)

        if (
            self.media_url
            and request.path.startswith(self.media_url)
            and response.status_code in {200, 206, 304}
            and not response.has_header("Cache-Control")
        ):
            response["Cache-Control"] = (
                f"public, max-age={self.max_age}, "
                f"stale-while-revalidate={self.stale_while_revalidate}"
            )

        return response
