from django.db import models
from django.utils.text import slugify
from django.utils.translation import get_language

from core.models import MultilingualSEOModel, TimeStampedModel


# ============================================================
# HELPERS
# ============================================================

SUPPORTED_LANGUAGES = ("fr", "de", "it", "en")
DEFAULT_LANGUAGE = "fr"


def current_language():
    language = (get_language() or DEFAULT_LANGUAGE).split("-")[0]

    if language not in SUPPORTED_LANGUAGES:
        return DEFAULT_LANGUAGE

    return language


def generate_unique_slug(instance, field_name, value):
    base_slug = slugify(value) or "service"
    slug = base_slug
    counter = 2

    queryset = instance.__class__.objects.exclude(pk=instance.pk)

    while queryset.filter(**{field_name: slug}).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug



# ============================================================
# SERVICE PAGE CONFIGURATION
# Configuración visual global de la sección Servicios.
# Centraliza imágenes generales y fallbacks administrables.
# ============================================================

class ServicePageConfiguration(TimeStampedModel):

    category_default_image = models.ImageField(
        "SERVICIOS · Categorías · Imagen de respaldo",
        upload_to="services/page/categories/",
        blank=True,
        null=True,
        help_text=(
            "Se utiliza en la página principal de Servicios cuando una categoría "
            "no tiene imagen propia. Fallback static: "
            "antra/assets/img/service/feature-img-1.png."
        ),
    )

    category_default_social_image = models.ImageField(
        "SERVICIOS · Categorías · Imagen social automática",
        upload_to="seo/defaults/services/",
        blank=True,
        null=True,
        editable=False,
        help_text=(
            "Versión social 1200 x 630 generada automáticamente desde "
            "category_default_image. No se carga manualmente."
        ),
    )

    list_cta_background = models.ImageField(
        "SERVICIOS · CTA principal · Fondo",
        upload_to="services/page/cta/",
        blank=True,
        null=True,
        help_text=(
            "Fondo del bloque 'Un projet à réaliser ?'. "
            "Fallback static: antra/assets/img/bg-img/cta-bg-1.webp."
        ),
    )

    method_background = models.ImageField(
        "SERVICIOS · Método / Savoir-faire · Imagen",
        upload_to="services/page/method/",
        blank=True,
        null=True,
        help_text=(
            "Imagen grande de la sección Método de trabajo / Savoir-faire. "
            "Fallback static: antra/assets/img/bg-img/testi-bg.webp."
        ),
    )

    page_header_background = models.ImageField(
        "SERVICIOS · Encabezados interiores · Fondo de respaldo",
        upload_to="services/page/headers/",
        blank=True,
        null=True,
        help_text=(
            "Fondo de respaldo para encabezados de categorías y servicios cuando "
            "no existe hero_image específica. Fallback static: "
            "antra/assets/img/bg-img/page-header-bg.webp."
        ),
    )

    sidebar_cta_background = models.ImageField(
        "SERVICIOS · CTA lateral · Fondo",
        upload_to="services/page/sidebar-cta/",
        blank=True,
        null=True,
        help_text=(
            "Fondo del bloque lateral de contacto en categorías y servicios. "
            "Fallback static: antra/assets/img/bg-img/service-cta-bg-2.png."
        ),
    )

    detail_default_image = models.ImageField(
        "SERVICIOS · Detalle · Imagen principal de respaldo",
        upload_to="services/page/detail/",
        blank=True,
        null=True,
        help_text=(
            "Imagen de respaldo del contenido principal de una categoría o servicio. "
            "Fallback static: antra/assets/img/service/service-details-img-1.png."
        ),
    )

    secondary_default_image = models.ImageField(
        "SERVICIOS · Detalle · Imagen secundaria de respaldo",
        upload_to="services/page/detail/",
        blank=True,
        null=True,
        help_text=(
            "Respaldo cuando un servicio no tiene secondary_image. "
            "Si queda vacío, se utiliza service-details-img-1.png."
        ),
    )

    third_default_image = models.ImageField(
        "SERVICIOS · Detalle · Tercera imagen de respaldo",
        upload_to="services/page/detail/",
        blank=True,
        null=True,
        help_text=(
            "Respaldo cuando un servicio no tiene third_image. "
            "Si queda vacío, se utiliza service-details-img-1.png."
        ),
    )

    gallery_default_image = models.ImageField(
        "SERVICIOS · Galería · Imagen de respaldo",
        upload_to="services/page/gallery/",
        blank=True,
        null=True,
        help_text=(
            "Se utiliza cuando existe un registro de galería pero su imagen fue "
            "limpiada. Si queda vacío, se utiliza service-details-img-1.png."
        ),
    )

    class Meta:
        verbose_name = '001 - Services Visual Configuration'
        verbose_name_plural = '001 - Services Visual Configuration'

    def __str__(self):
        return "Configuración visual · Servicios"


