from django.contrib import admin
from django.utils.html import format_html
from .visual_config import AboutPageConfiguration

from .models import (
    AboutContent,
    BusinessHour,
    Certification,
    CompanyValue,
    FAQ,
    FAQCategory,
    HomeContent,
    Insurance,
    InstitutionalPage,
    ProcessStep,
    ServiceArea,
    SiteConfiguration,
    SocialLink,
    Statistic,
    TeamMember,
    Testimonial,
    ProfessionalPage,
    ProfessionalBlock,
)

# ============================================================
# SITE CONFIGURATION
# ============================================================

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ("company_name", "legal_name", "city", "canton", "country", "phone", "email", "is_active")
    list_filter = ("is_active", "country", "canton")
    search_fields = ("company_name", "legal_name", "uid_number", "city", "canton", "country", "email", "phone")
    readonly_fields = (
        "footer_background_preview",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Empresa", {
            "fields": ("company_name", "logo", "white_logo", "favicon")
        }),

        ("Preloader / Transición de páginas", {
            "fields": (
                "preloader_background",
            ),
            "description": (
                "Imagen de fondo mostrada mientras se carga o cambia de página. "
                "Se recomienda una imagen horizontal 16:9."
            ),
        }),

        ("Pie de página · Fondo global", {
            "fields": (
                "footer_background",
                "footer_background_preview",
            ),
            "description": (
                "Imagen de fondo que aparece detrás de todo el pie de página. "
                "Si no se carga ninguna imagen, se mantiene automáticamente "
                "static/antra/assets/img/bg-img/footer-bg.webp. "
                "Recomendado: fotografía horizontal 16:9 de al menos 1600 px."
            ),
        }),

        ("🇪🇸 Español · Referencia interna", {
            "fields": ("slogan_es",)
        }),

        ("🇫🇷 Français · Principal", {
            "fields": ("slogan_fr",)
        }),

        ("🇩🇪 Deutsch", {
            "fields": ("slogan_de",)
        }),

        ("🇮🇹 Italiano", {
            "fields": ("slogan_it",)
        }),

        ("🇬🇧 English", {
            "fields": ("slogan_en",)
        }),

        ("Contacto", {
            "fields": ("phone", "whatsapp", "email")
        }),

        ("Ubicación", {
            "fields": ("address", "postal_code", "city", "canton", "country", "latitude", "longitude")
        }),

        ("Información legal · Mentions légales / Impressum", {
            "fields": ("legal_name", "legal_form", "uid_number", "vat_number", "commercial_register", "legal_representative", "insurance_info")
        }),

        ("Protección de datos · nLPD", {
            "fields": ("privacy_email",),
            "description": "Datos utilizados como referencia de contacto para solicitudes relacionadas con la protección de datos personales."
        }),

        ("Alojamiento web · Hébergement", {
            "fields": ("hosting_provider", "hosting_address", "hosting_country"),
            "description": "Información del proveedor donde se encuentra alojado el sitio web y, cuando corresponda, los datos asociados al servicio."
        }),

        ("Estado", {
            "fields": ("is_active",)
        }),

        ("Sistema", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at")
        }),
    )

# ============================================================
# SOCIAL LINKS
# ============================================================

    @admin.display(description="Vista previa · Fondo del pie de página")
    def footer_background_preview(self, obj):
        if not obj or not obj.footer_background:
            return "Sin imagen cargada · se utilizará el fondo estático del footer."

        try:
            return format_html(
                '<img src="{}" style="max-width:520px;max-height:260px;'
                'width:auto;height:auto;object-fit:contain;border-radius:8px;'
                'border:1px solid #ddd;background:#111;padding:4px;" />',
                obj.footer_background.url,
            )
        except (ValueError, AttributeError):
            return "Sin imagen cargada · se utilizará el fondo estático del footer."


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name", "url")
    ordering = ("order", "name")
    readonly_fields = ("created_at", "updated_at")

