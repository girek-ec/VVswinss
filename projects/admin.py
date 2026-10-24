from django.contrib import admin
from django.utils.html import format_html

from .models import (
    BeforeAfter,
    BuildingType,
    Intervention,
    Project,
    ProjectImage,
    ProjectType,
)

# ============================================================
# HELPERS
# ============================================================

def render_image(field, width=100, height=70):
    if not field:
        return "—"

    try:
        return format_html(
            '<img src="{}" style="width:{}px;height:{}px;object-fit:cover;border-radius:6px;" />',
            field.url,
            width,
            height,
        )
    except (ValueError, AttributeError):
        return "—"

# ============================================================
# BASE ADMIN
# ============================================================

class BaseProjectAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")
    save_on_top = True
    list_per_page = 30
    empty_value_display = "—"

# ============================================================
# PROJECT IMAGE INLINE
# ============================================================

class ProjectImageInline(admin.StackedInline):
    model = ProjectImage
    extra = 0
    show_change_link = True
    ordering = ("order",)

    readonly_fields = (
        "image_preview",
        "created_at",
    )

    fieldsets = (
        (
            "Imagen",
            {
                "fields": (
                    "image",
                    "image_preview",
                    "order",
                ),
            },
        ),
        (
            "🇫🇷 Français · Principal",
            {
                "fields": (
                    "alt_fr",
                ),
            },
        ),
        (
            "🇪🇸 Español · Referencia interna",
            {
                "classes": ("collapse",),
                "fields": (
                    "alt_es",
                ),
            },
        ),
        (
            "🇩🇪 Deutsch",
            {
                "classes": ("collapse",),
                "fields": (
                    "alt_de",
                ),
            },
        ),
        (
            "🇮🇹 Italiano",
            {
                "classes": ("collapse",),
                "fields": (
                    "alt_it",
                ),
            },
        ),
        (
            "🇬🇧 English",
            {
                "classes": ("collapse",),
                "fields": (
                    "alt_en",
                ),
            },
        ),
        (
            "Sistema",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                ),
            },
        ),
    )

    @admin.display(description="Vista previa")
    def image_preview(self, obj):
        return render_image(obj.image if obj else None, 240, 150)

# ============================================================
# BEFORE / AFTER INLINE
# ============================================================

class BeforeAfterInline(admin.StackedInline):
    model = BeforeAfter
    extra = 0
    show_change_link = True
    ordering = ("order",)

    readonly_fields = (
        "before_preview",
        "after_preview",
        "created_at",
    )

    fieldsets = (
        (
            "Imágenes",
            {
                "fields": (
                    "before_image",
                    "before_preview",
                    "after_image",
                    "after_preview",
                    "order",
                ),
            },
        ),
        (
            "🇫🇷 Français · Principal",
            {
                "fields": (
                    "title_fr",
                ),
            },
        ),
        (
            "🇪🇸 Español · Referencia interna",
            {
                "classes": ("collapse",),
                "fields": (
                    "title_es",
                ),
            },
        ),
        (
            "🇩🇪 Deutsch",
            {
                "classes": ("collapse",),
                "fields": (
                    "title_de",
                ),
            },
        ),
        (
            "🇮🇹 Italiano",
            {
                "classes": ("collapse",),
                "fields": (
                    "title_it",
                ),
            },
        ),
        (
            "🇬🇧 English",
            {
                "classes": ("collapse",),
                "fields": (
                    "title_en",
                ),
            },
        ),
        (
            "Sistema",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                ),
            },
        ),
    )

    @admin.display(description="Antes")
    def before_preview(self, obj):
        return render_image(obj.before_image if obj else None, 240, 150)

    @admin.display(description="Después")
    def after_preview(self, obj):
        return render_image(obj.after_image if obj else None, 240, 150)

# ============================================================
# INTERVENTION INLINE
# ============================================================

class InterventionInline(admin.StackedInline):
    model = Intervention
    extra = 0
    show_change_link = True
    ordering = ("order",)

    readonly_fields = (
        "created_at",
    )

    fieldsets = (
        (
            "Configuración",
            {
                "fields": (
                    "order",
                ),
            },
        ),
        (
            "🇫🇷 Français · Principal",
            {
                "fields": (
                    "title_fr",
                    "description_fr",
                ),
            },
        ),
        (
            "🇪🇸 Español · Referencia interna",
            {
                "classes": ("collapse",),
                "fields": (
                    "title_es",
                    "description_es",
                ),
            },
        ),
        (
            "🇩🇪 Deutsch",
            {
                "classes": ("collapse",),
                "fields": (
                    "title_de",
                    "description_de",
                ),
            },
        ),
        (
            "🇮🇹 Italiano",
            {
                "classes": ("collapse",),
                "fields": (
                    "title_it",
                    "description_it",
                ),
            },
        ),
        (
            "🇬🇧 English",
            {
                "classes": ("collapse",),
                "fields": (
                    "title_en",
                    "description_en",
                ),
            },
        ),
        (
            "Sistema",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                ),
            },
        ),
    )