# ============================================================
# SERVICE CATEGORY
# ============================================================

class ServiceCategory(
    MultilingualSEOModel,
    TimeStampedModel,
):

    # ========================================================
    # ESPAÑOL · REFERENCIA INTERNA
    # ========================================================

    name_es = models.CharField(max_length=150, blank=True)
    description_es = models.TextField(blank=True)

    # ========================================================
    # FRANÇAIS · PRINCIPAL
    # ========================================================

    name_fr = models.CharField(max_length=150)
    description_fr = models.TextField(blank=True)

    # ========================================================
    # DEUTSCH
    # ========================================================

    name_de = models.CharField(max_length=150, blank=True)
    description_de = models.TextField(blank=True)

    # ========================================================
    # ITALIANO
    # ========================================================

    name_it = models.CharField(max_length=150, blank=True)
    description_it = models.TextField(blank=True)

    # ========================================================
    # ENGLISH
    # ========================================================

    name_en = models.CharField(max_length=150, blank=True)
    description_en = models.TextField(blank=True)

    # ========================================================
    # SLUGS
    # ========================================================

    slug_fr = models.SlugField(max_length=170, blank=True, unique=True)
    slug_de = models.SlugField(max_length=170, blank=True, null=True, unique=True)
    slug_it = models.SlugField(max_length=170, blank=True, null=True, unique=True)
    slug_en = models.SlugField(max_length=170, blank=True, null=True, unique=True)

    # ========================================================
    # MEDIA
    # ========================================================

    hero_image = models.ImageField(
        "Hero / encabezado panorámico",
        upload_to="services/categories/hero/",
        blank=True,
        null=True,
        help_text=(
            "Imagen panorámica para el encabezado de la página de esta categoría. "
            "Si queda vacía, se utiliza la configuración visual global de Servicios."
        ),
    )

    image = models.ImageField(
        "Imagen principal / tarjeta",
        upload_to="services/categories/",
        blank=True,
        null=True,
        help_text=(
            "Imagen utilizada en listados y como imagen principal del contenido "
            "de la categoría."
        ),
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Clase CSS del icono. Ej.: fa-solid fa-house",
    )

    # ========================================================
    # SETTINGS
    # ========================================================

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = '002 - Service Category'
        verbose_name_plural = '002 - Service Categories'
        ordering = ["order", "name_fr"]

    def __str__(self):
        return self.name_fr

    def save(self, *args, **kwargs):

        if not self.slug_fr:
            self.slug_fr = generate_unique_slug(self, "slug_fr", self.name_fr)

        if self.name_de and not self.slug_de:
            self.slug_de = generate_unique_slug(self, "slug_de", self.name_de)

        if self.name_it and not self.slug_it:
            self.slug_it = generate_unique_slug(self, "slug_it", self.name_it)

        if self.name_en and not self.slug_en:
            self.slug_en = generate_unique_slug(self, "slug_en", self.name_en)

        if not self.name_de:
            self.slug_de = None

        if not self.name_it:
            self.slug_it = None

        if not self.name_en:
            self.slug_en = None

        self.autofill_seo(
            title_sources=(
                "name",
            ),
            description_sources=(
                "description",
            ),
        )

        super().save(*args, **kwargs)


