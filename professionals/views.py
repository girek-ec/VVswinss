from django.shortcuts import render
from django.templatetags.static import static
from contact.forms import ContactRequestForm
from projects.models import Project
from .models import (
    ProfessionalSitePage, ProfessionalNeedItem, ProfessionalProcessItem,
    ProfessionalAdvantageItem, ProfessionalProjectItem, ProfessionalExtraBlock,
    ProfessionalVisualSettings,
)

# IMAGEN ESTÁTICA UNIVERSAL | UNIVERSAL STATIC FALLBACK
STATIC_DEFAULT = "antra/assets/img/professionals/professionals_default.webp"


def _image_url(item):
    if item.image:
        return item.image.url
    return static(getattr(item, "fallback_static", STATIC_DEFAULT))


# PROFESIONALES · CONTENIDOS EXCLUSIVAMENTE V2 | ALL CONTENT COMES FROM NEW TABLES
def professionals(request):
    page = ProfessionalSitePage.objects.filter(slug="main", is_active=True).prefetch_related("services").first()
    visuals = ProfessionalVisualSettings.objects.filter(page=page).first() if page else None
    needs = list(ProfessionalNeedItem.objects.filter(page=page, is_active=True)) if page else []
    processes = list(ProfessionalProcessItem.objects.filter(page=page, is_active=True)) if page else []
    advantages = list(ProfessionalAdvantageItem.objects.filter(page=page, is_active=True)) if page else []
    blocks = list(ProfessionalExtraBlock.objects.filter(page=page, is_active=True)) if page else []
    for item in (*needs, *processes):
        item.resolved_image_url = _image_url(item)

    # SELECCIÓN ESPECÍFICA O PROYECTOS GLOBALES DESTACADOS | SELECTED OR EXISTING FEATURED PROJECTS
    selections = list(ProfessionalProjectItem.objects.filter(
        page=page, is_active=True, project__is_published=True
    ).select_related("project").prefetch_related("project__services")) if page else []
    if selections:
        featured_projects = [selection.project for selection in selections]
    else:
        featured_projects = (Project.objects.filter(is_published=True, is_featured=True)
                             .prefetch_related("services").order_by("-created_at")[:6])

    for project in featured_projects:
        project.resolved_image_url = (
            project.main_image.url if project.main_image
            else static("antra/assets/img/project/VVS_placeholder_cuadrado.webp")
        )

    return render(request, "professionals/index.html", {
        "professional_page": page,
        "professional_visuals": visuals,
        "page_images": bool(visuals),
        "professional_needs": needs,
        "professional_processes": processes,
        "professional_advantages": advantages,
        "professional_blocks": blocks,
        "featured_projects": featured_projects,
        "form": ContactRequestForm(),
    })