# ============================================================
# PROJECT TYPE
# ============================================================

@admin.register(ProjectType)
class ProjectTypeAdmin(BaseProjectAdmin):

    list_display = (
        "name_fr",
        "name_es",
        "order",
        "is_active",
    )

    list_editable = (
        "order",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name_es",
        "name_fr",
        "name_de",
        "name_it",
        "name_en",
    )

    ordering = (
        "order",
        "name_fr",
    )

    fieldsets = (
        (
            "🇫🇷 Français · Principal",
            {
                "fields": (
                    "name_fr",
                ),
            },
        ),
        (
            "🇪🇸 Español · Referencia interna",
            {
                "classes": ("collapse",),
                "fields": (
                    "name_es",
                ),
            },
        ),
        (
            "🇩🇪 Deutsch",
            {
                "classes": ("collapse",),
                "fields": (
                    "name_de",
                ),
            },
        ),
        (
            "🇮🇹 Italiano",
            {
                "classes": ("collapse",),
                "fields": (
                    "name_it",
                ),
            },
        ),
        (
            "🇬🇧 English",
            {
                "classes": ("collapse",),
                "fields": (
                    "name_en",
                ),
            },
        ),
        (
            "Configuración",
            {
                "fields": (
                    "order",
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

# ============================================================
# BUILDING TYPE
# ============================================================

@admin.register(BuildingType)
class BuildingTypeAdmin(BaseProjectAdmin):

    list_display = (
        "name_fr",
        "name_es",
        "order",
        "is_active",
    )

    list_editable = (
        "order",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name_es",
        "name_fr",
        "name_de",
        "name_it",
        "name_en",
    )

    ordering = (
        "order",
        "name_fr",
    )

    fieldsets = (
        (
            "🇫🇷 Français · Principal",
            {
                "fields": (
                    "name_fr",
                ),
            },
        ),
        (
            "🇪🇸 Español · Referencia interna",
            {
                "classes": ("collapse",),
                "fields": (
                    "name_es",
                ),
            },
        ),
        (
            "🇩🇪 Deutsch",
            {
                "classes": ("collapse",),
                "fields": (
                    "name_de",
                ),
            },
        ),
        (
            "🇮🇹 Italiano",
            {
                "classes": ("collapse",),
                "fields": (
                    "name_it",
                ),
            },
        ),
        (
            "🇬🇧 English",
            {
                "classes": ("collapse",),
                "fields": (
                    "name_en",
                ),
            },
        ),
        (
            "Configuración",
            {
                "fields": (
                    "order",
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

# ============================================================
# PROJECT
# ============================================================

@admin.register(Project)
class ProjectAdmin(BaseProjectAdmin):

    list_display = (
        "main_image_thumb",
        "title_fr",
        "project_type",
        "building_type",
        "location",
        "end_date",
        "show_on_map",
        "is_featured",
        "is_published",
    )

    list_display_links = (
        "main_image_thumb",
        "title_fr",
    )

    list_editable = (
        "show_on_map",
        "is_featured",
        "is_published",
    )

    list_filter = (
        "is_published",
        "is_featured",
        "show_on_map",
        "project_type",
        "building_type",
        "services",
        "start_date",
        "end_date",
        "created_at",
    )

    search_fields = (
        "title_es",
        "title_fr",
        "title_de",
        "title_it",
        "title_en",
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
        "location",
        "client",
    )

    autocomplete_fields = (
        "project_type",
        "building_type",
    )

    filter_horizontal = (
        "services",
    )

    list_select_related = (
        "project_type",
        "building_type",
    )

    prepopulated_fields = {
        "slug_fr": ("title_fr",),
        "slug_de": ("title_de",),
        "slug_it": ("title_it",),
        "slug_en": ("title_en",),
    }

    readonly_fields = (
        "main_image_preview",
        "og_image_preview",
        "created_at",
        "updated_at",
    )

    date_hierarchy = "created_at"

    ordering = (
        "-created_at",
    )

    inlines = (
        ProjectImageInline,
        BeforeAfterInline,
        InterventionInline,
    )

    actions = (
        "publish_selected",
        "unpublish_selected",
        "feature_selected",
        "unfeature_selected",
    )

    fieldsets = (
        (
            "Clasificación",
            {
                "fields": (
                    "project_type",
                    "building_type",
                    "services",
                ),
            },
        ),
        (
            "Información del proyecto",
            {
                "fields": (
                    "location",
                    "client",
                    "start_date",
                    "end_date",
                ),
            },
        ),
        (
            "Mapa de realizaciones",
            {
                "description": "Indique las coordenadas del proyecto y active su visualización en el mapa público.",
                "fields": (
                    "latitude",
                    "longitude",
                    "show_on_map",
                ),
            },
        ),
        (
            "Imagen principal",
            {
                "fields": (
                    "main_image",
                    "main_image_preview",
                ),
            },
        ),
        (
            "🇫🇷 Français · Principal",
            {
                "fields": (
                    "title_fr",
                    "slug_fr",
                    "summary_fr",
                    "content_fr",
                    "seo_title_fr",
                    "meta_description_fr",
                ),
            },
        ),
        (
            "🇪🇸 Español · Referencia interna",
            {
                "classes": ("collapse",),
                "description": "Estos campos son únicamente de referencia interna y no corresponden a un idioma público del sitio.",
                "fields": (
                    "title_es",
                    "summary_es",
                    "content_es",
                    "seo_title_es",
                    "meta_description_es",
                ),
            },
        ),
        (
            "🇩🇪 Deutsch",
            {
                "classes": ("collapse",),
                "fields": (
                    "title_de",
                    "slug_de",
                    "summary_de",
                    "content_de",
                    "seo_title_de",
                    "meta_description_de",
                ),
            },
        ),
        (
            "🇮🇹 Italiano",
            {
                "classes": ("collapse",),
                "fields": (
                    "title_it",
                    "slug_it",
                    "summary_it",
                    "content_it",
                    "seo_title_it",
                    "meta_description_it",
                ),
            },
        ),
        (
            "🇬🇧 English",
            {
                "classes": ("collapse",),
                "fields": (
                    "title_en",
                    "slug_en",
                    "summary_en",
                    "content_en",
                    "seo_title_en",
                    "meta_description_en",
                ),
            },
        ),
        (
            "SEO social",
            {
                "fields": (
                    "og_image",
                    "og_image_preview",
                    "is_indexable",
                ),
            },
        ),
        (
            "Publicación",
            {
                "fields": (
                    "is_featured",
                    "is_published",
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

    @admin.display(description="Imagen")
    def main_image_thumb(self, obj):
        return render_image(obj.main_image, 80, 55)

    @admin.display(description="Vista previa")
    def main_image_preview(self, obj):
        return render_image(obj.main_image if obj else None, 500, 300)

    @admin.display(description="Vista previa Open Graph")
    def og_image_preview(self, obj):
        return render_image(obj.og_image if obj else None, 500, 263)

    @admin.action(description="Publicar proyectos seleccionados")
    def publish_selected(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description="Despublicar proyectos seleccionados")
    def unpublish_selected(self, request, queryset):
        queryset.update(is_published=False)

    @admin.action(description="Marcar como destacados")
    def feature_selected(self, request, queryset):
        queryset.update(is_featured=True)

    @admin.action(description="Quitar de destacados")
    def unfeature_selected(self, request, queryset):
        queryset.update(is_featured=False)

# ============================================================
# PROJECT IMAGE
# ============================================================

@admin.register(ProjectImage)
class ProjectImageAdmin(BaseProjectAdmin):

    list_display = (
        "image_preview",
        "project",
        "alt_fr",
        "order",
        "created_at",
    )

    list_display_links = (
        "image_preview",
        "project",
    )

    list_filter = (
        "project",
    )

    search_fields = (
        "project__title_es",
        "project__title_fr",
        "project__title_de",
        "project__title_it",
        "project__title_en",
        "alt_es",
        "alt_fr",
        "alt_de",
        "alt_it",
        "alt_en",
    )

    autocomplete_fields = (
        "project",
    )

    list_editable = (
        "order",
    )

    ordering = (
        "project",
        "order",
    )

    readonly_fields = (
        "image_preview_large",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Imagen",
            {
                "fields": (
                    "project",
                    "image",
                    "image_preview_large",
                    "order",
                ),
            },
        ),
        (
            "🇫🇷 Français · Principal",
            {
                "fields": (
                    "alt_fr",
                ),
            },
        ),
        (
            "🇪🇸 Español · Referencia interna",
            {
                "classes": ("collapse",),
                "fields": (
                    "alt_es",
                ),
            },
        ),
        (
            "🇩🇪 Deutsch",
            {
                "classes": ("collapse",),
                "fields": (
                    "alt_de",
                ),
            },
        ),
        (
            "🇮🇹 Italiano",
            {
                "classes": ("collapse",),
                "fields": (
                    "alt_it",
                ),
            },
        ),
        (
            "🇬🇧 English",
            {
                "classes": ("collapse",),
                "fields": (
                    "alt_en",
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

    @admin.display(description="Imagen")
    def image_preview(self, obj):
        return render_image(obj.image, 90, 60)

    @admin.display(description="Vista previa")
    def image_preview_large(self, obj):
        return render_image(obj.image if obj else None, 500, 300)

# ============================================================
# BEFORE / AFTER
# ============================================================

@admin.register(BeforeAfter)
class BeforeAfterAdmin(BaseProjectAdmin):

    list_display = (
        "before_thumb",
        "after_thumb",
        "project",
        "title_fr",
        "order",
        "created_at",
    )

    list_display_links = (
        "before_thumb",
        "project",
    )

    list_filter = (
        "project",
    )

    search_fields = (
        "project__title_es",
        "project__title_fr",
        "project__title_de",
        "project__title_it",
        "project__title_en",
        "title_es",
        "title_fr",
        "title_de",
        "title_it",
        "title_en",
    )

    autocomplete_fields = (
        "project",
    )

    list_editable = (
        "order",
    )

    ordering = (
        "project",
        "order",
    )

    readonly_fields = (
        "before_preview",
        "after_preview",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Proyecto e imágenes",
            {
                "fields": (
                    "project",
                    "before_image",
                    "before_preview",
                    "after_image",
                    "after_preview",
                    "order",
                ),
            },
        ),
        (
            "🇫🇷 Français · Principal",
            {
                "fields": (
                    "title_fr",
                ),
            },
        ),
        (
            "🇪🇸 Español · Referencia interna",
            {
                "classes": ("collapse",),
                "fields": (
                    "title_es",
                ),
            },
        ),
        (
            "🇩🇪 Deutsch",
            {
                "classes": ("collapse",),
                "fields": (
                    "title_de",
                ),
            },
        ),
        (
            "🇮🇹 Italiano",
            {
                "classes": ("collapse",),
                "fields": (
                    "title_it",
                ),
            },
        ),
        (
            "🇬🇧 English",
            {
                "classes": ("collapse",),
                "fields": (
                    "title_en",
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

    @admin.display(description="Antes")
    def before_thumb(self, obj):
        return render_image(obj.before_image, 80, 55)

    @admin.display(description="Después")
    def after_thumb(self, obj):
        return render_image(obj.after_image, 80, 55)

    @admin.display(description="Vista previa · Antes")
    def before_preview(self, obj):
        return render_image(obj.before_image if obj else None, 400, 260)

    @admin.display(description="Vista previa · Después")
    def after_preview(self, obj):
        return render_image(obj.after_image if obj else None, 400, 260)

# ============================================================
# INTERVENTION
# ============================================================

@admin.register(Intervention)
class InterventionAdmin(BaseProjectAdmin):

    list_display = (
        "project",
        "title_fr",
        "order",
        "created_at",
    )

    list_display_links = (
        "project",
        "title_fr",
    )

    list_filter = (
        "project",
    )

    search_fields = (
        "project__title_es",
        "project__title_fr",
        "project__title_de",
        "project__title_it",
        "project__title_en",
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

    autocomplete_fields = (
        "project",
    )

    list_editable = (
        "order",
    )

    ordering = (
        "project",
        "order",
    )

    fieldsets = (
        (
            "Proyecto",
            {
                "fields": (
                    "project",
                    "order",
                ),
            },
        ),
        (
            "🇫🇷 Français · Principal",
            {
                "fields": (
                    "title_fr",
                    "description_fr",
                ),
            },
        ),
        (
            "🇪🇸 Español · Referencia interna",
            {
                "classes": ("collapse",),
                "fields": (
                    "title_es",
                    "description_es",
                ),
            },
        ),
        (
            "🇩🇪 Deutsch",
            {
                "classes": ("collapse",),
                "fields": (
                    "title_de",
                    "description_de",
                ),
            },
        ),
        (
            "🇮🇹 Italiano",
            {
                "classes": ("collapse",),
                "fields": (
                    "title_it",
                    "description_it",
                ),
            },
        ),
        (
            "🇬🇧 English",
            {
                "classes": ("collapse",),
                "fields": (
                    "title_en",
                    "description_en",
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