# ============================================================
# SERVICE
# ============================================================

class Service(TimeStampedModel):

    # ========================================================
    # CATEGORY
    # ========================================================

    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.PROTECT,
        related_name="services",
    )

    # ========================================================
    # TITLE
    # ========================================================

    name_es = models.CharField(max_length=180, blank=True)
    name_fr = models.CharField(max_length=180)
    name_de = models.CharField(max_length=180, blank=True)
    name_it = models.CharField(max_length=180, blank=True)
    name_en = models.CharField(max_length=180, blank=True)


    # ========================================================
    # SUBTITLE
    # Frase comercial debajo del título
    # ========================================================
    subtitle_es = models.CharField(max_length=300, blank=True)
    subtitle_fr = models.CharField(max_length=300, blank=True)
    subtitle_de = models.CharField(max_length=300, blank=True)
    subtitle_it = models.CharField(max_length=300, blank=True)
    subtitle_en = models.CharField(max_length=300, blank=True)
    # ========================================================
    # HERO TITLE PREFIX
    # Complemento corto antes del nombre principal del servicio.
    # Ejemplo: "Travaux de"
    # ========================================================
    hero_title_prefix_es = models.CharField(max_length=100, blank=True)
    hero_title_prefix_fr = models.CharField(max_length=100, blank=True)
    hero_title_prefix_de = models.CharField(max_length=100, blank=True)
    hero_title_prefix_it = models.CharField(max_length=100, blank=True)
    hero_title_prefix_en = models.CharField(max_length=100, blank=True)
    # ========================================================
    # HERO TITLE SUFFIX
    # Complemento destacado después del nombre del servicio.
    # Se mostrará con el segundo color del diseño.
    # Ejemplo: "Solide et durable"
    # ========================================================
    hero_title_suffix_es = models.CharField(max_length=120, blank=True)
    hero_title_suffix_fr = models.CharField(max_length=120, blank=True)
    hero_title_suffix_de = models.CharField(max_length=120, blank=True)
    hero_title_suffix_it = models.CharField(max_length=120, blank=True)
    hero_title_suffix_en = models.CharField(max_length=120, blank=True)
    # ========================================================
    # SLUGS
    # ========================================================
    slug_fr = models.SlugField(max_length=200, blank=True, unique=True)
    slug_de = models.SlugField(max_length=200, blank=True, null=True, unique=True)
    slug_it = models.SlugField(max_length=200, blank=True, null=True, unique=True)
    slug_en = models.SlugField(max_length=200, blank=True, null=True, unique=True)
    # ========================================================


    # SUMMARY
    # Texto corto para tarjetas y listados
    # ========================================================

    summary_es = models.TextField(blank=True)
    summary_fr = models.TextField(blank=True)
    summary_de = models.TextField(blank=True)
    summary_it = models.TextField(blank=True)
    summary_en = models.TextField(blank=True)

    # ========================================================
    # MAIN CONTENT
    # Descripción principal de la página individual
    # ========================================================

    content_es = models.TextField(blank=True)
    content_fr = models.TextField()
    content_de = models.TextField(blank=True)
    content_it = models.TextField(blank=True)
    content_en = models.TextField(blank=True)

    # ========================================================
    # DETAIL 1
    # ========================================================

    detail_1_title_es = models.CharField(max_length=255, blank=True)
    detail_1_title_fr = models.CharField(max_length=255, blank=True)
    detail_1_title_de = models.CharField(max_length=255, blank=True)
    detail_1_title_it = models.CharField(max_length=255, blank=True)
    detail_1_title_en = models.CharField(max_length=255, blank=True)

    detail_1_text_es = models.TextField(blank=True)
    detail_1_text_fr = models.TextField(blank=True)
    detail_1_text_de = models.TextField(blank=True)
    detail_1_text_it = models.TextField(blank=True)
    detail_1_text_en = models.TextField(blank=True)

    detail_1_list_es = models.TextField(
        blank=True,
        help_text="Un elemento por línea.",
    )

    detail_1_list_fr = models.TextField(
        blank=True,
        help_text="Un élément par ligne.",
    )

    detail_1_list_de = models.TextField(
        blank=True,
        help_text="Ein Element pro Zeile.",
    )

    detail_1_list_it = models.TextField(
        blank=True,
        help_text="Un elemento per riga.",
    )

    detail_1_list_en = models.TextField(
        blank=True,
        help_text="One item per line.",
    )

    # ========================================================
    # DETAIL 2
    # ========================================================

    detail_2_title_es = models.CharField(max_length=255, blank=True)
    detail_2_title_fr = models.CharField(max_length=255, blank=True)
    detail_2_title_de = models.CharField(max_length=255, blank=True)
    detail_2_title_it = models.CharField(max_length=255, blank=True)
    detail_2_title_en = models.CharField(max_length=255, blank=True)

    detail_2_text_es = models.TextField(blank=True)
    detail_2_text_fr = models.TextField(blank=True)
    detail_2_text_de = models.TextField(blank=True)
    detail_2_text_it = models.TextField(blank=True)
    detail_2_text_en = models.TextField(blank=True)

    detail_2_list_es = models.TextField(
        blank=True,
        help_text="Un elemento por línea.",
    )

    detail_2_list_fr = models.TextField(
        blank=True,
        help_text="Un élément par ligne.",
    )

    detail_2_list_de = models.TextField(
        blank=True,
        help_text="Ein Element pro Zeile.",
    )

    detail_2_list_it = models.TextField(
        blank=True,
        help_text="Un elemento per riga.",
    )

    detail_2_list_en = models.TextField(
        blank=True,
        help_text="One item per line.",
    )

    # ========================================================
    # CTA
    # Bloque final destinado a captar al cliente
    # ========================================================

    cta_title_es = models.CharField(max_length=255, blank=True)
    cta_title_fr = models.CharField(max_length=255, blank=True)
    cta_title_de = models.CharField(max_length=255, blank=True)
    cta_title_it = models.CharField(max_length=255, blank=True)
    cta_title_en = models.CharField(max_length=255, blank=True)

    cta_text_es = models.TextField(blank=True)
    cta_text_fr = models.TextField(blank=True)
    cta_text_de = models.TextField(blank=True)
    cta_text_it = models.TextField(blank=True)
    cta_text_en = models.TextField(blank=True)

    # ========================================================
    # CTA BUTTON
    # Texto del botón de WhatsApp
    # Puede personalizarse por servicio.
    # Si está vacío se genera uno automático.
    # ========================================================

    cta_button_es = models.CharField(max_length=100, blank=True)
    cta_button_fr = models.CharField(max_length=100, blank=True)
    cta_button_de = models.CharField(max_length=100, blank=True)
    cta_button_it = models.CharField(max_length=100, blank=True)
    cta_button_en = models.CharField(max_length=100, blank=True)

    # ========================================================
    # WHATSAPP MESSAGE
    # Mensaje que aparecerá automáticamente al abrir WhatsApp.
    # Editable desde Admin.
    # Si queda vacío se genera automáticamente.
    # ========================================================

    whatsapp_message_es = models.TextField(
        blank=True,
        help_text="Mensaje personalizado de WhatsApp. Si queda vacío se generará automáticamente.",
    )

    whatsapp_message_fr = models.TextField(
        blank=True,
        help_text="Message WhatsApp personnalisé. Laissez vide pour générer automatiquement.",
    )

    whatsapp_message_de = models.TextField(
        blank=True,
        help_text="Individuelle WhatsApp-Nachricht. Leer lassen für automatische Erstellung.",
    )

    whatsapp_message_it = models.TextField(
        blank=True,
        help_text="Messaggio WhatsApp personalizzato. Lasciare vuoto per generarlo automaticamente.",
    )

    whatsapp_message_en = models.TextField(
        blank=True,
        help_text="Custom WhatsApp message. Leave blank to generate automatically.",
    )

    whatsapp_enabled = models.BooleanField(
        default=True,
        verbose_name="Show WhatsApp CTA",
    )

    # ========================================================
    # MEDIA
    # ========================================================

    hero_image = models.ImageField(
        "Hero / encabezado panorámico",
        upload_to="services/hero/",
        blank=True,
        null=True,
        help_text=(
            "Imagen panorámica exclusiva del encabezado de este servicio. "
            "No reutiliza la imagen principal del contenido."
        ),
    )

    main_image = models.ImageField(
        "Imagen principal del contenido",
        upload_to="services/main/",
        blank=True,
        null=True,
    )

    secondary_image = models.ImageField(
        upload_to="services/secondary/",
        blank=True,
        null=True,
    )

    third_image = models.ImageField(
        upload_to="services/third/",
        blank=True,
        null=True,
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Clase CSS del icono.",
    )

    # ========================================================
    # PUBLICATION
    # ========================================================

    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = '003 - Service'
        verbose_name_plural = '003 - Services'
        ordering = ["order", "name_fr"]

    def __str__(self):
        return self.name_fr

    # ========================================================
    # LOCALIZED HELPER
    # ========================================================

    def get_localized_field(self, field_name):
        language = current_language()

        value = getattr(self, f"{field_name}_{language}", "")

        if value:
            return value

        value_fr = getattr(self, f"{field_name}_fr", "")

        if value_fr:
            return value_fr

        for fallback in ("de", "it", "en", "es"):
            value = getattr(self, f"{field_name}_{fallback}", "")

            if value:
                return value

        return ""

    # ========================================================
    # CURRENT SERVICE NAME
    # ========================================================

    def get_current_name(self):
        return self.get_localized_field("name")

    # ========================================================
    # CTA BUTTON
    # Si Admin tiene texto, lo usa.
    # Si no, genera uno automáticamente.
    # ========================================================

    # ========================================================
    # CURRENT SERVICE NAME
    # ========================================================


    def get_current_subtitle(self):
        return self.get_localized_field("subtitle")

    def get_current_hero_title_prefix(self):
        return self.get_localized_field("hero_title_prefix")

    def get_current_hero_title_suffix(self):
        return self.get_localized_field("hero_title_suffix")

    def get_current_summary(self):
        return self.get_localized_field("summary")

    def get_current_content(self):
        return self.get_localized_field("content")

    def get_current_detail_1_title(self):
        return self.get_localized_field("detail_1_title")

    def get_current_detail_1_text(self):
        return self.get_localized_field("detail_1_text")

    def get_current_detail_2_title(self):
        return self.get_localized_field("detail_2_title")

    def get_current_detail_2_text(self):
        return self.get_localized_field("detail_2_text")

    def get_current_cta_title(self):
        return self.get_localized_field("cta_title")

    def get_current_cta_text(self):
        return self.get_localized_field("cta_text")
    
    # ========================================================
    # DETAIL LISTS
    # Convierte cada línea del TextField en un elemento
    # independiente para usarlo en el template.
    # ========================================================

    def get_detail_1_items(self):
        value = self.get_localized_field("detail_1_list")

        if not value:
            return []

        return [
            line.strip().lstrip("•-").strip()
            for line in value.splitlines()
            if line.strip()
        ]

    def get_detail_2_items(self):
        value = self.get_localized_field("detail_2_list")

        if not value:
            return []

        return [
            line.strip().lstrip("•-").strip()
            for line in value.splitlines()
            if line.strip()
        ]

    # ========================================================
    # CTA BUTTON
    # Si Admin tiene texto, lo usa.
    # Si no, genera uno automáticamente.
    # ========================================================

    def get_cta_button(self):
        language = current_language()

        custom_button = getattr(
            self,
            f"cta_button_{language}",
            "",
        )

        if custom_button:
            return custom_button

        defaults = {
            "fr": "Demander des informations",
            "de": "Informationen anfordern",
            "it": "Richiedere informazioni",
            "en": "Request information",
        }

        return defaults.get(language, defaults["fr"])

    # ========================================================
    # WHATSAPP MESSAGE
    # Prioridad:
    # 1. Mensaje personalizado del Admin
    # 2. Mensaje automático utilizando nombre del servicio
    # ========================================================

    def get_whatsapp_message(self):
        language = current_language()

        custom_message = getattr(
            self,
            f"whatsapp_message_{language}",
            "",
        )

        if custom_message:
            return custom_message

        service_name = self.get_current_name()

        messages = {
            "fr": (
                f"Bonjour, je souhaite obtenir plus d’informations concernant le service "
                f"« {service_name} » et, si possible, recevoir un devis pour mon projet. Merci."
            ),
            "de": (
                f"Guten Tag, ich möchte weitere Informationen zur Dienstleistung "
                f"« {service_name} » erhalten und wenn möglich eine Offerte für mein Projekt anfragen. "
                f"Vielen Dank."
            ),
            "it": (
                f"Buongiorno, desidero ricevere maggiori informazioni sul servizio "
                f"« {service_name} » e, se possibile, richiedere un preventivo per il mio progetto. Grazie."
            ),
            "en": (
                f"Hello, I would like more information about the service "
                f"“{service_name}” and, if possible, a quote for my project. Thank you."
            ),
        }

        return messages.get(language, messages["fr"])

    # ========================================================
    # SAVE
    # ========================================================

    def save(self, *args, **kwargs):

        if not self.slug_fr:
            self.slug_fr = generate_unique_slug(
                self,
                "slug_fr",
                self.name_fr,
            )

        if self.name_de and not self.slug_de:
            self.slug_de = generate_unique_slug(
                self,
                "slug_de",
                self.name_de,
            )

        if self.name_it and not self.slug_it:
            self.slug_it = generate_unique_slug(
                self,
                "slug_it",
                self.name_it,
            )

        if self.name_en and not self.slug_en:
            self.slug_en = generate_unique_slug(
                self,
                "slug_en",
                self.name_en,
            )

        if not self.name_de:
            self.slug_de = None

        if not self.name_it:
            self.slug_it = None

        if not self.name_en:
            self.slug_en = None

        super().save(*args, **kwargs)


