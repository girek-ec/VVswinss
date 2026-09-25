from django.db import models

# Create your models here.
from django.db import models

from core.models import TimeStampedModel
from services.models import Service


class ContactRequest(TimeStampedModel):
    ESTADO_NUEVO = "nuevo"
    ESTADO_CONTACTADO = "contactado"
    ESTADO_PRESUPUESTO = "presupuesto"
    ESTADO_CERRADO = "cerrado"
    ESTADO_DESCARTADO = "descartado"

    ESTADOS = [
        (ESTADO_NUEVO, "Nuevo"),
        (ESTADO_CONTACTADO, "Contactado"),
        (ESTADO_PRESUPUESTO, "Presupuesto"),
        (ESTADO_CERRADO, "Cerrado"),
        (ESTADO_DESCARTADO, "Descartado"),
    ]

    nombre = models.CharField(max_length=150)
    empresa = models.CharField(max_length=150, blank=True)

    email = models.EmailField()
    telefono = models.CharField(max_length=50, blank=True)

    servicio = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="solicitudes_contacto",
    )

    ubicacion_proyecto = models.CharField(max_length=200, blank=True)

    mensaje = models.TextField()

    acepta_privacidad = models.BooleanField(default=False)

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default=ESTADO_NUEVO,
    )

    idioma = models.CharField(
        max_length=5,
        default="fr",
    )

    notas_internas = models.TextField(blank=True)

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
    )

    user_agent = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Solicitud de contacto"
        verbose_name_plural = "Solicitudes de contacto"

    def __str__(self):
        return f"{self.nombre} - {self.email}"


class ContactAttachment(TimeStampedModel):
    solicitud = models.ForeignKey(
        ContactRequest,
        on_delete=models.CASCADE,
        related_name="archivos",
    )

    archivo = models.FileField(upload_to="contact/attachments/")

    class Meta:
        verbose_name = "Archivo adjunto"
        verbose_name_plural = "Archivos adjuntos"

    def __str__(self):
        return self.archivo.name