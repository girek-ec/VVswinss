from django.shortcuts import render

from blog.models import Post
from contact.forms import ContactRequestForm
from projects.models import BeforeAfter, Project
from services.models import Service, ServiceCategory

from .models import (
    AboutContent,
    Certification,
    CompanyValue,
    FAQ,
    HomeContent,
    Insurance,
    InstitutionalPage,
    ProcessStep,
    Statistic,
    TeamMember,
    Testimonial,
    ProfessionalPage
)


# ============================================================
# HOME
# ============================================================

def home(request):
    context = {
        "home": HomeContent.objects.filter(is_active=True).first(),
        "about_page": InstitutionalPage.objects.filter(is_active=True, slug_fr="entreprise").first(),
        "hero_statistic": Statistic.objects.filter(is_active=True).order_by("order").first(),
        "statistics": Statistic.objects.filter(is_active=True).order_by("order")[:4],
        "featured_services": Service.objects.filter(is_active=True).select_related("category").order_by("order"),
        "services": Service.objects.filter(is_active=True).select_related("category").prefetch_related("images").order_by("order", "name_fr"),
        "featured_projects": Project.objects.filter(is_published=True, is_featured=True).prefetch_related("services")[:6],

        # ========================================================
        # DERNIÈRE RÉALISATION AVANT / APRÈS
        # ========================================================

        "home_before_after_item": BeforeAfter.objects.filter(project__is_published=True).select_related("project").order_by("-project__created_at", "order").first(),

        "process_steps": ProcessStep.objects.filter(is_active=True).order_by("number"),
        "insurances": Insurance.objects.filter(is_active=True).order_by("order", "name_fr"),
        "testimonials": Testimonial.objects.filter(is_active=True).order_by("order")[:6],
        "faqs": FAQ.objects.filter(is_active=True).select_related("category").order_by("order")[:8],
        "service_categories": ServiceCategory.objects.filter(is_active=True).order_by("order", "name_fr"),
        "form": ContactRequestForm(),
        "company_values": CompanyValue.objects.filter(is_active=True).order_by("order")[:5],
        "latest_posts": Post.objects.filter(is_published=True).select_related("category", "author").prefetch_related("tags").order_by("-published_at")[:6],
    }

    return render(request, "core/home.html", context)


# ============================================================
# ABOUT
# ============================================================

def about(request):
    context = {
        "about_content": AboutContent.objects.filter(is_active=True).first(),
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



# ============================================================
# PROFESSIONALS
# ============================================================

def professionals(request):
    professional_page = (
        ProfessionalPage.objects
        .filter(is_active=True)
        .prefetch_related("blocks", "services")
        .first()
    )

    featured_projects = (
        Project.objects
        .filter(
            is_published=True,
            is_featured=True,
        )
        .prefetch_related("services")
        .order_by("-created_at")[:6]
    )

    context = {
        "professional_page": professional_page,
        "featured_projects": featured_projects,
        "form": ContactRequestForm(),
    }

    return render(request, "core/professionals.html", context)



# ============================================================
# LEGAL NOTICE
# ============================================================

def mentions_legales(request):
    page = InstitutionalPage.objects.filter(is_active=True, slug_fr="mentions-legales").first()

    context = {
        "page": page,
    }

    return render(request, "core/mentions_legales.html", context)


# ============================================================
# DATA PROTECTION
# ============================================================

def protection_donnees(request):
    page = InstitutionalPage.objects.filter(is_active=True, slug_fr="protection-des-donnees").first()

    context = {
        "page": page,
    }

    return render(request, "core/protection_donnees.html", context)


# ============================================================
# DESIGN SYSTEM · INTERNE
# ============================================================

def design_system(request):
    """
    Muestrario visual interno de V&V Swiss Services.

    Permite visualizar y documentar:
    - Tipografía
    - Colores
    - Botones
    - Iconos
    - Espaciados
    - Grid
    - Imágenes
    - Componentes
    - Responsive
    """

    return render(request, "core/design_system.html")