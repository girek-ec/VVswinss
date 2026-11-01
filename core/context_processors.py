from .models import BusinessHour, ServiceArea, SiteConfiguration, SocialLink


# ============================================================
# GLOBAL SITE CONTEXT
# ============================================================


from .visual_config import AboutPageConfiguration, ProfessionalPageConfiguration
from projects.visual_config import ProjectPageConfiguration
from blog.visual_config import BlogPageConfiguration
from contact.visual_config import ContactPageConfiguration
def global_site(request):
    return {
        "about_visuals": AboutPageConfiguration.objects.order_by("pk").first(),
        "professional_visuals": ProfessionalPageConfiguration.objects.order_by("pk").first(),
        "project_visuals": ProjectPageConfiguration.objects.order_by("pk").first(),
        "blog_visuals": BlogPageConfiguration.objects.order_by("pk").first(),
        "contact_visuals": ContactPageConfiguration.objects.order_by("pk").first(),
        "site_configuration": SiteConfiguration.objects.filter(is_active=True).first(),
        "social_links": SocialLink.objects.filter(is_active=True).order_by("order"),
        "business_hours": BusinessHour.objects.filter(is_active=True).order_by("order"),
        "service_areas": ServiceArea.objects.filter(is_active=True).order_by("order"),
    }
