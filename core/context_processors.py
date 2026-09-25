from .models import (
    BusinessHour,
    ServiceArea,
    SiteConfiguration,
    SocialLink,
)


def global_site(request):
    return {
        "site_configuration": (
            SiteConfiguration.objects
            .filter(activo=True)
            .first()
        ),

        "social_links": (
            SocialLink.objects
            .filter(activo=True)
            .order_by("orden")
        ),

        "business_hours": (
            BusinessHour.objects
            .filter(activo=True)
            .order_by("orden")
        ),

        "service_areas": (
            ServiceArea.objects
            .filter(activo=True)
            .order_by("orden")
        ),
    }