from django import forms

from services.models import Service

from .models import ContactRequest


class ContactRequestForm(forms.ModelForm):

    class Meta:
        model = ContactRequest

        fields = [
            "nombre",
            "empresa",
            "email",
            "telefono",
            "servicio",
            "ubicacion_proyecto",
            "mensaje",
            "acepta_privacidad",
        ]

        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "empresa": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "telefono": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "servicio": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "ubicacion_proyecto": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "mensaje": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                }
            ),

            "acepta_privacidad": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["servicio"].queryset = (
            Service.objects
            .filter(activo=True)
            .order_by("orden")
        )

        self.fields["servicio"].required = False

        self.fields["acepta_privacidad"].required = True