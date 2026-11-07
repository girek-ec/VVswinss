# -*- coding: utf-8 -*-
# V&V · CATÁLOGO OFICIAL DE SERVICIOS | OFFICIAL SERVICES CATALOGUE
import json
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from services.models import Service, ServiceBenefit, ServiceCategory, ServicePageVisualConfiguration

LANGUAGES = ("es", "fr", "de", "it", "en")
SOURCE_FILE = Path(__file__).with_name("_catalogo_vv_37.json")
CATEGORY_ICONS = (
    "fa-solid fa-house", "fa-solid fa-trowel-bricks", "fa-solid fa-temperature-half",
    "fa-solid fa-layer-group", "fa-solid fa-paint-roller", "fa-solid fa-broom",
    "fa-solid fa-building",
)

# TEXTOS GENERALES ADMINISTRABLES | EDITABLE GENERAL TEXT
TEXTS = {
    "es": {
        "work_title": "Trabajos incluidos", "work_intro": "Según el estado del inmueble y el alcance acordado, los trabajos pueden comprender:",
        "quality_title": "Organización y acabados", "quality_text": "Cada intervención se organiza según las características del inmueble y las necesidades del proyecto, prestando atención a la protección de los espacios y a los acabados.",
        "quality_list": "Evaluación de los trabajos necesarios\nOrganización de la intervención\nRevisión de las terminaciones",
        "cta_title": "¿Desea consultar este servicio?", "cta_text": "Cuéntenos las necesidades de su inmueble para estudiar las intervenciones y preparar una propuesta.", "cta_button": "Solicitar presupuesto",
        "hero_suffix": "Soluciones adaptadas a su inmueble",
    },
    "fr": {
        "work_title": "Travaux possibles", "work_intro": "Selon l’état du bâtiment et le périmètre convenu, les travaux peuvent comprendre :",
        "quality_title": "Organisation et finitions", "quality_text": "Chaque intervention est organisée selon les caractéristiques du bâtiment et les besoins du projet, avec une attention particulière à la protection des lieux et aux finitions.",
        "quality_list": "Évaluation des travaux nécessaires\nOrganisation de l’intervention\nContrôle des finitions",
        "cta_title": "Parlons de votre projet", "cta_text": "Décrivez-nous vos besoins pour examiner les interventions envisageables et préparer une proposition adaptée.", "cta_button": "Demander un devis",
        "hero_suffix": "Des solutions adaptées à votre bâtiment",
    },
    "de": {
        "work_title": "Mögliche Arbeiten", "work_intro": "Je nach Gebäudezustand und vereinbartem Umfang können die Arbeiten Folgendes umfassen:",
        "quality_title": "Organisation und Ausführung", "quality_text": "Wir planen die Arbeiten entsprechend der Bausubstanz und den Anforderungen des Projekts. Dabei achten wir auf den Schutz der Räume und eine sorgfältige Ausführung.",
        "quality_list": "Beurteilung der erforderlichen Arbeiten\nOrganisation der Ausführung\nKontrolle der Abschlüsse",
        "cta_title": "Besprechen wir Ihr Vorhaben", "cta_text": "Beschreiben Sie uns Ihr Projekt. Wir prüfen den möglichen Leistungsumfang und erstellen eine passende Offerte.", "cta_button": "Offerte anfragen",
        "hero_suffix": "Passende Lösungen für Ihre Liegenschaft",
    },
    "it": {
        "work_title": "Interventi possibili", "work_intro": "In base allo stato dell’immobile e ai lavori concordati, gli interventi possono comprendere:",
        "quality_title": "Organizzazione e finiture", "quality_text": "Organizziamo i lavori secondo le caratteristiche dell’immobile e le esigenze del progetto, con attenzione alla protezione degli ambienti e alle finiture.",
        "quality_list": "Valutazione dei lavori necessari\nOrganizzazione dell’intervento\nVerifica delle finiture",
        "cta_title": "Parliamo del vostro progetto", "cta_text": "Descriveteci le vostre esigenze per valutare i lavori e predisporre una proposta adeguata.", "cta_button": "Richiedere un preventivo",
        "hero_suffix": "Soluzioni adatte al vostro immobile",
    },
    "en": {
        "work_title": "Scope of work", "work_intro": "Depending on the property and the agreed scope, the work may include:",
        "quality_title": "Planning and finishes", "quality_text": "Each project is planned around the condition of the building and the required outcome, with attention to protecting the premises and achieving careful finishes.",
        "quality_list": "Assessment of the required work\nPlanning of the intervention\nReview of finishes",
        "cta_title": "Discuss your project with us", "cta_text": "Tell us what your property needs. We can review the scope and prepare a suitable quotation.", "cta_button": "Request a quote",
        "hero_suffix": "Solutions tailored to your property",
    },
}

