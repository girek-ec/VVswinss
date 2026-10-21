import os

from django import forms
from django.urls import NoReverseMatch, reverse
from django.utils import timezone
from django.utils.html import format_html

from core.utils import current_language, get_localized_value
from services.models import Service

from .models import ContactRequest


# ============================================================
# PRIVACY POLICY VERSION
# Actualizar únicamente cuando cambie el contenido legal
# ============================================================

PRIVACY_POLICY_VERSION = "2026-10"


# ============================================================
# LANGUAGE
# ============================================================

def get_form_language():
    language = current_language() or "fr"
    language = str(language).lower().replace("_", "-").split("-")[0]

    if language not in {"fr", "de", "it", "en"}:
        language = "fr"

    return language


# ============================================================
# PRIVACY URL
# ============================================================

def get_privacy_policy_url():
    try:
        return reverse("core:protection_donnees")
    except NoReverseMatch:
        return reverse("protection_donnees")


# ============================================================
# LOCALIZED SERVICE SELECT
# ============================================================

class LocalizedServiceChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return get_localized_value(obj, "name")


# ============================================================
# MULTIPLE FILE INPUT
# ============================================================

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


# ============================================================
# MULTIPLE IMAGE FIELD
# ============================================================

class MultipleImageField(forms.ImageField):
    widget = MultipleFileInput

    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
    MAX_FILES = 8
    MAX_FILE_SIZE = 8 * 1024 * 1024

    def clean(self, data, initial=None):
        if not data:
            return []

        files = data if isinstance(data, (list, tuple)) else [data]
        language = get_form_language()

        messages = {
            "max_files": {
                "fr": "Vous pouvez joindre un maximum de 8 photos.",
                "de": "Sie können maximal 8 Fotos hochladen.",
                "it": "È possibile allegare un massimo di 8 foto.",
                "en": "You can attach a maximum of 8 photos.",
            },
            "max_size": {
                "fr": "Chaque photo doit avoir une taille inférieure à 8 Mo.",
                "de": "Jedes Foto muss kleiner als 8 MB sein.",
                "it": "Ogni foto deve avere una dimensione inferiore a 8 MB.",
                "en": "Each photo must be smaller than 8 MB.",
            },
            "invalid_format": {
                "fr": "Seuls les fichiers JPG, JPEG, PNG et WebP sont autorisés.",
                "de": "Nur JPG-, JPEG-, PNG- und WebP-Dateien sind erlaubt.",
                "it": "Sono consentiti solo file JPG, JPEG, PNG e WebP.",
                "en": "Only JPG, JPEG, PNG and WebP files are allowed.",
            },
        }

        if len(files) > self.MAX_FILES:
            raise forms.ValidationError(messages["max_files"][language])

        cleaned_files = []

        for uploaded_file in files:
            extension = os.path.splitext(uploaded_file.name)[1].lower()

            if extension not in self.ALLOWED_EXTENSIONS:
                raise forms.ValidationError(messages["invalid_format"][language])

            image = super().clean(uploaded_file, initial)

            if image.size > self.MAX_FILE_SIZE:
                raise forms.ValidationError(messages["max_size"][language])

            cleaned_files.append(image)

        return cleaned_files


# ============================================================
# CONTACT REQUEST FORM
# ============================================================

class ContactRequestForm(forms.ModelForm):

    # ========================================================
    # SERVICE
    # ========================================================

    service = LocalizedServiceChoiceField(queryset=Service.objects.none(), required=True, empty_label=None, widget=forms.Select(attrs={"class": "form-control service-native-select"}))

    # ========================================================
    # PHOTOS
    # ========================================================

    photos = MultipleImageField(required=False, widget=MultipleFileInput(attrs={"class": "form-control", "accept": "image/jpeg,image/png,image/webp"}))

    # ========================================================
    # META
    # ========================================================

    class Meta:
        model = ContactRequest

        fields = [
            "name",
            "company",
            "email",
            "phone",
            "service",
            "project_location",
            "message",
            "request_visit",
            "preferred_date",
            "preferred_time",
            "privacy_accepted",
        ]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "autocomplete": "name"}),
            "company": forms.TextInput(attrs={"class": "form-control", "autocomplete": "organization"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "autocomplete": "tel"}),
            "project_location": forms.TextInput(attrs={"class": "form-control"}),
            "message": forms.Textarea(attrs={"class": "form-control address", "rows": 5}),
            "request_visit": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "preferred_date": forms.DateInput(format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}),
            "preferred_time": forms.TimeInput(format="%H:%M", attrs={"class": "form-control", "type": "time"}),
            "privacy_accepted": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    # ========================================================
    # INIT
    # ========================================================

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        language = get_form_language()

        texts = {
            "fr": {
                "labels": {
                    "name": "Nom complet",
                    "company": "Entreprise",
                    "email": "Adresse e-mail",
                    "phone": "Téléphone",
                    "service": "Service souhaité",
                    "project_location": "Lieu du projet",
                    "message": "Décrivez votre projet",
                    "photos": "Photos du projet",
                    "request_visit": "Je souhaite demander une visite technique",
                    "preferred_date": "Date souhaitée",
                    "preferred_time": "Heure souhaitée",
                },
                "placeholders": {
                    "name": "Votre nom et prénom",
                    "company": "Nom de votre entreprise (facultatif)",
                    "email": "Votre adresse e-mail",
                    "phone": "Votre numéro de téléphone",
                    "project_location": "Ville ou localité du projet",
                    "message": "Décrivez brièvement les travaux que vous souhaitez réaliser...",
                },
                "service_empty": "Sélectionnez un service",
                "privacy_prefix": "J'accepte la",
                "privacy_link": "politique de confidentialité",
                "privacy_required": "Vous devez accepter la politique de confidentialité pour envoyer votre demande.",
            },

            "de": {
                "labels": {
                    "name": "Vollständiger Name",
                    "company": "Unternehmen",
                    "email": "E-Mail-Adresse",
                    "phone": "Telefon",
                    "service": "Gewünschte Dienstleistung",
                    "project_location": "Projektstandort",
                    "message": "Beschreiben Sie Ihr Projekt",
                    "photos": "Fotos des Projekts",
                    "request_visit": "Ich möchte einen technischen Besichtigungstermin anfragen",
                    "preferred_date": "Gewünschtes Datum",
                    "preferred_time": "Gewünschte Uhrzeit",
                },
                "placeholders": {
                    "name": "Vor- und Nachname",
                    "company": "Name Ihres Unternehmens (optional)",
                    "email": "Ihre E-Mail-Adresse",
                    "phone": "Ihre Telefonnummer",
                    "project_location": "Ort des Projekts",
                    "message": "Beschreiben Sie kurz die gewünschten Arbeiten...",
                },
                "service_empty": "Dienstleistung auswählen",
                "privacy_prefix": "Ich akzeptiere die",
                "privacy_link": "Datenschutzerklärung",
                "privacy_required": "Sie müssen die Datenschutzerklärung akzeptieren, um Ihre Anfrage zu senden.",
            },

            "it": {
                "labels": {
                    "name": "Nome completo",
                    "company": "Azienda",
                    "email": "Indirizzo e-mail",
                    "phone": "Telefono",
                    "service": "Servizio desiderato",
                    "project_location": "Luogo del progetto",
                    "message": "Descrivi il tuo progetto",
                    "photos": "Foto del progetto",
                    "request_visit": "Desidero richiedere una visita tecnica",
                    "preferred_date": "Data desiderata",
                    "preferred_time": "Ora desiderata",
                },
                "placeholders": {
                    "name": "Nome e cognome",
                    "company": "Nome dell'azienda (facoltativo)",
                    "email": "Il tuo indirizzo e-mail",
                    "phone": "Il tuo numero di telefono",
                    "project_location": "Città o località del progetto",
                    "message": "Descrivi brevemente i lavori che desideri realizzare...",
                },
                "service_empty": "Seleziona un servizio",
                "privacy_prefix": "Accetto la",
                "privacy_link": "politica sulla privacy",
                "privacy_required": "Devi accettare l'informativa sulla privacy per inviare la richiesta.",
            },

            "en": {
                "labels": {
                    "name": "Full name",
                    "company": "Company",
                    "email": "Email address",
                    "phone": "Phone",
                    "service": "Requested service",
                    "project_location": "Project location",
                    "message": "Describe your project",
                    "photos": "Project photos",
                    "request_visit": "I would like to request a technical visit",
                    "preferred_date": "Preferred date",
                    "preferred_time": "Preferred time",
                },
                "placeholders": {
                    "name": "Your first and last name",
                    "company": "Company name (optional)",
                    "email": "Your email address",
                    "phone": "Your phone number",
                    "project_location": "City or project location",
                    "message": "Briefly describe the work you would like carried out...",
                },
                "service_empty": "Select a service",
                "privacy_prefix": "I accept the",
                "privacy_link": "privacy policy",
                "privacy_required": "You must accept the privacy policy before submitting your request.",
            },
        }

        current_texts = texts[language]

        # ====================================================
        # LABELS
        # ====================================================

        for field_name, label in current_texts["labels"].items():
            if field_name in self.fields:
                self.fields[field_name].label = label

        # ====================================================
        # PLACEHOLDERS
        # ====================================================

        for field_name, placeholder in current_texts["placeholders"].items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs["placeholder"] = placeholder

        # ====================================================
        # PRIVACY POLICY
        # ====================================================

        privacy_url = get_privacy_policy_url()

        self.fields["privacy_accepted"].label = format_html('{} <a href="{}" target="_blank" rel="noopener noreferrer">{}</a>', current_texts["privacy_prefix"], privacy_url, current_texts["privacy_link"])
        self.fields["privacy_accepted"].required = True
        self.fields["privacy_accepted"].error_messages["required"] = current_texts["privacy_required"]

        # ====================================================
        # SERVICES
        # ====================================================

        self.fields["service"].queryset = Service.objects.filter(is_active=True).order_by("order", "name_fr")
        self.fields["service"].empty_label = current_texts["service_empty"]

        # ====================================================
        # REQUIRED
        # ====================================================

        self.fields["name"].required = True
        self.fields["email"].required = True
        self.fields["phone"].required = True
        self.fields["service"].required = True
        self.fields["message"].required = True
        self.fields["privacy_accepted"].required = True

        self.fields["company"].required = False
        self.fields["project_location"].required = False
        self.fields["request_visit"].required = False
        self.fields["preferred_date"].required = False
        self.fields["preferred_time"].required = False

        # ====================================================
        # MINIMUM DATE
        # ====================================================

        self.fields["preferred_date"].widget.attrs["min"] = timezone.localdate().isoformat()

    # ========================================================
    # CLEAN
    # ========================================================

    def clean(self):
        cleaned_data = super().clean()

        language = get_form_language()
        request_visit = cleaned_data.get("request_visit")
        preferred_date = cleaned_data.get("preferred_date")

        messages = {
            "fr": {
                "date_required": "Veuillez sélectionner une date pour la visite technique.",
                "past_date": "La date de la visite ne peut pas être antérieure à aujourd'hui.",
            },
            "de": {
                "date_required": "Bitte wählen Sie ein Datum für die technische Besichtigung.",
                "past_date": "Das Besuchsdatum darf nicht in der Vergangenheit liegen.",
            },
            "it": {
                "date_required": "Seleziona una data per la visita tecnica.",
                "past_date": "La data della visita non può essere precedente a oggi.",
            },
            "en": {
                "date_required": "Please select a date for the technical visit.",
                "past_date": "The visit date cannot be in the past.",
            },
        }

        # ====================================================
        # TECHNICAL VISIT
        # ====================================================

        if request_visit:
            if not preferred_date:
                self.add_error("preferred_date", messages[language]["date_required"])
            elif preferred_date < timezone.localdate():
                self.add_error("preferred_date", messages[language]["past_date"])
        else:
            cleaned_data["preferred_date"] = None
            cleaned_data["preferred_time"] = None

        return cleaned_data

    # ========================================================
    # SAVE
    # ========================================================

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.cleaned_data.get("privacy_accepted"):
            if not instance.privacy_accepted_at:
                instance.privacy_accepted_at = timezone.now()

            instance.privacy_policy_version = PRIVACY_POLICY_VERSION
        else:
            instance.privacy_accepted_at = None
            instance.privacy_policy_version = ""

        if commit:
            instance.save()
            self.save_m2m()

        return instance