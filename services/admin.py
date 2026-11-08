from django.contrib import admin
from django.templatetags.static import static
from django.utils.html import format_html

from .models import (
    Service,
    ServiceBenefit,
    ServiceCategory,
)
from .fontawesome_icon_picker import FontAwesomeIconPickerMixin


# ============================================================
# HELPER · ICON PREVIEW
# ============================================================

def render_icon_preview(icon_class, size=30):
    """
    Renderiza visualmente una clase de icono (por ejemplo:
    fa-solid fa-house) y muestra también su nombre para facilitar
    la administración.
    """
    if not icon_class:
        return "—"

    return format_html(
        '<span style="display:inline-flex;align-items:center;gap:10px;">'
        '<span style="display:inline-flex;align-items:center;justify-content:center;'
        'width:42px;height:42px;border-radius:8px;background:#0a4c03;color:#fff;">'
        '<i class="{}" style="font-size:{}px;line-height:1;"></i>'
        '</span>'
        '<code style="font-size:11px;white-space:nowrap;">{}</code>'
        '</span>',
        icon_class,
        size,
        icon_class,
    )


# ============================================================
# MEDIA · FONT AWESOME EN DJANGO ADMIN
# Usa el mismo CSS que carga base.html en la web pública.
# ============================================================

class FontAwesomeAdminMediaMixin:
    class Media:
        css = {
            "all": ("antra/assets/css/fontawesome.min.css",),
        }


# ============================================================
# INLINE · SERVICE BENEFITS
# ============================================================

class ServiceBenefitInline(FontAwesomeIconPickerMixin, FontAwesomeAdminMediaMixin, admin.StackedInline):
    model = ServiceBenefit
    extra = 0
    show_change_link = True
    readonly_fields = ("icon_preview",)

    fieldsets = (
        ("Español · referencia interna", {
            "fields": ("title_es", "description_es"),
            "classes": ("collapse",),
        }),
        ("Français · langue principale", {
            "fields": ("title_fr", "description_fr"),
        }),
        ("Deutsch", {
            "fields": ("title_de", "description_de"),
            "classes": ("collapse",),
        }),
        ("Italiano", {
            "fields": ("title_it", "description_it"),
            "classes": ("collapse",),
        }),
        ("English", {
            "fields": ("title_en", "description_en"),
            "classes": ("collapse",),
        }),
        ("Configuración", {
            "fields": ("icon", "icon_preview", "order"),
        }),
    )

    @admin.display(description="Icon preview")
    def icon_preview(self, obj):
        return render_icon_preview(getattr(obj, "icon", ""), size=28)


# ============================================================
# INLINE · SERVICE IMAGES
# ============================================================





