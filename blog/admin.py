from django.contrib import admin
from django.db.models import Count
from django.templatetags.static import static
from django.utils.html import format_html

from .models import BlogCategory, BlogTag, Post, PostSection


BLOG_STATIC_FALLBACK = "antra/assets/img/images/VVS_placeholder_horizontal.webp"


def image_url_if_exists(image):
    if not image:
        return None
    try:
        if image.storage.exists(image.name):
            return image.url
    except (AttributeError, OSError, ValueError):
        return None
    return None


def effective_post_image(obj):
    own = image_url_if_exists(getattr(obj, "main_image", None))
    return (own, "Imagen propia") if own else (static(BLOG_STATIC_FALLBACK), "Imagen predeterminada · STATIC")


def effective_post_social_image(obj):
    own = image_url_if_exists(getattr(obj, "og_image", None))
    if own:
        return own, "Open Graph propio/automático"
    main = image_url_if_exists(getattr(obj, "main_image", None))
    if main:
        return main, "Imagen propia del artículo"
    return static(BLOG_STATIC_FALLBACK), "Imagen predeterminada · STATIC"


def render_preview(url, label, width=500, height=280):
    return format_html(
        '<div style="max-width:{}px;">'
        '<img src="{}" style="width:100%;height:{}px;object-fit:cover;border-radius:8px;display:block;" />'
        '<div style="margin-top:6px;font-size:12px;color:#666;">{}</div>'
        '</div>',
        width,
        url,
        height,
        label,
    )


# BLOG CATEGORY ADMIN
@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("name_fr", "slug_fr", "post_count", "is_active")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = (
        "name_fr", "name_de", "name_it", "name_en",
        "slug_fr", "slug_de", "slug_it", "slug_en",
    )
    ordering = ("name_fr",)
    list_per_page = 25
    prepopulated_fields = {
        "slug_fr": ("name_fr",),
        "slug_de": ("name_de",),
        "slug_it": ("name_it",),
        "slug_en": ("name_en",),
    }
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Français · Principal", {"fields": ("name_fr", "slug_fr")}),
        ("Deutsch", {"classes": ("collapse",), "fields": ("name_de", "slug_de")}),
        ("Italiano", {"classes": ("collapse",), "fields": ("name_it", "slug_it")}),
        ("English", {"classes": ("collapse",), "fields": ("name_en", "slug_en")}),
        ("Publicación", {"fields": ("is_active",)}),
        ("Sistema", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_post_count=Count("posts"))

    @admin.display(description="Entradas", ordering="_post_count")
    def post_count(self, obj):
        return obj._post_count


# BLOG TAG ADMIN
@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ("name_fr", "name_de", "name_it", "name_en", "is_active")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("name_fr", "name_de", "name_it", "name_en")
    ordering = ("name_fr",)
    list_per_page = 25


# POST SECTION INLINE
class PostSectionInline(admin.StackedInline):
    model = PostSection
    extra = 1
    ordering = ("order",)
    classes = ("collapse",)
    fields = (
        "order",
        "section_type",
        "is_active",
        "title_fr",
        "content_fr",
        "title_de",
        "content_de",
        "title_it",
        "content_it",
        "title_en",
        "content_en",
        "image_1",
        "image_2",
        "image_1_alt_fr",
        "image_1_alt_de",
        "image_1_alt_it",
        "image_1_alt_en",
        "image_2_alt_fr",
        "image_2_alt_de",
        "image_2_alt_it",
        "image_2_alt_en",
        "quote_fr",
        "quote_de",
        "quote_it",
        "quote_en",
        "quote_author",
        "quote_icon",
    )


