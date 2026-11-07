
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ProfessionalSitePage, ProfessionalVisualSettings, ProfessionalNeedItem,
    ProfessionalProcessItem, ProfessionalAdvantageItem, ProfessionalProjectItem,
    ProfessionalExtraBlock,
)

# ETIQUETAS EN INGLÉS Y AYUDAS EN ESPAÑOL | ENGLISH LABELS AND SPANISH HELP TEXTS
LANGUAGES = {
    "fr": ("French", "Idioma principal del sitio web. Completa primero este campo."),
    "de": ("German", "Versión en alemán. Si se deja vacío, la web puede utilizar el contenido francés como respaldo."),
    "it": ("Italian", "Versión en italiano. Si se deja vacío, la web puede utilizar el contenido francés como respaldo."),
    "en": ("English", "Versión en inglés. Si se deja vacío, la web puede utilizar el contenido francés como respaldo."),
    "es": ("Spanish (internal reference)", "Solo para referencia administrativa interna. El español no se muestra como idioma público de esta página."),
}
COMMON_HELP = {
    "page": "Selecciona la página de Profesionales a la que pertenece este registro.",
    "order": "Orden de aparición en la web. Los números menores se muestran primero; 0 es el primero.",
    "is_active": "Activa esta opción para mostrar el registro en la página; desactívala para ocultarlo sin eliminarlo.",
    "created_at": "Fecha y hora de creación del registro.",
    "updated_at": "Fecha y hora de su última actualización.",
    "image": "Fotografía opcional de esta sección. Las imágenes JPG, JPEG, PNG y WebP se optimizan automáticamente a WebP, con un máximo de 2200 px en su lado mayor. Si se deja vacía, se utilizará la imagen de respaldo disponible.",
}
COMMON_LABELS = {
    "page": "Professionals page",
    "order": "Display order",
    "is_active": "Visible on website",
    "created_at": "Created at",
    "updated_at": "Last updated",
    "image": "Section image",
}
for language, (language_name, guidance) in LANGUAGES.items():
    for prefix, field_label, field_description in (
        ("title", "Section title", "Título de la sección"),
        ("text", "Section description", "Descripción de la sección"),
    ):
        COMMON_LABELS[f"{prefix}_{language}"] = f"{field_label} · {language_name}"
        COMMON_HELP[f"{prefix}_{language}"] = f"{field_description} en {language_name}. {guidance}"
    COMMON_LABELS[f"hero_title_{language}"] = f"Hero heading · {language_name}"
    COMMON_LABELS[f"hero_text_{language}"] = f"Hero introduction · {language_name}"
    COMMON_HELP[f"hero_title_{language}"] = f"Título principal del encabezado de Profesionales. {guidance}"
    COMMON_HELP[f"hero_text_{language}"] = f"Texto introductorio situado debajo del título principal. {guidance}"

# NECESIDADES PROFESIONALES | PROFESSIONAL NEEDS
NEED_NAMES_EN = {
    "coordination": "Coordination of multiple trades",
    "planning": "Scheduled and responsive interventions",
    "turnover": "Property restoration between tenants",
    "maintenance": "Property maintenance and repairs",
    "occupancy": "Preparing premises for new occupants",
}

# ETAPAS DE INTERVENCIÓN | INTERVENTION STEPS
PROCESS_NAMES_EN = {
    "evaluation": "Property assessment",
    "planning": "Work planning",
    "intervention": "Coordinated intervention",
    "control": "Final inspection and handover",
}

# VENTAJAS PROFESIONALES | PROFESSIONAL ADVANTAGES
ADVANTAGE_NAMES_EN = {
    "single_contact": "Single point of contact",
    "coordination": "Coordination of multiple trades",
    "clear_quotes": "Clear quotations",
    "finishes": "Quality finishing",
    "responsiveness": "Responsiveness and organization",
    "flexibility": "Flexible collaboration",
}

# DISEÑOS DE BLOQUES | BLOCK LAYOUTS
LAYOUT_NAMES_EN = {
    "text": "Text section",
    "image_left": "Image on the left",
    "image_right": "Image on the right",
    "card": "Featured card",
    "cta": "Call-to-action section",
}


# AYUDAS COMUNES DEL ADMINISTRADOR | SHARED ADMIN HELP
class ProfessionalEnglishHelpMixin:
    """Mantiene las etiquetas y opciones en inglés, con instrucciones en español."""
    extra_help = {}
    extra_labels = {}
    english_choices = {}

    def get_form(self, request, obj=None, change=False, **kwargs):
        form_class = super().get_form(request, obj=obj, change=change, **kwargs)
        help_texts = {**COMMON_HELP, **self.extra_help}
        labels = {**COMMON_LABELS, **self.extra_labels}
        for name, form_field in form_class.base_fields.items():
            if name in help_texts:
                form_field.help_text = help_texts[name]
            if name in labels:
                form_field.label = labels[name]
            if name in self.english_choices:
                translations = self.english_choices[name]
                form_field.choices = [
                    (value, translations.get(value, caption))
                    for value, caption in form_field.choices
                ]
        return form_class


