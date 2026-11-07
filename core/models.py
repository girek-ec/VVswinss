import re

from django.db import models
from django.utils.html import strip_tags
from django.utils.text import Truncator, slugify
from django.utils.translation import get_language


# ============================================================
# BASE · TIMESTAMPS
# ============================================================

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ============================================================
# BASE · SEO MULTILINGÜE
# ============================================================

class MultilingualSEOModel(models.Model):
    SEO_LANGUAGES = ("es", "fr", "de", "it", "en")
    SEO_TITLE_MAX_LENGTH = 70
    SEO_DESCRIPTION_MAX_LENGTH = 160
    SEO_BRAND_NAME = "V&V Swiss Services"

    seo_title_es = models.CharField(max_length=160, blank=True, default="")
    seo_title_fr = models.CharField(max_length=160, blank=True, default="")
    seo_title_de = models.CharField(max_length=160, blank=True, default="")
    seo_title_it = models.CharField(max_length=160, blank=True, default="")
    seo_title_en = models.CharField(max_length=160, blank=True, default="")

    meta_description_es = models.CharField(max_length=320, blank=True, default="")
    meta_description_fr = models.CharField(max_length=320, blank=True, default="")
    meta_description_de = models.CharField(max_length=320, blank=True, default="")
    meta_description_it = models.CharField(max_length=320, blank=True, default="")
    meta_description_en = models.CharField(max_length=320, blank=True, default="")

    og_image = models.ImageField(
        upload_to="seo/",
        blank=True,
        null=True,
        verbose_name="Imagen social",
        help_text=(
            "Opcional. Si se deja vacía, el sistema utilizará "
            "automáticamente la imagen principal del contenido."
        ),
    )

    is_indexable = models.BooleanField(default=True)

    class Meta:
        abstract = True

    @staticmethod
    def _clean_seo_text(value):
        if not value:
            return ""

        value = strip_tags(str(value))
        value = re.sub(r"\s+", " ", value).strip()

        return value

    def _get_seo_source(self, language, source_fields):
        for source_field in source_fields:
            field_name = f"{source_field}_{language}"

            if not hasattr(self, field_name):
                continue

            value = self._clean_seo_text(
                getattr(self, field_name, "")
            )

            if value:
                return value

        return ""

    def _build_seo_title(self, value):
        value = self._clean_seo_text(value)

        if not value:
            return ""

        suffix = f" | {self.SEO_BRAND_NAME}"
        available_length = (
            self.SEO_TITLE_MAX_LENGTH
            - len(suffix)
        )

        if available_length <= 0:
            return Truncator(value).chars(
                self.SEO_TITLE_MAX_LENGTH,
                truncate="…",
            )

        title = Truncator(value).chars(
            available_length,
            truncate="…",
        )

        return f"{title}{suffix}"

    def _build_meta_description(self, value):
        value = self._clean_seo_text(value)

        if not value:
            return ""

        return Truncator(value).chars(
            self.SEO_DESCRIPTION_MAX_LENGTH,
            truncate="…",
        )

    def autofill_seo(
        self,
        *,
        title_sources,
        description_sources,
    ):
        """
        Completa automáticamente SEO por idioma.

        Reglas:
        - No traduce contenido.
        - No copia FR hacia DE/IT/EN.
        - Solo genera SEO si existe contenido en ese idioma.
        - Nunca sobrescribe SEO escrito manualmente.
        """

        for language in self.SEO_LANGUAGES:
            seo_title_field = f"seo_title_{language}"
            meta_description_field = (
                f"meta_description_{language}"
            )

            if not getattr(self, seo_title_field, ""):
                title_source = self._get_seo_source(
                    language,
                    title_sources,
                )

                if title_source:
                    setattr(
                        self,
                        seo_title_field,
                        self._build_seo_title(
                            title_source
                        ),
                    )

            if not getattr(
                self,
                meta_description_field,
                "",
            ):
                description_source = (
                    self._get_seo_source(
                        language,
                        description_sources,
                    )
                )

                if description_source:
                    setattr(
                        self,
                        meta_description_field,
                        self._build_meta_description(
                            description_source
                        ),
                    )
