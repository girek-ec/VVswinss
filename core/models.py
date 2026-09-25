from django.db import models

# Create your models here.
from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MultilingualSEOModel(models.Model):
    seo_titulo_fr = models.CharField(max_length=160, blank=True)
    seo_titulo_es = models.CharField(max_length=160, blank=True)
    seo_titulo_en = models.CharField(max_length=160, blank=True)

    meta_descripcion_fr = models.CharField(max_length=320, blank=True)
    meta_descripcion_es = models.CharField(max_length=320, blank=True)
    meta_descripcion_en = models.CharField(max_length=320, blank=True)

    og_imagen = models.ImageField(upload_to="seo/", blank=True, null=True)
    indexar = models.BooleanField(default=True)

    class Meta:
        abstract = True


class SiteConfiguration(TimeStampedModel):
    nombre_empresa = models.CharField(max_length=150)

    slogan_fr = models.CharField(max_length=255, blank=True)
    slogan_es = models.CharField(max_length=255, blank=True)
    slogan_en = models.CharField(max_length=255, blank=True)

    logo = models.ImageField(upload_to="site/")
    logo_blanco = models.ImageField(upload_to="site/", blank=True, null=True)
    favicon = models.ImageField(upload_to="site/", blank=True, null=True)

    telefono = models.CharField(max_length=50, blank=True)
    whatsapp = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)

    direccion = models.CharField(max_length=255, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    canton = models.CharField(max_length=100, blank=True)
    pais = models.CharField(max_length=100, default="Suisse")

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
    )

    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Configuración del sitio"
        verbose_name_plural = "Configuración del sitio"

    def __str__(self):
        return self.nombre_empresa


class SocialLink(TimeStampedModel):
    nombre = models.CharField(max_length=50)
    url = models.URLField()
    icono = models.CharField(
        max_length=100,
        blank=True,
        help_text="Clase CSS del icono, por ejemplo bi bi-facebook",
    )
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["orden", "nombre"]
        verbose_name = "Red social"
        verbose_name_plural = "Redes sociales"

    def __str__(self):
        return self.nombre


class BusinessHour(TimeStampedModel):
    dia_fr = models.CharField(max_length=30)
    dia_es = models.CharField(max_length=30, blank=True)
    dia_en = models.CharField(max_length=30, blank=True)

    horario = models.CharField(max_length=100)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["orden"]
        verbose_name = "Horario"
        verbose_name_plural = "Horarios"

    def __str__(self):
        return f"{self.dia_fr}: {self.horario}"


class ServiceArea(TimeStampedModel):
    nombre = models.CharField(max_length=120)
    canton = models.CharField(max_length=120, blank=True)
    descripcion = models.CharField(max_length=255, blank=True)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["orden", "nombre"]
        verbose_name = "Zona de servicio"
        verbose_name_plural = "Zonas de servicio"

    def __str__(self):
        return self.nombre


