from django.core.management.base import BaseCommand, CommandError

from core.models import HomeContent


class Command(BaseCommand):
    help = "Crea o actualiza el contenido principal de la Home de V&V Swiss Services."

    def handle(self, *args, **options):
        count = HomeContent.objects.count()

        if count > 1:
            raise CommandError(
                "Existen varios registros HomeContent. "
                "No se modificó nada para evitar actualizar el registro equivocado."
            )

        data = {
            # ==========================================================
            # ESPAÑOL · REFERENCIA INTERNA
            # ==========================================================
            "title_es": (
                "Renovación integral y trabajos del edificio "
                "en la Suiza francófona"
            ),
            "subtitle_es": (
                "V&V Swiss Services acompaña a particulares, propietarios, "
                "gerencias inmobiliarias y profesionales en proyectos de "
                "renovación interior y exterior. Albañilería, aislamiento "
                "térmico, yesería y pladur, pintura, acabados y mantenimiento "
                "inmobiliario con un solo interlocutor. Nuestro equipo reúne "
                "más de 20 años de experiencia en el sector de la construcción "
                "en Suiza."
            ),

            # ==========================================================
            # FRANÇAIS · SUISSE ROMANDE · PRINCIPAL
            # ==========================================================
            "title_fr": (
                "Rénovation intérieure et extérieure "
                "en Suisse romande"
            ),
            "subtitle_fr": (
                "V&V Swiss Services accompagne les particuliers, les propriétaires, "
                "les régies immobilières et les professionnels pour leurs travaux "
                "de rénovation. Maçonnerie, isolation thermique, plâtrerie, "
                "peinture, finitions et entretien immobilier avec un interlocuteur "
                "unique. Notre équipe bénéficie de plus de 20 ans d’expérience "
                "dans le secteur de la construction en Suisse."
            ),

            # ==========================================================
            # DEUTSCH · SCHWEIZER HOCHDEUTSCH
            # ==========================================================
            "title_de": (
                "Renovationen im Innen- und Aussenbereich "
                "in der Westschweiz"
            ),
            "subtitle_de": (
                "V&V Swiss Services begleitet Privatpersonen, Eigentümer, "
                "Immobilienverwaltungen und Fachpartner bei Renovationsprojekten. "
                "Maurerarbeiten, Wärmedämmung, Gipserarbeiten, Malerarbeiten, "
                "Ausbau und Immobilienunterhalt aus einer Hand. Unser Team "
                "verfügt über mehr als 20 Jahre Erfahrung im Schweizer Baugewerbe."
            ),

            # ==========================================================
            # ITALIANO · CONTESTO SVIZZERO
            # ==========================================================
            "title_it": (
                "Ristrutturazioni interne ed esterne "
                "nella Svizzera romanda"
            ),
            "subtitle_it": (
                "V&V Swiss Services affianca privati, proprietari, "
                "amministrazioni immobiliari e professionisti nei progetti di "
                "ristrutturazione. Muratura, isolamento termico, intonacatura "
                "e cartongesso, pittura, finiture e manutenzione immobiliare "
                "con un unico interlocutore. Il nostro team vanta oltre 20 anni "
                "di esperienza nel settore delle costruzioni in Svizzera."
            ),

            # ==========================================================
            # ENGLISH · BRITISH ENGLISH
            # ==========================================================
            "title_en": (
                "Interior and exterior renovation "
                "in French-speaking Switzerland"
            ),
            "subtitle_en": (
                "V&V Swiss Services supports homeowners, property owners, "
                "property managers and construction professionals with renovation "
                "projects. Masonry, thermal insulation, plastering, painting, "
                "finishing works and property maintenance through a single point "
                "of contact. Our team brings more than 20 years of experience "
                "in the Swiss construction sector."
            ),

            "is_active": True,
        }

        if count == 0:
            obj = HomeContent.objects.create(**data)

            self.stdout.write(
                self.style.SUCCESS(
                    f"HomeContent creado correctamente. ID={obj.pk}"
                )
            )

        else:
            obj = HomeContent.objects.first()

            for field_name, value in data.items():
                setattr(obj, field_name, value)

            obj.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"HomeContent actualizado correctamente. ID={obj.pk}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Contenido Home cargado en ES, FR, DE, IT y EN."
            )
        )

        self.stdout.write(
            "La imagen y el vídeo existentes, si los hubiera, no fueron modificados."
        )
