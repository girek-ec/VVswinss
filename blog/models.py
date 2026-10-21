from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from core.models import MultilingualSEOModel, TimeStampedModel


class BlogCategory(TimeStampedModel):
    name_fr = models.CharField(max_length=120)
    name_de = models.CharField(max_length=120, blank=True)
    name_it = models.CharField(max_length=120, blank=True)
    name_en = models.CharField(max_length=120, blank=True)

    slug_fr = models.SlugField(
        max_length=140,
        unique=True,
    )
    slug_de = models.SlugField(
        max_length=140,
        blank=True,
        null=True,
        unique=True,
    )
    slug_it = models.SlugField(
        max_length=140,
        blank=True,
        null=True,
        unique=True,
    )
    slug_en = models.SlugField(
        max_length=140,
        blank=True,
        null=True,
        unique=True,
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name_fr"]
        verbose_name = "Blog category"
        verbose_name_plural = "Blog categories"

    def __str__(self):
        return self.name_fr

    def save(self, *args, **kwargs):
        if not self.slug_fr:
            self.slug_fr = slugify(self.name_fr)

        if self.name_de and not self.slug_de:
            self.slug_de = slugify(self.name_de)

        if self.name_it and not self.slug_it:
            self.slug_it = slugify(self.name_it)

        if self.name_en and not self.slug_en:
            self.slug_en = slugify(self.name_en)

        super().save(*args, **kwargs)

class BlogTag(models.Model):
    name_fr = models.CharField("Nom FR", max_length=80)
    slug_fr = models.SlugField("Slug FR", max_length=100, unique=True, blank=True)

    name_de = models.CharField("Name DE", max_length=80, blank=True)
    slug_de = models.SlugField("Slug DE", max_length=100, unique=True, blank=True, null=True)

    name_it = models.CharField("Nome IT", max_length=80, blank=True)
    slug_it = models.SlugField("Slug IT", max_length=100, unique=True, blank=True, null=True)

    name_en = models.CharField("Name EN", max_length=80, blank=True)
    slug_en = models.SlugField("Slug EN", max_length=100, unique=True, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name_fr",)
        verbose_name = "BLOG · 02 Tag"
        verbose_name_plural = "BLOG · 02 Tags"

    def __str__(self):
        return self.name_fr

class Post(
    MultilingualSEOModel,
    TimeStampedModel,
):
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vvswinss_posts",
    )

    title_fr = models.CharField(max_length=220)
    title_de = models.CharField(max_length=220, blank=True)
    title_it = models.CharField(max_length=220, blank=True)
    title_en = models.CharField(max_length=220, blank=True)

    slug_fr = models.SlugField(
        max_length=240,
        unique=True,
    )
    slug_de = models.SlugField(
        max_length=240,
        blank=True,
        null=True,
        unique=True,
    )
    slug_it = models.SlugField(
        max_length=240,
        blank=True,
        null=True,
        unique=True,
    )
    slug_en = models.SlugField(
        max_length=240,
        blank=True,
        null=True,
        unique=True,
    )
    tags = models.ManyToManyField(BlogTag, blank=True, related_name="posts")
    excerpt_fr = models.TextField(blank=True)
    excerpt_de = models.TextField(blank=True)
    excerpt_it = models.TextField(blank=True)
    excerpt_en = models.TextField(blank=True)

    content_fr = models.TextField()
    content_de = models.TextField(blank=True)
    content_it = models.TextField(blank=True)
    content_en = models.TextField(blank=True)

    main_image = models.ImageField(
        upload_to="blog/",
        blank=True,
        null=True,
    )

    published_at = models.DateTimeField(
        default=timezone.now,
    )

    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-published_at"]
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title_fr

    def save(self, *args, **kwargs):
        if not self.slug_fr:
            self.slug_fr = slugify(self.title_fr)

        if self.title_de and not self.slug_de:
            self.slug_de = slugify(self.title_de)

        if self.title_it and not self.slug_it:
            self.slug_it = slugify(self.title_it)

        if self.title_en and not self.slug_en:
            self.slug_en = slugify(self.title_en)

        super().save(*args, **kwargs)



class PostSection(models.Model):
    SECTION_TEXT = "text"
    SECTION_IMAGE = "image"
    SECTION_IMAGE_PAIR = "image_pair"
    SECTION_QUOTE = "quote"
    SECTION_TEXT_IMAGE = "text_image"

    SECTION_TYPES = [
        (SECTION_TEXT, "Texte"),
        (SECTION_IMAGE, "Image"),
        (SECTION_IMAGE_PAIR, "Deux images"),
        (SECTION_QUOTE, "Citation"),
        (SECTION_TEXT_IMAGE, "Texte + image"),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="sections")
    order = models.PositiveIntegerField(default=0)
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES, default=SECTION_TEXT)
    is_active = models.BooleanField(default=True)

    # ============================================================
    # FRANÇAIS · PRINCIPAL
    # ============================================================

    title_fr = models.CharField("Titre FR", max_length=220, blank=True)
    content_fr = models.TextField("Contenu FR", blank=True)

    # ============================================================
    # DEUTSCH
    # ============================================================

    title_de = models.CharField("Titel DE", max_length=220, blank=True)
    content_de = models.TextField("Inhalt DE", blank=True)

    # ============================================================
    # ITALIANO
    # ============================================================

    title_it = models.CharField("Titolo IT", max_length=220, blank=True)
    content_it = models.TextField("Contenuto IT", blank=True)

    # ============================================================
    # ENGLISH
    # ============================================================

    title_en = models.CharField("Title EN", max_length=220, blank=True)
    content_en = models.TextField("Content EN", blank=True)

    # ============================================================
    # IMAGES
    # ============================================================

    image_1 = models.ImageField(upload_to="blog/sections/", blank=True)
    image_2 = models.ImageField(upload_to="blog/sections/", blank=True)

    image_1_alt_fr = models.CharField("Alt image 1 FR", max_length=180, blank=True)
    image_1_alt_de = models.CharField("Alt image 1 DE", max_length=180, blank=True)
    image_1_alt_it = models.CharField("Alt image 1 IT", max_length=180, blank=True)
    image_1_alt_en = models.CharField("Alt image 1 EN", max_length=180, blank=True)

    image_2_alt_fr = models.CharField("Alt image 2 FR", max_length=180, blank=True)
    image_2_alt_de = models.CharField("Alt image 2 DE", max_length=180, blank=True)
    image_2_alt_it = models.CharField("Alt image 2 IT", max_length=180, blank=True)
    image_2_alt_en = models.CharField("Alt image 2 EN", max_length=180, blank=True)

    # ============================================================
    # QUOTE
    # ============================================================

    quote_fr = models.TextField("Citation FR", blank=True)
    quote_de = models.TextField("Zitat DE", blank=True)
    quote_it = models.TextField("Citazione IT", blank=True)
    quote_en = models.TextField("Quote EN", blank=True)

    quote_author = models.CharField("Auteur de la citation", max_length=120, blank=True)
    quote_icon = models.ImageField(upload_to="blog/quotes/", blank=True)

    class Meta:
        ordering = ("order", "id")
        verbose_name = "BLOG · 04 Section d’article"
        verbose_name_plural = "BLOG · 04 Sections d’article"

    def __str__(self):
        return f"{self.post.title_fr} · {self.order}"