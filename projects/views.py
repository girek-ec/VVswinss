from django.shortcuts import render

from core.utils import get_by_localized_slug

from .models import Project


def project_list(request):
    proyectos = (
        Project.objects
        .filter(publicado=True)
        .select_related(
            "tipo",
            "tipo_edificio",
        )
        .prefetch_related("servicios")
    )

    context = {
        "proyectos": proyectos,
    }

    return render(
        request,
        "projects/project_list.html",
        context,
    )


def project_detail(request, slug):
    queryset = (
        Project.objects
        .filter(publicado=True)
        .select_related(
            "tipo",
            "tipo_edificio",
        )
        .prefetch_related(
            "servicios",
            "imagenes",
            "antes_despues",
            "intervenciones",
        )
    )

    proyecto = get_by_localized_slug(
        Project,
        slug,
        queryset=queryset,
    )

    relacionados = (
        Project.objects
        .filter(publicado=True)
        .exclude(pk=proyecto.pk)
        .order_by("-fecha_fin", "-created_at")[:3]
    )

    context = {
        "proyecto": proyecto,
        "relacionados": relacionados,
    }

    return render(
        request,
        "projects/project_detail.html",
        context,
    )