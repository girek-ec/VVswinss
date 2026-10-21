from .models import BusinessHour, ServiceArea, SiteConfiguration, SocialLink


# ============================================================
# GLOBAL SITE CONTEXT
# ============================================================

def global_site(request):
    return {
        "site_configuration": SiteConfiguration.objects.filter(is_active=True).first(),
        "social_links": SocialLink.objects.filter(is_active=True).order_by("order"),
        "business_hours": BusinessHour.objects.filter(is_active=True).order_by("order"),
        "service_areas": ServiceArea.objects.filter(is_active=True).order_by("order"),
    }