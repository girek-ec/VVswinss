from django.core.management.base import BaseCommand
from django.db import transaction
from professionals.models import (
    ProfessionalSitePage, ProfessionalVisualSettings, ProfessionalNeedItem,
    ProfessionalProcessItem, ProfessionalAdvantageItem,
    NEED_DEFAULTS, PROCESS_DEFAULTS, ADVANTAGE_DEFAULTS,
)


class Command(BaseCommand):
    help = "Crea la página y 15 registros V2 sin sobrescribir contenido ya configurado."

    @transaction.atomic
    def handle(self, *args, **options):
        # COPIA INICIAL OPCIONAL | COPY OLD PAGE ONLY THE FIRST TIME
        from core.models import ProfessionalPage as LegacyPage
        from core.visual_config import ProfessionalPageConfiguration as LegacyVisuals
        old = LegacyPage.objects.filter(is_active=True).first()
        initial = {"hero_title_fr": old.hero_title_fr if old and old.hero_title_fr else "Solutions pour professionnels"}
        page, created = ProfessionalSitePage.objects.get_or_create(slug="main", defaults=initial)
        if created and old:
            for lang in ("fr", "de", "it", "en", "es"):
                for field in ("hero_title", "hero_text"):
                    setattr(page, f"{field}_{lang}", getattr(old, f"{field}_{lang}", ""))
            page.hero_image = old.hero_image.name if old.hero_image else None
            page.save()
            page.services.set(old.services.all())
        # SERVICIOS · VINCULAR SOLO AL CREAR | KEEP LATER ADMIN SELECTIONS
        if created:
            from services.models import Service
            page.services.set(Service.objects.filter(is_active=True))
        visuals, _ = ProfessionalVisualSettings.objects.get_or_create(page=page)
        legacy_visuals = LegacyVisuals.objects.first()
        if created and legacy_visuals:
            for field in ("hero_default_image", "turnover_background", "faq_image"):
                img = getattr(legacy_visuals, field, None)
                if img:
                    setattr(visuals, field, img.name)
            visuals.save()

        count = 0
        for model, defaults, legacy_model in (
            (ProfessionalNeedItem, NEED_DEFAULTS, "need"),
            (ProfessionalProcessItem, PROCESS_DEFAULTS, "process"),
            (ProfessionalAdvantageItem, ADVANTAGE_DEFAULTS, "advantage"),
        ):
            for order, (key, config) in enumerate(defaults.items(), 1):
                item, is_new = model.objects.get_or_create(page=page, key=key, defaults={
                    "title_fr": config[0], "text_fr": config[1], "order": order,
                })
                count += int(is_new)
                if is_new and legacy_visuals and hasattr(item, "image") and len(config) > 2:
                    image = getattr(legacy_visuals, config[2], None)
                    if image:
                        item.image = image.name
                        item.save(update_fields=["image"])
        self.stdout.write(self.style.SUCCESS(f"PROFESSIONALS V2 · Página {'creada' if created else 'existente'}, {count} secciones nuevas. No se han borrado registros antiguos."))
