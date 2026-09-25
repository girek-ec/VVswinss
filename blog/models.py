from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from core.models import MultilingualSEOModel, TimeStampedModel


class BlogCategory(TimeStampedModel):
    nombre_fr = models.CharField(max_length=120)
    nombre_es = models.CharField(max_length=120, blank=True)
    nombre_en = models.CharField(max_length=120, blank=True)

    slug_fr = models.SlugField(max_length=140, unique=True)
    slug_es = models.SlugField(
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

    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre_fr"]
        verbose_name = "Categoría del blog"
        verbose_name_plural = "Categorías del blog"

    def __str__(self):
        return self.nombre_fr

    def save(self, *args, **kwargs):
        if not self.slug_fr:
            self.slug_fr = slugify(self.nombre_fr)

        if self.nombre_es and not self.slug_es:
            self.slug_es = slugify(self.nombre_es)

        if self.nombre_en and not self.slug_en:
            self.slug_en = slugify(self.nombre_en)

        super().save(*args, **kwargs)


class Post(MultilingualSEOModel, TimeStampedModel):
    categoria = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )

    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vvswinss_posts",
    )

    titulo_fr = models.CharField(max_length=220)
    titulo_es = models.CharField(max_length=220, blank=True)
    titulo_en = models.CharField(max_length=220, blank=True)

    slug_fr = models.SlugField(max_length=240, unique=True)
    slug_es = models.SlugField(
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

    extracto_fr = models.TextField(blank=True)
    extracto_es = models.TextField(blank=True)
    extracto_en = models.TextField(blank=True)

    contenido_fr = models.TextField()
    contenido_es = models.TextField(blank=True)
    contenido_en = models.TextField(blank=True)

    imagen_principal = models.ImageField(
        upload_to="blog/",
        blank=True,
        null=True,
    )

    fecha_publicacion = models.DateTimeField(default=timezone.now)

    publicado = models.BooleanField(default=False)
    destacado = models.BooleanField(default=False)

    class Meta:
        ordering = ["-fecha_publicacion"]
        verbose_name = "Publicación"
        verbose_name_plural = "Publicaciones"

    def __str__(self):
        return self.titulo_fr

    def save(self, *args, **kwargs):
        if not self.slug_fr:
            self.slug_fr = slugify(self.titulo_fr)

        if self.titulo_es and not self.slug_es:
            self.slug_es = slugify(self.titulo_es)

        if self.titulo_en and not self.slug_en:
            self.slug_en = slugify(self.titulo_en)

        super().save(*args, **kwargs)