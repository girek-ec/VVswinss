from django.db import models


class BlogPageConfiguration(models.Model):
    header_background = models.ImageField(
        "Fondo del encabezado",
        upload_to="blog/page/",
        blank=True,
        null=True,
        help_text="Imagen panorámica utilizada en el encabezado principal del Blog.",
    )
    post_default_image = models.ImageField(
        "Imagen por defecto de artículos",
        upload_to="blog/page/",
        blank=True,
        null=True,
        help_text="Se utiliza cuando una publicación no tiene imagen principal propia.",
    )
    post_default_social_image = models.ImageField(
        "Imagen social por defecto",
        upload_to="seo/defaults/blog/",
        blank=True,
        null=True,
        editable=False,
        help_text="Se genera automáticamente en JPEG 1200 × 630 desde la imagen por defecto.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '001 - Blog Visual Configuration'
        verbose_name_plural = '001 - Blog Visual Configuration'

    def __str__(self):
        return "Configuración visual · News & Advice"