# ============================================================
# ABOUT CONTENT
# ============================================================

@admin.register(AboutContent)
class AboutContentAdmin(admin.ModelAdmin):
    list_display = ("intro_title_fr", "is_active", "updated_at")
    list_filter = ("is_active",)
    readonly_fields = ("image_preview", "video_image_preview", "created_at", "updated_at")

    fieldsets = (
        ("Configuration", {
            "fields": ("is_active", "image", "image_preview"),
        }),
        ("Présentation · ES", {
            "fields": ("intro_title_es", "intro_text_es"),
            "classes": ("collapse",),
        }),
        ("Présentation · FR", {
            "fields": ("intro_title_fr", "intro_text_fr"),
        }),
        ("Présentation · DE", {
            "fields": ("intro_title_de", "intro_text_de"),
            "classes": ("collapse",),
        }),
        ("Présentation · IT", {
            "fields": ("intro_title_it", "intro_text_it"),
            "classes": ("collapse",),
        }),
        ("Présentation · EN", {
            "fields": ("intro_title_en", "intro_text_en"),
            "classes": ("collapse",),
        }),
        ("Mission · ES", {
            "fields": ("mission_es",),
            "classes": ("collapse",),
        }),
        ("Mission · FR", {
            "fields": ("mission_fr",),
        }),
        ("Mission · DE", {
            "fields": ("mission_de",),
            "classes": ("collapse",),
        }),
        ("Mission · IT", {
            "fields": ("mission_it",),
            "classes": ("collapse",),
        }),
        ("Mission · EN", {
            "fields": ("mission_en",),
            "classes": ("collapse",),
        }),
        ("Vision · ES", {
            "fields": ("vision_es",),
            "classes": ("collapse",),
        }),
        ("Vision · FR", {
            "fields": ("vision_fr",),
        }),
        ("Vision · DE", {
            "fields": ("vision_de",),
            "classes": ("collapse",),
        }),
        ("Vision · IT", {
            "fields": ("vision_it",),
            "classes": ("collapse",),
        }),
        ("Vision · EN", {
            "fields": ("vision_en",),
            "classes": ("collapse",),
        }),
        ("Histoire · ES", {
            "fields": ("history_es",),
            "classes": ("collapse",),
        }),
        ("Histoire · FR", {
            "fields": ("history_fr",),
        }),
        ("Histoire · DE", {
            "fields": ("history_de",),
            "classes": ("collapse",),
        }),
        ("Histoire · IT", {
            "fields": ("history_it",),
            "classes": ("collapse",),
        }),
        ("Histoire · EN", {
            "fields": ("history_en",),
            "classes": ("collapse",),
        }),
        ("Multimedia · vídeo", {
            "description": "Configure el vídeo de la sección Sobre nosotros. Si existe una URL de vídeo, se mostrará el botón de reproducción. Si no existe, se mostrará únicamente la imagen cargada.",
            "fields": ("video_url", "video_image", "video_image_preview"),
        }),
        ("Sistema", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="Vista previa · imagen principal")
    def image_preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" style="max-height:220px;max-width:420px;object-fit:cover;border-radius:6px;" />', obj.image.url)
        return "—"

    @admin.display(description="Vista previa · imagen del vídeo")
    def video_image_preview(self, obj):
        if obj and obj.video_image:
            return format_html('<img src="{}" style="max-height:220px;max-width:420px;object-fit:cover;border-radius:6px;" />', obj.video_image.url)
        return "—"

# ============================================================
# BUSINESS HOURS
# ============================================================

@admin.register(BusinessHour)
class BusinessHourAdmin(admin.ModelAdmin):
    list_display = ("day_fr", "hours", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Días", {
            "fields": ("day_fr", "day_de", "day_it", "day_en")
        }),

        ("Horario", {
            "fields": ("hours", "order", "is_active")
        }),

        ("Sistema", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at")
        }),
    )

# ============================================================
# SERVICE AREA
# ============================================================

