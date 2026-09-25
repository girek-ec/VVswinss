from django.db import models

# Create your models here.
from django.db import models
from django.utils.text import slugify

from core.models import MultilingualSEOModel, TimeStampedModel
from services.models import Service


class ProjectType(TimeStampedModel):
    nombre_fr = models.CharField(max_length=120)
    nombre_es = models.CharField(max_length=120, blank=True)
    nombre_en = models.CharField(max_length=120, blank=True)

    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["orden", "nombre_fr"]

    def __str__(self):
        return self.nombre_fr


class BuildingType(TimeStampedModel):
    nombre_fr = models.CharField(max_length=120)
    nombre_es = models.CharField(max_length=120, blank=True)
    nombre_en = models.CharField(max_length=120, blank=True)

    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["orden", "nombre_fr"]

    def __str__(self):
        return self.nombre_fr


class Project(
    MultilingualSEOModel,
    TimeStampedModel,
):
    titulo_fr = models.CharField(max_length=200)
    titulo_es = models.CharField(max_length=200, blank=True)
    titulo_en = models.CharField(max_length=200, blank=True)

    slug_fr = models.SlugField(max_length=220, unique=True)
    slug_es = models.SlugField(max_length=220, blank=True, null=True, unique=True)
    slug_en = models.SlugField(max_length=220, blank=True, null=True, unique=True)

    tipo = models.ForeignKey(
        ProjectType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="proyectos",
    )

    tipo_edificio = models.ForeignKey(
        BuildingType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="proyectos",
    )

    servicios = models.ManyToManyField(
        Service,
        related_name="proyectos",
        blank=True,
    )

    ubicacion = models.CharField(max_length=160, blank=True)
    cliente = models.CharField(max_length=160, blank=True)

    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)

    resumen_fr = models.TextField(blank=True)
    resumen_es = models.TextField(blank=True)
    resumen_en = models.TextField(blank=True)

    contenido_fr = models.TextField()
    contenido_es = models.TextField(blank=True)
    contenido_en = models.TextField(blank=True)

    imagen_principal = models.ImageField(
        upload_to="projects/main/",
        blank=True,
        null=True,
    )

    destacado = models.BooleanField(default=False)
    publicado = models.BooleanField(default=True)

    class Meta:
        ordering = ["-fecha_fin", "-created_at"]

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


class ProjectImage(TimeStampedModel):
    proyecto = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="imagenes",
    )

    imagen = models.ImageField(upload_to="projects/gallery/")

    alt_fr = models.CharField(max_length=180, blank=True)
    alt_es = models.CharField(max_length=180, blank=True)
    alt_en = models.CharField(max_length=180, blank=True)

    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden"]

    def __str__(self):
        return f"Imagen - {self.proyecto}"


class BeforeAfter(TimeStampedModel):
    proyecto = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="antes_despues",
    )

    imagen_antes = models.ImageField(upload_to="projects/before-after/")
    imagen_despues = models.ImageField(upload_to="projects/before-after/")

    titulo_fr = models.CharField(max_length=160, blank=True)
    titulo_es = models.CharField(max_length=160, blank=True)
    titulo_en = models.CharField(max_length=160, blank=True)

    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden"]

    def __str__(self):
        return f"Antes / Después - {self.proyecto}"


class Intervention(TimeStampedModel):
    proyecto = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="intervenciones",
    )

    titulo_fr = models.CharField(max_length=160)
    titulo_es = models.CharField(max_length=160, blank=True)
    titulo_en = models.CharField(max_length=160, blank=True)

    descripcion_fr = models.TextField(blank=True)
    descripcion_es = models.TextField(blank=True)
    descripcion_en = models.TextField(blank=True)

    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden"]

    def __str__(self):
        return self.titulo_fr