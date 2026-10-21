from django.shortcuts import redirect, render

from contact.forms import ContactRequestForm
from core.utils import current_language, get_by_localized_slug

from .models import Project


# ============================================================
# PROJECT LIST
# ============================================================

def project_list(request):
    projects = Project.objects.filter(is_published=True).select_related("project_type", "building_type").prefetch_related("services")

    context = {
        "projects": projects,
    }

    return render(request, "projects/project_list.html", context)


# ============================================================
# PROJECT DETAIL
# ============================================================

def project_detail(request, slug):
    language = current_language()

    queryset = Project.objects.filter(is_published=True).select_related("project_type", "building_type").prefetch_related(
        "services",
        "images",
        "before_after",
        "interventions",
    )

    project = get_by_localized_slug(
        Project,
        slug,
        queryset=queryset,
    )

    # ========================================================
    # CANONICAL LOCALIZED SLUG
    # ========================================================

    localized_slug = getattr(project, f"slug_{language}", None) or project.slug_fr

    if slug != localized_slug:
        return redirect("projects:detail", slug=localized_slug)

    # ========================================================
    # CONTEXT
    # ========================================================

    context = {
        "project": project,
        "form": ContactRequestForm(),
    }

    return render(request, "projects/project_detail.html", context)