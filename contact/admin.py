from django.contrib import admin

from .models import ContactAttachment, ContactRequest


class ContactAttachmentInline(admin.TabularInline):
    model = ContactAttachment
    extra = 0
    readonly_fields = ("created_at",)


@admin.action(description="Marcar como contactado")
def marcar_contactado(modeladmin, request, queryset):
    queryset.update(
        estado=ContactRequest.ESTADO_CONTACTADO
    )


@admin.action(description="Marcar como presupuesto")
def marcar_presupuesto(modeladmin, request, queryset):
    queryset.update(
        estado=ContactRequest.ESTADO_PRESUPUESTO
    )


@admin.action(description="Marcar como cerrado")
def marcar_cerrado(modeladmin, request, queryset):
    queryset.update(
        estado=ContactRequest.ESTADO_CERRADO
    )


@admin.action(description="Marcar como descartado")
def marcar_descartado(modeladmin, request, queryset):
    queryset.update(
        estado=ContactRequest.ESTADO_DESCARTADO
    )


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "empresa",
        "email",
        "telefono",
        "servicio",
        "estado",
        "idioma",
        "created_at",
    )

    list_filter = (
        "estado",
        "idioma",
        "servicio",
        "acepta_privacidad",
        "created_at",
    )

    search_fields = (
        "nombre",
        "empresa",
        "email",
        "telefono",
        "ubicacion_proyecto",
        "mensaje",
    )

    readonly_fields = (
        "ip_address",
        "user_agent",
        "created_at",
        "updated_at",
    )

    date_hierarchy = "created_at"

    inlines = [
        ContactAttachmentInline,
    ]

    actions = [
        marcar_contactado,
        marcar_presupuesto,
        marcar_cerrado,
        marcar_descartado,
    ]

    fieldsets = (
        (
            "Cliente",
            {
                "fields": (
                    "nombre",
                    "empresa",
                    "email",
                    "telefono",
                )
            },
        ),
        (
            "Proyecto",
            {
                "fields": (
                    "servicio",
                    "ubicacion_proyecto",
                    "mensaje",
                    "idioma",
                )
            },
        ),
        (
            "Gestión comercial",
            {
                "fields": (
                    "estado",
                    "notas_internas",
                )
            },
        ),
        (
            "Privacidad y registro",
            {
                "fields": (
                    "acepta_privacidad",
                    "ip_address",
                    "user_agent",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


@admin.register(ContactAttachment)
class ContactAttachmentAdmin(admin.ModelAdmin):
    list_display = (
        "solicitud",
        "archivo",
        "created_at",
    )

    search_fields = (
        "solicitud__nombre",
        "solicitud__email",
    )