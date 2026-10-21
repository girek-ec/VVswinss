from django.urls import path

from . import views


app_name = "contact"


urlpatterns = [

    # ========================================================
    # PUBLIC CONTACT
    # ========================================================

    path(
        "",
        views.contact,
        name="contact",
    ),

    # ========================================================
    # SUCCESS
    # ========================================================

    path(
        "success/",
        views.contact_success,
        name="success",
    ),

    # ========================================================
    # PRIVATE INBOX LOGIN
    # ========================================================

    path(
        "inbox/login/",
        views.inbox_login,
        name="inbox_login",
    ),

    # ========================================================
    # PRIVATE INBOX LOGOUT
    # ========================================================

    path(
        "inbox/logout/",
        views.inbox_logout,
        name="inbox_logout",
    ),

    # ========================================================
    # PRIVATE INBOX
    # ========================================================

    path(
        "inbox/",
        views.inbox,
        name="inbox",
    ),

    # ========================================================
    # REQUEST DETAIL
    # ========================================================

    path(
        "inbox/<int:pk>/",
        views.inbox_detail,
        name="inbox_detail",
    ),

    # ========================================================
    # REQUEST UPDATE
    # ========================================================

    path(
        "inbox/<int:pk>/update/",
        views.inbox_update,
        name="inbox_update",
    ),

]