@admin.register(ServiceArea)
class ServiceAreaAdmin(admin.ModelAdmin):
    list_display = ("name", "canton", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name", "canton", "description_es", "description_fr")
    ordering = ("order", "name")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Zona de servicio", {
            "fields": ("name", "canton")
        }),

        ("🇪🇸 Español · Referencia interna", {
            "fields": ("description_es",)
        }),

        ("🇫🇷 Français · Principal", {
            "fields": ("description_fr",)
        }),

        ("🇩🇪 Deutsch", {
            "fields": ("description_de",)
        }),

        ("🇮🇹 Italiano", {
            "fields": ("description_it",)
        }),

        ("🇬🇧 English", {
            "fields": ("description_en",)
        }),

        ("Configuración", {
            "fields": ("order", "is_active")
        }),

        ("Sistema", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at")
        }),
    )

# ============================================================
# PROCESS STEP
# ============================================================

@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ("number", "title_es", "title_fr", "is_active")
    list_editable = ("is_active",)
    ordering = ("number",)
    search_fields = ("title_es", "title_fr", "title_de", "title_it", "title_en")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Configuración", {
            "fields": ("number", "icon", "is_active")
        }),

        ("🇪🇸 Español · Referencia interna", {
            "fields": ("title_es",)
        }),

        ("🇫🇷 Français · Principal", {
            "fields": ("title_fr", "description_fr")
        }),

        ("🇩🇪 Deutsch", {
            "fields": ("title_de", "description_de")
        }),

        ("🇮🇹 Italiano", {
            "fields": ("title_it", "description_it")
        }),

        ("🇬🇧 English", {
            "fields": ("title_en", "description_en")
        }),

        ("Sistema", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at")
        }),
    )

# ============================================================
# TEAM MEMBER
# ============================================================

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "position_fr", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order", "name")
    search_fields = ("name", "position_fr", "position_de", "position_it", "position_en")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Miembro", {
            "fields": ("name", "photo", "email", "phone")
        }),

        ("🇫🇷 Français · Principal", {
            "fields": ("position_fr", "biography_fr")
        }),

        ("🇩🇪 Deutsch", {
            "fields": ("position_de", "biography_de")
        }),

        ("🇮🇹 Italiano", {
            "fields": ("position_it", "biography_it")
        }),

        ("🇬🇧 English", {
            "fields": ("position_en", "biography_en")
        }),

        ("Configuración", {
            "fields": ("order", "is_active")
        }),

        ("Sistema", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at")
        }),
    )

# ============================================================
# INSURANCE
# ============================================================

