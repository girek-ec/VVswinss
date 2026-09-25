from django.shortcuts import render

from core.utils import get_by_localized_slug

from .models import Service, ServiceCategory


def service_list(request):
    categorias = (
        ServiceCategory.objects
        .filter(activo=True)
        .prefetch_related("servicios")
        .order_by("orden")
    )

    servicios = (
        Service.objects
        .filter(activo=True)
        .select_related("categoria")
        .order_by("orden")
    )

    context = {
        "categorias": categorias,
        "servicios": servicios,
    }

    return render(
        request,
        "services/service_list.html",
        context,
    )


def service_detail(request, slug):
    queryset = (
        Service.objects
        .filter(activo=True)
        .select_related("categoria")
        .prefetch_related(
            "beneficios",
            "imagenes",
        )
    )

    servicio = get_by_localized_slug(
        Service,
        slug,
        queryset=queryset,
    )

    relacionados = (
        Service.objects
        .filter(
            activo=True,
            categoria=servicio.categoria,
        )
        .exclude(pk=servicio.pk)
        .order_by("orden")[:3]
    )

    context = {
        "servicio": servicio,
        "relacionados": relacionados,
    }

    return render(
        request,
        "services/service_detail.html",
        context,
    )