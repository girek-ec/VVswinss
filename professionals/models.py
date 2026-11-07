from django.db import models
from django.utils.translation import get_language, gettext

from core.models import ProfessionalBlock as CoreProfessionalBlock
from core.models import ProfessionalPage as CoreProfessionalPage
from core.visual_config import ProfessionalPageConfiguration as CoreProfessionalVisuals


# MODELOS DE ACCESO · CONSERVAN TABLAS Y REGISTROS CORE | PROXIES PRESERVE EXISTING DATABASE
class ProfessionalPage(CoreProfessionalPage):
    class Meta:
        proxy = True
        verbose_name = "01 · Page Professionnels"
        verbose_name_plural = "01 · Page Professionnels"


class ProfessionalBlock(CoreProfessionalBlock):
    class Meta:
        proxy = True
        verbose_name = "07 · Bloc complémentaire"
        verbose_name_plural = "07 · Blocs complémentaires"


class ProfessionalVisualConfiguration(CoreProfessionalVisuals):
    class Meta:
        proxy = True
        verbose_name = "06 · Configuration visuelle"
        verbose_name_plural = "06 · Configuration visuelle"


# CONTENIDOS PREDETERMINADOS · TEXTOS FR IDÉNTICOS A LA PLANTILLA ACTUAL
NEED_DEFAULTS = {
    "coordination": ("Coordination de plusieurs corps de métier", "Nous coordonnons plusieurs interventions afin de simplifier le suivi de vos travaux et de limiter les échanges avec différents prestataires.", "need_coordination_image", "antra/assets/img/professionals/01_coordinacion_varios_oficios.webp"),
    "planning": ("Interventions rapides et planifiées", "Nous organisons les interventions selon vos priorités, les délais disponibles et les contraintes propres à chaque bien immobilier.", "need_planning_image", "antra/assets/img/professionals/02_intervenciones_planificadas.webp"),
    "turnover": ("Remise en état entre locataires", "Nous intervenons entre deux locations pour remettre les logements ou locaux en état et préparer efficacement leur prochaine occupation.", "need_turnover_image", "antra/assets/img/professionals/03_remise_en_etat.webp"),
    "maintenance": ("Entretien, réparations et finitions", "Nous prenons en charge les travaux d’entretien, les réparations et les finitions nécessaires au maintien de vos biens.", "need_maintenance_image", "antra/assets/img/professionals/04_mantenimiento_inmueble.webp"),
    "occupancy": ("Préparation avant nouvelle occupation", "Nous préparons les logements et locaux avant une nouvelle occupation en coordonnant les travaux nécessaires avec un interlocuteur unique.", "need_occupancy_image", "antra/assets/img/professionals/05_preparacion_nueva_ocupacion.webp"),
}
PROCESS_DEFAULTS = {
    "evaluation": ("Évaluation", "Nous identifions les travaux nécessaires et les priorités afin de définir clairement les interventions à réaliser.", "evaluation_image", "antra/assets/img/professionals/01_evaluation.webp"),
    "planning": ("Planification", "Nous organisons les différents travaux selon les délais disponibles, les priorités du bien et la date prévue pour sa prochaine occupation.", "planning_image", "antra/assets/img/professionals/02_planification.webp"),
    "intervention": ("Intervention", "Nos équipes interviennent de manière coordonnée pour réaliser les travaux de rénovation, réparation, entretien et finition nécessaires.", "intervention_image", "antra/assets/img/professionals/03_intervention.webp"),
    "control": ("Contrôle et remise en état", "Nous vérifions les travaux réalisés afin de préparer le bien pour sa remise en location ou sa prochaine occupation.", "control_image", "antra/assets/img/professionals/04_controle_remise_en_etat.webp"),
}
ADVANTAGE_DEFAULTS = {
    "single_contact": ("Un interlocuteur unique", "Un seul point de contact simplifie le suivi de vos demandes, la coordination des interventions et les échanges tout au long du projet."),
    "coordination": ("Coordination de plusieurs corps de métier", "Nous coordonnons les différentes prestations nécessaires afin de faciliter l’organisation des travaux et d’éviter la multiplication des interlocuteurs."),
    "clear_quotes": ("Des devis clairs", "Les travaux à réaliser sont présentés de manière claire afin de faciliter votre validation, votre planification et le suivi de chaque intervention."),
    "finishes": ("Des finitions soignées", "Nous accordons une attention particulière à la qualité d’exécution et aux finitions afin de livrer des espaces propres, fonctionnels et prêts pour leur prochaine utilisation."),
    "responsiveness": ("Réactivité et organisation", "Nous organisons les interventions en fonction des priorités du bien, des contraintes du chantier et des délais disponibles."),
    "flexibility": ("Une collaboration flexible", "Intervention ponctuelle, remise en état entre locataires, entretien régulier ou rénovation plus importante : nous adaptons notre organisation aux besoins de chaque partenaire."),
}


