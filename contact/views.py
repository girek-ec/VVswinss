import logging

from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext as _
from django.views.decorators.http import (
    require_http_methods,
    require_POST,
)

from core.utils import (
    current_language,
    get_localized_value,
)
from services.models import Service

from .forms import ContactRequestForm
from .models import (
    ContactAttachment,
    ContactRequest,
)


logger = logging.getLogger(__name__)



# ============================================================
# PUBLIC CONTACT
# ============================================================

@require_http_methods(["GET", "POST"])
def contact(request):

    # ========================================================
    # POST
    # ========================================================

    if request.method == "POST":

        form = ContactRequestForm(
            request.POST,
            request.FILES,
        )

        # ====================================================
        # VALID FORM
        # ====================================================

        if form.is_valid():

            with transaction.atomic():

                # =============================================
                # CONTACT REQUEST
                # =============================================

                contact_request = form.save(
                    commit=False
                )

                # =============================================
                # LANGUAGE
                # =============================================

                contact_request.language = current_language()

                # =============================================
                # IP
                # =============================================

                contact_request.ip_address = (
                    get_client_ip(request)
                )

                # =============================================
                # USER AGENT
                # =============================================

                contact_request.user_agent = (
                    request.META.get(
                        "HTTP_USER_AGENT",
                        "",
                    )
                )

                # =============================================
                # STATUS
                # =============================================

                contact_request.status = (
                    ContactRequest.STATUS_NEW
                )

                # =============================================
                # SAVE
                # =============================================

                contact_request.save()

                # =============================================
                # PHOTOS
                # =============================================

                photos = form.cleaned_data.get(
                    "photos",
                    [],
                )

                for photo in photos:

                    ContactAttachment.objects.create(
                        request=contact_request,
                        file=photo,
                    )

            logger.info(
                "Contact request saved. ID=%s",
                contact_request.pk,
            )

            return redirect(
                "contact:success"
            )

        # ====================================================
        # INVALID FORM
        # ====================================================

        logger.warning(
            "Invalid contact form: %s",
            form.errors.as_json(),
        )

    # ========================================================
    # GET
    # ========================================================

    else:

        initial = {}

        service_id = request.GET.get(
            "service"
        )

        if service_id:

            service = (
                Service.objects
                .filter(
                    pk=service_id,
                    is_active=True,
                )
                .only("pk")
                .first()
            )

            if service:

                initial[
                    "service"
                ] = service.pk

        form = ContactRequestForm(
            initial=initial
        )

    # ========================================================
    # RENDER
    # ========================================================

    return render(
        request,
        "contact/contact.html",
        {
            "form": form,
        },
    )


# ============================================================
# SUCCESS
# ============================================================

@require_http_methods(["GET"])
def contact_success(request):

    return render(
        request,
        "contact/contact_success.html",
    )


# ============================================================
# CLIENT IP
# ============================================================

def get_client_ip(request):

    forwarded_for = request.META.get(
        "HTTP_X_FORWARDED_FOR"
    )

    if forwarded_for:

        return (
            forwarded_for
            .split(",")[0]
            .strip()
        )

    return request.META.get(
        "REMOTE_ADDR"
    )


# ============================================================
# STAFF USER CHECK
# ============================================================

def is_staff_user(user):

    return (
        user.is_authenticated
        and user.is_active
        and user.is_staff
    )


# ============================================================
# INBOX LOGIN
# ============================================================

@require_http_methods(["GET", "POST"])
def inbox_login(request):

    # ========================================================
    # ALREADY LOGGED IN
    # ========================================================

    if (
        request.user.is_authenticated
        and request.user.is_staff
    ):

        return redirect(
            "contact:inbox"
        )

    error = None

    # ========================================================
    # LOGIN POST
    # ========================================================

    if request.method == "POST":

        username = (
            request.POST
            .get(
                "username",
                "",
            )
            .strip()
        )

        password = request.POST.get(
            "password",
            "",
        )

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        # ====================================================
        # AUTHORIZED USER
        # ====================================================

        if (
            user is not None
            and user.is_active
            and user.is_staff
        ):

            login(
                request,
                user,
            )

            # ================================================
            # RETURN TO ORIGINAL PAGE
            # ================================================

            next_url = (
                request.POST.get("next")
                or request.GET.get("next")
            )

            if (
                next_url
                and url_has_allowed_host_and_scheme(
                    url=next_url,
                    allowed_hosts={
                        request.get_host()
                    },
                    require_https=request.is_secure(),
                )
            ):

                return redirect(
                    next_url
                )

            return redirect(
                "contact:inbox"
            )

        # ====================================================
        # INVALID LOGIN
        # ====================================================

        error = _(
            "Identifiants incorrects ou accès non autorisé."
        )

    # ========================================================
    # RENDER LOGIN
    # ========================================================

    return render(
        request,
        "contact/inbox_login.html",
        {
            "error": error,
            "next": request.GET.get(
                "next",
                "",
            ),
        },
    )


# ============================================================
# INBOX LOGOUT
# ============================================================

@login_required(login_url="contact:inbox_login")
@require_POST
def inbox_logout(request):
    logout(request)
    return redirect("contact:inbox_login")

# ============================================================
# PRIVATE INBOX
# ============================================================