@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = (
        "image_preview_list",
        "name_fr",
        "name_es",
        "order",
        "is_active",
    )
    list_display_links = ("name_fr",)
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name_es", "name_fr", "name_de", "name_it", "name_en")
    ordering = ("order", "name_fr")
    readonly_fields = ("image_preview", "created_at", "updated_at")

    fieldsets = (
        ("Imagen y documentos", {
            "fields": (
                "image",
                "image_preview",
                "pdf",
                "url",
            ),
            "description": (
                "Si no se carga una imagen propia, se mostrará automáticamente "
                "la imagen por defecto configurada en «Configuración visual · About»."
            ),
        }),
        ("🇪🇸 Español · Referencia interna", {
            "fields": ("name_es", "description_es"),
            "classes": ("collapse",),
        }),
        ("🇫🇷 Français · Principal", {
            "fields": ("name_fr", "description_fr"),
        }),
        ("🇩🇪 Deutsch", {
            "fields": ("name_de", "description_de"),
            "classes": ("collapse",),
        }),
        ("🇮🇹 Italiano", {
            "fields": ("name_it", "description_it"),
            "classes": ("collapse",),
        }),
        ("🇬🇧 English", {
            "fields": ("name_en", "description_en"),
            "classes": ("collapse",),
        }),
        ("Configuración", {
            "fields": ("order", "is_active"),
        }),
        ("Sistema", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at"),
        }),
    )

    @staticmethod
    def _get_effective_image(obj):
        if obj and obj.image:
            return obj.image, False

        config = AboutPageConfiguration.objects.first()
        default_image = getattr(config, "insurance_default_image", None) if config else None

        if default_image:
            return default_image, True

        return None, False

    @admin.display(description="Imagen")
    def image_preview_list(self, obj):
        image, is_default = self._get_effective_image(obj)

        if not image:
            return "—"

        try:
            border = "2px solid #d4a72c" if is_default else "1px solid #ddd"

            return format_html(
                '<img src="{}" style="height:55px;width:80px;'
                'object-fit:cover;border-radius:6px;border:{};" '
                'title="{}" />',
                image.url,
                border,
                "Imagen por defecto de About" if is_default else "Imagen propia",
            )
        except (ValueError, AttributeError):
            return "—"

    @admin.display(description="Vista previa")
    def image_preview(self, obj):
        image, is_default = self._get_effective_image(obj)

        if not image:
            return format_html(
                '<div style="padding:12px;border:1px dashed #bbb;border-radius:8px;'
                'max-width:420px;">Sin imagen propia ni imagen por defecto configurada.</div>'
            )

        try:
            label = (
                "IMAGEN POR DEFECTO · Configuración visual · About"
                if is_default
                else "IMAGEN PROPIA · Insurance"
            )

            return format_html(
                '<div style="max-width:420px;">'
                '<div style="margin-bottom:8px;font-size:12px;font-weight:600;">{}</div>'
                '<img src="{}" style="max-width:420px;max-height:230px;'
                'width:auto;height:auto;object-fit:contain;border-radius:8px;'
                'border:1px solid #ddd;padding:4px;background:#f7f7f7;" />'
                '</div>',
                label,
                image.url,
            )
        except (ValueError, AttributeError):
            return "—"
# ============================================================
# CERTIFICATION
# ============================================================

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ("name", "issuer", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order", "name")
    search_fields = ("name", "issuer")
    readonly_fields = ("created_at", "updated_at")

# ============================================================
# STATISTIC
# ============================================================

@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ("value", "title_es", "title_fr", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order",)
    search_fields = ("value", "title_es", "title_fr")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Valor", {
            "fields": ("value", "order", "is_active")
        }),

        ("🇪🇸 Español · Referencia interna", {
            "fields": ("title_es",)
        }),

        ("🇫🇷 Français · Principal", {
            "fields": ("title_fr",)
        }),

        ("🇩🇪 Deutsch", {
            "fields": ("title_de",)
        }),

        ("🇮🇹 Italiano", {
            "fields": ("title_it",)
        }),

        ("🇬🇧 English", {
            "fields": ("title_en",)
        }),

        ("Sistema", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at")
        }),
    )

# ============================================================
# TESTIMONIAL
# ============================================================

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "rating", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order", "-created_at")
    search_fields = ("name", "company", "text_es", "text_fr")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Cliente", {
            "fields": ("name", "company", "photo", "rating")
        }),

        ("🇪🇸 Español · Referencia interna", {
            "fields": ("text_es",)
        }),

        ("🇫🇷 Français · Principal", {
            "fields": ("text_fr",)
        }),

        ("🇩🇪 Deutsch", {
            "fields": ("text_de",)
        }),

        ("🇮🇹 Italiano", {
            "fields": ("text_it",)
        }),

        ("🇬🇧 English", {
            "fields": ("text_en",)
        }),

        ("Configuración", {
            "fields": ("order", "is_active")
        }),

        ("Sistema", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at")
        }),
    )

# ============================================================
# FAQ CATEGORY
# ============================================================

