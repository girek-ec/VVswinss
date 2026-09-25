from django.db import models

# Create your models here.
from django.db import models
from django.utils.text import slugify

from core.models import MultilingualSEOModel, TimeStampedModel


class ServiceCategory(TimeStampedModel):
    nombre_fr = models.CharField(max_length=150)
    nombre_es = models.CharField(max_length=150, blank=True)
    nombre_en = models.CharField(max_length=150, blank=True)

    slug_fr = models.SlugField(max_length=170, unique=True)
    slug_es = models.SlugField(max_length=170, blank=True, null=True, unique=True)
    slug_en = models.SlugField(max_length=170, blank=True, null=True, unique=True)

    descripcion_fr = models.TextField(blank=True)
    descripcion_es = models.TextField(blank=True)
    descripcion_en = models.TextField(blank=True)

    imagen = models.ImageField(
        upload_to="services/categories/",
        blank=True,
        null=True,
    )

    icono = models.CharField(max_length=100, blank=True)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["orden", "nombre_fr"]
        verbose_name = "Categoría de servicio"
        verbose_name_plural = "Categorías de servicios"

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


class Service(
    MultilingualSEOModel,
    TimeStampedModel,
):
    categoria = models.ForeignKey(
        ServiceCategory,
        on_delete=models.PROTECT,
        related_name="servicios",
    )

    nombre_fr = models.CharField(max_length=180)
    nombre_es = models.CharField(max_length=180, blank=True)
    nombre_en = models.CharField(max_length=180, blank=True)

    slug_fr = models.SlugField(max_length=200, unique=True)
    slug_es = models.SlugField(max_length=200, blank=True, null=True, unique=True)
    slug_en = models.SlugField(max_length=200, blank=True, null=True, unique=True)

    resumen_fr = models.TextField(blank=True)
    resumen_es = models.TextField(blank=True)
    resumen_en = models.TextField(blank=True)

    contenido_fr = models.TextField()
    contenido_es = models.TextField(blank=True)
    contenido_en = models.TextField(blank=True)

    imagen_principal = models.ImageField(
        upload_to="services/main/",
        blank=True,
        null=True,
    )

    icono = models.CharField(max_length=100, blank=True)

    destacado = models.BooleanField(default=False)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["orden", "nombre_fr"]

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


class ServiceBenefit(TimeStampedModel):
    servicio = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="beneficios",
    )

    titulo_fr = models.CharField(max_length=160)
    titulo_es = models.CharField(max_length=160, blank=True)
    titulo_en = models.CharField(max_length=160, blank=True)

    descripcion_fr = models.TextField(blank=True)
    descripcion_es = models.TextField(blank=True)
    descripcion_en = models.TextField(blank=True)

    icono = models.CharField(max_length=100, blank=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden"]

    def __str__(self):
        return self.titulo_fr


class ServiceImage(TimeStampedModel):
    servicio = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="imagenes",
    )

    imagen = models.ImageField(upload_to="services/gallery/")

    alt_fr = models.CharField(max_length=180, blank=True)
    alt_es = models.CharField(max_length=180, blank=True)
    alt_en = models.CharField(max_length=180, blank=True)

    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden"]

    def __str__(self):
        return f"Imagen - {self.servicio}"