# BENEFICIOS BASADOS EN VALORES CONFIRMADOS | BENEFITS BASED ON CONFIRMED COMPANY VALUES
BENEFITS = (
    ("fa-solid fa-file-invoice", {
        "es": ("Presupuesto claro", "Información comprensible sobre el trabajo y su alcance."),
        "fr": ("Devis clair", "Une présentation compréhensible des travaux et de leur périmètre."),
        "de": ("Klare Offerte", "Eine verständliche Beschreibung der Arbeiten und ihres Umfangs."),
        "it": ("Preventivo chiaro", "Una descrizione comprensibile dei lavori e del loro ambito."),
        "en": ("Clear quotation", "An understandable description of the proposed works and their scope."),
    }),
    ("fa-solid fa-list-check", {
        "es": ("Organización coordinada", "Intervenciones planificadas según las necesidades del inmueble."),
        "fr": ("Organisation coordonnée", "Des interventions planifiées selon les besoins du bâtiment."),
        "de": ("Koordinierte Planung", "Arbeiten, die sich nach dem Bedarf der Liegenschaft richten."),
        "it": ("Organizzazione coordinata", "Interventi pianificati in base alle esigenze dell’immobile."),
        "en": ("Coordinated approach", "Works planned according to the requirements of the property."),
    }),
    ("fa-solid fa-sparkles", {
        "es": ("Acabados cuidados", "Atención a las superficies, la protección y el estado final de los espacios."),
        "fr": ("Finitions soignées", "Une attention portée aux surfaces, à la protection et à l’état final des lieux."),
        "de": ("Sorgfältige Ausführung", "Aufmerksamkeit für Oberflächen, Schutz und den fertigen Zustand der Räume."),
        "it": ("Finiture curate", "Attenzione alle superfici, alla protezione e allo stato finale degli spazi."),
        "en": ("Careful finishes", "Attention to surfaces, protection and the final condition of the premises."),
    }),
)


def load_catalog():
    data = json.loads(SOURCE_FILE.read_text(encoding="utf-8"))
    categories = len(data)
    services = [service for category in data for service in category["services"]]
    slugs = [service["slug_fr"] for service in services]
    cat_slugs = [category["slug_fr"] for category in data]
    if categories != 7 or len(services) != 37 or len(set(slugs)) != 37 or len(set(cat_slugs)) != 7:
        raise ValueError("El catálogo debe incluir 7 categorías, 37 servicios y slugs únicos.")
    if [service["order"] for service in services] != list(range(1, 38)):
        raise ValueError("La numeración de los servicios debe ser correlativa, de 1 a 37.")
    return data


def safe_fields(model, values):
    fields = {f.name for f in model._meta.concrete_fields}
    return {key: value for key, value in values.items() if key in fields}


def clip(text, length):
    return text[:length].rsplit(" ", 1)[0].rstrip(" ,;.-") + ("…" if len(text) > length else "") if len(text) > length else text


