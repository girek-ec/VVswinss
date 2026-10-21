from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html

from .models import BlogCategory, BlogTag, Post, PostSection


# ============================================================
# BLOG CATEGORY ADMIN
# ============================================================

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name_fr",
        "slug_fr",
        "post_count",
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name_fr",
        "name_de",
        "name_it",
        "name_en",
        "slug_fr",
        "slug_de",
        "slug_it",
        "slug_en",
    )

    ordering = (
        "name_fr",
    )

    list_per_page = 25

    prepopulated_fields = {
        "slug_fr": ("name_fr",),
        "slug_de": ("name_de",),
        "slug_it": ("name_it",),
        "slug_en": ("name_en",),
    }

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Français · Principal",
            {
                "fields": (
                    "name_fr",
                    "slug_fr",
                ),
            },
        ),
        (
            "Deutsch",
            {
                "classes": ("collapse",),
                "fields": (
                    "name_de",
                    "slug_de",
                ),
            },
        ),
        (
            "Italiano",
            {
                "classes": ("collapse",),
                "fields": (
                    "name_it",
                    "slug_it",
                ),
            },
        ),
        (
            "English",
            {
                "classes": ("collapse",),
                "fields": (
                    "name_en",
                    "slug_en",
                ),
            },
        ),
        (
            "Publicación",
            {
                "fields": (
                    "is_active",
                ),
            },
        ),
        (
            "Sistema",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(_post_count=Count("posts"))

    @admin.display(description="Entradas", ordering="_post_count")
    def post_count(self, obj):
        return obj._post_count


# ============================================================
# BLOG TAG ADMIN
# ============================================================

@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = (
        "name_fr",
        "name_de",
        "name_it",
        "name_en",
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name_fr",
        "name_de",
        "name_it",
        "name_en",
    )

    ordering = (
        "name_fr",
    )

    list_per_page = 25


# ============================================================
# POST SECTION INLINE
# ============================================================

class PostSectionInline(admin.StackedInline):
    model = PostSection
    extra = 1

    ordering = (
        "order",
    )

    classes = (
        "collapse",
    )

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


# ============================================================
# POST ADMIN
# ============================================================

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "image_preview",
        "title_fr",
        "category",
        "author",
        "published_at",
        "is_featured",
        "is_published",
    )

    list_display_links = (
        "image_preview",
        "title_fr",
    )

    list_editable = (
        "is_featured",
        "is_published",
    )

    list_filter = (
        "is_published",
        "is_featured",
        "category",
        "is_indexable",
        "published_at",
    )

    search_fields = (
        "title_fr",
        "title_de",
        "title_it",
        "title_en",
        "excerpt_fr",
        "excerpt_de",
        "excerpt_it",
        "excerpt_en",
        "content_fr",
        "content_de",
        "content_it",
        "content_en",
    )

    ordering = (
        "-published_at",
    )

    list_per_page = 25

    list_select_related = (
        "category",
        "author",
    )

    date_hierarchy = "published_at"

    autocomplete_fields = (
        "category",
    )

    filter_horizontal = (
        "tags",
    )

    prepopulated_fields = {
        "slug_fr": ("title_fr",),
        "slug_de": ("title_de",),
        "slug_it": ("title_it",),
        "slug_en": ("title_en",),
    }

    readonly_fields = (
        "image_preview_large",
        "created_at",
        "updated_at",
    )

    actions = (
        "publish_selected",
        "unpublish_selected",
        "feature_selected",
        "unfeature_selected",
    )

    inlines = (
        PostSectionInline,
    )

    # ========================================================
    # FIELDSETS
    # ========================================================

    def get_fieldsets(self, request, obj=None):
        grouped_fields = {
            "category",
            "tags",
            "author",
            "main_image",
            "image_preview_large",
            "title_fr",
            "slug_fr",
            "excerpt_fr",
            "content_fr",
            "title_de",
            "slug_de",
            "excerpt_de",
            "content_de",
            "title_it",
            "slug_it",
            "excerpt_it",
            "content_it",
            "title_en",
            "slug_en",
            "excerpt_en",
            "content_en",
            "published_at",
            "is_published",
            "is_featured",
            "created_at",
            "updated_at",
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
            (
                "Información general",
                {
                    "fields": (
                        "category",
                        "author",
                        "tags",
                    ),
                },
            ),
            (
                "Imagen principal",
                {
                    "fields": (
                        "main_image",
                        "image_preview_large",
                    ),
                },
            ),
            (
                "Français · Principal",
                {
                    "fields": (
                        "title_fr",
                        "slug_fr",
                        "excerpt_fr",
                        "content_fr",
                    ),
                },
            ),
            (
                "Deutsch",
                {
                    "classes": ("collapse",),
                    "fields": (
                        "title_de",
                        "slug_de",
                        "excerpt_de",
                        "content_de",
                    ),
                },
            ),
            (
                "Italiano",
                {
                    "classes": ("collapse",),
                    "fields": (
                        "title_it",
                        "slug_it",
                        "excerpt_it",
                        "content_it",
                    ),
                },
            ),
            (
                "English",
                {
                    "classes": ("collapse",),
                    "fields": (
                        "title_en",
                        "slug_en",
                        "excerpt_en",
                        "content_en",
                    ),
                },
            ),
            (
                "Publicación",
                {
                    "fields": (
                        "published_at",
                        "is_published",
                        "is_featured",
                    ),
                },
            ),
        ]

        if extra_fields:
            fieldsets.append(
                (
                    "SEO",
                    {
                        "classes": ("collapse",),
                        "fields": tuple(extra_fields),
                    },
                )
            )

        fieldsets.append(
            (
                "Sistema",
                {
                    "classes": ("collapse",),
                    "fields": (
                        "created_at",
                        "updated_at",
                    ),
                },
            )
        )

        return fieldsets

    # ========================================================
    # IMAGE PREVIEW · LIST
    # ========================================================

    @admin.display(description="Imagen")
    def image_preview(self, obj):
        if not obj.main_image:
            return "—"

        return format_html(
            '<img src="{}" style="width:80px;height:55px;object-fit:cover;border-radius:6px;" />',
            obj.main_image.url,
        )

    # ========================================================
    # IMAGE PREVIEW · FORM
    # ========================================================

    @admin.display(description="Vista previa")
    def image_preview_large(self, obj):
        if not obj or not obj.main_image:
            return "Sin imagen"

        return format_html(
            '<img src="{}" style="width:100%;max-width:500px;height:280px;object-fit:cover;border-radius:10px;" />',
            obj.main_image.url,
        )

    # ========================================================
    # AUTO AUTHOR
    # ========================================================

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user

        super().save_model(request, obj, form, change)

    # ========================================================
    # ACTIONS
    # ========================================================

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