@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ("name_es", "name_fr", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order", "name_fr")
    search_fields = ("name_es", "name_fr", "name_de", "name_it", "name_en")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("🇪🇸 Español · Referencia interna", {
            "fields": ("name_es",)
        }),

        ("🇫🇷 Français · Principal", {
            "fields": ("name_fr",)
        }),

        ("🇩🇪 Deutsch", {
            "fields": ("name_de",)
        }),

        ("🇮🇹 Italiano", {
            "fields": ("name_it",)
        }),

        ("🇬🇧 English", {
            "fields": ("name_en",)
        }),

        ("Configuración", {
            "fields": ("order", "is_active")
        }),

        ("Sistema", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at")
        }),
    )

# ============================================================
# FAQ
# ============================================================

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question_fr", "category", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("category", "is_active")
    ordering = ("order", "question_fr")
    search_fields = ("question_fr", "question_de", "question_it", "question_en")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Configuración", {
            "fields": ("category", "order", "is_active")
        }),

        ("🇫🇷 Français · Principal", {
            "fields": ("question_fr", "answer_fr")
        }),

        ("🇩🇪 Deutsch", {
            "fields": ("question_de", "answer_de")
        }),

        ("🇮🇹 Italiano", {
            "fields": ("question_it", "answer_it")
        }),

        ("🇬🇧 English", {
            "fields": ("question_en", "answer_en")
        }),

        ("Sistema", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at")
        }),
    )

# ============================================================
# INSTITUTIONAL PAGE
#
# Incluye:
# - Entreprise
# - Mentions légales / Impressum
# - Protection des données / nLPD
# - Otras páginas institucionales
# ============================================================

@admin.register(InstitutionalPage)
class InstitutionalPageAdmin(admin.ModelAdmin):
    list_display = ("title_es", "title_fr", "slug_fr", "is_active", "is_indexable")
    list_filter = ("is_active", "is_indexable")
    search_fields = ("title_es", "title_fr", "title_de", "title_it", "title_en", "slug_fr", "slug_de", "slug_it", "slug_en")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("🇪🇸 Español · Referencia interna", {
            "fields": ("title_es", "content_es", "seo_title_es", "meta_description_es")
        }),

        ("🇫🇷 Français · Principal", {
            "fields": ("title_fr", "slug_fr", "content_fr", "seo_title_fr", "meta_description_fr")
        }),

        ("🇩🇪 Deutsch", {
            "fields": ("title_de", "slug_de", "content_de", "seo_title_de", "meta_description_de")
        }),

        ("🇮🇹 Italiano", {
            "fields": ("title_it", "slug_it", "content_it", "seo_title_it", "meta_description_it")
        }),

        ("🇬🇧 English", {
            "fields": ("title_en", "slug_en", "content_en", "seo_title_en", "meta_description_en")
        }),

        ("Imagen y SEO social", {
            "fields": ("image", "og_image")
        }),

        ("Publicación", {
            "fields": ("is_active", "is_indexable")
        }),

        ("Sistema", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at")
        }),
    )

# ============================================================
# HOME CONTENT
# ============================================================

