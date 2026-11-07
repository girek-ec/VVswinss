from django.conf import settings
from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views
from about import views as about_views
from professionals import views as professional_views


app_name = "core"


urlpatterns = [
    path("", views.home, name="home"),

    # ============================================================
    # ENTREPRISE
    # ============================================================
    path(_("a-propos/"), about_views.about, name="about"),

    # ============================================================
    # PROFESSIONNELS
    # ============================================================
    path(_("professionnels/"), professional_views.professionals, name="professionals"),

    # ============================================================
    # INFORMATIONS LÉGALES
    # ============================================================
    path(_("mentions-legales/"), views.mentions_legales, name="mentions_legales"),
    path(_("protection-des-donnees/"), views.protection_donnees, name="protection_donnees"),
]


# ============================================================
# DESIGN SYSTEM · DÉVELOPPEMENT UNIQUEMENT
# ============================================================

if settings.DEBUG:
    urlpatterns += [
        path("design-system/", views.design_system, name="design_system"),
    ]