# ============================================================
# SITE CONFIGURATION
# Configuración general, contacto y datos legales
# ============================================================

class SiteConfiguration(TimeStampedModel):

    # ========================================================
    # EMPRESA
    # ========================================================

    company_name = models.CharField(max_length=150)

    slogan_es = models.CharField(max_length=255, blank=True)
    slogan_fr = models.CharField(max_length=255, blank=True)
    slogan_de = models.CharField(max_length=255, blank=True)
    slogan_it = models.CharField(max_length=255, blank=True)
    slogan_en = models.CharField(max_length=255, blank=True)

    # ========================================================
    # IDENTIDAD VISUAL
    # ========================================================

    logo = models.ImageField(
        upload_to="site/",
        blank = True,
        null = True,
    )

    white_logo = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True,
    )

    favicon = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True,
    )

    preloader_background = models.ImageField(
        upload_to="site/preloader/",
        blank=True,
        null=True,
        verbose_name="Imagen de fondo del preloader",
        help_text=(
            "Imagen mostrada durante la transición/carga entre páginas. "
            "Recomendado: formato horizontal 16:9, mínimo 1600 px de ancho."
        ),
    )

    footer_background = models.ImageField(
        "PIE DE PÁGINA · Imagen de fondo",
        upload_to="site/footer/",
        blank=True,
        null=True,
        help_text=(
            "Imagen de fondo global del pie de página en todo el sitio. "
            "Si se deja vacía o se usa Limpiar, se mostrará la imagen estática "
            "antra/assets/img/bg-img/footer-bg.webp. "
            "Recomendado: horizontal 16:9, mínimo 1600 px de ancho."
        ),
    )

    # ========================================================
    # CONTACTO
    # ========================================================

    phone = models.CharField(
        max_length=50,
        blank=True,
    )

    whatsapp = models.CharField(
        max_length=50,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    # ========================================================
    # DIRECCIÓN
    # ========================================================

    address = models.CharField(
        max_length=255,
        blank=True,
    )

    postal_code = models.CharField(
        max_length=20,
        blank=True,
        help_text="NPA / code postal.",
    )

    city = models.CharField(
        max_length=100,
        blank=True,
    )

    canton = models.CharField(
        max_length=100,
        blank=True,
    )

    country = models.CharField(
        max_length=100,
        default="Switzerland",
    )

    # ========================================================
    # GEOLOCALIZACIÓN
    # ========================================================

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
    )

    # ========================================================
    # DATOS LEGALES
    # Mentions légales / Impressum
    # ========================================================

    legal_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Raison sociale ou nom juridique officiel de l'entreprise.",
    )

    legal_form = models.CharField(
        max_length=100,
        blank=True,
        help_text="Ex. entreprise individuelle, Sàrl, SA.",
    )

    uid_number = models.CharField(
        max_length=50,
        blank=True,
        help_text="Numéro IDE / UID / CHE.",
    )

    vat_number = models.CharField(
        max_length=50,
        blank=True,
        help_text="Numéro TVA, si applicable.",
    )

    commercial_register = models.CharField(
        max_length=150,
        blank=True,
        help_text="Informations relatives au registre du commerce, si applicable.",
    )

    legal_representative = models.CharField(
        max_length=200,
        blank=True,
        help_text="Responsable ou représentant légal de l'entreprise.",
    )

    insurance_info = models.CharField(
        max_length=255,
        blank=True,
    )

    # ========================================================
    # PROTECTION DES DONNÉES · nLPD
    # ========================================================

    privacy_email = models.EmailField(
        blank=True,
        help_text=(
            "Adresse e-mail utilisée pour les demandes relatives "
            "à la protection des données. Si vide, l'e-mail principal "
            "du site peut être utilisé."
        ),
    )

    # ========================================================
    # HÉBERGEMENT
    # Informations utiles pour les mentions légales
    # et la politique de confidentialité
    # ========================================================

    hosting_provider = models.CharField(
        max_length=200,
        blank=True,
        help_text="Nom du prestataire d'hébergement du site web.",
    )

    hosting_address = models.CharField(
        max_length=255,
        blank=True,
        help_text="Adresse du prestataire d'hébergement, si connue.",
    )

    hosting_country = models.CharField(
        max_length=100,
        blank=True,
        help_text="Pays dans lequel le site ou les données sont hébergés.",
    )

    # ========================================================
    # CONFIGURATION
    # ========================================================

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        verbose_name = '001 - General Configuration'
        verbose_name_plural = '001 - General Configuration'

    def __str__(self):
        return self.company_name


# ============================================================
# SOCIAL LINKS
# ============================================================

class SocialLink(TimeStampedModel):
    name = models.CharField(max_length=50)
    url = models.URLField()

    icon = models.CharField(
        max_length=100,
        blank=True,
    )

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = '020 - Social Link'
        verbose_name_plural = '020 - Social Links'
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


# ============================================================
# BUSINESS HOURS
# ============================================================

class BusinessHour(TimeStampedModel):
    day_fr = models.CharField(max_length=30)
    day_de = models.CharField(max_length=30, blank=True)
    day_it = models.CharField(max_length=30, blank=True)
    day_en = models.CharField(max_length=30, blank=True)

    hours = models.CharField(max_length=100)

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = '013 - Business Hour'
        verbose_name_plural = '013 - Business Hours'
        ordering = ["order"]

    def __str__(self):
        return f"{self.day_fr}: {self.hours}"

# ============================================================
# ABOUT CONTENT
# ============================================================

class AboutContent(TimeStampedModel):
    intro_title_es = models.CharField(max_length=255, blank=True)
    intro_title_fr = models.CharField(max_length=255)
    intro_title_de = models.CharField(max_length=255, blank=True)
    intro_title_it = models.CharField(max_length=255, blank=True)
    intro_title_en = models.CharField(max_length=255, blank=True)

    intro_text_es = models.TextField(blank=True)
    intro_text_fr = models.TextField()
    intro_text_de = models.TextField(blank=True)
    intro_text_it = models.TextField(blank=True)
    intro_text_en = models.TextField(blank=True)

    mission_es = models.TextField(blank=True)
    mission_fr = models.TextField()
    mission_de = models.TextField(blank=True)
    mission_it = models.TextField(blank=True)
    mission_en = models.TextField(blank=True)

    vision_es = models.TextField(blank=True)
    vision_fr = models.TextField()
    vision_de = models.TextField(blank=True)
    vision_it = models.TextField(blank=True)
    vision_en = models.TextField(blank=True)

    history_es = models.TextField(blank=True)
    history_fr = models.TextField(blank=True)
    history_de = models.TextField(blank=True)
    history_it = models.TextField(blank=True)
    history_en = models.TextField(blank=True)

    # ========================================================
    # IMAGEN PRINCIPAL
    # ========================================================

    image = models.ImageField(
        upload_to="about/",
        blank=True,
        null=True,
    )

    # ========================================================
    # VIDEO / MULTIMEDIA
    # ========================================================

    video_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="URL del vídeo",
        help_text="Enlace de YouTube, Vimeo u otra plataforma compatible.",
    )

    video_image = models.ImageField(
        upload_to="about/video/",
        blank=True,
        null=True,
        verbose_name="Imagen de portada del vídeo",
        help_text="Se muestra como fondo del vídeo o como imagen cuando no existe vídeo.",
    )

    # ========================================================
    # PUBLICACIÓN
    # ========================================================

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = '003 - About Us'
        verbose_name_plural = '003 - About Us'

    def __str__(self):
        return self.intro_title_fr or "About V&V Swiss Services"

# ============================================================
# SERVICE AREA
# ============================================================