# ============================================================
# SERVICE BENEFIT
# Beneficios adicionales opcionales.
# Ejemplo:
# "Interlocuteur unique"
# "Devis clair"
# "Finitions soignées"
# ============================================================

class ServiceBenefit(TimeStampedModel):

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="benefits",
    )

    title_es = models.CharField(max_length=160, blank=True)
    title_fr = models.CharField(max_length=160)
    title_de = models.CharField(max_length=160, blank=True)
    title_it = models.CharField(max_length=160, blank=True)
    title_en = models.CharField(max_length=160, blank=True)

    description_es = models.TextField(blank=True)
    description_fr = models.TextField(blank=True)
    description_de = models.TextField(blank=True)
    description_it = models.TextField(blank=True)
    description_en = models.TextField(blank=True)

    icon = models.CharField(
        max_length=100,
        blank=True,
    )

    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = '004 - Service Benefit'
        verbose_name_plural = '004 - Service Benefits'
        ordering = ["order"]

    def __str__(self):
        return self.title_fr


# ============================================================
# SERVICE IMAGE
# Galería opcional.
# Además de:
# main_image
# secondary_image
# third_image
# ============================================================

class ServiceImage(TimeStampedModel):

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = models.ImageField(
        upload_to="services/gallery/",
        blank=True,
        null=True,
    )

    alt_es = models.CharField(max_length=180, blank=True)
    alt_fr = models.CharField(max_length=180, blank=True)
    alt_de = models.CharField(max_length=180, blank=True)
    alt_it = models.CharField(max_length=180, blank=True)
    alt_en = models.CharField(max_length=180, blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = '005 - Service Image'
        verbose_name_plural = '005 - Images / Gallery'
        ordering = ["order"]

    def __str__(self):
        return f"Image - {self.service}"
