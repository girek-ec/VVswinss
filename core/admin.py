from django.contrib import admin

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
)


# ============================================================
# SITE CONFIGURATION
# ============================================================

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ("company_name", "legal_name", "city", "canton", "country", "phone", "email", "is_active")
    list_filter = ("is_active", "country", "canton")
    search_fields = ("company_name", "legal_name", "uid_number", "city", "canton", "country", "email", "phone")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Empresa", {
            "fields": ("company_name", "logo", "white_logo", "favicon")
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
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Configuration", {
            "fields": ("is_active", "image"),
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

        ("Dates", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )


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
    list_display = ("name_fr", "name_es", "order", "is_active")
    list_display_links = ("name_fr",)
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name_es", "name_fr", "name_de", "name_it", "name_en")
    ordering = ("order", "name_fr")


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
    list_display = ("title_es", "title_fr", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title_es", "title_fr", "title_de", "title_it", "title_en")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("🇪🇸 Español · Referencia interna", {
            "fields": ("title_es", "subtitle_es")
        }),

        ("🇫🇷 Français · Principal", {
            "fields": ("title_fr", "subtitle_fr")
        }),

        ("🇩🇪 Deutsch", {
            "fields": ("title_de", "subtitle_de")
        }),

        ("🇮🇹 Italiano", {
            "fields": ("title_it", "subtitle_it")
        }),

        ("🇬🇧 English", {
            "fields": ("title_en", "subtitle_en")
        }),

        ("Multimedia", {
            "fields": ("hero_image", "video_url")
        }),

        ("Publicación", {
            "fields": ("is_active",)
        }),

        ("Sistema", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at")
        }),
    )


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