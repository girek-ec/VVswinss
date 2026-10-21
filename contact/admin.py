from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from .models import ContactAttachment, ContactRequest


# ============================================================
# ATTACHMENTS INLINE
# ============================================================

class ContactAttachmentInline(admin.TabularInline):
    model = ContactAttachment
    extra = 0
    fields = ("file", "file_link", "created_at")
    readonly_fields = ("file_link", "created_at")

    @admin.display(description="Archivo")
    def file_link(self, obj):
        if not obj.pk or not obj.file:
            return "—"

        try:
            return format_html('<a href="{}" target="_blank" rel="noopener">Abrir archivo</a>', obj.file.url)
        except ValueError:
            return "—"


# ============================================================
# STATUS HELPER
# ============================================================

def update_status(queryset, status):
    queryset.update(status=status, updated_at=timezone.now())


# ============================================================
# ADMIN ACTIONS
# ============================================================

@admin.action(description="Marcar como nueva")
def mark_new(modeladmin, request, queryset):
    update_status(queryset, ContactRequest.STATUS_NEW)


@admin.action(description="Marcar como contactada")
def mark_contacted(modeladmin, request, queryset):
    update_status(queryset, ContactRequest.STATUS_CONTACTED)


@admin.action(description="Marcar como visita técnica")
def mark_visit(modeladmin, request, queryset):
    update_status(queryset, ContactRequest.STATUS_VISIT)


@admin.action(description="Marcar como presupuesto")
def mark_quote(modeladmin, request, queryset):
    update_status(queryset, ContactRequest.STATUS_QUOTE)


@admin.action(description="Marcar como cerrada")
def mark_closed(modeladmin, request, queryset):
    update_status(queryset, ContactRequest.STATUS_CLOSED)


@admin.action(description="Marcar como descartada")
def mark_discarded(modeladmin, request, queryset):
    update_status(queryset, ContactRequest.STATUS_DISCARDED)


# ============================================================
# CONTACT REQUEST ADMIN
# ============================================================

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "email_link", "phone_link", "service", "project_location", "visit_requested", "privacy_status", "status_badge", "attachment_count", "language", "created_at")
    list_display_links = ("name",)
    list_filter = ("status", "language", "service", "request_visit", "privacy_accepted", "privacy_policy_version", "created_at")
    search_fields = ("name", "company", "email", "phone", "project_location", "message", "internal_notes")
    readonly_fields = ("language", "privacy_accepted", "privacy_accepted_at", "privacy_policy_version", "ip_address", "user_agent", "created_at", "updated_at")
    list_select_related = ("service",)
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    list_per_page = 30
    save_on_top = True
    empty_value_display = "—"
    inlines = (ContactAttachmentInline,)
    actions = (mark_new, mark_contacted, mark_visit, mark_quote, mark_closed, mark_discarded)

    fieldsets = (
        ("Cliente", {
            "fields": ("name", "company", "email", "phone")
        }),

        ("Proyecto", {
            "fields": ("service", "project_location", "message")
        }),

        ("Visita técnica", {
            "fields": ("request_visit", "preferred_date", "preferred_time")
        }),

        ("Gestión de la solicitud", {
            "fields": ("status", "internal_notes")
        }),

        ("Privacidad e idioma", {
            "fields": ("privacy_accepted", "privacy_accepted_at", "privacy_policy_version", "language")
        }),

        ("Información técnica", {
            "classes": ("collapse",),
            "fields": ("ip_address", "user_agent", "created_at", "updated_at")
        }),
    )

    @admin.display(description="E-mail", ordering="email")
    def email_link(self, obj):
        if not obj.email:
            return "—"

        return format_html('<a href="mailto:{}">{}</a>', obj.email, obj.email)

    @admin.display(description="Teléfono", ordering="phone")
    def phone_link(self, obj):
        if not obj.phone:
            return "—"

        return format_html('<a href="tel:{}">{}</a>', obj.phone, obj.phone)

    @admin.display(description="Visita", boolean=True, ordering="request_visit")
    def visit_requested(self, obj):
        return obj.request_visit

    @admin.display(description="Privacidad", boolean=True, ordering="privacy_accepted")
    def privacy_status(self, obj):
        return obj.privacy_accepted

    @admin.display(description="Estado", ordering="status")
    def status_badge(self, obj):
        styles = {
            ContactRequest.STATUS_NEW: ("Nueva", "#2563eb", "#eff6ff"),
            ContactRequest.STATUS_CONTACTED: ("Contactada", "#7c3aed", "#f5f3ff"),
            ContactRequest.STATUS_VISIT: ("Visita técnica", "#d97706", "#fffbeb"),
            ContactRequest.STATUS_QUOTE: ("Presupuesto", "#0891b2", "#ecfeff"),
            ContactRequest.STATUS_CLOSED: ("Cerrada", "#15803d", "#f0fdf4"),
            ContactRequest.STATUS_DISCARDED: ("Descartada", "#b91c1c", "#fef2f2"),
        }

        label, color, background = styles.get(obj.status, (obj.get_status_display(), "#374151", "#f3f4f6"))

        return format_html('<span style="display:inline-block;padding:4px 9px;border-radius:12px;font-size:11px;font-weight:600;color:{};background:{};">{}</span>', color, background, label)

    @admin.display(description="Archivos")
    def attachment_count(self, obj):
        return len(obj.attachments.all())

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("service").prefetch_related("attachments")


# ============================================================
# CONTACT ATTACHMENT ADMIN
# ============================================================

@admin.register(ContactAttachment)
class ContactAttachmentAdmin(admin.ModelAdmin):
    list_display = ("request", "file_name", "file_link", "created_at")
    list_display_links = ("request",)
    search_fields = ("request__name", "request__company", "request__email", "file")
    list_filter = ("created_at",)
    readonly_fields = ("file_link", "created_at", "updated_at")
    list_select_related = ("request",)
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    list_per_page = 30
    empty_value_display = "—"

    @admin.display(description="Archivo")
    def file_name(self, obj):
        if not obj.file:
            return "—"

        return obj.file.name.rsplit("/", 1)[-1]

    @admin.display(description="Abrir")
    def file_link(self, obj):
        if not obj.pk or not obj.file:
            return "—"

        try:
            return format_html('<a href="{}" target="_blank" rel="noopener">Abrir archivo</a>', obj.file.url)
        except ValueError:
            return "—"