@login_required(
    login_url="contact:inbox_login"
)
@user_passes_test(
    is_staff_user,
    login_url="contact:inbox_login",
)
def inbox(request):

    # ========================================================
    # FILTERS
    # ========================================================

    search = request.GET.get(
        "q",
        "",
    ).strip()

    selected_status = request.GET.get(
        "status",
        "",
    ).strip()

    contact_requests = (
        ContactRequest.objects
        .select_related(
            "service"
        )
        .prefetch_related(
            "attachments"
        )
        .all()
    )

    # ========================================================
    # SEARCH
    # ========================================================

    if search:

        contact_requests = (
            contact_requests
            .filter(

                Q(
                    name__icontains=search
                )

                |

                Q(
                    company__icontains=search
                )

                |

                Q(
                    email__icontains=search
                )

                |

                Q(
                    phone__icontains=search
                )

                |

                Q(
                    project_location__icontains=search
                )

                |

                Q(
                    message__icontains=search
                )

            )
        )

    # ========================================================
    # STATUS FILTER
    # ========================================================

    valid_statuses = dict(
        ContactRequest.STATUS_CHOICES
    )

    if selected_status in valid_statuses:

        contact_requests = (
            contact_requests
            .filter(
                status=selected_status
            )
        )

    # ========================================================
    # COUNTERS
    # ========================================================

    counters = {

        "all": (
            ContactRequest.objects
            .count()
        ),

        "new": (
            ContactRequest.objects
            .filter(
                status=ContactRequest.STATUS_NEW
            )
            .count()
        ),

        "contacted": (
            ContactRequest.objects
            .filter(
                status=ContactRequest.STATUS_CONTACTED
            )
            .count()
        ),

        "visit": (
            ContactRequest.objects
            .filter(
                status=ContactRequest.STATUS_VISIT
            )
            .count()
        ),

        "quote": (
            ContactRequest.objects
            .filter(
                status=ContactRequest.STATUS_QUOTE
            )
            .count()
        ),

        "closed": (
            ContactRequest.objects
            .filter(
                status=ContactRequest.STATUS_CLOSED
            )
            .count()
        ),

        "discarded": (
            ContactRequest.objects
            .filter(
                status=ContactRequest.STATUS_DISCARDED
            )
            .count()
        ),

    }

    # ========================================================
    # PAGINATION
    # ========================================================

    paginator = Paginator(
        contact_requests,
        15,
    )

    page = paginator.get_page(
        request.GET.get(
            "page"
        )
    )

    # ========================================================
    # LOCALIZED SERVICE NAME
    # ========================================================

    for item in page.object_list:

        item.localized_service_name = ""

        if item.service:

            item.localized_service_name = (
                get_localized_value(
                    item.service,
                    "name",
                )
            )

    # ========================================================
    # RENDER
    # ========================================================

    return render(
        request,
        "contact/inbox.html",
        {
            "page": page,
            "counters": counters,
            "search": search,
            "selected_status": selected_status,
            "status_choices": (
                ContactRequest.STATUS_CHOICES
            ),
        },
    )


# ============================================================
# INBOX DETAIL
# ============================================================

@login_required(
    login_url="contact:inbox_login"
)
@user_passes_test(
    is_staff_user,
    login_url="contact:inbox_login",
)
def inbox_detail(
    request,
    pk,
):

    contact_request = get_object_or_404(
        ContactRequest.objects
        .select_related(
            "service"
        )
        .prefetch_related(
            "attachments"
        ),
        pk=pk,
    )

    # ========================================================
    # LOCALIZED SERVICE
    # ========================================================

    localized_service_name = ""

    if contact_request.service:

        localized_service_name = (
            get_localized_value(
                contact_request.service,
                "name",
            )
        )

    # ========================================================
    # RENDER
    # ========================================================

    return render(
        request,
        "contact/inbox_detail.html",
        {
            "contact_request": (
                contact_request
            ),
            "localized_service_name": (
                localized_service_name
            ),
            "status_choices": (
                ContactRequest.STATUS_CHOICES
            ),
        },
    )


# ============================================================
# UPDATE REQUEST
# ============================================================

@login_required(
    login_url="contact:inbox_login"
)
@user_passes_test(
    is_staff_user,
    login_url="contact:inbox_login",
)
@require_POST
def inbox_update(
    request,
    pk,
):

    contact_request = get_object_or_404(
        ContactRequest,
        pk=pk,
    )

    # ========================================================
    # DATA
    # ========================================================

    status = request.POST.get(
        "status"
    )

    internal_notes = (
        request.POST
        .get(
            "internal_notes",
            "",
        )
        .strip()
    )

    # ========================================================
    # STATUS VALIDATION
    # ========================================================

    valid_statuses = dict(
        ContactRequest.STATUS_CHOICES
    )

    if status in valid_statuses:

        contact_request.status = (
            status
        )

    # ========================================================
    # INTERNAL NOTES
    # ========================================================

    contact_request.internal_notes = (
        internal_notes
    )

    # ========================================================
    # SAVE
    # ========================================================

    contact_request.save(
        update_fields=[
            "status",
            "internal_notes",
            "updated_at",
        ]
    )

    # ========================================================
    # MESSAGE
    # ========================================================

    messages.success(
        request,
        _(
            "Demande mise à jour avec succès."
        ),
    )

    # ========================================================
    # RETURN
    # ========================================================

    return redirect(
        "contact:inbox_detail",
        pk=contact_request.pk,
    )