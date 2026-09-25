from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render
from django.utils.translation import get_language

from .forms import ContactRequestForm


def contact(request):

    if request.method == "POST":

        form = ContactRequestForm(request.POST)

        if form.is_valid():

            solicitud = form.save(commit=False)

            language = (
                get_language() or "fr"
            ).split("-")[0]

            solicitud.idioma = language

            solicitud.ip_address = get_client_ip(
                request
            )

            solicitud.user_agent = (
                request.META.get(
                    "HTTP_USER_AGENT",
                    "",
                )
            )

            solicitud.save()

            return redirect(
                "contact:success"
            )

    else:
        form = ContactRequestForm()

    return render(
        request,
        "contact/contact.html",
        {
            "form": form,
        },
    )


def contact_success(request):

    return render(
        request,
        "contact/contact_success.html",
    )


def get_client_ip(request):

    forwarded_for = request.META.get(
        "HTTP_X_FORWARDED_FOR"
    )

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    return request.META.get(
        "REMOTE_ADDR"
    )