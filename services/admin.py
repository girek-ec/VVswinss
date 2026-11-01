from django.contrib import admin
from django.templatetags.static import static
from django.utils.html import format_html

from .models import (
    Service,
    ServiceBenefit,
    ServiceCategory,
    ServiceImage,
    ServicePageConfiguration,
)


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

class ServiceBenefitInline(FontAwesomeAdminMediaMixin, admin.StackedInline):
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

    @admin.display(description="Vista previa del icono")
    def icon_preview(self, obj):
        return render_icon_preview(getattr(obj, "icon", ""), size=28)


# ============================================================
# INLINE · SERVICE IMAGES
# ============================================================

class ServiceImageInline(admin.StackedInline):
    model = ServiceImage
    extra = 0
    show_change_link = True
    readonly_fields = ("image_preview",)

    fieldsets = (
        ("Imagen", {
            "fields": ("image", "image_preview", "order"),
        }),
        ("Español · referencia interna", {
            "fields": ("alt_es",),
            "classes": ("collapse",),
        }),
        ("Français · langue principale", {
            "fields": ("alt_fr",),
        }),
        ("Deutsch", {
            "fields": ("alt_de",),
            "classes": ("collapse",),
        }),
        ("Italiano", {
            "fields": ("alt_it",),
            "classes": ("collapse",),
        }),
        ("English", {
            "fields": ("alt_en",),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="Vista previa")
    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="max-height:140px;max-width:220px;object-fit:cover;border-radius:6px;" />',
                obj.image.url,
            )
        return "—"



# ============================================================
# SERVICE PAGE CONFIGURATION ADMIN
# ============================================================

@admin.register(ServicePageConfiguration)
class ServicePageConfigurationAdmin(admin.ModelAdmin):
    list_display = ("__str__", "image_status", "updated_at")

    readonly_fields = (
        "category_default_image_preview",
        "category_default_social_image_preview",
        "list_cta_background_preview",
        "method_background_preview",
        "page_header_background_preview",
        "sidebar_cta_background_preview",
        "detail_default_image_preview",
        "secondary_default_image_preview",
        "third_default_image_preview",
        "gallery_default_image_preview",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("01 · Página principal · Categorías", {
            "description": (
                "Respaldo visual cuando una categoría no tiene imagen propia."
            ),
            "fields": (
                "category_default_image",
                "category_default_image_preview",
                "category_default_social_image_preview",
            ),
        }),
        ("02 · Página principal · CTA", {
            "description": (
                "Fondo general del bloque de llamada a la acción. "
                "Ya no depende de la imagen secundaria del primer servicio."
            ),
            "fields": (
                "list_cta_background",
                "list_cta_background_preview",
            ),
        }),
        ("03 · Página principal · Método / Savoir-faire", {
            "description": (
                "Imagen general de la sección Método de trabajo. "
                "Ya no depende de la tercera imagen del primer servicio."
            ),
            "fields": (
                "method_background",
                "method_background_preview",
            ),
        }),
        ("04 · Categorías y servicios · Encabezado", {
            "description": (
                "Fondo de respaldo de los encabezados interiores. "
                "Cada categoría y servicio puede tener su propio hero_image."
            ),
            "fields": (
                "page_header_background",
                "page_header_background_preview",
            ),
        }),
        ("05 · Categorías y servicios · CTA lateral", {
            "fields": (
                "sidebar_cta_background",
                "sidebar_cta_background_preview",
            ),
        }),
        ("06 · Detalle · Imágenes de respaldo", {
            "fields": (
                "detail_default_image",
                "detail_default_image_preview",
                "secondary_default_image",
                "secondary_default_image_preview",
                "third_default_image",
                "third_default_image_preview",
                "gallery_default_image",
                "gallery_default_image_preview",
            ),
        }),
        ("Sistema", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at"),
        }),
    )

    def has_add_permission(self, request):
        if ServicePageConfiguration.objects.exists():
            return False
        return super().has_add_permission(request)

    @staticmethod
    def _preview(field, max_width=420, max_height=230):
        if not field:
            return "Sin imagen cargada · se utilizará el respaldo de /static/."
        try:
            return format_html(
                '<img src="{}" style="max-width:{}px;max-height:{}px;'
                'width:auto;height:auto;object-fit:contain;border-radius:8px;'
                'border:1px solid #ddd;padding:4px;background:#f7f7f7;" />',
                field.url,
                max_width,
                max_height,
            )
        except (ValueError, AttributeError):
            return "Sin imagen cargada · se utilizará el respaldo de /static/."

    @admin.display(description="Vista previa · Categorías")
    def category_default_image_preview(self, obj):
        return self._preview(obj.category_default_image if obj else None)

    @admin.display(description="Vista previa · SEO social automático")
    def category_default_social_image_preview(self, obj):
        return self._preview(
            obj.category_default_social_image if obj else None,
            max_width=420,
            max_height=230,
        )

    @admin.display(description="Vista previa · CTA principal")
    def list_cta_background_preview(self, obj):
        return self._preview(obj.list_cta_background if obj else None)

    @admin.display(description="Vista previa · Método / Savoir-faire")
    def method_background_preview(self, obj):
        return self._preview(obj.method_background if obj else None)

    @admin.display(description="Vista previa · Encabezados")
    def page_header_background_preview(self, obj):
        return self._preview(obj.page_header_background if obj else None)

    @admin.display(description="Vista previa · CTA lateral")
    def sidebar_cta_background_preview(self, obj):
        return self._preview(obj.sidebar_cta_background if obj else None)

    @admin.display(description="Vista previa · Detalle principal")
    def detail_default_image_preview(self, obj):
        return self._preview(obj.detail_default_image if obj else None)

    @admin.display(description="Vista previa · Secundaria")
    def secondary_default_image_preview(self, obj):
        return self._preview(obj.secondary_default_image if obj else None)

    @admin.display(description="Vista previa · Tercera")
    def third_default_image_preview(self, obj):
        return self._preview(obj.third_default_image if obj else None)

    @admin.display(description="Vista previa · Galería")
    def gallery_default_image_preview(self, obj):
        return self._preview(obj.gallery_default_image if obj else None)

    @admin.display(description="Imágenes personalizadas")
    def image_status(self, obj):
        fields = (
            "category_default_image",
            "list_cta_background",
            "method_background",
            "page_header_background",
            "sidebar_cta_background",
            "detail_default_image",
            "secondary_default_image",
            "third_default_image",
            "gallery_default_image",
        )
        loaded = sum(bool(getattr(obj, name, None)) for name in fields)
        return f"{loaded}/{len(fields)}"


