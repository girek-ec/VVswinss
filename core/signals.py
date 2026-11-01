import logging
from functools import partial

from django.apps import apps
from django.db import models, transaction
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


# ============================================================
# LIMPIEZA AUTOMÁTICA DE IMÁGENES EN /media/
# ============================================================
#
# Comportamiento:
# - Si se reemplaza una imagen, elimina el archivo anterior.
# - Si se usa "Limpiar" en Django Admin, elimina el archivo anterior.
# - Si se elimina un registro, elimina sus ImageField asociados.
# - La eliminación física se ejecuta después del COMMIT.
# - Antes de borrar, comprueba que ningún otro ImageField siga
#   haciendo referencia al mismo nombre de archivo.
#
# Este sistema actúa únicamente sobre ImageField. No toca /static/
# ni elimina PDF u otros FileField.
# ============================================================


def _get_image_fields(model):
    """Devuelve los ImageField concretos de un modelo."""
    return [
        field
        for field in model._meta.concrete_fields
        if isinstance(field, models.ImageField)
    ]


def _image_is_referenced(name):
    """
    Comprueba si algún ImageField de algún modelo sigue apuntando
    al mismo archivo. Es una protección adicional antes de borrar.
    """
    if not name:
        return False

    for model in apps.get_models():
        for field in _get_image_fields(model):
            try:
                if model._default_manager.filter(
                    **{field.name: name}
                ).exists():
                    return True
            except Exception:
                # Algunos modelos/managers especiales podrían no permitir
                # la consulta durante ciertas operaciones. En ese caso,
                # preferimos no bloquear la limpieza global.
                continue

    return False


def _delete_image_if_unreferenced(storage, name):
    """
    Elimina físicamente un archivo únicamente si ya no está
    referenciado por ningún ImageField.
    """
    if not name:
        return

    try:
        if _image_is_referenced(name):
            return

        if storage.exists(name):
            storage.delete(name)

    except Exception:
        logger.exception(
            "No se pudo eliminar la imagen huérfana de media: %s",
            name,
        )


@receiver(
    pre_save,
    dispatch_uid="vvs_capture_replaced_image_files",
)
def capture_replaced_image_files(sender, instance, **kwargs):
    """
    Antes de guardar, identifica imágenes anteriores que serán:
    - reemplazadas por una nueva,
    - o limpiadas desde el Admin.

    No elimina nada todavía.
    """
    image_fields = _get_image_fields(sender)

    if not image_fields:
        return

    if not getattr(instance, "pk", None):
        return

    try:
        previous_instance = sender._default_manager.filter(
            pk=instance.pk
        ).first()
    except Exception:
        return

    if previous_instance is None:
        return

    pending = []

    for field in image_fields:
        old_file = getattr(previous_instance, field.name, None)
        new_file = getattr(instance, field.name, None)

        old_name = getattr(old_file, "name", "") if old_file else ""
        new_name = getattr(new_file, "name", "") if new_file else ""

        if not old_name:
            continue

        new_is_uncommitted = bool(
            new_file
            and not getattr(new_file, "_committed", True)
        )

        was_cleared = not new_name
        was_replaced = (
            new_is_uncommitted
            or new_name != old_name
        )

        if was_cleared or was_replaced:
            pending.append(
                (
                    old_file.storage,
                    old_name,
                )
            )

    instance._vvs_old_images_to_delete = pending


@receiver(
    post_save,
    dispatch_uid="vvs_delete_replaced_image_files",
)
def delete_replaced_image_files(sender, instance, **kwargs):
    """
    Después de guardar correctamente, programa la eliminación
    del archivo anterior al finalizar la transacción.
    """
    pending = getattr(
        instance,
        "_vvs_old_images_to_delete",
        [],
    )

    if not pending:
        return

    # Limpiamos el atributo para evitar reutilizaciones accidentales.
    instance._vvs_old_images_to_delete = []

    # Evita programar dos veces el mismo archivo.
    seen_names = set()

    for storage, name in pending:
        if not name or name in seen_names:
            continue

        seen_names.add(name)

        transaction.on_commit(
            partial(
                _delete_image_if_unreferenced,
                storage,
                name,
            )
        )