@admin.register(HomeContent)
class HomeContentAdmin(admin.ModelAdmin):
    list_display = (
        "title_fr",
        "home_images_status",
        "is_active",
        "updated_at",
    )
    list_filter = ("is_active",)
    search_fields = ("title_es", "title_fr", "title_de", "title_it", "title_en")

    readonly_fields = (
        "hero_image_preview",
        "services_default_image_preview",
        "about_image_primary_preview",
        "about_image_secondary_preview",
        "values_default_image_preview",
        "skill_image_preview",
        "before_fallback_image_preview",
        "after_fallback_image_preview",
        "testimonials_section_image_preview",
        "testimonial_avatar_default_preview",
        "contact_image_preview",
        "blog_default_image_preview",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("🇪🇸 Español · Referencia interna", {
            "fields": ("title_es", "subtitle_es"),
            "classes": ("collapse",),
        }),

        ("🇫🇷 Français · Principal", {
            "fields": ("title_fr", "subtitle_fr"),
        }),

        ("🇩🇪 Deutsch", {
            "fields": ("title_de", "subtitle_de"),
            "classes": ("collapse",),
        }),

        ("🇮🇹 Italiano", {
            "fields": ("title_it", "subtitle_it"),
            "classes": ("collapse",),
        }),

        ("🇬🇧 English", {
            "fields": ("title_en", "subtitle_en"),
            "classes": ("collapse",),
        }),

        ("HOME · 01 · HERO", {
            "description": (
                "Imagen de respaldo del Hero. Las categorías conservan prioridad: "
                "si una categoría tiene su propia imagen, esa imagen se mostrará. "
                "Si no la tiene, se usará esta; y si esta también está vacía, "
                "se mostrará images/hero-img-1.webp."
            ),
            "fields": (
                "hero_image",
                "hero_image_preview",
            ),
        }),

        ("HOME · 02 · SERVICIOS / CATEGORÍAS", {
            "description": (
                "Imagen de respaldo de las tarjetas de categorías del Home. "
                "Solo aparece cuando una categoría no tiene imagen propia."
            ),
            "fields": (
                "services_default_image",
                "services_default_image_preview",
            ),
        }),

        ("HOME · 03 · EMPRESA / EXPERIENCIA", {
            "description": (
                "Las dos fotografías superpuestas de la sección Empresa. "
                "La principal corresponde a about-img-4 y la secundaria a about-img-5."
            ),
            "fields": (
                "about_image_primary",
                "about_image_primary_preview",
                "about_image_secondary",
                "about_image_secondary_preview",
            ),
        }),

        ("HOME · 04 · VALORES", {
            "description": (
                "Imagen de respaldo para un valor empresarial que no tenga una "
                "imagen propia configurada en Company Value."
            ),
            "fields": (
                "values_default_image",
                "values_default_image_preview",
            ),
        }),

        ("HOME · 05 · SAVOIR-FAIRE", {
            "description": (
                "Fotografía principal de la sección Notre savoir-faire."
            ),
            "fields": (
                "skill_image",
                "skill_image_preview",
            ),
        }),

        ("HOME · 06 · ÚLTIMA REALIZACIÓN · ANTES / DESPUÉS", {
            "description": (
                "Imágenes de respaldo del comparador Antes/Después. "
                "Las imágenes cargadas en el propio proyecto tienen prioridad."
            ),
            "fields": (
                "before_fallback_image",
                "before_fallback_image_preview",
                "after_fallback_image",
                "after_fallback_image_preview",
            ),
        }),

        ("HOME · 07 · TESTIMONIOS", {
            "description": (
                "Imagen grande de la sección y avatar de respaldo para testimonios "
                "sin fotografía."
            ),
            "fields": (
                "testimonials_section_image",
                "testimonials_section_image_preview",
                "testimonial_avatar_default",
                "testimonial_avatar_default_preview",
            ),
        }),

        ("HOME · 09 · CONTACTO", {
            "description": (
                "Fotografía de la sección de contacto situada junto al formulario."
            ),
            "fields": (
                "contact_image",
                "contact_image_preview",
            ),
        }),

        ("HOME · 10 · BLOG / ACTUALIDAD", {
            "description": (
                "Imagen utilizada cuando una entrada del blog no tiene main_image."
            ),
            "fields": (
                "blog_default_image",
                "blog_default_image_preview",
            ),
        }),

        ("Multimedia adicional", {
            "fields": ("video_url",),
            "classes": ("collapse",),
        }),

        ("Publicación", {
            "fields": ("is_active",)
        }),

        ("Sistema", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at")
        }),
    )

    @staticmethod
    def _render_home_preview(field, max_width=360, max_height=210):
        if not field:
            return "Sin imagen cargada · se utilizará el respaldo de /static/."

        try:
            return format_html(
                '<img src="{}" style="max-width:{}px;max-height:{}px;'
                'width:auto;height:auto;object-fit:contain;border-radius:8px;'
                'border:1px solid #ddd;background:#f7f7f7;padding:4px;" />',
                field.url,
                max_width,
                max_height,
            )
        except (ValueError, AttributeError):
            return "Sin imagen cargada · se utilizará el respaldo de /static/."

    @admin.display(description="Vista previa · Hero")
    def hero_image_preview(self, obj):
        return self._render_home_preview(obj.hero_image if obj else None)

    @admin.display(description="Vista previa · Servicios")
    def services_default_image_preview(self, obj):
        return self._render_home_preview(obj.services_default_image if obj else None)

    @admin.display(description="Vista previa · Empresa principal")
    def about_image_primary_preview(self, obj):
        return self._render_home_preview(obj.about_image_primary if obj else None)

    @admin.display(description="Vista previa · Empresa secundaria")
    def about_image_secondary_preview(self, obj):
        return self._render_home_preview(obj.about_image_secondary if obj else None)

    @admin.display(description="Vista previa · Valores")
    def values_default_image_preview(self, obj):
        return self._render_home_preview(obj.values_default_image if obj else None)

    @admin.display(description="Vista previa · Savoir-faire")
    def skill_image_preview(self, obj):
        return self._render_home_preview(obj.skill_image if obj else None)

    @admin.display(description="Vista previa · Antes")
    def before_fallback_image_preview(self, obj):
        return self._render_home_preview(obj.before_fallback_image if obj else None)

    @admin.display(description="Vista previa · Después")
    def after_fallback_image_preview(self, obj):
        return self._render_home_preview(obj.after_fallback_image if obj else None)

    @admin.display(description="Vista previa · Testimonios")
    def testimonials_section_image_preview(self, obj):
        return self._render_home_preview(obj.testimonials_section_image if obj else None)

    @admin.display(description="Vista previa · Avatar de testimonio")
    def testimonial_avatar_default_preview(self, obj):
        return self._render_home_preview(
            obj.testimonial_avatar_default if obj else None,
            max_width=160,
            max_height=160,
        )

    @admin.display(description="Vista previa · Contacto")
    def contact_image_preview(self, obj):
        return self._render_home_preview(obj.contact_image if obj else None)

    @admin.display(description="Vista previa · Blog")
    def blog_default_image_preview(self, obj):
        return self._render_home_preview(obj.blog_default_image if obj else None)

    @admin.display(description="Imágenes Home")
    def home_images_status(self, obj):
        image_fields = (
            "hero_image",
            "services_default_image",
            "about_image_primary",
            "about_image_secondary",
            "values_default_image",
            "skill_image",
            "before_fallback_image",
            "after_fallback_image",
            "testimonials_section_image",
            "testimonial_avatar_default",
            "contact_image",
            "blog_default_image",
        )
        loaded = sum(bool(getattr(obj, field_name, None)) for field_name in image_fields)
        return f"{loaded}/{len(image_fields)} personalizadas"

