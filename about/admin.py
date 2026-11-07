
# ABOUT · INDEPENDENT ADMIN | ADMINISTRACIÓN INDEPENDIENTE
from django import forms
from django.contrib import admin
from django.db import transaction
from django.templatetags.static import static
from django.utils.html import format_html, format_html_join
from core.admin import (
    AboutContentAdmin as LegacyAboutContentAdmin,
    TeamMemberAdmin as LegacyTeamMemberAdmin,
    InsuranceAdmin as LegacyInsuranceAdmin,
    CertificationAdmin as LegacyCertificationAdmin,
    CompanyValueAdmin as LegacyCompanyValueAdmin,
    ProcessStepAdmin as LegacyProcessStepAdmin,
)
from core.models import (
    AboutContent as LegacyAboutContent,
    TeamMember as LegacyTeamMember,
    Insurance as LegacyInsurance,
    Certification as LegacyCertification,
    CompanyValue as LegacyCompanyValue,
    ProcessStep as LegacyProcessStep,
)
from core.visual_config import AboutPageConfiguration as LegacyAboutPageConfiguration
from core.visual_config_admin import AboutPageConfigurationAdmin as LegacyVisualAdmin
from .models import (
    AboutContent,
    AboutPageConfiguration,
    TeamMember,
    Insurance,
    Certification,
    CompanyValue,
    ProcessStep,
)

# ABOUT · REMOVE ORIGINAL CORE REGISTRATIONS | ELIMINAR REGISTROS DUPLICADOS
for legacy_model in (
    LegacyAboutContent,
    LegacyAboutPageConfiguration,
    LegacyTeamMember,
    LegacyInsurance,
    LegacyCertification,
    LegacyCompanyValue,
    LegacyProcessStep,
):
    if admin.site.is_registered(legacy_model):
        admin.site.unregister(legacy_model)

# ABOUT CONTENT · TEXT ONLY | SOLO CONTENIDO EDITORIAL
@admin.register(AboutContent)
class AboutContentAdmin(LegacyAboutContentAdmin):
    fieldsets = tuple(
        (
            title,
            {
                **options,
                "fields": tuple(
                    field for field in options["fields"]
                    if field not in ("image", "image_preview")
                ),
            },
        )
        for title, options in LegacyAboutContentAdmin.fieldsets
    )
    readonly_fields = tuple(
        field for field in LegacyAboutContentAdmin.readonly_fields
        if field != "image_preview"
    )

# ABOUT · LINKED MAIN IMAGE FORM | FORMULARIO DE IMAGEN PRINCIPAL VINCULADA
class AboutVisualConfigurationForm(forms.ModelForm):
    intro_image = forms.ImageField(
        required=False,
        label="Introduction image",
        help_text="Image used in the About introduction. Leave empty to use the default static image.",
        widget=forms.ClearableFileInput,
    )

    class Meta:
        model = AboutPageConfiguration
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.about_record = (
            LegacyAboutContent.objects.filter(is_active=True).order_by("pk").first()
            or LegacyAboutContent.objects.order_by("pk").first()
        )
        if self.about_record and self.about_record.image:
            self.fields["intro_image"].initial = self.about_record.image

    def clean_intro_image(self):
        value = self.cleaned_data.get("intro_image")
        if self.about_record is None and "intro_image" in self.changed_data:
            raise forms.ValidationError(
                "Create an About Us content record before uploading an introduction image."
            )
        return value

