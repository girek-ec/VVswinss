from django.shortcuts import redirect, render

from contact.forms import ContactRequestForm
from core.utils import current_language, get_by_localized_slug

from .models import Service, ServiceCategory


# ============================================================
# SERVICE LIST
# Página principal de servicios.
# Ahora presenta las categorías disponibles.
# ============================================================

def service_list(request):
    categories = (
        ServiceCategory.objects
        .filter(is_active=True)
        .order_by("order", "name_fr")
    )

    services = (
        Service.objects
        .filter(is_active=True)
        .select_related("category")
        .order_by("order", "name_fr")
    )

    # ========================================================
    # COMPATIBILIDAD CON ENLACES ANTIGUOS
    # Ejemplo:
    # /services/?category=isolation
    #
    # Si todavía existe uno de estos enlaces, redirige
    # automáticamente a la nueva página de categoría.
    # ========================================================

    category_slug = request.GET.get("category", "").strip()

    if category_slug:
        language = current_language()

        selected_category = None

        slug_field = f"slug_{language}"

        selected_category = categories.filter(
            **{slug_field: category_slug}
        ).first()

        # ====================================================
        # FALLBACK A OTROS IDIOMAS
        # ====================================================

        if selected_category is None:
            for fallback_language in ("fr", "de", "it", "en"):
                if fallback_language == language:
                    continue

                selected_category = categories.filter(
                    **{
                        f"slug_{fallback_language}": category_slug
                    }
                ).first()

                if selected_category is not None:
                    break

        # ====================================================
        # REDIRECCIÓN A LA NUEVA PÁGINA DE CATEGORÍA
        # ====================================================

        if selected_category:
            localized_slug = (
                getattr(
                    selected_category,
                    f"slug_{language}",
                    None,
                )
                or selected_category.slug_fr
            )

            return redirect(
                "services:category_detail",
                slug=localized_slug,
            )

    # ========================================================
    # FORMULARIO
    # ========================================================

    form = ContactRequestForm()

    # ========================================================
    # CONTEXTO
    # ========================================================

    context = {
        "categories": categories,
        "services": services,
        "form": form,
    }

    return render(
        request,
        "services/service_list.html",
        context,
    )


# ============================================================
# CATEGORY DETAIL
# Página individual de cada categoría.
#
# Ejemplo:
# /en/services/category/renovation/
#
# Presenta:
# - nombre de categoría
# - descripción
# - imagen
# - todas las categorías en el lateral
# - servicios pertenecientes a esa categoría
# ============================================================

def category_detail(request, slug):
    language = current_language()

    # ========================================================
    # TODAS LAS CATEGORÍAS ACTIVAS
    # ========================================================

    categories = (
        ServiceCategory.objects
        .filter(is_active=True)
        .order_by("order", "name_fr")
    )

    # ========================================================
    # CATEGORÍA ACTUAL
    # ========================================================

    category = get_by_localized_slug(
        ServiceCategory,
        slug,
        queryset=categories,
    )

    # ========================================================
    # SLUG LOCALIZADO CANÓNICO
    # ========================================================

    localized_slug = (
        getattr(
            category,
            f"slug_{language}",
            None,
        )
        or category.slug_fr
    )

    if slug != localized_slug:
        return redirect(
            "services:category_detail",
            slug=localized_slug,
        )

    # ========================================================
    # SERVICIOS PERTENECIENTES A ESTA CATEGORÍA
    # ========================================================

    category_services = (
        Service.objects
        .filter(
            is_active=True,
            category=category,
        )
        .select_related("category")
        .prefetch_related(
            "benefits",
            "images",
        )
        .order_by(
            "order",
            "name_fr",
        )
    )

    # ========================================================
    # OTRAS CATEGORÍAS
    # ========================================================

    other_categories = (
        categories
        .exclude(pk=category.pk)
    )

    # ========================================================
    # FORMULARIO
    # ========================================================

    form = ContactRequestForm()

    # ========================================================
    # CONTEXTO
    # ========================================================

    context = {
        "category": category,
        "categories": categories,
        "other_categories": other_categories,
        "category_services": category_services,

        # Se mantiene también "services" para compatibilidad
        # con bloques reutilizados que puedan usar esta variable.
        "services": category_services,

        "form": form,
    }

    return render(
        request,
        "services/category_detail.html",
        context,
    )


# ============================================================
# SERVICE DETAIL
# Página individual de cada servicio.
#
# Ejemplo:
# /en/services/isolation-thermique-exterieure/
# ============================================================

def service_detail(request, slug):
    language = current_language()

    # ========================================================
    # SERVICIOS ACTIVOS
    # ========================================================

    queryset = (
        Service.objects
        .filter(is_active=True)
        .select_related("category")
        .prefetch_related(
            "benefits",
            "images",
        )
    )

    # ========================================================
    # SERVICIO ACTUAL
    # ========================================================

    service = get_by_localized_slug(
        Service,
        slug,
        queryset=queryset,
    )

    # ========================================================
    # SLUG LOCALIZADO CANÓNICO
    # ========================================================

    localized_slug = (
        getattr(
            service,
            f"slug_{language}",
            None,
        )
        or service.slug_fr
    )

    if slug != localized_slug:
        return redirect(
            "services:detail",
            slug=localized_slug,
        )

    # ========================================================
    # SERVICIOS RELACIONADOS
    # Solo servicios pertenecientes a la misma categoría.
    # ========================================================

    related_services = (
        Service.objects
        .filter(
            is_active=True,
            category=service.category,
        )
        .exclude(pk=service.pk)
        .select_related("category")
        .order_by(
            "order",
            "name_fr",
        )[:3]
    )

    # ========================================================
    # FORMULARIO
    # ========================================================

    form = ContactRequestForm(
        initial={
            "service": service.pk,
        }
    )

    # ========================================================
    # CONTEXTO
    # ========================================================

    context = {
        "service": service,
        "related_services": related_services,
        "form": form,
    }

    return render(
        request,
        "services/service_detail.html",
        context,
    )