@receiver(
    post_delete,
    dispatch_uid="vvs_delete_images_when_instance_deleted",
)
def delete_images_when_instance_deleted(sender, instance, **kwargs):
    """
    Al eliminar un registro, elimina después del COMMIT todos sus
    archivos ImageField que ya no estén referenciados.
    """
    image_fields = _get_image_fields(sender)

    if not image_fields:
        return

    seen_names = set()

    for field in image_fields:
        image = getattr(instance, field.name, None)

        if not image:
            continue

        name = getattr(image, "name", "")

        if not name or name in seen_names:
            continue

        seen_names.add(name)

        transaction.on_commit(
            partial(
                _delete_image_if_unreferenced,
                image.storage,
                name,
            )
        )


# ============================================================
# OPTIMIZACIÓN DE IMÁGENES
# Se conservan las señales existentes del proyecto.
# ============================================================

from .image_utils import optimize_instance_image_fields
from .models import (
    AboutContent,
    Certification,
    CompanyValue,
    HomeContent,
    Insurance,
    InstitutionalPage,
    ProfessionalBlock,
    ProfessionalPage,
    SiteConfiguration,
    TeamMember,
    Testimonial,
)


@receiver(
    pre_save,
    sender=SiteConfiguration,
    dispatch_uid="optimize_site_configuration_images",
)
def optimize_site_configuration_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        (
            "logo",
            "white_logo",
            "favicon",
            "preloader_background",
            "footer_background",
        ),
        max_dimension=2200,
        quality=82,
    )


@receiver(
    pre_save,
    sender=AboutContent,
    dispatch_uid="optimize_about_images",
)
def optimize_about_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        (
            "image",
            "video_image",
        ),
        max_dimension=2200,
        quality=82,
    )


@receiver(
    pre_save,
    sender=TeamMember,
    dispatch_uid="optimize_team_images",
)
def optimize_team_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        ("photo",),
        max_dimension=2200,
        quality=82,
    )


@receiver(
    pre_save,
    sender=CompanyValue,
    dispatch_uid="optimize_company_value_images",
)
def optimize_company_value_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        ("image",),
        max_dimension=2200,
        quality=82,
    )


@receiver(
    pre_save,
    sender=Testimonial,
    dispatch_uid="optimize_testimonial_images",
)
def optimize_testimonial_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        ("photo",),
        max_dimension=2200,
        quality=82,
    )


@receiver(
    pre_save,
    sender=InstitutionalPage,
    dispatch_uid="optimize_institutional_page_images",
)
def optimize_institutional_page_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        ("image",),
        max_dimension=2200,
        quality=82,
    )


@receiver(
    pre_save,
    sender=HomeContent,
    dispatch_uid="optimize_home_images",
)
def optimize_home_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        (
            "hero_image",
            "services_default_image",
            "about_image_primary",
            "about_image_secondary",
            "values_default_image",
            "skill_image",
            "before_fallback_image",
            "after_fallback_image",
            "testimonials_section_image",
            "testimonial_avatar_default",
            "contact_image",
            "blog_default_image",
        ),
        max_dimension=2200,
        quality=82,
    )


@receiver(
    pre_save,
    sender=ProfessionalPage,
    dispatch_uid="optimize_professional_page_images",
)
def optimize_professional_page_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        ("hero_image",),
        max_dimension=2200,
        quality=82,
    )


@receiver(
    pre_save,
    sender=ProfessionalBlock,
    dispatch_uid="optimize_professional_block_images",
)
def optimize_professional_block_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        ("image",),
        max_dimension=2200,
        quality=82,
    )


@receiver(
    pre_save,
    sender=Insurance,
    dispatch_uid="optimize_insurance_images",
)
def optimize_insurance_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        ("image",),
        max_dimension=2200,
        quality=88,
    )


@receiver(
    pre_save,
    sender=Certification,
    dispatch_uid="optimize_certification_images",
)
def optimize_certification_images(sender, instance, **kwargs):
    optimize_instance_image_fields(
        instance,
        ("image",),
        max_dimension=2200,
        quality=88,
    )