# ============================================================
# COMPANY VALUE
# ============================================================

@admin.register(CompanyValue)
class CompanyValueAdmin(admin.ModelAdmin):
    list_display = ("title_es", "title_fr", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order",)
    search_fields = ("title_es", "title_fr", "title_de", "title_it", "title_en")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("🇪🇸 Español · Referencia interna", {
            "fields": ("title_es", "description_es")
        }),

        ("🇫🇷 Français · Principal", {
            "fields": ("title_fr", "description_fr")
        }),

        ("🇩🇪 Deutsch", {
            "fields": ("title_de", "description_de")
        }),

        ("🇮🇹 Italiano", {
            "fields": ("title_it", "description_it")
        }),

        ("🇬🇧 English", {
            "fields": ("title_en", "description_en")
        }),

        ("Imagen", {
            "fields": ("image",)
        }),

        ("Configuración", {
            "fields": ("order", "is_active")
        }),

        ("Sistema", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at")
        }),
    )

# ============================================================
# PROFESSIONNELS · BLOQUES DE CONTENIDO
# ============================================================


class ProfessionalBlockInline(admin.StackedInline):
    model = ProfessionalBlock
    extra = 0
    show_change_link = True

    fieldsets = (
        ("Configuración del bloque", {
            "fields": ("layout", "image", "icon", "order", "is_active"),
            "description": "Agregue únicamente lo que necesite. La imagen y el icono son opcionales.",
        }),

        ("🇫🇷 Français · Principal", {
            "fields": ("title_fr", "text_fr"),
            "description": "Contenido principal en francés para la Suisse romande.",
        }),

        ("🇩🇪 Deutsch", {
            "fields": ("title_de", "text_de"),
            "classes": ("collapse",),
        }),

        ("🇮🇹 Italiano", {
            "fields": ("title_it", "text_it"),
            "classes": ("collapse",),
        }),

        ("🇬🇧 English", {
            "fields": ("title_en", "text_en"),
            "classes": ("collapse",),
        }),

        ("🇪🇸 Español · Referencia interna", {
            "fields": ("title_es", "text_es"),
            "classes": ("collapse",),
            "description": "Referencia administrativa interna. No es el idioma público principal.",
        }),
    )