class ProcessStep(TimeStampedModel):
    numero = models.PositiveIntegerField()

    titulo_fr = models.CharField(max_length=150)
    titulo_es = models.CharField(max_length=150, blank=True)
    titulo_en = models.CharField(max_length=150, blank=True)

    descripcion_fr = models.TextField()
    descripcion_es = models.TextField(blank=True)
    descripcion_en = models.TextField(blank=True)

    icono = models.CharField(max_length=100, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["numero"]
        verbose_name = "Etapa del proceso"
        verbose_name_plural = "Etapas del proceso"

    def __str__(self):
        return f"{self.numero}. {self.titulo_fr}"


class TeamMember(TimeStampedModel):
    nombre = models.CharField(max_length=150)

    cargo_fr = models.CharField(max_length=150)
    cargo_es = models.CharField(max_length=150, blank=True)
    cargo_en = models.CharField(max_length=150, blank=True)

    biografia_fr = models.TextField(blank=True)
    biografia_es = models.TextField(blank=True)
    biografia_en = models.TextField(blank=True)

    foto = models.ImageField(upload_to="team/", blank=True, null=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=50, blank=True)

    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["orden", "nombre"]
        verbose_name = "Miembro del equipo"
        verbose_name_plural = "Equipo"

    def __str__(self):
        return self.nombre


class Certification(TimeStampedModel):
    nombre = models.CharField(max_length=150)
    entidad = models.CharField(max_length=150, blank=True)
    imagen = models.ImageField(upload_to="certifications/", blank=True, null=True)
    url = models.URLField(blank=True)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["orden", "nombre"]

    def __str__(self):
        return self.nombre


class Statistic(TimeStampedModel):
    valor = models.CharField(max_length=30)

    titulo_fr = models.CharField(max_length=100)
    titulo_es = models.CharField(max_length=100, blank=True)
    titulo_en = models.CharField(max_length=100, blank=True)

    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["orden"]

    def __str__(self):
        return f"{self.valor} - {self.titulo_fr}"


class Testimonial(TimeStampedModel):
    nombre = models.CharField(max_length=150)
    empresa = models.CharField(max_length=150, blank=True)

    texto_fr = models.TextField()
    texto_es = models.TextField(blank=True)
    texto_en = models.TextField(blank=True)

    foto = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    valoracion = models.PositiveSmallIntegerField(default=5)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden", "-created_at"]

    def __str__(self):
        return self.nombre


class FAQCategory(TimeStampedModel):
    nombre_fr = models.CharField(max_length=120)
    nombre_es = models.CharField(max_length=120, blank=True)
    nombre_en = models.CharField(max_length=120, blank=True)

    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["orden", "nombre_fr"]
        verbose_name = "Categoría FAQ"
        verbose_name_plural = "Categorías FAQ"

    def __str__(self):
        return self.nombre_fr


class FAQ(TimeStampedModel):
    categoria = models.ForeignKey(
        FAQCategory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="preguntas",
    )

    pregunta_fr = models.CharField(max_length=255)
    pregunta_es = models.CharField(max_length=255, blank=True)
    pregunta_en = models.CharField(max_length=255, blank=True)

    respuesta_fr = models.TextField()
    respuesta_es = models.TextField(blank=True)
    respuesta_en = models.TextField(blank=True)

    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["orden", "pregunta_fr"]
        verbose_name = "Pregunta frecuente"
        verbose_name_plural = "Preguntas frecuentes"

    def __str__(self):
        return self.pregunta_fr


class InstitutionalPage(
    MultilingualSEOModel,
    TimeStampedModel,
):
    titulo_fr = models.CharField(max_length=160)
    titulo_es = models.CharField(max_length=160, blank=True)
    titulo_en = models.CharField(max_length=160, blank=True)

    slug_fr = models.SlugField(max_length=180, unique=True)
    slug_es = models.SlugField(max_length=180, blank=True, null=True, unique=True)
    slug_en = models.SlugField(max_length=180, blank=True, null=True, unique=True)

    contenido_fr = models.TextField()
    contenido_es = models.TextField(blank=True)
    contenido_en = models.TextField(blank=True)

    imagen = models.ImageField(upload_to="pages/", blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Página institucional"
        verbose_name_plural = "Páginas institucionales"

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


class HomeContent(TimeStampedModel):
    titulo_fr = models.CharField(max_length=200)
    titulo_es = models.CharField(max_length=200, blank=True)
    titulo_en = models.CharField(max_length=200, blank=True)

    subtitulo_fr = models.TextField(blank=True)
    subtitulo_es = models.TextField(blank=True)
    subtitulo_en = models.TextField(blank=True)

    imagen_hero = models.ImageField(upload_to="home/", blank=True, null=True)
    video_url = models.URLField(blank=True)

    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Contenido de inicio"
        verbose_name_plural = "Contenido de inicio"

    def __str__(self):
        return self.titulo_fr