# ABOUT VISUAL CONFIGURATION | CONFIGURACIÓN VISUAL DE ABOUT
@admin.register(AboutPageConfiguration)
class AboutPageConfigurationAdmin(LegacyVisualAdmin):
    form = AboutVisualConfigurationForm

    # IMAGE FIELDS AND STATIC FALLBACKS | CAMPOS Y RESPALDOS STATIC
    _image_config = {
        "intro_image": (
            "Introduction image",
            "antra/assets/img/images/about-img-2.png",
        ),
        "header_background": (
            "Header background",
            "antra/assets/img/bg-img/page-header-bg.webp",
        ),
        "mission_primary_image": (
            "Mission primary image",
            "antra/assets/img/images/about-img-4.webp",
        ),
        "mission_secondary_image": (
            "Mission secondary image",
            "antra/assets/img/images/about-img-5.webp",
        ),
        "vision_background": (
            "Vision background",
            "antra/assets/img/bg-img/service-bg-1.png",
        ),
        "vision_image": (
            "Vision image",
            "antra/assets/img/images/skill-img-1.webp",
        ),
        "projects_background": (
            "Projects section background",
            "antra/assets/img/bg-img/gallary-bg-1.webp",
        ),
    }

    readonly_fields = tuple(
        getattr(LegacyVisualAdmin, "readonly_fields", ())
    ) + tuple(
        name + "_preview" for name in _image_config
    )

    list_display = (
        "__str__",
        "image_thumbnails",
        "updated_at",
    )

    class Media:
        js = ("about/admin/about_visual_previews.js",)
        css = {
            "all": ("about/admin/about_visual_previews.css",)
        }

    # VISUAL CONFIGURATION FIELDSETS | ORGANIZACIÓN DE CAMPOS
    def get_fieldsets(self, request, obj=None):
        result = [
            (
                "ABOUT · Introduction",
                {
                    "fields": (
                        "intro_image",
                        "intro_image_preview",
                    )
                },
            )
        ]

        for title, options in super().get_fieldsets(request, obj):
            updated = dict(options)
            fields = []

            for entry in options.get("fields", ()):
                fields.append(entry)
                names = (
                    entry if isinstance(entry, (tuple, list))
                    else (entry,)
                )
                for name in names:
                    if name in self._image_config and name != "intro_image":
                        fields.append(name + "_preview")

            updated["fields"] = tuple(fields)
            result.append((title, updated))

        return tuple(result)

    # SAVE LINKED INTRODUCTION IMAGE | GUARDAR IMAGEN PRINCIPAL VINCULADA
    @transaction.atomic
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if "intro_image" not in form.changed_data:
            return

        about_record = form.about_record

        if about_record is None:
            return

        image = form.cleaned_data.get("intro_image")

        if image is False:
            about_record.image = None
        elif image is not None:
            about_record.image = image
        else:
            return

        about_record.save(update_fields=("image", "updated_at"))

    # GET IMAGE URL | OBTENER URL DE IMAGEN
    def _image_url(self, obj, field_name):
        if field_name == "intro_image":
            record = (
                LegacyAboutContent.objects.filter(is_active=True).order_by("pk").first()
                or LegacyAboutContent.objects.order_by("pk").first()
            )
            image = record.image if record else None
        else:
            image = (
                getattr(obj, field_name, None)
                if obj is not None else None
            )

        if not image:
            return None

        try:
            return image.url
        except (ValueError, OSError):
            return None

    # IMAGE CARD | TARJETA DE MINIATURA
    @staticmethod
    def _image_card(url, label, status):
        return format_html(
            '<div style="display:inline-flex;flex-direction:column;gap:5px;max-width:235px">'
            '<a href="{}" target="_blank" rel="noopener noreferrer" title="{}">'
            '<img src="{}" alt="{}" loading="lazy" '
            'style="width:220px;height:130px;object-fit:cover;'
            'border:1px solid #d5dbe1;border-radius:6px;background:#f4f6f9"></a>'
            '<strong style="font-size:12px">{}</strong>'
            '<span style="font-size:12px;color:#666">{}</span>'
            '</div>',
            url, label, url, label, label, status,
        )

    # CURRENT IMAGE AND FALLBACK | IMAGEN ACTUAL Y RESPALDO
    def _preview(self, obj, field_name):
        label, fallback = self._image_config[field_name]
        custom_url = self._image_url(obj, field_name)

        if not custom_url:
            return self._image_card(
                static(fallback),
                label,
                "Currently displayed · Default from static",
            )

        return format_html(
            '<div style="display:flex;gap:16px;flex-wrap:wrap">{}{}</div>',
            self._image_card(
                custom_url,
                label,
                "Currently displayed · Uploaded image",
            ),
            self._image_card(
                static(fallback),
                label,
                "Default image from static",
            ),
        )

    # INTRODUCTION IMAGE PREVIEW | VISTA PREVIA DE INTRODUCCIÓN
    @admin.display(description="Image preview")
    def intro_image_preview(self, obj):
        return self._preview(obj, "intro_image")

    # HEADER PREVIEW | VISTA PREVIA DEL ENCABEZADO
    @admin.display(description="Image preview")
    def header_background_preview(self, obj):
        return self._preview(obj, "header_background")

    # MISSION PRIMARY PREVIEW | MISIÓN PRINCIPAL
    @admin.display(description="Image preview")
    def mission_primary_image_preview(self, obj):
        return self._preview(obj, "mission_primary_image")

    # MISSION SECONDARY PREVIEW | MISIÓN SECUNDARIA
    @admin.display(description="Image preview")
    def mission_secondary_image_preview(self, obj):
        return self._preview(obj, "mission_secondary_image")

    # VISION BACKGROUND PREVIEW | FONDO DE VISIÓN
    @admin.display(description="Image preview")
    def vision_background_preview(self, obj):
        return self._preview(obj, "vision_background")

    # VISION IMAGE PREVIEW | IMAGEN DE VISIÓN
    @admin.display(description="Image preview")
    def vision_image_preview(self, obj):
        return self._preview(obj, "vision_image")

    # PROJECTS BACKGROUND PREVIEW | FONDO DE PROYECTOS
    @admin.display(description="Image preview")
    def projects_background_preview(self, obj):
        return self._preview(obj, "projects_background")

    # CHANGELIST IMAGE THUMBNAILS | MINIATURAS EN EL LISTADO
    @admin.display(description="Image thumbnails")
    def image_thumbnails(self, obj):
        entries = []

        for field_name, (label, fallback) in self._image_config.items():
            custom_url = self._image_url(obj, field_name)
            entries.append((
                custom_url or static(fallback),
                label,
                "Uploaded image" if custom_url else "Default from static",
            ))

        return format_html_join(
            " ",
            '<a href="{}" title="{} · {}" target="_blank" rel="noopener noreferrer">'
            '<img src="{}" alt="{}" loading="lazy" '
            'style="width:72px;height:52px;object-fit:cover;'
            'border:1px solid #d5dbe1;border-radius:5px"></a>',
            (
                (url, label, status, url, label)
                for url, label, status in entries
            ),
        )

# ABOUT · CORPORATE ADMINISTRATION | ADMINISTRACIÓN CORPORATIVA
@admin.register(TeamMember)
class TeamMemberAdmin(LegacyTeamMemberAdmin):
    pass

@admin.register(Insurance)
class InsuranceAdmin(LegacyInsuranceAdmin):
    pass

@admin.register(Certification)
class CertificationAdmin(LegacyCertificationAdmin):
    pass

@admin.register(CompanyValue)
class CompanyValueAdmin(LegacyCompanyValueAdmin):
    pass

@admin.register(ProcessStep)
class ProcessStepAdmin(LegacyProcessStepAdmin):
    pass