# ============================================================
# ============================================================
# SERVICE CATEGORY ADMIN
# ============================================================

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(FontAwesomeIconPickerMixin, FontAwesomeAdminMediaMixin, admin.ModelAdmin):
    list_display = (
        "image_preview_list",
        "icon_preview_list",
        "name_es",
        "name_fr",
        "order",
        "is_active",
    )

    list_display_links = (
        "name_es",
        "name_fr",
    )

    list_editable = (
        "order",
        "is_active",
    )

    list_filter = (
        "is_active",
        "is_indexable",
    )

    search_fields = (
        "name_es",
        "name_fr",
        "name_de",
        "name_it",
        "name_en",
        "description_es",
        "description_fr",
        "description_de",
        "description_it",
        "description_en",
        "seo_title_es",
        "seo_title_fr",
        "seo_title_de",
        "seo_title_it",
        "seo_title_en",
        "meta_description_es",
        "meta_description_fr",
        "meta_description_de",
        "meta_description_it",
        "meta_description_en",
    )

    prepopulated_fields = {
        "slug_fr": ("name_fr",),
        "slug_de": ("name_de",),
        "slug_it": ("name_it",),
        "slug_en": ("name_en",),
    }

    readonly_fields = (
        "hero_image_preview",
        "image_preview",
        "icon_preview",
        "og_image_preview",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Español · referencia interna", {
            "description": "Contenido únicamente de referencia para la administración. No se publica como idioma del sitio.",
            "fields": (
                "name_es",
                "description_es",
                "seo_title_es",
                "meta_description_es",
            ),
        }),
        ("Français · langue principale", {
            "description": "Idioma principal del sitio web. Complete siempre estos campos.",
            "fields": (
                "name_fr",
                "slug_fr",
                "description_fr",
                "seo_title_fr",
                "meta_description_fr",
            ),
        }),
        ("Deutsch", {
            "fields": (
                "name_de",
                "slug_de",
                "description_de",
                "seo_title_de",
                "meta_description_de",
            ),
            "classes": ("collapse",),
        }),
        ("Italiano", {
            "fields": (
                "name_it",
                "slug_it",
                "description_it",
                "seo_title_it",
                "meta_description_it",
            ),
            "classes": ("collapse",),
        }),
        ("English · British English", {
            "fields": (
                "name_en",
                "slug_en",
                "description_en",
                "seo_title_en",
                "meta_description_en",
            ),
            "classes": ("collapse",),
        }),
        ("Imágenes e icono", {
            "description": (
                "Hero = encabezado panorámico. Imagen principal = tarjeta/listado y fotografía principal del contenido. "
                "Si un campo queda vacío, se muestra la imagen predeterminada ubicada en static/."
            ),
            "fields": (
                "hero_image",
                "hero_image_preview",
                "image",
                "image_preview",
                "icon",
                "icon_preview",
            ),
        }),
        ("SEO social", {
            "description": (
                "Imagen utilizada al compartir esta categoría en redes sociales. "
                "Si no existe una imagen social propia, se muestra la imagen predeterminada de static/."
            ),
            "fields": (
                "og_image",
                "og_image_preview",
                "is_indexable",
            ),
        }),
        ("Publicación", {
            "fields": ("order", "is_active"),
        }),
        ("Sistema", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    # VISTA PREVIA / PREVIEW · IMAGEN PROPIA O STATIC
    @staticmethod
    def _field_url(field):
        if field:
            try:
                return field.url
            except (ValueError, AttributeError):
                pass
        return None

    @staticmethod
    def _preview_card(url, source_label, max_width=420, max_height=220):
        return format_html(
            '<div style="display:inline-flex;flex-direction:column;gap:7px;">'
            '<img src="{}" style="max-width:{}px;max-height:{}px;width:auto;height:auto;'
            'object-fit:cover;border-radius:7px;border:1px solid #ddd;background:#f7f7f7;" />'
            '<span style="font-size:11px;font-weight:600;color:#245c24;">{}</span>'
            '</div>', url, max_width, max_height, source_label,
        )

    @admin.display(description="Icon")
    def icon_preview_list(self, obj):
        return render_icon_preview(getattr(obj, "icon", ""), size=22)

    @admin.display(description="Icon preview")
    def icon_preview(self, obj):
        return render_icon_preview(getattr(obj, "icon", ""), size=34)

    @admin.display(description="Vista previa · Hero")
    def hero_image_preview(self, obj):
        url = self._field_url(obj.hero_image) if obj else None
        return self._preview_card(
            url or static("antra/assets/img/bg-img/page-header-bg.webp"),
            "Imagen propia · Hero" if url else "Predeterminada · STATIC",
        )


    # CATEGORÍA · RESPALDO ESTÁTICO FIJO | CATEGORY · FIXED STATIC FALLBACK
    @admin.display(description="Image")
    def image_preview_list(self, obj):
        url = self._field_url(obj.image) if obj else None
        default_url = static("antra/assets/img/service/VVS_service.webp")
        return format_html(
            '<img src="{}" title="{}" style="height:55px;width:80px;object-fit:cover;border-radius:5px;" />',
            url or default_url,
            "Uploaded category image" if url else "Default · static/service/VVS_service.webp",
        )

    @admin.display(description="Image preview · Main / Static")
    def image_preview(self, obj):
        url = self._field_url(obj.image) if obj else None
        default_url = static("antra/assets/img/service/VVS_service.webp")
        static_card = self._preview_card(
            default_url,
            "Default image · static/antra/assets/img/service/VVS_service.webp",
            420, 240,
        )
        if not url:
            return static_card
        return format_html(
            '<div style="display:flex;flex-wrap:wrap;align-items:flex-start;gap:15px">{}{}</div>',
            self._preview_card(url, "Uploaded category image", 420, 240),
            static_card,
        )


    @admin.display(description="Vista previa · Imagen social")
    def og_image_preview(self, obj):
        url = self._field_url(obj.og_image) if obj else None
        return self._preview_card(
            url or current_social_fallback_url(),
            "Imagen social propia" if url else "Predeterminada · STATIC",
            420, 221,
        )

# ============================================================
# SERVICE ADMIN
# ============================================================

@admin.register(Service)
class ServiceAdmin(FontAwesomeIconPickerMixin, FontAwesomeAdminMediaMixin, admin.ModelAdmin):
    list_display = (
        "image_preview_list",
        "icon_preview_list",
        "name_es",
        "name_fr",
        "category",
        "is_featured",
        "order",
        "is_active",
    )

    list_display_links = (
        "name_es",
        "name_fr",
    )

    list_filter = (
        "category",
        "is_featured",
        "is_active",
    )

    list_editable = (
        "is_featured",
        "order",
        "is_active",
    )

    search_fields = (
        "name_es",
        "name_fr",
        "name_de",
        "name_it",
        "name_en",
        "hero_title_prefix_es",
        "hero_title_prefix_fr",
        "hero_title_prefix_de",
        "hero_title_prefix_it",
        "hero_title_prefix_en",
        "hero_title_suffix_es",
        "hero_title_suffix_fr",
        "hero_title_suffix_de",
        "hero_title_suffix_it",
        "hero_title_suffix_en",
        "subtitle_es",
        "subtitle_fr",
        "subtitle_de",
        "subtitle_it",
        "subtitle_en",
        "summary_es",
        "summary_fr",
        "summary_de",
        "summary_it",
        "summary_en",
        "content_es",
        "content_fr",
        "content_de",
        "content_it",
        "content_en",
    )

    prepopulated_fields = {
        "slug_fr": ("name_fr",),
        "slug_de": ("name_de",),
        "slug_it": ("name_it",),
        "slug_en": ("name_en",),
    }

    readonly_fields = (
        "image_preview",
        "icon_preview",
        "created_at",
        "updated_at",
    )

    list_select_related = ("category",)

    inlines = (
        ServiceBenefitInline,
    )

    fieldsets = (
        ("Configuración general", {
            "fields": ("category", "icon", "icon_preview"),
        }),
        ("Imagen principal · Servicio | Main service image", {
            "description": (
                "Suba la imagen principal del servicio. Los archivos nuevos se convierten "
                "automáticamente a WebP. Si no se carga una imagen, se muestra el "
                "respaldo de static/ también en la web pública."
            ),
            "fields": ("image", "image_preview"),
        }),
        ("Español · referencia interna", {
            "description": "Este idioma se utiliza únicamente como referencia interna en Django Admin. No se publica como idioma del sitio.",
            "fields": (
                "name_es",
                "hero_title_prefix_es",
                "hero_title_suffix_es",
                "subtitle_es",
                "summary_es",
                "content_es",
                "detail_1_title_es",
                "detail_1_text_es",
                "detail_1_list_es",
                "detail_2_title_es",
                "detail_2_text_es",
                "detail_2_list_es",
                "cta_title_es",
                "cta_text_es",
                "cta_button_es",
                "whatsapp_message_es",
            ),
            "classes": ("collapse",),
        }),
        ("Français · langue principale", {
            "description": "Idioma público principal de V&V Swiss Services. Estos campos deben completarse siempre.",
            "fields": (
                "name_fr",
                "hero_title_prefix_fr",
                "hero_title_suffix_fr",
                "subtitle_fr",
                "slug_fr",
                "summary_fr",
                "content_fr",
                "detail_1_title_fr",
                "detail_1_text_fr",
                "detail_1_list_fr",
                "detail_2_title_fr",
                "detail_2_text_fr",
                "detail_2_list_fr",
                "cta_title_fr",
                "cta_text_fr",
                "cta_button_fr",
                "whatsapp_message_fr",
            ),
        }),
        ("Deutsch", {
            "description": "Contenido público para la versión alemana del sitio.",
            "fields": (
                "name_de",
                "hero_title_prefix_de",
                "hero_title_suffix_de",
                "subtitle_de",
                "slug_de",
                "summary_de",
                "content_de",
                "detail_1_title_de",
                "detail_1_text_de",
                "detail_1_list_de",
                "detail_2_title_de",
                "detail_2_text_de",
                "detail_2_list_de",
                "cta_title_de",
                "cta_text_de",
                "cta_button_de",
                "whatsapp_message_de",
            ),
            "classes": ("collapse",),
        }),
        ("Italiano", {
            "description": "Contenido público para la versión italiana del sitio.",
            "fields": (
                "name_it",
                "hero_title_prefix_it",
                "hero_title_suffix_it",
                "subtitle_it",
                "slug_it",
                "summary_it",
                "content_it",
                "detail_1_title_it",
                "detail_1_text_it",
                "detail_1_list_it",
                "detail_2_title_it",
                "detail_2_text_it",
                "detail_2_list_it",
                "cta_title_it",
                "cta_text_it",
                "cta_button_it",
                "whatsapp_message_it",
            ),
            "classes": ("collapse",),
        }),
        ("English · British English", {
            "description": "Contenido público para la versión inglesa del sitio.",
            "fields": (
                "name_en",
                "hero_title_prefix_en",
                "hero_title_suffix_en",
                "subtitle_en",
                "slug_en",
                "summary_en",
                "content_en",
                "detail_1_title_en",
                "detail_1_text_en",
                "detail_1_list_en",
                "detail_2_title_en",
                "detail_2_text_en",
                "detail_2_list_en",
                "cta_title_en",
                "cta_text_en",
                "cta_button_en",
                "whatsapp_message_en",
            ),
            "classes": ("collapse",),
        }),
        ("WhatsApp", {
            "description": "Activa o desactiva el botón de WhatsApp en este servicio. El texto específico del mensaje se configura dentro de cada idioma.",
            "fields": ("whatsapp_enabled",),
        }),
        ("Publicación", {
            "fields": ("is_featured", "order", "is_active"),
        }),
        ("Sistema", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="Icon")
    def icon_preview_list(self, obj):
        return render_icon_preview(getattr(obj, "icon", ""), size=22)

    @admin.display(description="Icon preview")
    def icon_preview(self, obj):
        return render_icon_preview(getattr(obj, "icon", ""), size=34)

    # IMAGEN PRINCIPAL · PREVIEWS CON STATIC | MAIN SERVICE IMAGE PREVIEWS
    @staticmethod
    def _service_image_source(obj):
        image = getattr(obj, "image", None) if obj else None
        if image:
            try:
                return image.url, True
            except (AttributeError, ValueError):
                pass
        return obj.static_image_url if obj else static("antra/assets/img/service/VVS_service.webp"), False

    @admin.display(description="Imagen")
    def image_preview_list(self, obj):
        url, uploaded = self._service_image_source(obj)
        return format_html(
            '<a href="{}" target="_blank" rel="noopener noreferrer" title="{}">'
            '<img src="{}" alt="{}" loading="lazy" '
            'style="display:block;width:85px;height:60px;object-fit:cover;'
            'border-radius:6px;border:1px solid #ddd;background:#f7f7f7"></a>',
            url,
            "Imagen cargada" if uploaded else "Imagen predeterminada · STATIC",
            url,
            obj.name_fr,
        )

    @admin.display(description="Vista previa · Imagen del servicio")
    def image_preview(self, obj):
        url, uploaded = self._service_image_source(obj)
        return format_html(
            '<div style="display:inline-flex;flex-direction:column;gap:7px;">'
            '<a href="{}" target="_blank" rel="noopener noreferrer">'
            '<img src="{}" alt="{}" loading="lazy" '
            'style="display:block;width:320px;max-width:100%;height:200px;object-fit:cover;'
            'border-radius:7px;border:1px solid #ddd;background:#f7f7f7;"></a>'
            '<span style="font-size:12px;font-weight:600;color:#245c24">{}</span>'
            '</div>',
            url,
            url,
            obj.name_fr if obj else "Service",
            "Imagen del servicio" if uploaded else "Predeterminada · STATIC · VVS_service.webp",
        )

    # IMAGE PREVIEWS | VISTA PREVIA DE IMÁGENES










# ============================================================
# SERVICE BENEFIT ADMIN
# ============================================================

@admin.register(ServiceBenefit)
class ServiceBenefitAdmin(FontAwesomeIconPickerMixin, FontAwesomeAdminMediaMixin, admin.ModelAdmin):
    list_display = (
        "icon_preview_list",
        "title_es",
        "title_fr",
        "service",
        "order",
    )

    list_display_links = (
        "title_es",
        "title_fr",
    )

    list_filter = (
        "service",
    )

    list_editable = (
        "order",
    )

    search_fields = (
        "title_es",
        "title_fr",
        "title_de",
        "title_it",
        "title_en",
        "description_es",
        "description_fr",
        "description_de",
        "description_it",
        "description_en",
    )

    fieldsets = (
        ("Servicio", {
            "fields": ("service", "icon", "order"),
        }),

        ("Español · referencia interna", {
            "fields": ("title_es", "description_es"),
            "classes": ("collapse",),
        }),

        ("Français · langue principale", {
            "fields": ("title_fr", "description_fr"),
        }),

        ("Deutsch", {
            "fields": ("title_de", "description_de"),
            "classes": ("collapse",),
        }),

        ("Italiano", {
            "fields": ("title_it", "description_it"),
            "classes": ("collapse",),
        }),

        ("English", {
            "fields": ("title_en", "description_en"),
            "classes": ("collapse",),
        }),
    )


    @admin.display(description="Icon")
    def icon_preview_list(self, obj):
        return render_icon_preview(getattr(obj, "icon", ""), size=22)


# ============================================================
# ============================================================
# SERVICE IMAGE ADMIN
# ============================================================

# SERVICES · REGISTER VISUAL ADMIN | REGISTRAR CONFIGURACIÓN VISUAL
from .visual_config_admin import current_social_fallback_url
from . import visual_config_admin  # Register Services Visual Configuration
