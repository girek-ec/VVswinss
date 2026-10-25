from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from PIL import Image, ImageOps, UnidentifiedImageError


DEFAULT_MAX_DIMENSION = 2200
DEFAULT_QUALITY = 82


def optimize_uploaded_image(
    uploaded_file,
    *,
    max_dimension=DEFAULT_MAX_DIMENSION,
    quality=DEFAULT_QUALITY,
):
    """
    Convierte una imagen subida a WebP optimizado.

    - Corrige orientación EXIF.
    - Mantiene proporción.
    - Nunca amplía imágenes pequeñas.
    - Reduce el lado mayor al máximo indicado.
    - Conserva transparencia.
    - Elimina metadatos innecesarios.
    - Devuelve un ContentFile listo para un ImageField.
    """

    if not uploaded_file:
        return uploaded_file

    original_name = getattr(
        uploaded_file,
        "name",
        "image",
    )

    try:
        uploaded_file.seek(0)

        with Image.open(uploaded_file) as image:
            if getattr(image, "is_animated", False):
                uploaded_file.seek(0)
                return uploaded_file

            image = ImageOps.exif_transpose(image)

            if max(image.size) > max_dimension:
                image.thumbnail(
                    (max_dimension, max_dimension),
                    Image.Resampling.LANCZOS,
                )

            has_alpha = (
                image.mode in ("RGBA", "LA")
                or (
                    image.mode == "P"
                    and "transparency" in image.info
                )
            )

            if has_alpha:
                image = image.convert("RGBA")
            else:
                image = image.convert("RGB")

            output = BytesIO()

            image.save(
                output,
                format="WEBP",
                quality=quality,
                method=6,
            )

    except (
        UnidentifiedImageError,
        OSError,
        ValueError,
    ):
        uploaded_file.seek(0)
        return uploaded_file

    stem = Path(original_name).stem

    return ContentFile(
        output.getvalue(),
        name=f"{stem}.webp",
    )


def optimize_instance_image_fields(
    instance,
    field_names,
    *,
    max_dimension=DEFAULT_MAX_DIMENSION,
    quality=DEFAULT_QUALITY,
):
    """
    Optimiza solamente archivos nuevos o reemplazados
    en los ImageField indicados.

    Los archivos ya guardados (_committed=True)
    no se vuelven a procesar.
    """

    for field_name in field_names:
        image = getattr(instance, field_name, None)

        if not image:
            continue

        if getattr(image, "_committed", True):
            continue

        optimized = optimize_uploaded_image(
            image,
            max_dimension=max_dimension,
            quality=quality,
        )

        if optimized is image:
            continue

        setattr(instance, field_name, optimized)