# VISTA PREVIA DE IMÁGENES | IMAGE PREVIEW
class ProfessionalImagesMixin:
    readonly_fields = ("image_preview", "created_at", "updated_at")

    @admin.display(description="Image preview")
    def image_preview(self, obj):
        if obj and getattr(obj, "image", None):
            try:
                return format_html(
                    '<img src="{}" style="max-width:360px;max-height:190px;object-fit:contain;border-radius:8px;"/>',
                    obj.image.url,
                )
            except (ValueError, AttributeError):
                pass
        from django.templatetags.static import static
        fallback = getattr(obj, "fallback_static", "antra/assets/img/professionals/professionals_default.webp")
        return format_html(
            '<img src="{}" title="Imagen predeterminada · STATIC" '
            'style="max-width:360px;max-height:190px;object-fit:contain;border-radius:8px;" />',
            static(fallback),
        )


# PÁGINA PRINCIPAL, HERO Y SERVICIOS VINCULADOS | MAIN PAGE, HERO AND LINKED SERVICES
@admin.register(ProfessionalSitePage)
class ProfessionalSitePageAdmin(ProfessionalEnglishHelpMixin, admin.ModelAdmin):
    list_display = ("hero_title_fr", "slug", "is_active", "updated_at")
    search_fields = ("hero_title_fr", "hero_title_de", "hero_title_it", "hero_title_en")
    list_filter = ("is_active",)
    filter_horizontal = ("services",)
    readonly_fields = ("created_at", "updated_at")
    extra_labels = {
        "slug": "Page identifier",
        "hero_image": "Main hero image",
        "services": "Services displayed on Professionals",
    }
    extra_help = {
        "slug": "Identificador interno único de la página. Normalmente debe ser 'main'. No lo cambies en la página principal, porque se utiliza para localizar su configuración.",
        "hero_image": "Imagen principal del encabezado. Tiene prioridad sobre la imagen de respaldo configurada en Professionals Visual Configuration. Se aceptan JPG, JPEG, PNG y WebP, que se optimizan automáticamente a WebP (máximo 2200 px).",
        "services": "Selecciona los servicios existentes que aparecerán en el carrusel de Profesionales. Sus textos, imágenes y demás información se administran desde la aplicación Services; aquí no se duplican.",
        "is_active": "Activa para publicar la página de Profesionales o desactiva para ocultarla sin borrar su contenido.",
    }
    fieldsets = (
        ("General settings", {
            "fields": ("slug", "is_active", "hero_image", "services"),
            "description": "Configura la página principal, su imagen de portada y los servicios que aparecerán en el carrusel. Las fotografías y fichas de servicios se gestionan desde Services.",
        }),
        ("🇫🇷 French · Primary", {
            "fields": ("hero_title_fr", "hero_text_fr"),
            "description": "Contenido principal en francés para la Suiza francófona.",
        }),
        ("🇩🇪 German", {
            "fields": ("hero_title_de", "hero_text_de"),
            "classes": ("collapse",),
            "description": "Versión en alemán del encabezado y de su introducción.",
        }),
        ("🇮🇹 Italian", {
            "fields": ("hero_title_it", "hero_text_it"),
            "classes": ("collapse",),
            "description": "Versión en italiano del encabezado y de su introducción.",
        }),
        ("🇬🇧 English", {
            "fields": ("hero_title_en", "hero_text_en"),
            "classes": ("collapse",),
            "description": "Versión en inglés del encabezado y de su introducción.",
        }),
        ("🇪🇸 Spanish · Internal reference", {
            "fields": ("hero_title_es", "hero_text_es"),
            "classes": ("collapse",),
            "description": "Solo para referencia administrativa interna; el español no es un idioma público de esta página.",
        }),
        ("System information", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )


# ADMINISTRACIÓN COMÚN DE NECESIDADES Y ETAPAS | SHARED NEEDS AND STEPS ADMIN
class ProfessionalContentAdmin(ProfessionalEnglishHelpMixin, ProfessionalImagesMixin, admin.ModelAdmin):
    list_display = ("section_label_en", "page", "order", "is_active", "image_preview")
    list_editable = ("order", "is_active")
    list_filter = ("page", "is_active")
    ordering = ("page", "order", "id")
    extra_labels = {
        "key": "Section type",
        "image": "Photograph",
    }
    extra_help = {
        "key": "Selecciona la sección fija a la que corresponde este registro. Cada opción puede usarse una sola vez por página. Evita cambiarla después de ingresar el contenido.",
        "image": "Fotografía de esta necesidad o etapa. Los archivos JPG, JPEG, PNG y WebP se convierten y optimizan a WebP (máximo 2200 px). Si no se carga, se muestra la imagen de respaldo.",
    }
    fieldsets = (
        ("Section configuration", {
            "fields": ("page", "key", "order", "is_active", "image", "image_preview"),
            "description": "Selecciona el tipo de sección, su orden de presentación y la imagen opcional. Cada tipo corresponde a un bloque de la plantilla de Profesionales.",
        }),
        ("🇫🇷 French · Primary", {
            "fields": ("title_fr", "text_fr"),
            "description": "Contenido público principal en francés.",
        }),
        ("🇩🇪 German", {
            "fields": ("title_de", "text_de"),
            "classes": ("collapse",),
        }),
        ("🇮🇹 Italian", {
            "fields": ("title_it", "text_it"),
            "classes": ("collapse",),
        }),
        ("🇬🇧 English", {
            "fields": ("title_en", "text_en"),
            "classes": ("collapse",),
        }),
        ("🇪🇸 Spanish · Internal reference", {
            "fields": ("title_es", "text_es"),
            "classes": ("collapse",),
            "description": "Texto de referencia interna; no se publica en español.",
        }),
        ("System information", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="Section (EN)", ordering="key")
    def section_label_en(self, obj):
        return self.english_choices.get("key", {}).get(obj.key, obj.key)


# NECESIDADES PROFESIONALES | PROFESSIONAL NEEDS
@admin.register(ProfessionalNeedItem)
class ProfessionalNeedItemAdmin(ProfessionalContentAdmin):
    extra_labels = {
        **ProfessionalContentAdmin.extra_labels,
        "key": "Professional need",
    }
    extra_help = {
        **ProfessionalContentAdmin.extra_help,
        "key": "Selecciona una de las cinco necesidades que atendemos para los clientes profesionales. Cada necesidad puede asociarse una sola vez a una misma página.",
    }
    english_choices = {"key": NEED_NAMES_EN}


# ETAPAS DEL PROCESO DE INTERVENCIÓN | INTERVENTION PROCESS STEPS
@admin.register(ProfessionalProcessItem)
class ProfessionalProcessItemAdmin(ProfessionalContentAdmin):
    extra_labels = {
        **ProfessionalContentAdmin.extra_labels,
        "key": "Intervention step",
    }
    extra_help = {
        **ProfessionalContentAdmin.extra_help,
        "key": "Selecciona una fase del proceso: evaluación, planificación, intervención o control final. Cada fase solo puede utilizarse una vez por página.",
    }
    english_choices = {"key": PROCESS_NAMES_EN}


# VENTAJAS Y ARGUMENTOS DE POR QUÉ V&V | WHY V&V ACCORDION ADVANTAGES
@admin.register(ProfessionalAdvantageItem)
class ProfessionalAdvantageItemAdmin(ProfessionalEnglishHelpMixin, admin.ModelAdmin):
    list_display = ("advantage_label_en", "page", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("page", "is_active")
    readonly_fields = ("created_at", "updated_at")
    extra_labels = {
        "key": "Advantage / argument",
    }
    extra_help = {
        "key": "Selecciona uno de los seis argumentos que explican por qué trabajar con V&V. Cada argumento puede utilizarse una sola vez por página.",
    }
    english_choices = {"key": ADVANTAGE_NAMES_EN}
    fieldsets = (
        ("Advantage configuration", {
            "fields": ("page", "key", "order", "is_active"),
            "description": "Cada registro activo aparecerá como una pregunta desplegable en la sección «Pourquoi V&V».",
        }),
        ("🇫🇷 French · Primary", {
            "fields": ("title_fr", "text_fr"),
            "description": "Contenido público principal en francés para Suiza.",
        }),
        ("🇩🇪 German", {
            "fields": ("title_de", "text_de"),
            "classes": ("collapse",),
        }),
        ("🇮🇹 Italian", {
            "fields": ("title_it", "text_it"),
            "classes": ("collapse",),
        }),
        ("🇬🇧 English", {
            "fields": ("title_en", "text_en"),
            "classes": ("collapse",),
        }),
        ("🇪🇸 Spanish · Internal reference", {
            "fields": ("title_es", "text_es"),
            "classes": ("collapse",),
            "description": "Referencia administrativa interna; no corresponde a un idioma público.",
        }),
        ("System information", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="Advantage (EN)", ordering="key")
    def advantage_label_en(self, obj):
        return ADVANTAGE_NAMES_EN.get(obj.key, obj.key)


# PROYECTOS VINCULADOS A PROFESIONALES | PROJECTS LINKED TO PROFESSIONALS
@admin.register(ProfessionalProjectItem)
class ProfessionalProjectItemAdmin(ProfessionalEnglishHelpMixin, admin.ModelAdmin):
    list_display = ("project_title_en", "project", "page", "order", "is_active")
    list_display_links = ("project_title_en",)
    list_editable = ("order", "is_active")
    list_filter = ("page", "is_active")
    fields = ("page", "project", "order", "is_active")
    autocomplete_fields = ()
    list_select_related = ("project", "page")
    extra_labels = {
        "project": "Project to feature",
    }
    extra_help = {
        "project": "Selecciona un proyecto existente de la aplicación Projects. En la página pública solo se mostrarán proyectos publicados. Las imágenes y traducciones se administran desde Projects.",
        "page": "Elige la página de Profesionales donde deseas destacar este proyecto.",
        "order": "Orden de aparición en el carrusel de proyectos de Profesionales. Los números menores aparecen primero.",
        "is_active": "Activa para mostrar el proyecto en Profesionales o desactiva para ocultarlo aquí. El proyecto original seguirá disponible en Projects.",
    }

    @admin.display(description="Project title (EN)")
    def project_title_en(self, obj):
        project = obj.project
        return getattr(project, "title_en", "") or getattr(project, "title_fr", "") or str(project)


# BLOQUES ADICIONALES DE CONTENIDO | OPTIONAL CONTENT BLOCKS
@admin.register(ProfessionalExtraBlock)
class ProfessionalExtraBlockAdmin(ProfessionalEnglishHelpMixin, ProfessionalImagesMixin, admin.ModelAdmin):
    list_display = ("title_fr", "page", "layout_label_en", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("page", "layout", "is_active")
    extra_labels = {
        "layout": "Content layout",
        "icon": "Icon CSS class",
        "image": "Optional block image",
    }
    extra_help = {
        "layout": "Elige cómo mostrar el bloque: solo texto, imagen a la izquierda, imagen a la derecha, tarjeta destacada o llamada a la acción.",
        "icon": "Clase CSS opcional de Font Awesome, por ejemplo: 'fa-solid fa-building'. Su presentación depende del diseño del bloque. Déjala vacía si no necesitas icono.",
        "image": "Fotografía opcional del bloque. Se aceptan JPEG, PNG y WebP; se convierten automáticamente a WebP optimizado (máximo 2200 px). Algunos diseños no necesitan fotografía.",
        "order": "Orden de aparición entre los bloques adicionales. El valor inicial recomendado es 0.",
    }
    english_choices = {"layout": LAYOUT_NAMES_EN}
    fieldsets = (
        ("Block configuration", {
            "fields": ("page", "layout", "image", "image_preview", "icon", "order", "is_active"),
            "description": "Añade contenido opcional después de las secciones principales de Profesionales. Selecciona el diseño y carga una imagen o un icono solo cuando sea necesario.",
        }),
        ("🇫🇷 French · Primary", {
            "fields": ("title_fr", "text_fr"),
            "description": "Contenido principal en francés para Suiza.",
        }),
        ("🇩🇪 German", {
            "fields": ("title_de", "text_de"),
            "classes": ("collapse",),
        }),
        ("🇮🇹 Italian", {
            "fields": ("title_it", "text_it"),
            "classes": ("collapse",),
        }),
        ("🇬🇧 English", {
            "fields": ("title_en", "text_en"),
            "classes": ("collapse",),
        }),
        ("🇪🇸 Spanish · Internal reference", {
            "fields": ("title_es", "text_es"),
            "classes": ("collapse",),
            "description": "Contenido de referencia interna; no aparece como idioma público.",
        }),
        ("System information", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="Layout", ordering="layout")
    def layout_label_en(self, obj):
        return LAYOUT_NAMES_EN.get(obj.layout, obj.layout)


# IMÁGENES DE RESPALDO Y FONDOS DE PROFESIONALES | PROFESSIONALS VISUAL SETTINGS
@admin.register(ProfessionalVisualSettings)
class ProfessionalVisualSettingsAdmin(ProfessionalEnglishHelpMixin, admin.ModelAdmin):
    list_display = ("page", "updated_at")
    fields = ("page", "turnover_background", "faq_image")
    extra_labels = {
        "turnover_background": "Between-tenants section background",
        "faq_image": "Why V&V sidebar image",
    }
    extra_help = {
        "page": "Selecciona la página de Profesionales a la que se aplicará esta configuración visual. Solo se permite un registro de configuración por página.",
        "turnover_background": "Imagen horizontal de fondo para la sección del proceso entre inquilinos (Remise en état). Si se deja vacía, se utilizará la imagen estática de respaldo. La optimización WebP es automática.",
        "faq_image": "Imagen lateral junto al acordeón «Pourquoi V&V». Se recomienda un encuadre que también funcione en formato vertical. Si se deja vacía, se utilizará el respaldo estático. La optimización WebP es automática.",
    }