def localized_text(obj, field, default):
    """Respeta los textos manuales por idioma y, si faltan, conserva las traducciones gettext."""
    language = (get_language() or "fr").split("-")[0]
    if language not in ("fr", "de", "it", "en"):
        language = "fr"
    value = getattr(obj, f"{field}_{language}", "")
    return value or gettext(default)


class _ProfessionalSectionBase(models.Model):
    page = models.ForeignKey("core.ProfessionalPage", on_delete=models.CASCADE)
    title_fr = models.CharField("🇫🇷 Titre", max_length=255, blank=True)
    title_de = models.CharField("🇩🇪 Titel", max_length=255, blank=True)
    title_it = models.CharField("🇮🇹 Titolo", max_length=255, blank=True)
    title_en = models.CharField("🇬🇧 Title", max_length=255, blank=True)
    title_es = models.CharField("🇪🇸 Título · referencia interna", max_length=255, blank=True)
    text_fr = models.TextField("🇫🇷 Texte", blank=True)
    text_de = models.TextField("🇩🇪 Text", blank=True)
    text_it = models.TextField("🇮🇹 Testo", blank=True)
    text_en = models.TextField("🇬🇧 Text", blank=True)
    text_es = models.TextField("🇪🇸 Texto · referencia interna", blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # IMÁGENES WebP · SOLO LAS SECCIONES QUE DISPONEN DE IMAGEFIELD
        if hasattr(self, "image"):
            from core.image_utils import optimize_instance_image_fields
            optimize_instance_image_fields(self, ("image",), max_dimension=2200, quality=82)
        super().save(*args, **kwargs)

    def _label(self, defaults):
        return self.title_fr or defaults.get(self.key, (self.key,))[0]


class ProfessionalNeed(_ProfessionalSectionBase):
    image = models.ImageField(upload_to="professionals/needs/", blank=True, null=True)
    key = models.CharField(max_length=30, choices=[(key, value[0]) for key, value in NEED_DEFAULTS.items()])

    class Meta:
        verbose_name = "02 · Besoin professionnel"
        verbose_name_plural = "02 · Besoins professionnels"
        ordering = ("order", "id")
        constraints = [models.UniqueConstraint(fields=("page", "key"), name="prof_need_page_key_unique")]

    @property
    def display_title(self):
        return localized_text(self, "title", NEED_DEFAULTS[self.key][0])

    @property
    def display_text(self):
        return localized_text(self, "text", NEED_DEFAULTS[self.key][1])

    @property
    def legacy_visual_field(self):
        return NEED_DEFAULTS[self.key][2]

    @property
    def fallback_static(self):
        return NEED_DEFAULTS[self.key][3]

    def __str__(self):
        return self._label(NEED_DEFAULTS)


class ProfessionalProcess(_ProfessionalSectionBase):
    image = models.ImageField(upload_to="professionals/process/", blank=True, null=True)
    key = models.CharField(max_length=30, choices=[(key, value[0]) for key, value in PROCESS_DEFAULTS.items()])

    class Meta:
        verbose_name = "03 · Étape d’intervention"
        verbose_name_plural = "03 · Étapes d’intervention"
        ordering = ("order", "id")
        constraints = [models.UniqueConstraint(fields=("page", "key"), name="prof_process_page_key_unique")]

    @property
    def display_title(self):
        return localized_text(self, "title", PROCESS_DEFAULTS[self.key][0])

    @property
    def display_text(self):
        return localized_text(self, "text", PROCESS_DEFAULTS[self.key][1])

    @property
    def legacy_visual_field(self):
        return PROCESS_DEFAULTS[self.key][2]

    @property
    def fallback_static(self):
        return PROCESS_DEFAULTS[self.key][3]

    def __str__(self):
        return self._label(PROCESS_DEFAULTS)


class ProfessionalAdvantage(_ProfessionalSectionBase):
    key = models.CharField(max_length=30, choices=[(key, value[0]) for key, value in ADVANTAGE_DEFAULTS.items()])

    class Meta:
        verbose_name = "04 · Pourquoi V&V"
        verbose_name_plural = "04 · Pourquoi V&V"
        ordering = ("order", "id")
        constraints = [models.UniqueConstraint(fields=("page", "key"), name="prof_advantage_page_key_unique")]

    @property
    def display_title(self):
        return localized_text(self, "title", ADVANTAGE_DEFAULTS[self.key][0])

    @property
    def display_text(self):
        return localized_text(self, "text", ADVANTAGE_DEFAULTS[self.key][1])

    def __str__(self):
        return self._label(ADVANTAGE_DEFAULTS)


class ProfessionalFeaturedProject(models.Model):
    page = models.ForeignKey("core.ProfessionalPage", on_delete=models.CASCADE, related_name="professional_project_selections")
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE, related_name="professional_placements")
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "05 · Réalisation sélectionnée"
        verbose_name_plural = "05 · Réalisations sélectionnées"
        ordering = ("order", "id")
        constraints = [models.UniqueConstraint(fields=("page", "project"), name="prof_page_project_unique")]

    def __str__(self):
        return str(self.project)