class ServiceArea(TimeStampedModel):
    name = models.CharField(max_length=120)
    canton = models.CharField(max_length=120, blank=True)

    description_es = models.CharField(max_length=255, blank=True)
    description_fr = models.CharField(max_length=255, blank=True)
    description_de = models.CharField(max_length=255, blank=True)
    description_it = models.CharField(max_length=255, blank=True)
    description_en = models.CharField(max_length=255, blank=True)

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = '012 - Service Area'
        verbose_name_plural = '012 - Service Areas'
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


# ============================================================
# PROCESS STEP
# ============================================================

class ProcessStep(TimeStampedModel):
    number = models.PositiveIntegerField()

    title_es = models.CharField(max_length=150, blank=True)
    title_fr = models.CharField(max_length=150)
    title_de = models.CharField(max_length=150, blank=True)
    title_it = models.CharField(max_length=150, blank=True)
    title_en = models.CharField(max_length=150, blank=True)

    description_es = models.TextField(blank=True)
    description_fr = models.TextField()
    description_de = models.TextField(blank=True)
    description_it = models.TextField(blank=True)
    description_en = models.TextField(blank=True)

    icon = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = '011 - Process Step'
        verbose_name_plural = '011 - Work Process'
        ordering = ["number"]

    def __str__(self):
        return f"{self.number}. {self.title_fr}"


# ============================================================
# TEAM MEMBER
# ============================================================

class TeamMember(TimeStampedModel):
    name = models.CharField(max_length=150)

    position_fr = models.CharField(max_length=150)
    position_de = models.CharField(max_length=150, blank=True)
    position_it = models.CharField(max_length=150, blank=True)
    position_en = models.CharField(max_length=150, blank=True)

    biography_fr = models.TextField(blank=True)
    biography_de = models.TextField(blank=True)
    biography_it = models.TextField(blank=True)
    biography_en = models.TextField(blank=True)

    photo = models.ImageField(
        upload_to="team/",
        blank=True,
        null=True,
    )

    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = '005 - Team Member'
        verbose_name_plural = '005 - Team'
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


# ============================================================
# INSURANCE
# ============================================================

class Insurance(TimeStampedModel):
    name_es = models.CharField(
        "Nombre · referencia ES",
        max_length=150,
        blank=True,
    )

    name_fr = models.CharField(
        "Nom · FR",
        max_length=150,
    )

    name_de = models.CharField(
        "Name · DE",
        max_length=150,
        blank=True,
    )

    name_it = models.CharField(
        "Nome · IT",
        max_length=150,
        blank=True,
    )

    name_en = models.CharField(
        "Name · EN",
        max_length=150,
        blank=True,
    )

    description_es = models.TextField(
        "Descripción · referencia ES",
        blank=True,
    )

    description_fr = models.TextField(
        "Description · FR",
        blank=True,
    )

    description_de = models.TextField(
        "Beschreibung · DE",
        blank=True,
    )

    description_it = models.TextField(
        "Descrizione · IT",
        blank=True,
    )

    description_en = models.TextField(
        "Description · EN",
        blank=True,
    )

    image = models.ImageField(
        upload_to="insurances/",
        blank=True,
        null=True,
    )

    pdf = models.FileField(
        upload_to="insurances/documents/",
        blank=True,
        null=True,
    )

    url = models.URLField(blank=True)

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = '006 - Insurance'
        verbose_name_plural = '006 - Insurance'
        ordering = ["order", "name_fr"]

    def __str__(self):
        return self.name_fr


# ============================================================
# CERTIFICATION
# ============================================================

class Certification(TimeStampedModel):
    name = models.CharField(max_length=150)

    issuer = models.CharField(
        max_length=150,
        blank=True,
    )

    image = models.ImageField(
        upload_to="certifications/",
        blank=True,
        null=True,
    )

    pdf = models.FileField(
        upload_to="certifications/documents/",
        blank=True,
        null=True,
    )

    url = models.URLField(blank=True)

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = '007 - Certification'
        verbose_name_plural = '007 - Certifications'
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


# ============================================================
# COMPANY VALUE
# ============================================================

