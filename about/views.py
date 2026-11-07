# ABOUT · VISTA INDEPENDIENTE | ABOUT · INDEPENDENT VIEW
# La plantilla y los objetos corporativos compartidos mantienen su comportamiento.
from django.shortcuts import render
from contact.forms import ContactRequestForm
from projects.models import Project
from core.models import (
    Certification, CompanyValue, Insurance, InstitutionalPage,
    ProcessStep, Statistic, TeamMember, Testimonial,
)
from .models import AboutContent, AboutPageConfiguration


def about(request):
    context = {
        "about_content": AboutContent.objects.filter(is_active=True).first(),
        # ABOUT · ADMIN VISUAL IMAGES | ABOUT · ADMIN VISUAL IMAGES
        "about_visuals": AboutPageConfiguration.objects.order_by("pk").first(),
        "about_page": InstitutionalPage.objects.filter(is_active=True, slug_fr="entreprise").first(),
        "company_values": CompanyValue.objects.filter(is_active=True).order_by("order")[:5],
        "hero_statistic": Statistic.objects.filter(is_active=True).order_by("order").first(),
        "process_steps": ProcessStep.objects.filter(is_active=True).order_by("number")[:5],
        "certifications": Certification.objects.filter(is_active=True).order_by("order"),
        "team_members": TeamMember.objects.filter(is_active=True).order_by("order"),
        "featured_projects": Project.objects.filter(is_published=True, is_featured=True).prefetch_related("services")[:6],
        "testimonials": Testimonial.objects.filter(is_active=True).order_by("order")[:6],
        "insurances": Insurance.objects.filter(is_active=True).order_by("order", "name_fr"),
        "form": ContactRequestForm(),
    }
    return render(request, "core/about.html", context)