# POST ADMIN
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "image_preview",
        "title_fr",
        "category",
        "author",
        "published_at",
        "og_status",
        "is_featured",
        "is_published",
    )
    list_display_links = ("image_preview", "title_fr")
    list_editable = ("is_featured", "is_published")
    list_filter = (
        "is_published",
        "is_featured",
        "category",
        "is_indexable",
        "published_at",
    )
    search_fields = (
        "title_fr", "title_de", "title_it", "title_en",
        "excerpt_fr", "excerpt_de", "excerpt_it", "excerpt_en",
        "content_fr", "content_de", "content_it", "content_en",
    )
    ordering = ("-published_at",)
    list_per_page = 25
    list_select_related = ("category", "author")
    date_hierarchy = "published_at"
    autocomplete_fields = ("category",)
    filter_horizontal = ("tags",)
    prepopulated_fields = {
        "slug_fr": ("title_fr",),
        "slug_de": ("title_de",),
        "slug_it": ("title_it",),
        "slug_en": ("title_en",),
    }
    readonly_fields = (
        "image_preview_large",
        "og_image_effective_preview",
        "created_at",
        "updated_at",
    )
    actions = (
        "publish_selected",
        "unpublish_selected",
        "feature_selected",
        "unfeature_selected",
    )
    inlines = (PostSectionInline,)

    def get_fieldsets(self, request, obj=None):
        grouped_fields = {
            "category", "tags", "author", "main_image",
            "image_preview_large", "og_image_effective_preview",
            "title_fr", "slug_fr", "excerpt_fr", "content_fr",
            "title_de", "slug_de", "excerpt_de", "content_de",
            "title_it", "slug_it", "excerpt_it", "content_it",
            "title_en", "slug_en", "excerpt_en", "content_en",
            "published_at", "is_published", "is_featured",
            "created_at", "updated_at",
        }

        extra_fields = []
        for field in self.model._meta.get_fields():
            if field.auto_created:
                continue
            if not getattr(field, "editable", False):
                continue
            if field.name in grouped_fields:
                continue
            extra_fields.append(field.name)

        fieldsets = [
            ("Información general", {"fields": ("category", "author", "tags")}),
            (
                "Imagen principal",
                {
                    "description": (
                        "Si no se carga una imagen propia, el sitio y el Admin muestran "
                        "automáticamente la imagen predeterminada de static/."
                    ),
                    "fields": ("main_image", "image_preview_large"),
                },
            ),
            (
                "Français · Principal",
                {"fields": ("title_fr", "slug_fr", "excerpt_fr", "content_fr")},
            ),
            (
                "Deutsch",
                {
                    "classes": ("collapse",),
                    "fields": ("title_de", "slug_de", "excerpt_de", "content_de"),
                },
            ),
            (
                "Italiano",
                {
                    "classes": ("collapse",),
                    "fields": ("title_it", "slug_it", "excerpt_it", "content_it"),
                },
            ),
            (
                "English",
                {
                    "classes": ("collapse",),
                    "fields": ("title_en", "slug_en", "excerpt_en", "content_en"),
                },
            ),
        ]

        if extra_fields:
            fieldsets.append(
                (
                    "SEO",
                    {
                        "description": (
                            "Si existe imagen principal, og_image se genera automáticamente "
                            "en JPEG 1200 × 630. Si no existe, se muestra la imagen propia o el recurso de static/."
                        ),
                        "fields": tuple(extra_fields) + ("og_image_effective_preview",),
                    },
                )
            )
        else:
            fieldsets.append(
                (
                    "SEO social",
                    {"fields": ("og_image_effective_preview",)},
                )
            )

        fieldsets.extend(
            [
                (
                    "Publicación",
                    {"fields": ("published_at", "is_published", "is_featured")},
                ),
                (
                    "Sistema",
                    {
                        "classes": ("collapse",),
                        "fields": ("created_at", "updated_at"),
                    },
                ),
            ]
        )
        return fieldsets

    @admin.display(description="Imagen")
    def image_preview(self, obj):
        url, label = effective_post_image(obj)
        return format_html(
            '<div title="{}"><img src="{}" style="width:80px;height:55px;object-fit:cover;border-radius:6px;" /></div>',
            label,
            url,
        )

    @admin.display(description="Vista previa efectiva")
    def image_preview_large(self, obj):
        if not obj:
            return "Guarde el artículo para mostrar la vista previa."
        url, label = effective_post_image(obj)
        return render_preview(url, label)

    @admin.display(description="Vista previa · Open Graph / X")
    def og_image_effective_preview(self, obj):
        if not obj:
            return "Guarde el artículo para mostrar la vista previa."
        url, label = effective_post_social_image(obj)
        return render_preview(url, label, 500, 263)

    @admin.display(description="SEO social")
    def og_status(self, obj):
        if image_url_if_exists(getattr(obj, "og_image", None)):
            return "Generada automáticamente"
        if image_url_if_exists(getattr(obj, "main_image", None)):
            return "Imagen del artículo"
        return "STATIC"

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    @admin.action(description="Publicar entradas seleccionadas")
    def publish_selected(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description="Despublicar entradas seleccionadas")
    def unpublish_selected(self, request, queryset):
        queryset.update(is_published=False)

    @admin.action(description="Marcar como destacadas")
    def feature_selected(self, request, queryset):
        queryset.update(is_featured=True)

    @admin.action(description="Quitar de destacadas")
    def unfeature_selected(self, request, queryset):
        queryset.update(is_featured=False)


# CONFIGURACIÓN VISUAL · REGISTRO ADMIN
from . import visual_config_admin  # noqa: E402,F401

# BLOG · VISUAL PREVIEWS | VISTAS PREVIAS DE CONFIGURACIÓN VISUAL
from . import admin_visual_previews  # noqa: F401,E402