class CompanyValue(TimeStampedModel):
    title_es = models.CharField(max_length=150, blank=True)
    title_fr = models.CharField(max_length=150)
    title_de = models.CharField(max_length=150, blank=True)
    title_it = models.CharField(max_length=150, blank=True)
    title_en = models.CharField(max_length=150, blank=True)

    description_es = models.TextField(blank=True)
    description_fr = models.TextField()
    description_de = models.TextField(blank=True)
    description_it = models.TextField(blank=True)
    description_en = models.TextField(blank=True)

    image = models.ImageField(
        upload_to="company-values/",
        blank=True,
        null=True,
    )

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = '008 - Company Value'
        verbose_name_plural = '008 - Company Values'
        ordering = ["order"]

    def __str__(self):
        return self.title_fr


# ============================================================
# STATISTIC
# ============================================================

class Statistic(TimeStampedModel):
    value = models.CharField(max_length=30)

    title_es = models.CharField(max_length=100, blank=True)
    title_fr = models.CharField(max_length=100)
    title_de = models.CharField(max_length=100, blank=True)
    title_it = models.CharField(max_length=100, blank=True)
    title_en = models.CharField(max_length=100, blank=True)

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = '009 - Statistic'
        verbose_name_plural = '009 - Statistics'
        ordering = ["order"]

    def __str__(self):
        return f"{self.value} - {self.title_fr}"


# ============================================================
# TESTIMONIAL
# ============================================================

class Testimonial(TimeStampedModel):
    name = models.CharField(max_length=150)

    company = models.CharField(
        max_length=150,
        blank=True,
    )

    text_es = models.TextField(blank=True)
    text_fr = models.TextField()
    text_de = models.TextField(blank=True)
    text_it = models.TextField(blank=True)
    text_en = models.TextField(blank=True)

    photo = models.ImageField(
        upload_to="testimonials/",
        blank=True,
        null=True,
    )

    rating = models.PositiveSmallIntegerField(default=5)

    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = '010 - Testimonial'
        verbose_name_plural = '010 - Testimonials'
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.name


# ============================================================
# FAQ CATEGORY
# ============================================================

class FAQCategory(TimeStampedModel):
    name_es = models.CharField(max_length=120, blank=True)
    name_fr = models.CharField(max_length=120)
    name_de = models.CharField(max_length=120, blank=True)
    name_it = models.CharField(max_length=120, blank=True)
    name_en = models.CharField(max_length=120, blank=True)

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = '014 - FAQ Category'
        verbose_name_plural = '014 - FAQ Categories'
        ordering = ["order", "name_fr"]

    def __str__(self):
        return self.name_fr


# ============================================================
# FAQ
# ============================================================

class FAQ(TimeStampedModel):
    category = models.ForeignKey(
        FAQCategory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="questions",
    )

    question_fr = models.CharField(max_length=255)
    question_de = models.CharField(max_length=255, blank=True)
    question_it = models.CharField(max_length=255, blank=True)
    question_en = models.CharField(max_length=255, blank=True)

    answer_fr = models.TextField()
    answer_de = models.TextField(blank=True)
    answer_it = models.TextField(blank=True)
    answer_en = models.TextField(blank=True)

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = '015 - FAQ'
        verbose_name_plural = '015 - Frequently Asked Questions'
        ordering = ["order", "question_fr"]

    def __str__(self):
        return self.question_fr


# ============================================================
# INSTITUTIONAL PAGE
#
# Se utiliza también para:
# - Mentions légales / Impressum
# - Protection des données / nLPD
#
# Francés = idioma principal
# Español = referencia administrativa
# ============================================================