# ============================================================
# ============================================================
# SERVICE CATEGORY ADMIN
# ============================================================

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
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
                "Si un campo queda vacío, la vista previa muestra automáticamente la imagen de respaldo que utilizará el sitio."
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
                "Si no existe una imagen social propia, la vista previa muestra la imagen social global de respaldo."
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

    @staticmethod
    def _services_visuals():
        return (
            ServicePageConfiguration.objects
            .order_by("-updated_at")
            .first()
        )

    @staticmethod
    def _field_url(field):
        if not field:
            return None
        try:
            return field.url
        except (ValueError, AttributeError):
            return None

    @staticmethod
    def _preview_card(url, source_label, max_width=420, max_height=220):
        if not url:
            return "—"
        return format_html(
            '<div style="display:inline-flex;flex-direction:column;gap:7px;">'
            '<img src="{}" style="max-width:{}px;max-height:{}px;width:auto;height:auto;'
            'object-fit:cover;border-radius:7px;border:1px solid #ddd;background:#f7f7f7;" />'
            '<span style="display:inline-block;width:max-content;padding:3px 8px;border-radius:999px;'
            'font-size:11px;font-weight:600;background:#eef3ee;color:#245c24;">{}</span>'
            '</div>',
            url,
            max_width,
            max_height,
            source_label,
        )

    @admin.display(description="Icono")
    def icon_preview_list(self, obj):
        return render_icon_preview(getattr(obj, "icon", ""), size=22)

    @admin.display(description="Vista previa del icono")
    def icon_preview(self, obj):
        return render_icon_preview(getattr(obj, "icon", ""), size=34)

    @admin.display(description="Vista previa · Hero efectivo")
    def hero_image_preview(self, obj):
        if not obj:
            return "—"

        own_hero = self._field_url(obj.hero_image)
        if own_hero:
            return self._preview_card(own_hero, "Imagen propia · Hero")

        visuals = self._services_visuals()

        if visuals:
            global_header = self._field_url(visuals.page_header_background)
            if global_header:
                return self._preview_card(global_header, "Respaldo global · Encabezado")

        own_image = self._field_url(obj.image)
        if own_image:
            return self._preview_card(own_image, "Imagen propia · Principal")

        if visuals:
            global_category = self._field_url(visuals.category_default_image)
            if global_category:
                return self._preview_card(global_category, "Respaldo global · Categorías")

        return self._preview_card(
            static("antra/assets/img/bg-img/page-header-bg.webp"),
            "Respaldo estático · Encabezado",
        )

    @admin.display(description="Imagen")
    def image_preview_list(self, obj):
        if not obj:
            return "—"

        own_image = self._field_url(obj.image)
        if own_image:
            return format_html(
                '<img src="{}" title="Imagen propia" '
                'style="height:55px;width:80px;object-fit:cover;border-radius:5px;" />',
                own_image,
            )

        visuals = self._services_visuals()
        if visuals:
            fallback = self._field_url(visuals.category_default_image)
            if fallback:
                return format_html(
                    '<img src="{}" title="Respaldo global" '
                    'style="height:55px;width:80px;object-fit:cover;border-radius:5px;opacity:.82;" />',
                    fallback,
                )

        return format_html(
            '<img src="{}" title="Respaldo estático" '
            'style="height:55px;width:80px;object-fit:cover;border-radius:5px;opacity:.72;" />',
            static("antra/assets/img/service/VVS_service.webp"),
        )

    @admin.display(description="Vista previa · Imagen efectiva")
    def image_preview(self, obj):
        if not obj:
            return "—"

        own_image = self._field_url(obj.image)
        if own_image:
            return self._preview_card(own_image, "Imagen propia · Principal", 420, 240)

        own_hero = self._field_url(obj.hero_image)
        if own_hero:
            return self._preview_card(own_hero, "Imagen propia · Hero", 420, 240)

        visuals = self._services_visuals()

        if visuals:
            global_category = self._field_url(visuals.category_default_image)
            if global_category:
                return self._preview_card(
                    global_category,
                    "Respaldo global · Categorías",
                    420,
                    240,
                )

            detail_default = self._field_url(visuals.detail_default_image)
            if detail_default:
                return self._preview_card(
                    detail_default,
                    "Respaldo global · Detalle",
                    420,
                    240,
                )

        return self._preview_card(
            static("antra/assets/img/service/VVS_service.webp"),
            "Respaldo estático · Servicios",
            420,
            240,
        )

    @admin.display(description="Vista previa · Open Graph efectivo")
    def og_image_preview(self, obj):
        if not obj:
            return "—"

        own_og = self._field_url(obj.og_image)
        if own_og:
            return self._preview_card(
                own_og,
                "Imagen social propia · 1200 × 630",
                420,
                221,
            )

        visuals = self._services_visuals()
        if visuals:
            social_default = self._field_url(
                getattr(visuals, "category_default_social_image", None)
            )
            if social_default:
                return self._preview_card(
                    social_default,
                    "Respaldo social global · 1200 × 630",
                    420,
                    221,
                )

        return self._preview_card(
            static("antra/assets/img/service/VVS_service.webp"),
            "Respaldo estático · Servicios",
            420,
            221,
        )


