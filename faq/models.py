# FAQ · MODELOS PROXY | FAQ · PROXY MODELS
# Mantiene las mismas tablas core.* sin duplicar contenidos.
from core.models import FAQ as LegacyFAQ, FAQCategory as LegacyFAQCategory

class FAQCategory(LegacyFAQCategory):
    class Meta:
        proxy = True
        verbose_name = "001 - FAQ Category"
        verbose_name_plural = "001 - FAQ Categories"

class FAQ(LegacyFAQ):
    class Meta:
        proxy = True
        verbose_name = "002 - Frequently Asked Question"
        verbose_name_plural = "002 - Frequently Asked Questions"
