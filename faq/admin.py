# FAQ · ADMIN INDEPENDIENTE | FAQ · INDEPENDENT ADMIN
from django.contrib import admin
from core.admin import FAQCategoryAdmin as LegacyFAQCategoryAdmin, FAQAdmin as LegacyFAQAdmin
from core.models import FAQCategory as LegacyFAQCategory, FAQ as LegacyFAQ
from .models import FAQCategory, FAQ

# MOVER SOLO EL MENÚ | MOVE ADMIN ONLY
for legacy_model in (LegacyFAQCategory, LegacyFAQ):
    if admin.site.is_registered(legacy_model):
        admin.site.unregister(legacy_model)

@admin.register(FAQCategory)
class FAQCategoryAdmin(LegacyFAQCategoryAdmin):
    pass

@admin.register(FAQ)
class FAQAdmin(LegacyFAQAdmin):
    pass