# ============================================================
# SERVICE ADMIN
# ============================================================

@admin.register(Service)
class ServiceAdmin(FontAwesomeAdminMediaMixin, admin.ModelAdmin):
    list_display = (
        "icon_preview_list",
        "name_es",
        "name_fr",
        "category",
        "hero_image_preview_list",
        "main_image_preview_list",
        "secondary_image_preview_list",
        "third_image_preview_list",
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
        "icon_preview",
        "hero_image_preview",
        "main_image_preview",
        "secondary_image_preview",
        "third_image_preview",
        "created_at",
        "updated_at",
    )

    list_select_related = ("category",)

    inlines = (
        ServiceBenefitInline,
        ServiceImageInline,
    )

    fieldsets = (
        ("Configuración general", {
            "fields": ("category", "icon", "icon_preview"),
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
        ("Multimedia", {
            "description": (
                "Hero = encabezado panorámico. Principal/secundaria/tercera = "
                "contenido interior del servicio."
            ),
            "fields": (
                "hero_image",
                "hero_image_preview",
                "main_image",
                "main_image_preview",
                "secondary_image",
                "secondary_image_preview",
                "third_image",
                "third_image_preview",
            ),
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

    @admin.display(description="Icono")
    def icon_preview_list(self, obj):
        return render_icon_preview(getattr(obj, "icon", ""), size=22)

    @admin.display(description="Vista previa del icono")
    def icon_preview(self, obj):
        return render_icon_preview(getattr(obj, "icon", ""), size=34)

    @admin.display(description="Hero")
    def hero_image_preview_list(self, obj):
        if obj and obj.hero_image:
            return format_html(
                '<img src="{}" style="height:55px;width:90px;object-fit:cover;border-radius:5px;" />',
                obj.hero_image.url,
            )
        return "—"

    @admin.display(description="Principal")
    def main_image_preview_list(self, obj):
        if obj and obj.main_image:
            return format_html(
                '<img src="{}" style="height:55px;width:80px;object-fit:cover;border-radius:5px;" />',
                obj.main_image.url,
            )
        return "—"

    @admin.display(description="Secundaria")
    def secondary_image_preview_list(self, obj):
        if obj and obj.secondary_image:
            return format_html(
                '<img src="{}" style="height:55px;width:80px;object-fit:cover;border-radius:5px;" />',
                obj.secondary_image.url,
            )
        return "—"

    @admin.display(description="Tercera")
    def third_image_preview_list(self, obj):
        if obj and obj.third_image:
            return format_html(
                '<img src="{}" style="height:55px;width:80px;object-fit:cover;border-radius:5px;" />',
                obj.third_image.url,
            )
        return "—"

    @admin.display(description="Vista previa · Hero")
    def hero_image_preview(self, obj):
        if obj and obj.hero_image:
            return format_html(
                '<img src="{}" style="max-height:220px;max-width:420px;object-fit:cover;border-radius:6px;" />',
                obj.hero_image.url,
            )
        return "—"

    @admin.display(description="Vista previa · imagen principal")
    def main_image_preview(self, obj):
        if obj and obj.main_image:
            return format_html(
                '<img src="{}" style="max-height:220px;max-width:360px;object-fit:cover;border-radius:6px;" />',
                obj.main_image.url,
            )
        return "—"

    @admin.display(description="Vista previa · imagen secundaria")
    def secondary_image_preview(self, obj):
        if obj and obj.secondary_image:
            return format_html(
                '<img src="{}" style="max-height:220px;max-width:360px;object-fit:cover;border-radius:6px;" />',
                obj.secondary_image.url,
            )
        return "—"

    @admin.display(description="Vista previa · tercera imagen")
    def third_image_preview(self, obj):
        if obj and obj.third_image:
            return format_html(
                '<img src="{}" style="max-height:220px;max-width:360px;object-fit:cover;border-radius:6px;" />',
                obj.third_image.url,
            )
        return "—"


# ============================================================
# SERVICE BENEFIT ADMIN
# ============================================================

@admin.register(ServiceBenefit)
class ServiceBenefitAdmin(FontAwesomeAdminMediaMixin, admin.ModelAdmin):
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


    @admin.display(description="Icono")
    def icon_preview_list(self, obj):
        return render_icon_preview(getattr(obj, "icon", ""), size=22)


# ============================================================
# ============================================================
# SERVICE IMAGE ADMIN
# ============================================================

@admin.register(ServiceImage)
class ServiceImageAdmin(admin.ModelAdmin):
    list_display = (
        "image_preview_list",
        "service",
        "alt_es",
        "alt_fr",
        "order",
    )

    list_display_links = (
        "image_preview_list",
        "service",
    )

    list_filter = ("service",)
    list_editable = ("order",)

    search_fields = (
        "service__name_es",
        "service__name_fr",
        "service__name_de",
        "service__name_it",
        "service__name_en",
        "alt_es",
        "alt_fr",
        "alt_de",
        "alt_it",
        "alt_en",
    )

    readonly_fields = ("image_preview",)

    fieldsets = (
        ("Imagen", {
            "fields": ("service", "image", "image_preview", "order"),
        }),
        ("Español · referencia interna", {
            "fields": ("alt_es",),
            "classes": ("collapse",),
        }),
        ("Français · langue principale", {
            "fields": ("alt_fr",),
        }),
        ("Deutsch", {
            "fields": ("alt_de",),
            "classes": ("collapse",),
        }),
        ("Italiano", {
            "fields": ("alt_it",),
            "classes": ("collapse",),
        }),
        ("English · British English", {
            "fields": ("alt_en",),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="Imagen")
    def image_preview_list(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="height:55px;width:80px;object-fit:cover;border-radius:5px;" />',
                obj.image.url,
            )
        return "—"

    @admin.display(description="Vista previa")
    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="max-height:220px;max-width:360px;object-fit:cover;border-radius:6px;" />',
                obj.image.url,
            )
        return "—"
