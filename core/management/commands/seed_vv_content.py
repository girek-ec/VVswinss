# -*- coding: utf-8 -*-
from django.core.files.base import ContentFile
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from blog.models import (
    BlogCategory,
    BlogPageConfiguration,
    BlogTag,
    Post,
    PostSection,
)
from contact.models import (
    ContactAttachment,
    ContactPageConfiguration,
    ContactRequest,
)
from core.models import (
    AboutContent,
    AboutPageConfiguration,
    BusinessHour,
    Certification,
    CompanyValue,
    Insurance,
    FAQ,
    FAQCategory,
    HomeContent,
    InstitutionalPage,
    ProcessStep,
    ProfessionalBlock,
    ProfessionalPage,
    ProfessionalPageConfiguration,
    SocialLink,
    ServiceArea,
    SiteConfiguration,
    Statistic,
    TeamMember,
    Testimonial,
)
from projects.models import (
    BeforeAfter,
    BuildingType,
    Intervention,
    Project,
    ProjectImage,
    ProjectPageConfiguration,
    ProjectType,
)
from services.models import (
    Service,
    ServiceBenefit,
    ServiceCategory,
    ServicePageVisualConfiguration,
)
from services.management.commands.seed_catalogo_vv import seed_catalogo_vv

from ._seed_vv_data import (
    ABOUT_CONTENT,
    BENEFITS,
    CATEGORY_DATA,
    COMPANY_VALUES,
    FAQ_CATEGORIES,
    FAQS,
    HOME_CONTENT,
    INSTITUTIONAL_PAGES,
    PROCESS_STEPS,
    PROFESSIONAL_BLOCKS,
    PROFESSIONAL_PAGE,
    SERVICE_AREAS,
    SERVICE_DATA,
    SITE_CONTENT,
    STATISTICS,
    BUILDING_TYPES,
    DEMO_PROJECTS,
    PROJECT_TYPES,
    BLOG_CATEGORIES,
    BLOG_POSTS,
    BLOG_TAGS,
    DEMO_BUSINESS_HOURS,
    DEMO_CERTIFICATIONS,
    DEMO_CONTACT,
    DEMO_INSURANCES,
    DEMO_SOCIAL_LINKS,
    DEMO_TEAM,
    DEMO_TESTIMONIALS,
)


