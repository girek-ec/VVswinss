from .models import ServiceCategory


# ============================================================
# SERVICES MENU · GLOBAL CONTEXT
# ============================================================

def services_menu(request):
    return {
        "nav_service_categories": ServiceCategory.objects.filter(is_active=True).order_by("order", "name_fr")
    }