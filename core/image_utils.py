from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from PIL import Image, ImageOps, UnidentifiedImageError


DEFAULT_MAX_DIMENSION = 2200
DEFAULT_QUALITY = 82

SOCIAL_IMAGE_WIDTH = 1200
SOCIAL_IMAGE_HEIGHT = 630
SOCIAL_IMAGE_QUALITY = 88

AUTO_SOCIAL_PREFIX = "auto-social-"
MANUAL_SOCIAL_PREFIX = "manual-social-"


# OPTIMIZACIÓN WEB · WEB OPTIMIZATION
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
        try:
            uploaded_file.seek(0)
        except (AttributeError, OSError):
            pass

        return uploaded_file

    stem = Path(original_name).stem

    return ContentFile(
        output.getvalue(),
        name=f"{stem}.webp",
    )


# CAMPOS DE IMAGEN · IMAGE FIELDS
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
        image = getattr(
            instance,
            field_name,
            None,
        )

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

        setattr(
            instance,
            field_name,
            optimized,
        )


# NOMBRE DE IMAGEN SOCIAL · SOCIAL IMAGE NAME
def _social_image_name(
    original_name,
    prefix,
):
    stem = Path(original_name).stem

    return f"{prefix}{stem}.jpg"


# GENERACIÓN DE IMAGEN SOCIAL · SOCIAL IMAGE GENERATION
def generate_social_image(
    uploaded_file,
    *,
    width=SOCIAL_IMAGE_WIDTH,
    height=SOCIAL_IMAGE_HEIGHT,
    quality=SOCIAL_IMAGE_QUALITY,
    filename_prefix=AUTO_SOCIAL_PREFIX,
):
    """
    Genera una imagen social Open Graph.

    - Tamaño final: 1200 x 630 px.
    - Corrige orientación EXIF.
    - Recorta proporcionalmente desde el centro.
    - Convierte transparencias a fondo blanco.
    - Genera JPG optimizado para redes sociales.
    """
    if not uploaded_file:
        return None

    original_name = getattr(
        uploaded_file,
        "name",
        "social-image",
    )

    try:
        uploaded_file.seek(0)

        with Image.open(uploaded_file) as image:
            image = ImageOps.exif_transpose(image)

            if getattr(image, "is_animated", False):
                image.seek(0)

            has_alpha = (
                image.mode in ("RGBA", "LA")
                or (
                    image.mode == "P"
                    and "transparency" in image.info
                )
            )

            if has_alpha:
                image = image.convert("RGBA")

                background = Image.new(
                    "RGB",
                    image.size,
                    (255, 255, 255),
                )

                background.paste(
                    image,
                    mask=image.getchannel("A"),
                )

                image = background
            else:
                image = image.convert("RGB")

            image = ImageOps.fit(
                image,
                (width, height),
                method=Image.Resampling.LANCZOS,
                centering=(0.5, 0.5),
            )

            output = BytesIO()

            image.save(
                output,
                format="JPEG",
                quality=quality,
                optimize=True,
                progressive=True,
            )

    except (
        UnidentifiedImageError,
        OSError,
        ValueError,
    ):
        try:
            uploaded_file.seek(0)
        except (AttributeError, OSError):
            pass

        return None

    return ContentFile(
        output.getvalue(),
        name=_social_image_name(
            original_name,
            filename_prefix,
        ),
    )


# DETECCIÓN DE IMAGEN SOCIAL AUTOMÁTICA · AUTOMATIC SOCIAL IMAGE DETECTION
def is_auto_social_image(image):
    """
    Detecta si una imagen Open Graph fue generada automáticamente.

    También reconoce el formato antiguo:
    nombre-social.jpg
    """
    if not image:
        return False

    name = getattr(
        image,
        "name",
        "",
    )

    if not name:
        return False

    filename = Path(name).name

    return (
        filename.startswith(AUTO_SOCIAL_PREFIX)
        or (
            filename.endswith("-social.jpg")
            and not filename.startswith(MANUAL_SOCIAL_PREFIX)
        )
    )


# SINCRONIZACIÓN OPEN GRAPH · OPEN GRAPH SYNCHRONIZATION
def sync_social_image(
    instance,
    source_field_name,
    *,
    target_field_name="og_image",
):
    """
    Sincroniza una imagen principal con su imagen social Open Graph.

    Reglas:
    - Una imagen cargada manualmente en og_image tiene prioridad.
    - La imagen manual se adapta automáticamente a 1200 x 630 px.
    - Si og_image está vacío, se genera desde la imagen principal.
    - Si cambia la imagen principal, solo se reemplaza una OG automática.
    - Una imagen OG manual nunca se sobrescribe automáticamente.
    """
    source = getattr(
        instance,
        source_field_name,
        None,
    )

    target = getattr(
        instance,
        target_field_name,
        None,
    )

    # OG MANUAL NUEVA · NEW MANUAL OG
    if target and not getattr(target, "_committed", True):
        social_image = generate_social_image(
            target,
            filename_prefix=MANUAL_SOCIAL_PREFIX,
        )

        if social_image:
            setattr(
                instance,
                target_field_name,
                social_image,
            )

        return

    # OG MANUAL EXISTENTE · EXISTING MANUAL OG
    if target and not is_auto_social_image(target):
        return

    # SIN IMAGEN PRINCIPAL · NO SOURCE IMAGE
    if not source:
        if target and is_auto_social_image(target):
            setattr(
                instance,
                target_field_name,
                None,
            )

        return

    source_is_new = not getattr(
        source,
        "_committed",
        True,
    )

    # OG AUTOMÁTICA EXISTENTE + ORIGEN SIN CAMBIOS · EXISTING AUTO OG + UNCHANGED SOURCE
    if target and not source_is_new:
        return

    # GENERAR OG AUTOMÁTICA · GENERATE AUTOMATIC OG
    social_image = generate_social_image(
        source,
        filename_prefix=AUTO_SOCIAL_PREFIX,
    )

    if social_image:
        setattr(
            instance,
            target_field_name,
            social_image,
        )