class InstitutionalPage(
    MultilingualSEOModel,
    TimeStampedModel,
):
    # ========================================================
    # TITLES
    # ========================================================

    title_es = models.CharField(
        "Título · referencia ES",
        max_length=200,
        blank=True,
    )

    title_fr = models.CharField(max_length=160)
    title_de = models.CharField(max_length=160, blank=True)
    title_it = models.CharField(max_length=160, blank=True)
    title_en = models.CharField(max_length=160, blank=True)

    # ========================================================
    # SLUGS
    # ========================================================

    slug_fr = models.SlugField(
        max_length=180,
        unique=True,
    )

    slug_de = models.SlugField(
        max_length=180,
        blank=True,
        null=True,
        unique=True,
    )

    slug_it = models.SlugField(
        max_length=180,
        blank=True,
        null=True,
        unique=True,
    )

    slug_en = models.SlugField(
        max_length=180,
        blank=True,
        null=True,
        unique=True,
    )

    # ========================================================
    # CONTENT
    # ========================================================

    content_es = models.TextField(blank=True)
    content_fr = models.TextField()
    content_de = models.TextField(blank=True)
    content_it = models.TextField(blank=True)
    content_en = models.TextField(blank=True)

    # ========================================================
    # MEDIA
    # ========================================================

    image = models.ImageField(
        upload_to="pages/",
        blank=True,
        null=True,
    )

    # ========================================================
    # SETTINGS
    # ========================================================

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = '019 - Institutional Page'
        verbose_name_plural = '019 - Institutional Pages'

    def __str__(self):
        return self.title_fr

    # ========================================================
    # LOCALIZED FIELD
    # ========================================================

    def get_localized_field(self, field_name):
        language = (get_language() or "fr").split("-")[0]

        if language not in ("fr", "de", "it", "en"):
            language = "fr"

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
    # CURRENT VALUES
    # ========================================================

    def get_current_title(self):
        return self.get_localized_field("title")

    def get_current_content(self):
        return self.get_localized_field("content")

    def get_current_seo_title(self):
        return self.get_localized_field("seo_title")

    def get_current_meta_description(self):
        return self.get_localized_field("meta_description")

    # ========================================================
    # SAVE
    # ========================================================

    def save(self, *args, **kwargs):
        if not self.slug_fr:
            self.slug_fr = slugify(self.title_fr)

        if self.title_de and not self.slug_de:
            self.slug_de = slugify(self.title_de)

        if self.title_it and not self.slug_it:
            self.slug_it = slugify(self.title_it)

        if self.title_en and not self.slug_en:
            self.slug_en = slugify(self.title_en)

        super().save(*args, **kwargs)


# ============================================================
# HOME CONTENT
# ============================================================

