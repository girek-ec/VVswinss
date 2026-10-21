from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve


urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),

    # ========================================================
    # MEDIA
    #
    # Permite servir archivos cargados por Django Admin
    # también cuando DEBUG=False.
    # Se mantiene el mismo patrón actualmente utilizado
    # por Redplus en este servidor.
    # ========================================================
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
]


urlpatterns += i18n_patterns(
    path("", include("core.urls")),
    path("services/", include("services.urls")),
    path("projects/", include("projects.urls")),
    path("blog/", include("blog.urls")),
    path("contact/", include("contact.urls")),
    prefix_default_language=True,
)
