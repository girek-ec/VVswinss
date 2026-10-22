from django.core.management.base import BaseCommand, CommandError

from core.models import CompanyValue


class Command(BaseCommand):
    help = "Crea o actualiza los valores corporativos de V&V Swiss Services."

    def handle(self, *args, **options):

        values = [
            {
                "order": 1,

                "title_es": "Calidad",
                "description_es": (
                    "Trabajamos con atención al detalle y con el objetivo de "
                    "ofrecer ejecuciones cuidadas, acabados limpios y resultados "
                    "duraderos, de acuerdo con los estándares esperados en Suiza."
                ),

                "title_fr": "Qualité",
                "description_fr": (
                    "Nous accordons une attention particulière à la qualité "
                    "d’exécution, à la précision des détails et à la propreté "
                    "des finitions, afin de livrer des travaux soignés et durables."
                ),

                "title_de": "Qualität",
                "description_de": (
                    "Wir legen grossen Wert auf eine sorgfältige Ausführung, "
                    "präzise Details und saubere Abschlüsse, damit unsere Arbeiten "
                    "dauerhaft und den in der Schweiz erwarteten Qualitätsstandards "
                    "entsprechend ausgeführt werden."
                ),

                "title_it": "Qualità",
                "description_it": (
                    "Prestiamo particolare attenzione alla qualità dell’esecuzione, "
                    "alla precisione dei dettagli e alla pulizia delle finiture, "
                    "per garantire lavori curati e duraturi."
                ),

                "title_en": "Quality",
                "description_en": (
                    "We place particular emphasis on careful workmanship, precise "
                    "detailing and clean finishes, delivering durable work to the "
                    "standards expected in Switzerland."
                ),

                "is_active": True,
            },

            {
                "order": 2,

                "title_es": "Honestidad",
                "description_es": (
                    "Privilegiamos una comunicación transparente y presupuestos "
                    "claros, para que cada cliente conozca desde el inicio el "
                    "alcance de los trabajos y las condiciones de su proyecto."
                ),

                "title_fr": "Honnêteté",
                "description_fr": (
                    "Nous privilégions une communication transparente et des devis "
                    "clairs afin que chaque client connaisse dès le départ "
                    "l’étendue des travaux et les conditions de son projet."
                ),

                "title_de": "Ehrlichkeit",
                "description_de": (
                    "Wir setzen auf transparente Kommunikation und klare Offerten, "
                    "damit unsere Kunden von Anfang an den Umfang der Arbeiten "
                    "und die Rahmenbedingungen ihres Projekts kennen."
                ),

                "title_it": "Onestà",
                "description_it": (
                    "Privilegiamo una comunicazione trasparente e preventivi chiari, "
                    "affinché ogni cliente conosca fin dall’inizio l’entità dei "
                    "lavori e le condizioni del proprio progetto."
                ),

                "title_en": "Honesty",
                "description_en": (
                    "We believe in transparent communication and clear quotations, "
                    "so that every client understands the scope of the work and "
                    "the conditions of the project from the outset."
                ),

                "is_active": True,
            },

            {
                "order": 3,

                "title_es": "Confianza",
                "description_es": (
                    "Construimos relaciones basadas en el cumplimiento de los "
                    "compromisos, el respeto de los plazos acordados y un "
                    "seguimiento responsable de cada obra."
                ),

                "title_fr": "Confiance",
                "description_fr": (
                    "Nous construisons des relations durables en respectant nos "
                    "engagements, les délais convenus et en assurant un suivi "
                    "responsable de chaque chantier."
                ),

                "title_de": "Vertrauen",
                "description_de": (
                    "Wir schaffen langfristiges Vertrauen, indem wir unsere "
                    "Zusagen einhalten, vereinbarte Termine respektieren und "
                    "jedes Bauvorhaben verantwortungsvoll begleiten."
                ),

                "title_it": "Fiducia",
                "description_it": (
                    "Costruiamo rapporti duraturi rispettando gli impegni assunti, "
                    "le tempistiche concordate e garantendo un monitoraggio "
                    "responsabile di ogni cantiere."
                ),

                "title_en": "Trust",
                "description_en": (
                    "We build lasting relationships by honouring our commitments, "
                    "respecting agreed timescales and providing responsible "
                    "follow-up throughout every project."
                ),

                "is_active": True,
            },

            {
                "order": 4,

                "title_es": "Tradición e innovación",
                "description_es": (
                    "Combinamos el conocimiento del oficio tradicional con "
                    "soluciones técnicas actuales, adaptándonos a las nuevas "
                    "necesidades de la construcción y la renovación."
                ),

                "title_fr": "Tradition et innovation",
                "description_fr": (
                    "Nous associons le savoir-faire traditionnel du bâtiment "
                    "aux solutions techniques actuelles afin de répondre aux "
                    "nouvelles exigences de la construction et de la rénovation."
                ),

                "title_de": "Tradition und Innovation",
                "description_de": (
                    "Wir verbinden bewährtes handwerkliches Fachwissen mit "
                    "modernen technischen Lösungen und passen uns laufend an "
                    "die neuen Anforderungen im Bau- und Renovationsbereich an."
                ),

                "title_it": "Tradizione e innovazione",
                "description_it": (
                    "Uniamo il sapere artigianale tradizionale alle soluzioni "
                    "tecniche moderne, adattandoci costantemente alle nuove "
                    "esigenze della costruzione e della ristrutturazione."
                ),

                "title_en": "Tradition and innovation",
                "description_en": (
                    "We combine traditional building craftsmanship with modern "
                    "technical solutions, continually adapting to evolving "
                    "construction and renovation requirements."
                ),

                "is_active": True,
            },

            {
                "order": 5,

                "title_es": "Respeto por el entorno",
                "description_es": (
                    "Favorecemos obras ordenadas y soluciones que contribuyan "
                    "a mejorar la eficiencia energética de los edificios, "
                    "integrando las exigencias medioambientales actuales."
                ),

                "title_fr": "Respect de l’environnement",
                "description_fr": (
                    "Nous privilégions des chantiers propres et organisés ainsi "
                    "que des solutions contribuant à améliorer la performance "
                    "énergétique des bâtiments, dans le respect des exigences "
                    "environnementales actuelles."
                ),

                "title_de": "Respekt für die Umwelt",
                "description_de": (
                    "Wir achten auf saubere und gut organisierte Baustellen und "
                    "setzen auf Lösungen, die zur Verbesserung der Energieeffizienz "
                    "von Gebäuden beitragen und heutige Umweltanforderungen "
                    "berücksichtigen."
                ),

                "title_it": "Rispetto per l’ambiente",
                "description_it": (
                    "Promuoviamo cantieri ordinati e puliti e soluzioni che "
                    "contribuiscano a migliorare l’efficienza energetica degli "
                    "edifici, nel rispetto delle attuali esigenze ambientali."
                ),

                "title_en": "Respect for the environment",
                "description_en": (
                    "We promote clean, well-organised sites and solutions that "
                    "help improve the energy efficiency of buildings while "
                    "responding to current environmental requirements."
                ),

                "is_active": True,
            },
        ]

        expected_titles = {item["title_fr"] for item in values}

        existing = CompanyValue.objects.all()

        unexpected = [
            obj.title_fr
            for obj in existing
            if obj.title_fr not in expected_titles
        ]

        if unexpected:
            raise CommandError(
                "Existen valores corporativos no reconocidos: "
                + ", ".join(unexpected)
                + ". No se modificó nada para evitar sobrescribir contenido."
            )

        created_count = 0
        updated_count = 0

        for item in values:
            title_fr = item["title_fr"]

            defaults = item.copy()
            defaults.pop("title_fr")

            obj, created = CompanyValue.objects.update_or_create(
                title_fr=title_fr,
                defaults=defaults,
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"CREADO: {obj.title_fr}"
                    )
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"ACTUALIZADO: {obj.title_fr}"
                    )
                )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Proceso completado. "
                f"Creados: {created_count} | "
                f"Actualizados: {updated_count}"
            )
        )