# MÓDULO V2 · TABLAS EXCLUSIVAS DE PROFESSIONALS | NEW INDEPENDENT PROFESSIONALS TABLES
# Los modelos anteriores quedan únicamente por compatibilidad con migraciones ya aplicadas.
# The historical proxy/section models above remain registered but are no longer used by the page/admin.

class ProfessionalSitePage(models.Model):
    slug = models.SlugField(max_length=40, unique=True, default="main")
    hero_title_es = models.CharField(max_length=255, blank=True)
    hero_title_fr = models.CharField(max_length=255, default="Solutions pour professionnels")
    hero_title_de = models.CharField(max_length=255, blank=True)
    hero_title_it = models.CharField(max_length=255, blank=True)
    hero_title_en = models.CharField(max_length=255, blank=True)
    hero_text_es = models.TextField(blank=True)
    hero_text_fr = models.TextField(blank=True)
    hero_text_de = models.TextField(blank=True)
    hero_text_it = models.TextField(blank=True)
    hero_text_en = models.TextField(blank=True)
    hero_image = models.ImageField(upload_to="professionals/hero/", blank=True, null=True)
    services = models.ManyToManyField("services.Service", related_name="professionals_v2_pages", blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "001 - Professionals Page"
        verbose_name_plural = "001 - Professionals Page"

    def __str__(self):
        return self.hero_title_fr or "Professionnels"

    def save(self, *args, **kwargs):
        from core.image_utils import optimize_instance_image_fields
        optimize_instance_image_fields(self, ("hero_image",), max_dimension=2200, quality=82)
        super().save(*args, **kwargs)


class ProfessionalVisualSettings(models.Model):
    page = models.OneToOneField(ProfessionalSitePage, on_delete=models.CASCADE, related_name="visual_settings")
    turnover_background = models.ImageField("Remise en état · Fondo", upload_to="professionals/visuals/turnover/", blank=True, null=True)
    faq_image = models.ImageField("Pourquoi V&V · Imagen lateral", upload_to="professionals/visuals/faq/", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "007 - Professionals Visual Configuration"
        verbose_name_plural = "007 - Professionals Visual Configuration"

    def __str__(self):
        return f"Visuels · {self.page}"

    def save(self, *args, **kwargs):
        from core.image_utils import optimize_instance_image_fields
        optimize_instance_image_fields(self, ("turnover_background", "faq_image"), max_dimension=2200, quality=82)
        super().save(*args, **kwargs)


class _ProfessionalContentBase(models.Model):
    page = models.ForeignKey(ProfessionalSitePage, on_delete=models.CASCADE)
    key = models.CharField(max_length=40)
    title_fr = models.CharField(max_length=255, blank=True)
    title_de = models.CharField(max_length=255, blank=True)
    title_it = models.CharField(max_length=255, blank=True)
    title_en = models.CharField(max_length=255, blank=True)
    title_es = models.CharField(max_length=255, blank=True)
    text_fr = models.TextField(blank=True)
    text_de = models.TextField(blank=True)
    text_it = models.TextField(blank=True)
    text_en = models.TextField(blank=True)
    text_es = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("order", "id")

    def _source(self):
        raise NotImplementedError

    @property
    def display_title(self):
        return localized_text(self, "title", self._source()[0])

    @property
    def display_text(self):
        return localized_text(self, "text", self._source()[1])

    def __str__(self):
        return self.title_fr or self._source()[0]


class ProfessionalNeedItem(_ProfessionalContentBase):
    page = models.ForeignKey(ProfessionalSitePage, on_delete=models.CASCADE, related_name="need_items")
    key = models.CharField(max_length=40, choices=[(k, v[0]) for k, v in NEED_DEFAULTS.items()])
    image = models.ImageField(upload_to="professionals/needs/", blank=True, null=True)

    class Meta:
        verbose_name = "002 - Professional Need"
        verbose_name_plural = "002 - Professional Needs"
        ordering = ("order", "id")
        constraints = [models.UniqueConstraint(fields=("page", "key"), name="profv2_need_page_key_uniq")]

    def _source(self):
        return NEED_DEFAULTS[self.key]

    @property
    def fallback_static(self):
        return NEED_DEFAULTS[self.key][3]

    def save(self, *args, **kwargs):
        from core.image_utils import optimize_instance_image_fields
        optimize_instance_image_fields(self, ("image",), max_dimension=2200, quality=82)
        super().save(*args, **kwargs)


class ProfessionalProcessItem(_ProfessionalContentBase):
    page = models.ForeignKey(ProfessionalSitePage, on_delete=models.CASCADE, related_name="process_items")
    key = models.CharField(max_length=40, choices=[(k, v[0]) for k, v in PROCESS_DEFAULTS.items()])
    image = models.ImageField(upload_to="professionals/process/", blank=True, null=True)

    class Meta:
        verbose_name = "003 - Intervention Step"
        verbose_name_plural = "003 - Intervention Steps"
        ordering = ("order", "id")
        constraints = [models.UniqueConstraint(fields=("page", "key"), name="profv2_process_page_key_uniq")]

    def _source(self):
        return PROCESS_DEFAULTS[self.key]

    @property
    def fallback_static(self):
        return PROCESS_DEFAULTS[self.key][3]

    def save(self, *args, **kwargs):
        from core.image_utils import optimize_instance_image_fields
        optimize_instance_image_fields(self, ("image",), max_dimension=2200, quality=82)
        super().save(*args, **kwargs)


class ProfessionalAdvantageItem(_ProfessionalContentBase):
    page = models.ForeignKey(ProfessionalSitePage, on_delete=models.CASCADE, related_name="advantage_items")
    key = models.CharField(max_length=40, choices=[(k, v[0]) for k, v in ADVANTAGE_DEFAULTS.items()])

    class Meta:
        verbose_name = "004 - Why V&V Argument"
        verbose_name_plural = "004 - Why V&V"
        ordering = ("order", "id")
        constraints = [models.UniqueConstraint(fields=("page", "key"), name="profv2_adv_page_key_uniq")]

    def _source(self):
        return ADVANTAGE_DEFAULTS[self.key]


class ProfessionalProjectItem(models.Model):
    page = models.ForeignKey(ProfessionalSitePage, on_delete=models.CASCADE, related_name="project_items")
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE, related_name="professionals_v2_selections")
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "005 - Selected Project"
        verbose_name_plural = "005 - Selected Projects"
        ordering = ("order", "id")
        constraints = [models.UniqueConstraint(fields=("page", "project"), name="profv2_page_project_uniq")]

    def __str__(self):
        return str(self.project)


class ProfessionalExtraBlock(models.Model):
    LAYOUT_CHOICES = (
        ("text", "Texte"), ("image_left", "Image à gauche"),
        ("image_right", "Image à droite"), ("card", "Carte"), ("cta", "Appel à l’action"),
    )
    page = models.ForeignKey(ProfessionalSitePage, on_delete=models.CASCADE, related_name="extra_blocks")
    layout = models.CharField(max_length=25, choices=LAYOUT_CHOICES, default="text")
    title_fr = models.CharField(max_length=255, blank=True)
    title_de = models.CharField(max_length=255, blank=True)
    title_it = models.CharField(max_length=255, blank=True)
    title_en = models.CharField(max_length=255, blank=True)
    title_es = models.CharField(max_length=255, blank=True)
    text_fr = models.TextField(blank=True)
    text_de = models.TextField(blank=True)
    text_it = models.TextField(blank=True)
    text_en = models.TextField(blank=True)
    text_es = models.TextField(blank=True)
    image = models.ImageField(upload_to="professionals/blocks/", blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "006 - Additional Block"
        verbose_name_plural = "006 - Additional Blocks"
        ordering = ("order", "id")

    def __str__(self):
        return self.title_fr or f"Bloc {self.pk or ''}".strip()

    def save(self, *args, **kwargs):
        from core.image_utils import optimize_instance_image_fields
        optimize_instance_image_fields(self, ("image",), max_dimension=2200, quality=82)
        super().save(*args, **kwargs)
