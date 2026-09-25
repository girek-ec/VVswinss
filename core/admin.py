from django.contrib import admin
from django.utils.html import format_html

from .models import (
    BusinessHour,
    Certification,
    FAQ,
    FAQCategory,
    HomeContent,
    InstitutionalPage,
    ProcessStep,
    ServiceArea,
    SiteConfiguration,
    SocialLink,
    Statistic,
    TeamMember,
    Testimonial,
)


admin.site.site_header = "VVswinss | Administración"
admin.site.site_title = "VVswinss"
admin.site.index_title = "Gestión del sitio web"


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = (
        "nombre_empresa",
        "ciudad",
        "pais",
        "telefono",
        "email",
        "activo",
    )

    list_filter = ("activo", "pais")

    search_fields = (
        "nombre_empresa",
        "ciudad",
        "email",
        "telefono",
    )

    readonly_fields = (
        "logo_preview",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Empresa",
            {
                "fields": (
                    "nombre_empresa",
                    "slogan_fr",
                    "slogan_es",
                    "slogan_en",
                )
            },
        ),
        (
            "Identidad visual",
            {
                "fields": (
                    "logo",
                    "logo_preview",
                    "logo_blanco",
                    "favicon",
                )
            },
        ),
        (
            "Contacto",
            {
                "fields": (
                    "telefono",
                    "whatsapp",
                    "email",
                    "direccion",
                    "ciudad",
                    "canton",
                    "pais",
                )
            },
        ),
        (
            "Ubicación",
            {
                "fields": (
                    "latitude",
                    "longitude",
                )
            },
        ),
        (
            "Estado",
            {
                "fields": (
                    "activo",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    @admin.display(description="Vista previa")
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-height:80px; max-width:180px;" />',
                obj.logo.url,
            )
        return "Sin imagen"


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("nombre", "url", "orden", "activo")
    list_editable = ("orden", "activo")
    search_fields = ("nombre", "url")
    ordering = ("orden",)


@admin.register(BusinessHour)
class BusinessHourAdmin(admin.ModelAdmin):
    list_display = ("dia_fr", "horario", "orden", "activo")
    list_editable = ("horario", "orden", "activo")
    ordering = ("orden",)


@admin.register(ServiceArea)
class ServiceAreaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "canton", "orden", "activo")
    list_editable = ("orden", "activo")
    search_fields = ("nombre", "canton")
    ordering = ("orden",)


@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ("numero", "titulo_fr", "activo")
    list_editable = ("activo",)
    search_fields = ("titulo_fr", "titulo_es", "titulo_en")
    ordering = ("numero",)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "cargo_fr",
        "email",
        "orden",
        "activo",
    )

    list_editable = ("orden", "activo")

    search_fields = (
        "nombre",
        "cargo_fr",
        "cargo_es",
        "cargo_en",
        "email",
    )

    ordering = ("orden",)


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "entidad",
        "orden",
        "activo",
    )

    list_editable = ("orden", "activo")
    search_fields = ("nombre", "entidad")
    ordering = ("orden",)


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = (
        "valor",
        "titulo_fr",
        "orden",
        "activo",
    )

    list_editable = ("orden", "activo")
    ordering = ("orden",)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "empresa",
        "valoracion",
        "orden",
        "activo",
    )

    list_filter = ("valoracion", "activo")
    list_editable = ("orden", "activo")
    search_fields = ("nombre", "empresa", "texto_fr")


@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ("nombre_fr", "orden", "activo")
    list_editable = ("orden", "activo")
    search_fields = ("nombre_fr", "nombre_es", "nombre_en")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = (
        "pregunta_fr",
        "categoria",
        "orden",
        "activo",
    )

    list_filter = ("categoria", "activo")
    list_editable = ("orden", "activo")

    search_fields = (
        "pregunta_fr",
        "pregunta_es",
        "pregunta_en",
        "respuesta_fr",
    )


@admin.register(InstitutionalPage)
class InstitutionalPageAdmin(admin.ModelAdmin):
    list_display = (
        "titulo_fr",
        "slug_fr",
        "activo",
        "indexar",
        "updated_at",
    )

    list_filter = (
        "activo",
        "indexar",
    )

    search_fields = (
        "titulo_fr",
        "titulo_es",
        "titulo_en",
        "contenido_fr",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Francés",
            {
                "fields": (
                    "titulo_fr",
                    "slug_fr",
                    "contenido_fr",
                )
            },
        ),
        (
            "Español",
            {
                "fields": (
                    "titulo_es",
                    "slug_es",
                    "contenido_es",
                )
            },
        ),
        (
            "English",
            {
                "fields": (
                    "titulo_en",
                    "slug_en",
                    "contenido_en",
                )
            },
        ),
        (
            "Imagen",
            {
                "fields": ("imagen",)
            },
        ),
        (
            "SEO",
            {
                "fields": (
                    "seo_titulo_fr",
                    "seo_titulo_es",
                    "seo_titulo_en",
                    "meta_descripcion_fr",
                    "meta_descripcion_es",
                    "meta_descripcion_en",
                    "og_imagen",
                    "indexar",
                )
            },
        ),
        (
            "Estado",
            {
                "fields": (
                    "activo",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


@admin.register(HomeContent)
class HomeContentAdmin(admin.ModelAdmin):
    list_display = (
        "titulo_fr",
        "activo",
        "updated_at",
    )

    list_filter = ("activo",)

    search_fields = (
        "titulo_fr",
        "titulo_es",
        "titulo_en",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )