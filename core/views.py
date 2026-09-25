from django.shortcuts import render

from services.models import Service
from projects.models import Project

from .models import (
    FAQ,
    HomeContent,
    ProcessStep,
    Testimonial,
)


def home(request):
    context = {
        "home": (
            HomeContent.objects
            .filter(activo=True)
            .first()
        ),

        "servicios_destacados": (
            Service.objects
            .filter(
                activo=True,
                destacado=True,
            )
            .select_related("categoria")[:6]
        ),

        "proyectos_destacados": (
            Project.objects
            .filter(
                publicado=True,
                destacado=True,
            )
            .prefetch_related("servicios")[:6]
        ),

        "pasos": (
            ProcessStep.objects
            .filter(activo=True)
            .order_by("numero")
        ),

        "testimonios": (
            Testimonial.objects
            .filter(activo=True)[:6]
        ),

        "faqs": (
            FAQ.objects
            .filter(activo=True)
            .select_related("categoria")[:8]
        ),
    }

    return render(
        request,
        "core/home.html",
        context,
    )