# ============================================================
# PROFESSIONNELS · PÁGINA
# ============================================================


@admin.register(ProfessionalPage)
class ProfessionalPageAdmin(admin.ModelAdmin):
    inlines = (ProfessionalBlockInline,)

    list_display = ("hero_title_fr", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = (
        "hero_title_es",
        "hero_title_fr",
        "hero_title_de",
        "hero_title_it",
        "hero_title_en",
    )
    readonly_fields = ("created_at", "updated_at")
    filter_horizontal = ("services",)

    fieldsets = (
        ("Configuración", {
            "fields": ("is_active", "hero_image", "services"),
            "description": (
                "Configuración básica. Los contenidos adicionales se agregan "
                "más abajo como bloques independientes."
            ),
        }),

        ("🇫🇷 Français · Principal", {
            "fields": ("hero_title_fr", "hero_text_fr"),
            "description": "Contenido principal en francés para la Suisse romande.",
        }),

        ("🇩🇪 Deutsch", {
            "fields": ("hero_title_de", "hero_text_de"),
            "classes": ("collapse",),
        }),

        ("🇮🇹 Italiano", {
            "fields": ("hero_title_it", "hero_text_it"),
            "classes": ("collapse",),
        }),

        ("🇬🇧 English", {
            "fields": ("hero_title_en", "hero_text_en"),
            "classes": ("collapse",),
        }),

        ("🇪🇸 Español · Referencia interna", {
            "fields": ("hero_title_es", "hero_text_es"),
            "classes": ("collapse",),
            "description": "Referencia administrativa interna. No es el idioma público principal.",
        }),

        ("Sistema", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )


@admin.register(ProfessionalBlock)
class ProfessionalBlockAdmin(admin.ModelAdmin):
    list_display = ("title_fr", "page", "layout", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("layout", "is_active")
    search_fields = ("title_fr", "title_de", "title_it", "title_en", "title_es")
    ordering = ("page", "order", "id")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Configuración del bloque", {
            "fields": ("page", "layout", "image", "icon", "order", "is_active"),
        }),
        ("🇫🇷 Français · Principal", {
            "fields": ("title_fr", "text_fr"),
        }),
        ("🇩🇪 Deutsch", {
            "fields": ("title_de", "text_de"),
            "classes": ("collapse",),
        }),
        ("🇮🇹 Italiano", {
            "fields": ("title_it", "text_it"),
            "classes": ("collapse",),
        }),
        ("🇬🇧 English", {
            "fields": ("title_en", "text_en"),
            "classes": ("collapse",),
        }),
        ("🇪🇸 Español · Referencia interna", {
            "fields": ("title_es", "text_es"),
            "classes": ("collapse",),
        }),
        ("Sistema", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )


from . import visual_config_admin  # noqa: F401,E402
