# CONTACTO · ADJUNTOS PRIVADOS | PRIVATE CONTACT ATTACHMENTS
from pathlib import PurePosixPath
import posixpath

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import FileResponse, Http404
from django.views.decorators.cache import never_cache
from django.views.static import serve

from .models import ContactAttachment


@staff_member_required(login_url="/admin/login/")
@never_cache
def serve_private_contact_attachment(request, path):
    """Entrega exclusivamente adjuntos registrados, a usuarios staff autenticados."""
    # VALIDAR RUTA · NO ACEPTAR TRAVERSAL | VALIDATE RELATIVE PATH
    if not path or "\\" in path or path.startswith("/"):
        raise Http404("Adjunto no encontrado")
    relative = PurePosixPath(path)
    if any(part in ("", ".", "..") for part in relative.parts):
        raise Http404("Adjunto no encontrado")

    # SOLO ADJUNTOS DEL MODELO | ONLY FILES REGISTERED IN CONTACT ADMIN
    filename = "contact/attachments/" + relative.as_posix()
    attachment = ContactAttachment.objects.filter(file=filename).first()
    if attachment is None or not attachment.file:
        raise Http404("Adjunto no encontrado")

    try:
        stored_file = attachment.file.open("rb")
    except (OSError, ValueError):
        raise Http404("Archivo no disponible") from None

    # DESCARGA SEGURA · NO RENDERIZAR HTML/SVG SUBIDO | DOWNLOAD INSTEAD OF INLINE
    response = FileResponse(stored_file, as_attachment=True, filename=relative.name)
    response["Cache-Control"] = "private, no-store, max-age=0"
    response["X-Content-Type-Options"] = "nosniff"
    response["X-Robots-Tag"] = "noindex, nofollow, noarchive"
    return response


# MEDIA PÚBLICA · BLOQUEAR RUTAS ALTERNATIVAS DE ADJUNTOS | PUBLIC MEDIA GUARD
def serve_public_media(request, path):
    """Sirve únicamente media pública, sin permitir acceso alternativo a adjuntos."""
    if "\\" in path:
        raise Http404("Ruta no disponible")
    normalized = posixpath.normpath(path).lstrip("/")
    if normalized == "contact/attachments" or normalized.startswith("contact/attachments/"):
        raise Http404("Ruta privada")
    return serve(request, path, document_root=settings.MEDIA_ROOT, show_indexes=False)