class Command(BaseCommand):
    help = (
        "V&V Swiss Services · Create/update multilingual editorial content "
        "for Services, Core, Projects, Blog and support configuration."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--with-demo",
            action="store_true",
            help="EN: Also create demonstration content. ES: Crear también contenido demostrativo.",
        )
        parser.add_argument(
            "--reset-demo",
            action="store_true",
            help="EN: Remove only seed demonstration records. ES: Eliminar solo registros demo del seed.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="EN: Run and roll back. ES: Ejecutar y revertir al finalizar.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        with_demo = options["with_demo"]
        reset_demo = options["reset_demo"]

        if reset_demo:
            self.reset_demo(dry_run=dry_run)
            return

        self.stdout.write("")
        self.stdout.write("=" * 72)
        self.stdout.write(" V&V SWISS SERVICES · SEED CONTENT")
        self.stdout.write(" PHASES 1–5 · FULL CONTENT SEED · 2026-11")
        self.stdout.write("=" * 72)

        with transaction.atomic():
            services_summary = seed_catalogo_vv()
            core_summary = self.seed_core()
            # PROFESIONALES V2 · TABLAS UTILIZADAS POR LA WEB | ACTIVE PUBLIC PAGE
            call_command("seed_professionals_v2", stdout=self.stdout)
            projects_summary = self.seed_projects(with_demo=with_demo)
            blog_summary = self.seed_blog(with_demo=with_demo)
            support_summary = self.seed_support_content(
                with_demo=with_demo,
                dry_run=dry_run,
            )

            if dry_run:
                transaction.set_rollback(True)
                self.stdout.write(
                    self.style.WARNING(
                        "\nDRY RUN · No database changes were saved."
                    )
                )

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Seed completed successfully."))
        self.stdout.write(
            f"Services → Categories: {services_summary['categories']} · "
            f"Services: {services_summary['services']} · "
            f"Benefits: {services_summary['benefits']}"
        )
        self.stdout.write(
            f"Core → Values: {core_summary['values']} · "
            f"Process: {core_summary['process']} · "
            f"Areas: {core_summary['areas']} · "
            f"FAQs: {core_summary['faqs']} · "
            f"Pages: {core_summary['pages']} · "
            f"Professional blocks: {core_summary['professional_blocks']}"
        )
        self.stdout.write(
            f"Projects → Types: {projects_summary['types']} · "
            f"Buildings: {projects_summary['buildings']} · "
            f"Demo projects: {projects_summary['projects']} · "
            f"Interventions: {projects_summary['interventions']}"
        )
        self.stdout.write(
            f"Blog → Categories: {blog_summary['categories']} · "
            f"Tags: {blog_summary['tags']} · "
            f"Posts: {blog_summary['posts']} · "
            f"Sections: {blog_summary['sections']}"
        )
        self.stdout.write(
            f"Support/demo → Social: {support_summary['social']} · "
            f"Hours: {support_summary['hours']} · "
            f"Team: {support_summary['team']} · "
            f"Insurances: {support_summary['insurances']} · "
            f"Certifications: {support_summary['certifications']} · "
            f"Testimonials: {support_summary['testimonials']} · "
            f"Contact requests: {support_summary['contacts']}"
        )
        self.stdout.write("")

    # ------------------------------------------------------------------
    # Helpers / Ayudantes
    # ------------------------------------------------------------------

    @staticmethod
    def localized_fields(prefix, values):
        return {
            f"{prefix}_{language}": values.get(language, "")
            for language in ("es", "fr", "de", "it", "en")
        }

    @staticmethod
    def public_localized_fields(prefix, values):
        return {
            f"{prefix}_{language}": values.get(language, "")
            for language in ("fr", "de", "it", "en")
        }

    @staticmethod
    def public_slugs(names):
        return {
            "slug_fr": slugify(names["fr"]),
            "slug_de": slugify(names["de"]),
            "slug_it": slugify(names["it"]),
            "slug_en": slugify(names["en"]),
        }

    @staticmethod
    def model_field_names(model):
        """
        EN: Return concrete model field names only.
        ES: Devuelve únicamente los nombres de campos concretos del modelo.
        """
        return {
            field.name
            for field in model._meta.get_fields()
            if getattr(field, "concrete", False)
        }

    @classmethod
    def safe_values(cls, model, values):
        """
        EN: Ignore keys that no longer exist after a schema evolution.
        ES: Ignora claves que ya no existen después de una evolución del esquema.

        This keeps the seed compatible with the current migrations without
        hiding database or validation errors for fields that do exist.
        """
        allowed = cls.model_field_names(model)
        return {
            key: value
            for key, value in values.items()
            if key in allowed
        }

    @classmethod
    def update_singleton(cls, model, values):
        """
        EN: Update the first record or create one without deleting media fields.
        ES: Actualiza el primer registro o crea uno sin borrar campos multimedia.

        Only explicitly supplied fields are touched. Image/file fields already
        configured in Admin remain intact, including visual fallbacks and social
        images such as insurance_default_image or post_default_social_image.
        """
        obj = model.objects.order_by("pk").first()
        if obj is None:
            obj = model()
        for field, value in cls.safe_values(model, values).items():
            setattr(obj, field, value)
        obj.save()
        return obj

    @staticmethod
    def service_texts(names, category):
        lists = category["detail_lists"]

        summary = {
            "es": (
                f"V&V Swiss Services acompaña su proyecto de «{names['es']}» "
                "con una planificación clara, coordinación fiable y acabados cuidados."
            ),
            "fr": (
                f"V&V Swiss Services vous accompagne pour « {names['fr']} », "
                "avec une planification claire, une coordination fiable et des finitions soignées."
            ),
            "de": (
                f"V&V Swiss Services begleitet Sie bei «{names['de']}» "
                "mit klarer Planung, zuverlässiger Koordination und sorgfältiger Ausführung."
            ),
            "it": (
                f"V&V Swiss Services vi accompagna per «{names['it']}» "
                "con una pianificazione chiara, un coordinamento affidabile e finiture curate."
            ),
            "en": (
                f"V&V Swiss Services supports your project for “{names['en']}” "
                "with clear planning, reliable co-ordination and careful finishing."
            ),
        }

        content = {
            "es": (
                f"El servicio «{names['es']}» se planifica teniendo en cuenta el estado del inmueble, "
                "las limitaciones técnicas, el uso de los espacios y el nivel de acabado esperado. "
                "Nuestro objetivo es organizar los trabajos de forma clara, mantener una comunicación "
                "directa y ejecutar cada etapa con cuidado."
            ),
            "fr": (
                f"Le service « {names['fr']} » est planifié en tenant compte de l’état du bâtiment, "
                "des contraintes techniques, de l’usage des espaces et du niveau de finition recherché. "
                "Notre objectif est d’organiser les travaux de manière claire, de maintenir une communication "
                "directe et de réaliser chaque étape avec soin."
            ),
            "de": (
                f"Die Leistung «{names['de']}» wird unter Berücksichtigung des Gebäudezustands, "
                "der technischen Rahmenbedingungen, der Nutzung der Räume und des gewünschten "
                "Ausführungsstandards geplant. Unser Ziel ist eine klare Organisation, direkte Kommunikation "
                "und eine sorgfältige Umsetzung jeder Etappe."
            ),
            "it": (
                f"Il servizio «{names['it']}» viene pianificato considerando lo stato dell’edificio, "
                "i vincoli tecnici, l’utilizzo degli spazi e il livello di finitura desiderato. "
                "L’obiettivo è organizzare i lavori in modo chiaro, mantenere una comunicazione diretta "
                "e curare ogni fase dell’intervento."
            ),
            "en": (
                f"The “{names['en']}” service is planned around the condition of the building, "
                "technical constraints, the way the spaces are used and the required standard of finish. "
                "Our aim is to organise the work clearly, maintain direct communication and carry out "
                "each stage with care."
            ),
        }

        detail_1_title = {
            "es": "Una intervención adaptada al inmueble",
            "fr": "Une intervention adaptée à votre bâtiment",
            "de": "Eine auf Ihr Gebäude abgestimmte Ausführung",
            "it": "Un intervento adatto al vostro immobile",
            "en": "Work tailored to your building",
        }
        detail_1_text = {
            "es": "Antes de intervenir, se revisan las necesidades, el soporte existente y las prioridades del proyecto para definir una solución coherente.",
            "fr": "Avant l’intervention, nous examinons les besoins, les supports existants et les priorités du projet afin de définir une solution cohérente.",
            "de": "Vor Beginn prüfen wir die Anforderungen, die vorhandenen Untergründe und die Prioritäten des Projekts, um eine passende Lösung festzulegen.",
            "it": "Prima dell’intervento valutiamo le esigenze, i supporti esistenti e le priorità del progetto per definire una soluzione coerente.",
            "en": "Before work begins, we assess the requirements, existing surfaces and project priorities to define an appropriate solution.",
        }

        detail_2_title = {
            "es": "Organización y calidad de ejecución",
            "fr": "Organisation et qualité d’exécution",
            "de": "Organisation und Ausführungsqualität",
            "it": "Organizzazione e qualità dell’esecuzione",
            "en": "Organisation and quality of workmanship",
        }
        detail_2_text = {
            "es": "La planificación, la protección de las zonas de trabajo, la coordinación y la limpieza forman parte del seguimiento de cada intervención.",
            "fr": "La planification, la protection des zones de travail, la coordination et la propreté font partie du suivi de chaque intervention.",
            "de": "Planung, Schutz der Arbeitsbereiche, Koordination und Sauberkeit sind feste Bestandteile jeder Ausführung.",
            "it": "Pianificazione, protezione delle aree di lavoro, coordinamento e pulizia fanno parte del monitoraggio di ogni intervento.",
            "en": "Planning, protection of work areas, co-ordination and cleanliness form part of the management of every job.",
        }

        cta_title = {
            "es": f"¿Tiene un proyecto de «{names['es']}»?",
            "fr": f"Un projet de « {names['fr']} » ?",
            "de": f"Planen Sie «{names['de']}»?",
            "it": f"Avete un progetto di «{names['it']}»?",
            "en": f"Planning “{names['en']}”?",
        }
        cta_text = {
            "es": "Descríbanos sus necesidades. Podemos revisar el alcance del trabajo y preparar una propuesta clara para su proyecto.",
            "fr": "Décrivez-nous vos besoins. Nous pouvons examiner l’étendue des travaux et préparer une proposition claire pour votre projet.",
            "de": "Beschreiben Sie uns Ihr Vorhaben. Wir prüfen den Leistungsumfang und erstellen eine klare Offerte für Ihr Projekt.",
            "it": "Descriveteci le vostre esigenze. Possiamo valutare l’entità dei lavori e preparare un’offerta chiara per il vostro progetto.",
            "en": "Tell us about your requirements. We can review the scope of work and prepare a clear quotation for your project.",
        }
        cta_button = {
            "es": "Solicitar información",
            "fr": "Demander des informations",
            "de": "Informationen anfordern",
            "it": "Richiedere informazioni",
            "en": "Request information",
        }
        whatsapp = {
            "es": f"Hola, deseo información sobre «{names['es']}» y solicitar un presupuesto para mi proyecto. Gracias.",
            "fr": f"Bonjour, je souhaite obtenir des informations sur « {names['fr']} » et demander un devis pour mon projet. Merci.",
            "de": f"Guten Tag, ich wünsche Informationen zu «{names['de']}» und möchte eine Offerte für mein Projekt anfragen. Vielen Dank.",
            "it": f"Buongiorno, desidero informazioni su «{names['it']}» e vorrei richiedere un’offerta per il mio progetto. Grazie.",
            "en": f"Hello, I would like information about “{names['en']}” and would like to request a quotation for my project. Thank you.",
        }

        seo_title = {
            lang: f"{names[lang]} | V&V Swiss Services"
            for lang in ("es", "fr", "de", "it", "en")
        }
        meta = {
            "es": f"{summary['es']} Servicios de renovación en el cantón de Vaud y la Suiza francófona.",
            "fr": f"{summary['fr']} Prestations de rénovation dans le canton de Vaud et en Suisse romande.",
            "de": f"{summary['de']} Renovationsleistungen im Kanton Waadt und in der Romandie.",
            "it": f"{summary['it']} Servizi di ristrutturazione nel Canton Vaud e nella Svizzera romanda.",
            "en": f"{summary['en']} Renovation services in the canton of Vaud and French-speaking Switzerland.",
        }

        return {
            "summary": summary,
            "content": content,
            "detail_1_title": detail_1_title,
            "detail_1_text": detail_1_text,
            "detail_1_list": {lang: "\n".join(items) for lang, items in lists.items()},
            "detail_2_title": detail_2_title,
            "detail_2_text": detail_2_text,
            "detail_2_list": {lang: "\n".join(items) for lang, items in lists.items()},
            "cta_title": cta_title,
            "cta_text": cta_text,
            "cta_button": cta_button,
            "whatsapp_message": whatsapp,
            "seo_title": seo_title,
            "meta_description": meta,
        }

    # ------------------------------------------------------------------
    # Phase 1 · Services
    # ------------------------------------------------------------------

    def seed_services(self):
        # Keep one visual configuration row without touching images already
        # uploaded from Admin. New fields such as category_default_social_image
        # are therefore preserved automatically.
        self.update_singleton(ServicePageVisualConfiguration, {})

        categories = {}
        for category in CATEGORY_DATA:
            names = category["name"]
            descriptions = category["description"]

            category_seo_titles = {
                language: f"{names[language]} | V&V Swiss Services"
                for language in ("es", "fr", "de", "it", "en")
            }

            defaults = {
                **self.localized_fields("name", names),
                **self.localized_fields("description", descriptions),
                **self.public_slugs(names),
                **self.localized_fields("seo_title", category_seo_titles),
                **self.localized_fields("meta_description", descriptions),
                "icon": category["icon"],
                "order": category["order"],
                "is_active": True,
                "is_indexable": True,
            }

            obj, _ = ServiceCategory.objects.update_or_create(
                slug_fr=slugify(names["fr"]),
                defaults=self.safe_values(ServiceCategory, defaults),
            )
            categories[names["fr"]] = (obj, category)

        service_count = benefit_count = 0

        for service_data in SERVICE_DATA:
            category_obj, category_data = categories[service_data["category"]]
            names = service_data["names"]
            text = self.service_texts(names, category_data)

            defaults = {
                "category": category_obj,
                **self.localized_fields("name", names),
                **self.public_slugs(names),
                **self.localized_fields("subtitle", text["summary"]),
                **self.localized_fields(
                    "hero_title_prefix",
                    {
                        lang: "V&V Swiss Services"
                        for lang in ("es", "fr", "de", "it", "en")
                    },
                ),
                **self.localized_fields(
                    "hero_title_suffix",
                    {
                        "es": "Planificación clara y acabados cuidados",
                        "fr": "Planification claire et finitions soignées",
                        "de": "Klare Planung und sorgfältige Ausführung",
                        "it": "Pianificazione chiara e finiture curate",
                        "en": "Clear planning and careful finishing",
                    },
                ),
                **self.localized_fields("summary", text["summary"]),
                **self.localized_fields("content", text["content"]),
                **self.localized_fields("detail_1_title", text["detail_1_title"]),
                **self.localized_fields("detail_1_text", text["detail_1_text"]),
                **self.localized_fields("detail_1_list", text["detail_1_list"]),
                **self.localized_fields("detail_2_title", text["detail_2_title"]),
                **self.localized_fields("detail_2_text", text["detail_2_text"]),
                **self.localized_fields("detail_2_list", text["detail_2_list"]),
                **self.localized_fields("cta_title", text["cta_title"]),
                **self.localized_fields("cta_text", text["cta_text"]),
                **self.localized_fields("cta_button", text["cta_button"]),
                **self.localized_fields(
                    "whatsapp_message",
                    text["whatsapp_message"],
                ),
                **self.localized_fields("seo_title", text["seo_title"]),
                **self.localized_fields(
                    "meta_description",
                    text["meta_description"],
                ),
                "icon": category_data["icon"],
                "whatsapp_enabled": True,
                "is_featured": service_data["featured"],
                "order": service_data["order"],
                "is_active": True,
                # Kept only when the current Service model still exposes it.
                "is_indexable": True,
            }

            service, _ = Service.objects.update_or_create(
                slug_fr=slugify(names["fr"]),
                defaults=self.safe_values(Service, defaults),
            )
            service_count += 1

            for benefit in BENEFITS:
                benefit_defaults = {
                    **self.localized_fields("title", benefit["title"]),
                    **self.localized_fields(
                        "description",
                        benefit["description"],
                    ),
                    "icon": benefit["icon"],
                }
                ServiceBenefit.objects.update_or_create(
                    service=service,
                    order=benefit["order"],
                    defaults=self.safe_values(
                        ServiceBenefit,
                        benefit_defaults,
                    ),
                )
                benefit_count += 1

        return {
            "categories": len(categories),
            "services": service_count,
            "benefits": benefit_count,
        }

    # ------------------------------------------------------------------
    # Phase 2 · Core
    # ------------------------------------------------------------------

    def seed_core(self):
        # Site configuration / Configuración general
        self.update_singleton(
            SiteConfiguration,
            {
                "company_name": SITE_CONTENT["company_name"],
                **self.localized_fields("slogan", SITE_CONTENT["slogan"]),
                "country": SITE_CONTENT["country"],
                "canton": SITE_CONTENT["canton"],
                "is_active": True,
            },
        )

        # Visual singleton records / Registros visuales únicos
        self.update_singleton(AboutPageConfiguration, {})
        self.update_singleton(ProfessionalPageConfiguration, {})

        # Home / Inicio
        self.update_singleton(
            HomeContent,
            {
                **self.localized_fields("title", HOME_CONTENT["title"]),
                **self.localized_fields("subtitle", HOME_CONTENT["subtitle"]),
                "is_active": True,
            },
        )

        # About / Empresa
        self.update_singleton(
            AboutContent,
            {
                **self.localized_fields("intro_title", ABOUT_CONTENT["intro_title"]),
                **self.localized_fields("intro_text", ABOUT_CONTENT["intro_text"]),
                **self.localized_fields("mission", ABOUT_CONTENT["mission"]),
                **self.localized_fields("vision", ABOUT_CONTENT["vision"]),
                **self.localized_fields("history", ABOUT_CONTENT["history"]),
                "is_active": True,
            },
        )

        # Company values / Valores
        for item in COMPANY_VALUES:
            CompanyValue.objects.update_or_create(
                title_fr=item["title"]["fr"],
                defaults={
                    **self.localized_fields("title", item["title"]),
                    **self.localized_fields("description", item["description"]),
                    "order": item["order"],
                    "is_active": True,
                },
            )

        # Process / Proceso
        for item in PROCESS_STEPS:
            ProcessStep.objects.update_or_create(
                number=item["number"],
                defaults={
                    **self.localized_fields("title", item["title"]),
                    **self.localized_fields("description", item["description"]),
                    "icon": item["icon"],
                    "is_active": True,
                },
            )

        # Service areas / Zonas
        for item in SERVICE_AREAS:
            ServiceArea.objects.update_or_create(
                name=item["name"],
                defaults={
                    "canton": item["canton"],
                    **self.localized_fields("description", item["description"]),
                    "order": item["order"],
                    "is_active": True,
                },
            )

        # Statistics / Estadísticas
        for item in STATISTICS:
            Statistic.objects.update_or_create(
                value=item["value"],
                defaults={
                    **self.localized_fields("title", item["title"]),
                    "order": item["order"],
                    "is_active": True,
                },
            )

        # FAQ categories / Categorías FAQ
        faq_categories = {}
        for item in FAQ_CATEGORIES:
            obj, _ = FAQCategory.objects.update_or_create(
                name_fr=item["name"]["fr"],
                defaults={
                    **self.localized_fields("name", item["name"]),
                    "order": item["order"],
                    "is_active": True,
                },
            )
            faq_categories[item["name"]["fr"]] = obj

        # FAQs
        faq_count = 0
        for item in FAQS:
            FAQ.objects.update_or_create(
                question_fr=item["question"]["fr"],
                defaults={
                    "category": faq_categories[item["category"]],
                    **self.public_localized_fields("question", item["question"]),
                    **self.public_localized_fields("answer", item["answer"]),
                    "order": item["order"],
                    "is_active": True,
                },
            )
            faq_count += 1

        # Institutional pages / Páginas institucionales
        page_count = 0
        for item in INSTITUTIONAL_PAGES:
            titles = item["title"]
            content = item["content"]
            defaults = {
                **self.localized_fields("title", titles),
                **self.localized_fields("content", content),
                "slug_de": slugify(titles["de"]),
                "slug_it": slugify(titles["it"]),
                "slug_en": slugify(titles["en"]),
                "seo_title_es": f"{titles['es']} | V&V Swiss Services",
                "seo_title_fr": f"{titles['fr']} | V&V Swiss Services",
                "seo_title_de": f"{titles['de']} | V&V Swiss Services",
                "seo_title_it": f"{titles['it']} | V&V Swiss Services",
                "seo_title_en": f"{titles['en']} | V&V Swiss Services",
                "meta_description_es": content["es"][:300],
                "meta_description_fr": content["fr"][:300],
                "meta_description_de": content["de"][:300],
                "meta_description_it": content["it"][:300],
                "meta_description_en": content["en"][:300],
                "is_indexable": True,
                "is_active": True,
            }
            InstitutionalPage.objects.update_or_create(
                slug_fr=item["slug_fr"],
                defaults=defaults,
            )
            page_count += 1

        # Professionals / Profesionales
        professional_page = self.update_singleton(
            ProfessionalPage,
            {
                **self.localized_fields("hero_title", PROFESSIONAL_PAGE["hero_title"]),
                **self.localized_fields("hero_text", PROFESSIONAL_PAGE["hero_text"]),
                "is_active": True,
            },
        )
        professional_page.services.set(Service.objects.filter(is_active=True))

        for item in PROFESSIONAL_BLOCKS:
            ProfessionalBlock.objects.update_or_create(
                page=professional_page,
                order=item["order"],
                defaults={
                    "layout": item["layout"],
                    **self.localized_fields("title", item["title"]),
                    **self.localized_fields("text", item["text"]),
                    "icon": item["icon"],
                    "is_active": True,
                },
            )

        return {
            "values": len(COMPANY_VALUES),
            "process": len(PROCESS_STEPS),
            "areas": len(SERVICE_AREAS),
            "faqs": faq_count,
            "pages": page_count,
            "professional_blocks": len(PROFESSIONAL_BLOCKS),
        }

    # ------------------------------------------------------------------
    # Phase 3 · Projects / Réalisations
    # ------------------------------------------------------------------

    def seed_projects(self, with_demo=False):
        self.update_singleton(ProjectPageConfiguration, {})

        project_types = {}
        for item in PROJECT_TYPES:
            obj, _ = ProjectType.objects.update_or_create(
                name_fr=item["name"]["fr"],
                defaults={
                    **self.localized_fields("name", item["name"]),
                    "order": item["order"],
                    "is_active": True,
                },
            )
            project_types[item["name"]["fr"]] = obj

        building_types = {}
        for item in BUILDING_TYPES:
            obj, _ = BuildingType.objects.update_or_create(
                name_fr=item["name"]["fr"],
                defaults={
                    **self.localized_fields("name", item["name"]),
                    "order": item["order"],
                    "is_active": True,
                },
            )
            building_types[item["name"]["fr"]] = obj

        project_count = 0
        intervention_count = 0

        if not with_demo:
            return {
                "types": len(PROJECT_TYPES),
                "buildings": len(BUILDING_TYPES),
                "projects": 0,
                "interventions": 0,
            }

        services_by_name = {
            service.name_fr: service
            for service in Service.objects.filter(is_active=True)
        }

        for item in DEMO_PROJECTS:
            title = item["title"]
            summary = item["summary"]
            content = item["content"]

            project, _ = Project.objects.update_or_create(
                slug_fr=item["key"],
                defaults={
                    "project_type": project_types[item["project_type"]],
                    "building_type": building_types[item["building_type"]],
                    **self.localized_fields("title", title),
                    "slug_de": slugify(title["de"]),
                    "slug_it": slugify(title["it"]),
                    "slug_en": slugify(title["en"]),
                    "location": item["location"],
                    "client": "DÉMONSTRATION / DEMO",
                    **self.localized_fields("summary", summary),
                    **self.localized_fields("content", content),
                    "seo_title_es": f"{title['es']} | V&V Swiss Services",
                    "seo_title_fr": f"{title['fr']} | V&V Swiss Services",
                    "seo_title_de": f"{title['de']} | V&V Swiss Services",
                    "seo_title_it": f"{title['it']} | V&V Swiss Services",
                    "seo_title_en": f"{title['en']} | V&V Swiss Services",
                    "meta_description_es": summary["es"][:300],
                    "meta_description_fr": summary["fr"][:300],
                    "meta_description_de": summary["de"][:300],
                    "meta_description_it": summary["it"][:300],
                    "meta_description_en": summary["en"][:300],
                    "show_on_map": False,
                    "is_featured": False,
                    "is_published": False,
                    "is_indexable": False,
                },
            )

            related_services = [
                services_by_name[name]
                for name in item["services_fr"]
                if name in services_by_name
            ]
            project.services.set(related_services)

            # One gallery placeholder using visual/static fallback.
            ProjectImage.objects.update_or_create(
                project=project,
                order=1,
                defaults={
                    "alt_es": f"Imagen demostrativa · {title['es']}",
                    "alt_fr": f"Image de démonstration · {title['fr']}",
                    "alt_de": f"Demobild · {title['de']}",
                    "alt_it": f"Immagine dimostrativa · {title['it']}",
                    "alt_en": f"Demonstration image · {title['en']}",
                },
            )

            # One before/after placeholder using Home/Projects fallbacks.
            BeforeAfter.objects.update_or_create(
                project=project,
                order=1,
                defaults={
                    "title_es": "Antes / Después · demostración",
                    "title_fr": "Avant / Après · démonstration",
                    "title_de": "Vorher / Nachher · Demo",
                    "title_it": "Prima / Dopo · dimostrazione",
                    "title_en": "Before / After · demonstration",
                },
            )

            for order, intervention in enumerate(item["interventions"], start=1):
                Intervention.objects.update_or_create(
                    project=project,
                    order=order,
                    defaults={
                        "title_es": intervention["es"],
                        "title_fr": intervention["fr"],
                        "title_de": intervention["de"],
                        "title_it": intervention["it"],
                        "title_en": intervention["en"],
                        "description_es": "Etapa demostrativa del proyecto preparada para mostrar la estructura de una realización.",
                        "description_fr": "Étape de démonstration préparée pour illustrer la structure d’une réalisation.",
                        "description_de": "Demonstrationsetappe zur Darstellung der Struktur eines Referenzprojekts.",
                        "description_it": "Fase dimostrativa preparata per illustrare la struttura di una realizzazione.",
                        "description_en": "Demonstration stage prepared to illustrate the structure of a completed-project page.",
                    },
                )
                intervention_count += 1

            project_count += 1

        return {
            "types": len(PROJECT_TYPES),
            "buildings": len(BUILDING_TYPES),
            "projects": project_count,
            "interventions": intervention_count,
        }

    # ------------------------------------------------------------------
    # Phase 4 · Blog / Actualités & conseils
    # ------------------------------------------------------------------

    def seed_blog(self, with_demo=False):
        self.update_singleton(BlogPageConfiguration, {})

        categories = {}
        for order, item in enumerate(BLOG_CATEGORIES, start=1):
            names = item["name"]
            obj, _ = BlogCategory.objects.update_or_create(
                slug_fr=slugify(names["fr"]),
                defaults={
                    "name_fr": names["fr"],
                    "name_de": names["de"],
                    "name_it": names["it"],
                    "name_en": names["en"],
                    "slug_de": slugify(names["de"]),
                    "slug_it": slugify(names["it"]),
                    "slug_en": slugify(names["en"]),
                    "is_active": True,
                },
            )
            categories[names["fr"]] = obj

        tags = {}
        for item in BLOG_TAGS:
            names = item["name"]
            obj, _ = BlogTag.objects.update_or_create(
                slug_fr=slugify(names["fr"]),
                defaults={
                    "name_fr": names["fr"],
                    "name_de": names["de"],
                    "name_it": names["it"],
                    "name_en": names["en"],
                    "slug_de": slugify(names["de"]),
                    "slug_it": slugify(names["it"]),
                    "slug_en": slugify(names["en"]),
                    "is_active": True,
                },
            )
            tags[names["fr"]] = obj

        post_count = 0
        section_count = 0

        # BLOG · DATOS INICIALES SIN NOTICIAS FICTICIAS | NO FAKE POSTS BY DEFAULT
        if not with_demo:
            return {
                "categories": len(BLOG_CATEGORIES), "tags": len(BLOG_TAGS),
                "posts": 0, "sections": 0,
            }

        for item in BLOG_POSTS:
            title = item["title"]
            excerpt = item["excerpt"]
            content = item["content"]

            post, _ = Post.objects.update_or_create(
                slug_fr=slugify(title["fr"]),
                defaults={
                    "category": categories[item["category"]],
                    "title_fr": title["fr"],
                    "title_de": title["de"],
                    "title_it": title["it"],
                    "title_en": title["en"],
                    "slug_de": slugify(title["de"]),
                    "slug_it": slugify(title["it"]),
                    "slug_en": slugify(title["en"]),
                    "excerpt_fr": excerpt["fr"],
                    "excerpt_de": excerpt["de"],
                    "excerpt_it": excerpt["it"],
                    "excerpt_en": excerpt["en"],
                    "content_fr": content["fr"],
                    "content_de": content["de"],
                    "content_it": content["it"],
                    "content_en": content["en"],
                    "seo_title_es": f"{title['fr']} | V&V Swiss Services",
                    "seo_title_fr": f"{title['fr']} | V&V Swiss Services",
                    "seo_title_de": f"{title['de']} | V&V Swiss Services",
                    "seo_title_it": f"{title['it']} | V&V Swiss Services",
                    "seo_title_en": f"{title['en']} | V&V Swiss Services",
                    "meta_description_es": excerpt["fr"][:300],
                    "meta_description_fr": excerpt["fr"][:300],
                    "meta_description_de": excerpt["de"][:300],
                    "meta_description_it": excerpt["it"][:300],
                    "meta_description_en": excerpt["en"][:300],
                    "is_indexable": False,
                    "is_published": False,
                    "is_featured": False,
                },
            )

            post.tags.set([
                tags[name]
                for name in item["tags"]
                if name in tags
            ])

            for order, section in enumerate(item["sections"], start=1):
                PostSection.objects.update_or_create(
                    post=post,
                    order=order,
                    defaults={
                        "section_type": PostSection.SECTION_TEXT,
                        "is_active": True,
                        "title_fr": section["title"]["fr"],
                        "title_de": section["title"]["de"],
                        "title_it": section["title"]["it"],
                        "title_en": section["title"]["en"],
                        "content_fr": section["text"]["fr"],
                        "content_de": section["text"]["de"],
                        "content_it": section["text"]["it"],
                        "content_en": section["text"]["en"],
                    },
                )
                section_count += 1

            post_count += 1

        return {
            "categories": len(BLOG_CATEGORIES),
            "tags": len(BLOG_TAGS),
            "posts": post_count,
            "sections": section_count,
        }

    # ------------------------------------------------------------------
    # Phase 5 · Support / demo-only models
    # ------------------------------------------------------------------

    def seed_support_content(self, with_demo=False, dry_run=False):
        # Visual configuration exists in both local and production.
        self.update_singleton(ContactPageConfiguration, {})

        empty = {
            "social": 0,
            "hours": 0,
            "team": 0,
            "insurances": 0,
            "certifications": 0,
            "testimonials": 0,
            "contacts": 0,
        }

        if not with_demo:
            return empty

        for item in DEMO_SOCIAL_LINKS:
            SocialLink.objects.update_or_create(
                name=item["name"],
                defaults={
                    "url": item["url"],
                    "icon": item["icon"],
                    "order": item["order"],
                    "is_active": True,
                },
            )

        for item in DEMO_BUSINESS_HOURS:
            BusinessHour.objects.update_or_create(
                day_fr=item["day_fr"],
                defaults={
                    "day_de": item["day_de"],
                    "day_it": item["day_it"],
                    "day_en": item["day_en"],
                    "hours": item["hours"],
                    "order": item["order"],
                    "is_active": True,
                },
            )

        for item in DEMO_TEAM:
            TeamMember.objects.update_or_create(
                name=item["name"],
                defaults={
                    "position_fr": item["position"]["fr"],
                    "position_de": item["position"]["de"],
                    "position_it": item["position"]["it"],
                    "position_en": item["position"]["en"],
                    "biography_fr": item["biography"]["fr"],
                    "biography_de": item["biography"]["de"],
                    "biography_it": item["biography"]["it"],
                    "biography_en": item["biography"]["en"],
                    "order": item["order"],
                    "is_active": True,
                },
            )

        for item in DEMO_INSURANCES:
            Insurance.objects.update_or_create(
                name_fr=item["name"]["fr"],
                defaults={
                    **self.localized_fields("name", item["name"]),
                    **self.localized_fields("description", item["description"]),
                    "order": item["order"],
                    "is_active": True,
                },
            )

        for item in DEMO_CERTIFICATIONS:
            Certification.objects.update_or_create(
                name=item["name"],
                defaults={
                    "issuer": item["issuer"],
                    "order": item["order"],
                    "is_active": True,
                },
            )

        for item in DEMO_TESTIMONIALS:
            Testimonial.objects.update_or_create(
                name=item["name"],
                company=item["company"],
                defaults={
                    **self.localized_fields("text", item["text"]),
                    "rating": item["rating"],
                    "order": item["order"],
                    "is_active": True,
                },
            )

        # Contact request is demo-only and linked to a real Service row.
        demo_service = Service.objects.filter(is_active=True).order_by("order", "pk").first()
        contact, _ = ContactRequest.objects.update_or_create(
            email=DEMO_CONTACT["email"],
            name=DEMO_CONTACT["name"],
            defaults={
                "company": DEMO_CONTACT["company"],
                "phone": DEMO_CONTACT["phone"],
                "service": demo_service,
                "project_location": DEMO_CONTACT["project_location"],
                "message": DEMO_CONTACT["message"],
                "request_visit": False,
                "privacy_accepted": True,
                "privacy_policy_version": "DEMO",
                "status": ContactRequest.STATUS_NEW,
                "language": DEMO_CONTACT["language"],
                "internal_notes": DEMO_CONTACT["internal_notes"],
                "user_agent": "V&V seed demo",
            },
        )

        # Fill ContactAttachment as well. Avoid file-system side effects in
        # --dry-run because database rollback cannot remove files from MEDIA.
        if not dry_run and not contact.attachments.exists():
            attachment = ContactAttachment(request=contact)
            attachment.file.save(
                "demo-seed-vv.txt",
                ContentFile(
                    b"V&V Swiss Services - DEMO attachment generated by seed_vv_content.\n"
                ),
                save=True,
            )

        return {
            "social": len(DEMO_SOCIAL_LINKS),
            "hours": len(DEMO_BUSINESS_HOURS),
            "team": len(DEMO_TEAM),
            "insurances": len(DEMO_INSURANCES),
            "certifications": len(DEMO_CERTIFICATIONS),
            "testimonials": len(DEMO_TESTIMONIALS),
            "contacts": 1,
        }

    # ------------------------------------------------------------------
    # Remove seed demo content only / Eliminar solo contenido demo
    # ------------------------------------------------------------------

    def reset_demo(self, dry_run=False):
        self.stdout.write("")
        self.stdout.write("=" * 72)
        self.stdout.write(" V&V SWISS SERVICES · RESET DEMO CONTENT")
        self.stdout.write("=" * 72)

        with transaction.atomic():
            # Contact attachments cascade from ContactRequest.
            ContactRequest.objects.filter(
                email=DEMO_CONTACT["email"],
                name=DEMO_CONTACT["name"],
            ).delete()

            Testimonial.objects.filter(company="DÉMONSTRATION").delete()
            Certification.objects.filter(
                name__startswith="DÉMONSTRATION ·"
            ).delete()
            Insurance.objects.filter(
                name_fr__icontains="DÉMONSTRATION"
            ).delete()
            TeamMember.objects.filter(
                name__icontains="DÉMONSTRATION"
            ).delete()
            BusinessHour.objects.filter(
                day_fr__icontains="DÉMO"
            ).delete()
            SocialLink.objects.filter(name__icontains="DEMO").delete()

            # Projects and their related images/before-after/interventions cascade.
            Project.objects.filter(
                client="DÉMONSTRATION / DEMO"
            ).delete()

            if dry_run:
                transaction.set_rollback(True)

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    "DRY RUN · Demo records were not deleted."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "Demo records removed. Production/editorial content was preserved."
                )
            )
        self.stdout.write("")
