from django.db import models
from django.utils.text import slugify

from core.models import (
    MultilingualSEOModel,
    TimeStampedModel,
)
from services.models import Service


# ============================================================
# PROJECT TYPE
# ============================================================

class ProjectType(TimeStampedModel):

    # ========================================================
    # ESPAÑOL · REFERENCIA INTERNA
    # ========================================================

    name_es = models.CharField(
        max_length=120,
        blank=True,
    )

    # ========================================================
    # FRANÇAIS · PRINCIPAL
    # ========================================================

    name_fr = models.CharField(
        max_length=120,
    )

    # ========================================================
    # DEUTSCH
    # ========================================================

    name_de = models.CharField(
        max_length=120,
        blank=True,
    )

    # ========================================================
    # ITALIANO
    # ========================================================

    name_it = models.CharField(
        max_length=120,
        blank=True,
    )

    # ========================================================
    # ENGLISH
    # ========================================================

    name_en = models.CharField(
        max_length=120,
        blank=True,
    )

    # ========================================================
    # SETTINGS
    # ========================================================

    order = models.PositiveIntegerField(
        default=0,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = [
            "order",
            "name_fr",
        ]

        verbose_name = "Project type"
        verbose_name_plural = "Project types"

    def __str__(self):
        return self.name_fr


# ============================================================
# BUILDING TYPE
# ============================================================

class BuildingType(TimeStampedModel):

    # ========================================================
    # ESPAÑOL · REFERENCIA INTERNA
    # ========================================================

    name_es = models.CharField(
        max_length=120,
        blank=True,
    )

    # ========================================================
    # FRANÇAIS · PRINCIPAL
    # ========================================================

    name_fr = models.CharField(
        max_length=120,
    )

    # ========================================================
    # DEUTSCH
    # ========================================================

    name_de = models.CharField(
        max_length=120,
        blank=True,
    )

    # ========================================================
    # ITALIANO
    # ========================================================

    name_it = models.CharField(
        max_length=120,
        blank=True,
    )

    # ========================================================
    # ENGLISH
    # ========================================================

    name_en = models.CharField(
        max_length=120,
        blank=True,
    )

    # ========================================================
    # SETTINGS
    # ========================================================

    order = models.PositiveIntegerField(
        default=0,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = [
            "order",
            "name_fr",
        ]

        verbose_name = "Building type"
        verbose_name_plural = "Building types"

    def __str__(self):
        return self.name_fr


# ============================================================
# PROJECT
# ============================================================

class Project(
    MultilingualSEOModel,
    TimeStampedModel,
):

    # ========================================================
    # TITLE
    # ESPAÑOL · REFERENCIA INTERNA
    # ========================================================

    title_es = models.CharField(
        max_length=200,
        blank=True,
    )

    # ========================================================
    # TITLE · PUBLIC LANGUAGES
    # ========================================================

    title_fr = models.CharField(
        max_length=200,
    )

    title_de = models.CharField(
        max_length=200,
        blank=True,
    )

    title_it = models.CharField(
        max_length=200,
        blank=True,
    )

    title_en = models.CharField(
        max_length=200,
        blank=True,
    )

    # ========================================================
    # SLUGS
    #
    # IMPORTANTE:
    # No existe slug_es porque el español no es público.
    # ========================================================

    slug_fr = models.SlugField(
        max_length=220,
        unique=True,
    )

    slug_de = models.SlugField(
        max_length=220,
        blank=True,
        null=True,
        unique=True,
    )

    slug_it = models.SlugField(
        max_length=220,
        blank=True,
        null=True,
        unique=True,
    )

    slug_en = models.SlugField(
        max_length=220,
        blank=True,
        null=True,
        unique=True,
    )

    # ========================================================
    # CLASSIFICATION
    # ========================================================

    project_type = models.ForeignKey(
        ProjectType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects",
    )

    building_type = models.ForeignKey(
        BuildingType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects",
    )

    # ========================================================
    # RELATED SERVICES
    # ========================================================

    services = models.ManyToManyField(
        Service,
        related_name="projects",
        blank=True,
    )

    # ========================================================
    # PROJECT INFORMATION
    # ========================================================

    location = models.CharField(
        max_length=160,
        blank=True,
    )

    client = models.CharField(
        max_length=160,
        blank=True,
    )

    start_date = models.DateField(
        blank=True,
        null=True,
    )

    end_date = models.DateField(
        blank=True,
        null=True,
    )

    # ========================================================
    # SUMMARY
    # ESPAÑOL · REFERENCIA INTERNA
    # ========================================================

    summary_es = models.TextField(
        blank=True,
    )

    # ========================================================
    # SUMMARY · PUBLIC LANGUAGES
    # ========================================================

    summary_fr = models.TextField(
        blank=True,
    )

    summary_de = models.TextField(
        blank=True,
    )

    summary_it = models.TextField(
        blank=True,
    )

    summary_en = models.TextField(
        blank=True,
    )

    # ========================================================
    # CONTENT
    # ESPAÑOL · REFERENCIA INTERNA
    # ========================================================

    content_es = models.TextField(
        blank=True,
    )

    # ========================================================
    # CONTENT · PUBLIC LANGUAGES
    # ========================================================

    content_fr = models.TextField()

    content_de = models.TextField(
        blank=True,
    )

    content_it = models.TextField(
        blank=True,
    )

    content_en = models.TextField(
        blank=True,
    )

    # ========================================================
    # MAIN IMAGE
    # ========================================================

    main_image = models.ImageField(
        upload_to="projects/main/",
        blank=True,
        null=True,
    )

    # ========================================================
    # PUBLICATION
    # ========================================================

    is_featured = models.BooleanField(
        default=False,
    )

    is_published = models.BooleanField(
        default=True,
    )

    class Meta:

        ordering = [
            "-end_date",
            "-created_at",
        ]

        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title_fr

    # ========================================================
    # SAVE
    # ========================================================

    def save(self, *args, **kwargs):

        # ====================================================
        # FRANÇAIS
        # ====================================================

        if not self.slug_fr:

            self.slug_fr = slugify(
                self.title_fr
            )

        # ====================================================
        # DEUTSCH
        # ====================================================

        if self.title_de and not self.slug_de:

            self.slug_de = slugify(
                self.title_de
            )

        if not self.title_de:
            self.slug_de = None

        # ====================================================
        # ITALIANO
        # ====================================================

        if self.title_it and not self.slug_it:

            self.slug_it = slugify(
                self.title_it
            )

        if not self.title_it:
            self.slug_it = None

        # ====================================================
        # ENGLISH
        # ====================================================

        if self.title_en and not self.slug_en:

            self.slug_en = slugify(
                self.title_en
            )

        if not self.title_en:
            self.slug_en = None

        super().save(
            *args,
            **kwargs,
        )


# ============================================================
# PROJECT IMAGE
# ============================================================

class ProjectImage(TimeStampedModel):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = models.ImageField(
        upload_to="projects/gallery/",
    )

    # ========================================================
    # ESPAÑOL · REFERENCIA INTERNA
    # ========================================================

    alt_es = models.CharField(
        max_length=180,
        blank=True,
    )

    # ========================================================
    # PUBLIC LANGUAGES
    # ========================================================

    alt_fr = models.CharField(
        max_length=180,
        blank=True,
    )

    alt_de = models.CharField(
        max_length=180,
        blank=True,
    )

    alt_it = models.CharField(
        max_length=180,
        blank=True,
    )

    alt_en = models.CharField(
        max_length=180,
        blank=True,
    )

    order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:

        ordering = [
            "order",
        ]

        verbose_name = "Project image"
        verbose_name_plural = "Project images"

    def __str__(self):
        return f"Image - {self.project}"


# ============================================================
# BEFORE / AFTER
# ============================================================

class BeforeAfter(TimeStampedModel):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="before_after",
    )

    before_image = models.ImageField(
        upload_to="projects/before-after/",
    )

    after_image = models.ImageField(
        upload_to="projects/before-after/",
    )

    # ========================================================
    # ESPAÑOL · REFERENCIA INTERNA
    # ========================================================

    title_es = models.CharField(
        max_length=160,
        blank=True,
    )

    # ========================================================
    # PUBLIC LANGUAGES
    # ========================================================

    title_fr = models.CharField(
        max_length=160,
        blank=True,
    )

    title_de = models.CharField(
        max_length=160,
        blank=True,
    )

    title_it = models.CharField(
        max_length=160,
        blank=True,
    )

    title_en = models.CharField(
        max_length=160,
        blank=True,
    )

    order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:

        ordering = [
            "order",
        ]

        verbose_name = "Before and after"
        verbose_name_plural = "Before and after"

    def __str__(self):

        return (
            self.title_fr
            or self.title_es
            or f"Before / After - {self.project}"
        )


# ============================================================
# INTERVENTION
# ============================================================

class Intervention(TimeStampedModel):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="interventions",
    )

    # ========================================================
    # TITLE · ESPAÑOL · REFERENCIA INTERNA
    # ========================================================

    title_es = models.CharField(
        max_length=160,
        blank=True,
    )

    # ========================================================
    # TITLE · PUBLIC LANGUAGES
    # ========================================================

    title_fr = models.CharField(
        max_length=160,
    )

    title_de = models.CharField(
        max_length=160,
        blank=True,
    )

    title_it = models.CharField(
        max_length=160,
        blank=True,
    )

    title_en = models.CharField(
        max_length=160,
        blank=True,
    )

    # ========================================================
    # DESCRIPTION · ESPAÑOL · REFERENCIA INTERNA
    # ========================================================

    description_es = models.TextField(
        blank=True,
    )

    # ========================================================
    # DESCRIPTION · PUBLIC LANGUAGES
    # ========================================================

    description_fr = models.TextField(
        blank=True,
    )

    description_de = models.TextField(
        blank=True,
    )

    description_it = models.TextField(
        blank=True,
    )

    description_en = models.TextField(
        blank=True,
    )

    order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:

        ordering = [
            "order",
        ]

        verbose_name = "Intervention"
        verbose_name_plural = "Interventions"

    def __str__(self):
        return self.title_fr or self.title_es