class HomeContent(TimeStampedModel):
    title_es = models.CharField(max_length=200, blank=True)
    title_fr = models.CharField(max_length=200)
    title_de = models.CharField(max_length=200, blank=True)
    title_it = models.CharField(max_length=200, blank=True)
    title_en = models.CharField(max_length=200, blank=True)

    subtitle_es = models.TextField(blank=True)
    subtitle_fr = models.TextField(blank=True)
    subtitle_de = models.TextField(blank=True)
    subtitle_it = models.TextField(blank=True)
    subtitle_en = models.TextField(blank=True)

    # ========================================================
    # HOME · IMÁGENES ADMINISTRABLES
    #
    # Regla general:
    # - Si se carga una imagen, se muestra la imagen de /media/.
    # - Si queda vacía, el template usa su imagen original de /static/.
    # ========================================================


    about_image_primary = models.ImageField(
        "HOME · 03 Empresa · Imagen principal",
        upload_to="home/about/",
        blank=True,
        null=True,
        help_text=(
            "Primera imagen de la sección Empresa / Experiencia. "
            "Respaldo estático: images/about-img-4.webp."
        ),
    )

    about_image_secondary = models.ImageField(
        "HOME · 03 Empresa · Imagen secundaria",
        upload_to="home/about/",
        blank=True,
        null=True,
        help_text=(
            "Segunda imagen superpuesta de la sección Empresa / Experiencia. "
            "Respaldo estático: images/about-img-5.webp."
        ),
    )


    skill_image = models.ImageField(
        "HOME · 05 Savoir-faire · Imagen principal",
        upload_to="home/skill/",
        blank=True,
        null=True,
        help_text=(
            "Imagen de la sección Notre savoir-faire. "
            "Respaldo estático: images/skill-img-1.webp."
        ),
    )


    testimonials_section_image = models.ImageField(
        "HOME · 07 Testimonios · Imagen grande de sección",
        upload_to="home/testimonials/",
        blank=True,
        null=True,
        help_text=(
            "Imagen grande situada junto al carrusel de testimonios. "
            "Respaldo estático: testi/testi-img-2.webp."
        ),
    )


    contact_image = models.ImageField(
        "HOME · 09 Contacto · Imagen principal",
        upload_to="home/contact/",
        blank=True,
        null=True,
        help_text=(
            "Imagen de la sección de contacto del Home. "
            "Respaldo estático: images/contact-img-1.png."
        ),
    )


    video_url = models.URLField(blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = '002 - Home'
        verbose_name_plural = '002 - Home'

    def __str__(self):
        return self.title_fr

    # WEBP · IMÁGENES PROPIAS DEL HOME | HOME-ONLY IMAGE OPTIMIZATION
    def save(self, *args, **kwargs):
        from .image_utils import optimize_instance_image_fields
        optimize_instance_image_fields(
            self,
            ("about_image_primary", "about_image_secondary", "skill_image", "testimonials_section_image", "contact_image"),
            max_dimension=2200,
            quality=82,
        )
        super().save(*args, **kwargs)


# ============================================================
# PROFESSIONAL PAGE
# PAGE PROFESSIONNELS
#
# Estructura simplificada:
# - La página guarda únicamente el contenido principal.
# - Los contenidos adicionales se crean libremente como bloques.
# - Los servicios existentes se seleccionan sin duplicarlos.
# ============================================================


class ProfessionalPage(TimeStampedModel):
    hero_title_es = models.CharField(
        "Main title",
        max_length=255,
        blank=True,
        help_text="Título principal de la página. Español se utiliza como referencia interna.",
    )
    hero_title_fr = models.CharField(
        "Main title",
        max_length=255,
        help_text="Título principal de la página en francés. Es el idioma principal.",
    )
    hero_title_de = models.CharField(
        "Main title",
        max_length=255,
        blank=True,
        help_text="Título principal de la página en alemán.",
    )
    hero_title_it = models.CharField(
        "Main title",
        max_length=255,
        blank=True,
        help_text="Título principal de la página en italiano.",
    )
    hero_title_en = models.CharField(
        "Main title",
        max_length=255,
        blank=True,
        help_text="Título principal de la página en inglés.",
    )

    hero_text_es = models.TextField(
        "Main text",
        blank=True,
        help_text="Texto introductorio de la página. Español se utiliza como referencia interna.",
    )
    hero_text_fr = models.TextField(
        "Main text",
        blank=True,
        help_text="Texto introductorio de la página en francés.",
    )
    hero_text_de = models.TextField(
        "Main text",
        blank=True,
        help_text="Texto introductorio de la página en alemán.",
    )
    hero_text_it = models.TextField(
        "Main text",
        blank=True,
        help_text="Texto introductorio de la página en italiano.",
    )
    hero_text_en = models.TextField(
        "Main text",
        blank=True,
        help_text="Texto introductorio de la página en inglés.",
    )

    hero_image = models.ImageField(
        "Main image",
        upload_to="professionals/hero/",
        blank=True,
        null=True,
        help_text="Imagen principal de la página de Profesionales.",
    )

    services = models.ManyToManyField(
        "services.Service",
        blank=True,
        related_name="professional_pages",
        verbose_name="Services",
        help_text="Seleccione únicamente los servicios que desea mostrar en la página de Profesionales.",
    )

    is_active = models.BooleanField(
        "Active",
        default=True,
        help_text="Desactive esta opción para ocultar la página.",
    )

    class Meta:
        verbose_name = '016 - Professionals Page'
        verbose_name_plural = '016 - Professionals'

    def __str__(self):
        return self.hero_title_fr or "Professionnels"

    def get_localized_field(self, field_name):
        language = (get_language() or "fr").split("-")[0]

        if language not in ("fr", "de", "it", "en"):
            language = "fr"

        value = getattr(self, f"{field_name}_{language}", "")

        if value:
            return value

        return getattr(self, f"{field_name}_fr", "")


# ============================================================
# PROFESSIONAL BLOCK
#
# Cada bloque es una pieza independiente de contenido.
# Se pueden agregar, quitar y ordenar libremente desde el admin.
# ============================================================


class ProfessionalBlock(TimeStampedModel):
    LAYOUT_TEXT = "text"
    LAYOUT_IMAGE_LEFT = "image_left"
    LAYOUT_IMAGE_RIGHT = "image_right"
    LAYOUT_CARD = "card"
    LAYOUT_CTA = "cta"

    LAYOUT_CHOICES = (
        (LAYOUT_TEXT, "Text"),
        (LAYOUT_IMAGE_LEFT, "Image left"),
        (LAYOUT_IMAGE_RIGHT, "Image right"),
        (LAYOUT_CARD, "Featured card"),
        (LAYOUT_CTA, "Call to action"),
    )

    page = models.ForeignKey(
        ProfessionalPage,
        on_delete=models.CASCADE,
        related_name="blocks",
        verbose_name="Page",
    )

    layout = models.CharField(
        "Layout",
        max_length=30,
        choices=LAYOUT_CHOICES,
        default=LAYOUT_TEXT,
        help_text="Seleccione cómo desea presentar este bloque en la página.",
    )

    title_es = models.CharField(
        "Title",
        max_length=255,
        blank=True,
        help_text="Título del bloque. Español se utiliza como referencia interna.",
    )
    title_fr = models.CharField(
        "Title",
        max_length=255,
        blank=True,
        help_text="Título del bloque en francés.",
    )
    title_de = models.CharField(
        "Title",
        max_length=255,
        blank=True,
        help_text="Título del bloque en alemán.",
    )
    title_it = models.CharField(
        "Title",
        max_length=255,
        blank=True,
        help_text="Título del bloque en italiano.",
    )
    title_en = models.CharField(
        "Title",
        max_length=255,
        blank=True,
        help_text="Título del bloque en inglés.",
    )

    text_es = models.TextField(
        "Content",
        blank=True,
        help_text="Contenido del bloque. Español se utiliza como referencia interna.",
    )
    text_fr = models.TextField(
        "Content",
        blank=True,
        help_text="Contenido del bloque en francés.",
    )
    text_de = models.TextField(
        "Content",
        blank=True,
        help_text="Contenido del bloque en alemán.",
    )
    text_it = models.TextField(
        "Content",
        blank=True,
        help_text="Contenido del bloque en italiano.",
    )
    text_en = models.TextField(
        "Content",
        blank=True,
        help_text="Contenido del bloque en inglés.",
    )

    image = models.ImageField(
        "Image",
        upload_to="professionals/blocks/",
        blank=True,
        null=True,
        help_text="Opcional. Se utiliza especialmente en los diseños con imagen.",
    )

    icon = models.CharField(
        "Icon",
        max_length=100,
        blank=True,
        help_text="Opcional. Clase de Font Awesome, por ejemplo: fa-solid fa-building.",
    )

    order = models.PositiveIntegerField(
        "Order",
        default=0,
        help_text="Los números más bajos aparecen primero.",
    )

    is_active = models.BooleanField(
        "Active",
        default=True,
        help_text="Permite mostrar u ocultar este bloque sin eliminarlo.",
    )

    class Meta:
        verbose_name = '017 - Professionals Block'
        verbose_name_plural = '017 - Professionals Blocks'
        ordering = ["order", "id"]

    def __str__(self):
        return self.title_fr or f"Bloque {self.pk or ''}".strip()

    def get_localized_field(self, field_name):
        language = (get_language() or "fr").split("-")[0]

        if language not in ("fr", "de", "it", "en"):
            language = "fr"

        value = getattr(self, f"{field_name}_{language}", "")

        if value:
            return value

        return getattr(self, f"{field_name}_fr", "")


from .visual_config import AboutPageConfiguration, ProfessionalPageConfiguration  # noqa: F401,E402
