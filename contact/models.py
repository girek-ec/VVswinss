from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel
from services.models import Service


# ============================================================
# CONTACT REQUEST
# ============================================================

class ContactRequest(TimeStampedModel):

    # ========================================================
    # STATUS
    # ========================================================

    STATUS_NEW = "new"
    STATUS_CONTACTED = "contacted"
    STATUS_VISIT = "visit"
    STATUS_QUOTE = "quote"
    STATUS_CLOSED = "closed"
    STATUS_DISCARDED = "discarded"

    STATUS_CHOICES = [
        (STATUS_NEW, _("Nouvelle")),
        (STATUS_CONTACTED, _("Contactée")),
        (STATUS_VISIT, _("Visite technique")),
        (STATUS_QUOTE, _("Devis")),
        (STATUS_CLOSED, _("Clôturée")),
        (STATUS_DISCARDED, _("Écartée")),
    ]

    # ========================================================
    # LANGUAGES
    # ========================================================

    LANGUAGE_CHOICES = [
        ("fr", "Français"),
        ("de", "Deutsch"),
        ("it", "Italiano"),
        ("en", "English"),
    ]

    # ========================================================
    # CLIENT
    # ========================================================

    name = models.CharField(max_length=150, verbose_name=_("Nom"))

    company = models.CharField(max_length=150, blank=True, verbose_name=_("Entreprise"))

    email = models.EmailField(verbose_name=_("E-mail"))

    phone = models.CharField(max_length=50, blank=True, verbose_name=_("Téléphone"))

    # ========================================================
    # SERVICE
    # ========================================================

    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name="contact_requests", verbose_name=_("Service"))

    # ========================================================
    # PROJECT
    # ========================================================

    project_location = models.CharField(max_length=200, blank=True, verbose_name=_("Lieu du projet"))

    message = models.TextField(verbose_name=_("Message"))

    # ========================================================
    # TECHNICAL VISIT
    # ========================================================

    request_visit = models.BooleanField(default=False, verbose_name=_("Demander une visite technique"))

    preferred_date = models.DateField(blank=True, null=True, verbose_name=_("Date souhaitée"))

    preferred_time = models.TimeField(blank=True, null=True, verbose_name=_("Heure souhaitée"))

    # ========================================================
    # PRIVACY
    # ========================================================

    privacy_accepted = models.BooleanField(default=False, verbose_name=_("Politique de confidentialité acceptée"))

    privacy_accepted_at = models.DateTimeField(blank=True, null=True, verbose_name=_("Date d’acceptation de la politique de confidentialité"))

    privacy_policy_version = models.CharField(max_length=30, blank=True, verbose_name=_("Version de la politique de confidentialité"))

    # ========================================================
    # STATUS
    # ========================================================

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW, db_index=True, verbose_name=_("État"))

    # ========================================================
    # LANGUAGE
    # ========================================================

    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default="fr", db_index=True, verbose_name=_("Langue"))

    # ========================================================
    # INTERNAL MANAGEMENT
    # ========================================================

    internal_notes = models.TextField(blank=True, verbose_name=_("Notes internes"))

    # ========================================================
    # TECHNICAL DATA
    # ========================================================

    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name=_("Adresse IP"))

    user_agent = models.TextField(blank=True, verbose_name=_("Agent utilisateur"))

    # ========================================================
    # META
    # ========================================================

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Demande de contact")
        verbose_name_plural = _("Demandes de contact")

    # ========================================================
    # STRING
    # ========================================================

    def __str__(self):
        return f"{self.name} - {self.email}"


# ============================================================
# CONTACT ATTACHMENT
# ============================================================

class ContactAttachment(TimeStampedModel):

    request = models.ForeignKey(ContactRequest, on_delete=models.CASCADE, related_name="attachments", verbose_name=_("Demande de contact"))

    file = models.FileField(upload_to="contact/attachments/%Y/%m/", verbose_name=_("Fichier"))

    class Meta:
        ordering = ["created_at"]
        verbose_name = _("Pièce jointe")
        verbose_name_plural = _("Pièces jointes")

    def __str__(self):
        return self.file.name