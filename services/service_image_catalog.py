# CATÁLOGO VISUAL DE 37 SERVICIOS | 37-SERVICE VISUAL CATALOGUE
# Imágenes demo editables en Django Admin. Las fotografías reales tienen prioridad.
from django.templatetags.static import static

SERVICE_IMAGE_DIRECTORY = "antra/assets/img/service/catalogue_37"
SERVICE_GENERIC_IMAGE = "antra/assets/img/service/VVS_service.webp"
SERVICE_SLUGS = frozenset({
    'renovation-complete-appartements',
    'renovation-complete-maisons',
    'renovation-interieure',
    'renovation-exterieure',
    'remise-a-neuf-logements',
    'travaux-maconnerie-generale',
    'construction-cloisons-maconnees',
    'reparation-murs-maconneries',
    'enduits-crepis',
    'renovation-facades-maconnees',
    'transformation-gros-oeuvre',
    'isolation-thermique-exterieure-ite',
    'crepis-isolants-facades',
    'isolation-combles-perdus',
    'isolation-combles-amenages',
    'isolation-sous-sols-caves',
    'isolation-thermique-toitures',
    'cloisons-plaques-platre',
    'installation-faux-plafonds',
    'doublage-habillage-murs',
    'enduits-platre-lissage',
    'reparation-finition-platrerie',
    'peinture-interieure-murs-plafonds',
    'peinture-exterieure-facades',
    'peinture-apres-renovation',
    'peinture-decorative-finitions',
    'preparation-surfaces-peinture',
    'nettoyage-fin-chantier-complet',
    'nettoyage-apres-renovation',
    'nettoyage-approfondi-surfaces',
    'nettoyage-remise-des-cles',
    'remise-en-etat-entre-locataires',
    'entretien-courant-biens-immobiliers',
    'reparations-logements-locatifs',
    'renovation-partielle-logements-locatifs',
    'renovation-parties-communes-ppe',
    'coordination-travaux-regies',
})


def service_image_static_path(service_or_slug):
    slug = service_or_slug if isinstance(service_or_slug, str) else getattr(service_or_slug, "slug_fr", "")
    if slug in SERVICE_SLUGS:
        return f"{SERVICE_IMAGE_DIRECTORY}/{slug}.webp"
    return SERVICE_GENERIC_IMAGE


def service_image_static_url(service_or_slug):
    return static(service_image_static_path(service_or_slug))