def seed_catalogo_vv():
    """Crea o actualiza un catálogo de 7 categorías / 37 servicios sin tocar imágenes del Admin."""
    catalog = load_catalog()
    if not ServicePageVisualConfiguration.objects.exists():
        ServicePageVisualConfiguration.objects.create()
    category_records = {}
    for category in catalog:
        values = {
            "order": category["order"], "is_active": True,
            "icon": CATEGORY_ICONS[category["order"] - 1], "is_indexable": True,
        }
        for lang in LANGUAGES:
            name = category["name_" + lang]
            description = category["description_" + lang]
            values.update({
                "name_" + lang: name,
                "description_" + lang: description,
                "seo_title_" + lang: clip(f"{name} | V&V Swiss Services", 70),
                "meta_description_" + lang: clip(description, 157),
            })
            if lang != "es":
                values["slug_" + lang] = category["slug_fr"] if lang == "fr" else slugify(name)
        category_obj, _ = ServiceCategory.objects.update_or_create(
            slug_fr=category["slug_fr"], defaults=safe_fields(ServiceCategory, values)
        )
        category_records[category["slug_fr"]] = category_obj

    benefit_count = 0
    for category in catalog:
        category_obj = category_records[category["slug_fr"]]
        for service in category["services"]:
            values = {
                "category": category_obj, "is_active": True,
                "is_featured": service["order"] == category["services"][0]["order"],
                "order": service["order"],
                "icon": CATEGORY_ICONS[category["order"] - 1],
                "whatsapp_enabled": True,
            }
            for lang in LANGUAGES:
                txt = TEXTS[lang]
                name = service["name_" + lang]
                desc = service["description_" + lang]
                summary = clip(desc, 275)
                work_items = service["work_fr"].split("; ") if lang == "fr" else (
                    [x.strip() for x in service["work_es"].rstrip(".").split(",")] if lang == "es"
                    else [name, txt["quality_list"].splitlines()[0]]
                )
                values.update({
                    "name_" + lang: name,
                    "subtitle_" + lang: clip(desc, 290),
                    "summary_" + lang: summary,
                    "content_" + lang: desc,  # La descripción original FR se conserva íntegra.
                    "hero_title_prefix_" + lang: "V&V Swiss Services",
                    "hero_title_suffix_" + lang: txt["hero_suffix"],
                    "detail_1_title_" + lang: txt["work_title"],
                    "detail_1_text_" + lang: txt["work_intro"],
                    "detail_1_list_" + lang: "\n".join(work_items),
                    "detail_2_title_" + lang: txt["quality_title"],
                    "detail_2_text_" + lang: txt["quality_text"],
                    "detail_2_list_" + lang: txt["quality_list"],
                    "cta_title_" + lang: txt["cta_title"],
                    "cta_text_" + lang: txt["cta_text"],
                    "cta_button_" + lang: txt["cta_button"],
                })
                if lang != "es":
                    values["slug_" + lang] = service["slug_fr"] if lang == "fr" else slugify(name)
            service_obj, _ = Service.objects.update_or_create(
                slug_fr=service["slug_fr"], defaults=safe_fields(Service, values)
            )
            for idx, (icon, trans) in enumerate(BENEFITS, start=1):
                benefit_values = {"icon": icon}
                for lang in LANGUAGES:
                    title, description = trans[lang]
                    benefit_values["title_" + lang] = title
                    benefit_values["description_" + lang] = description
                ServiceBenefit.objects.update_or_create(
                    service=service_obj, order=idx,
                    defaults=safe_fields(ServiceBenefit, benefit_values)
                )
                benefit_count += 1
    return {"categories": len(catalog), "services": 37, "benefits": benefit_count}


class Command(BaseCommand):
    help = "V&V · Catálogo editorial 7 categorías y 37 servicios (FR, DE, IT, EN; ES interno)"

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Probar sin guardar cambios")

    def handle(self, *args, **options):
        with transaction.atomic():
            counts = seed_catalogo_vv()
            if options["dry_run"]:
                transaction.set_rollback(True)
        label = "SIMULACIÓN / SIN CAMBIOS" if options["dry_run"] else "CONTENIDO GUARDADO"
        self.stdout.write(self.style.SUCCESS(
            f"{label} · Categorías: {counts['categories']} · Servicios: {counts['services']} · Beneficios: {counts['benefits']}"
        ))
