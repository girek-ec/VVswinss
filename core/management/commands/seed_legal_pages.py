from django.core.management.base import BaseCommand

from core.models import InstitutionalPage


class Command(BaseCommand):
    help = "Crea o actualiza las páginas legales de V&V Swiss Services en ES, FR, DE, IT y EN."

    def handle(self, *args, **options):
        legal_pages = [
            {
                "slug_fr": "mentions-legales",
                "defaults": {
                    "title_es": "Aviso legal",
                    "title_fr": "Mentions légales",
                    "title_de": "Impressum",
                    "title_it": "Note legali",
                    "title_en": "Legal notice",

                    "slug_de": "impressum",
                    "slug_it": "note-legali",
                    "slug_en": "legal-notice",

                    "seo_title_es": "Aviso legal | V&V Swiss Services",
                    "seo_title_fr": "Mentions légales | V&V Swiss Services",
                    "seo_title_de": "Impressum | V&V Swiss Services",
                    "seo_title_it": "Note legali | V&V Swiss Services",
                    "seo_title_en": "Legal notice | V&V Swiss Services",

                    "meta_description_es": "Información legal, responsabilidad, propiedad intelectual y condiciones de utilización del sitio web de V&V Swiss Services en Suiza.",
                    "meta_description_fr": "Informations légales, responsabilité, propriété intellectuelle et conditions d’utilisation du site internet de V&V Swiss Services en Suisse.",
                    "meta_description_de": "Rechtliche Informationen, Haftung, geistiges Eigentum und Nutzungsbedingungen der Website von V&V Swiss Services in der Schweiz.",
                    "meta_description_it": "Informazioni legali, responsabilità, proprietà intellettuale e condizioni di utilizzo del sito web di V&V Swiss Services in Svizzera.",
                    "meta_description_en": "Legal information, liability, intellectual property and terms of use relating to the V&V Swiss Services website in Switzerland.",

                    "content_es": """
<h2>Objeto del sitio web</h2>
<p>El presente sitio web tiene por finalidad presentar V&V Swiss Services, sus actividades, sus servicios de renovación y construcción, así como facilitar el contacto con clientes, propietarios, administraciones inmobiliarias, empresas y otros interesados.</p>

<h2>Propiedad intelectual</h2>
<p>Salvo indicación contraria, los contenidos de este sitio web, incluidos textos, fotografías, imágenes, gráficos, elementos visuales, logotipos, documentos, estructura y diseño, están protegidos por la legislación aplicable en materia de propiedad intelectual.</p>
<p>La reproducción, distribución, modificación, publicación, transmisión o utilización de estos contenidos, total o parcialmente, requiere autorización previa del titular de los derechos, salvo cuando la legislación aplicable permita expresamente dicha utilización.</p>

<h2>Exactitud de la información</h2>
<p>V&V Swiss Services procura mantener la información publicada en este sitio actualizada, clara y correcta. No obstante, no puede garantizar que todos los contenidos estén permanentemente completos, actualizados o libres de errores.</p>
<p>La información disponible en el sitio tiene carácter informativo y no constituye por sí sola una oferta contractual, un presupuesto vinculante ni un compromiso de ejecución.</p>

<h2>Presupuestos y servicios</h2>
<p>Las solicitudes realizadas a través del sitio web no constituyen automáticamente la celebración de un contrato. Las condiciones, alcance, precios, plazos y características de cada trabajo se determinan individualmente mediante la correspondiente oferta, presupuesto, confirmación o contrato.</p>

<h2>Responsabilidad</h2>
<p>Dentro de los límites permitidos por la legislación aplicable, V&V Swiss Services no asume responsabilidad por daños derivados del acceso, utilización, imposibilidad de utilización o interrupciones temporales de este sitio web, salvo cuando una responsabilidad resulte obligatoria conforme a la ley.</p>

<h2>Enlaces externos</h2>
<p>El sitio puede contener enlaces a páginas web, plataformas o servicios de terceros. V&V Swiss Services no controla necesariamente dichos contenidos y no asume responsabilidad por la disponibilidad, seguridad, contenido o políticas de privacidad de esos servicios externos.</p>

<h2>Disponibilidad del sitio</h2>
<p>V&V Swiss Services procura garantizar un funcionamiento adecuado del sitio web, pero no puede asegurar una disponibilidad permanente e ininterrumpida. El sitio puede ser suspendido temporalmente por mantenimiento, mejoras técnicas, actualizaciones, fallos o circunstancias fuera de nuestro control.</p>

<h2>Protección de datos</h2>
<p>El tratamiento de los datos personales realizado a través de este sitio se describe en la declaración de protección de datos disponible en la página correspondiente.</p>

<h2>Derecho aplicable</h2>
<p>El presente sitio web y estas menciones legales se rigen principalmente por el derecho suizo, sin perjuicio de las disposiciones legales imperativas que puedan resultar aplicables.</p>

<h2>Modificaciones</h2>
<p>V&V Swiss Services puede modificar o actualizar estas menciones legales cuando resulte necesario para adaptarlas a cambios técnicos, comerciales, organizativos o jurídicos.</p>
""",

                    "content_fr": """
<h2>Objet du site internet</h2>
<p>Le présent site internet a pour objectif de présenter V&V Swiss Services, ses activités et ses prestations dans le domaine de la rénovation et du bâtiment, ainsi que de faciliter la prise de contact avec les clients, propriétaires, régies immobilières, entreprises et autres personnes intéressées.</p>

<h2>Propriété intellectuelle</h2>
<p>Sauf indication contraire, les contenus de ce site internet, notamment les textes, photographies, images, éléments graphiques, logos, documents, structure et design, sont protégés par les dispositions applicables en matière de propriété intellectuelle.</p>
<p>Toute reproduction, distribution, modification, publication, transmission ou utilisation de ces contenus, en totalité ou en partie, nécessite l’autorisation préalable du titulaire des droits, sauf lorsque la législation applicable autorise expressément une telle utilisation.</p>

<h2>Exactitude des informations</h2>
<p>V&V Swiss Services s’efforce de maintenir les informations publiées sur ce site à jour, claires et exactes. Nous ne pouvons toutefois garantir que l’ensemble des contenus soit en permanence complet, actualisé ou exempt d’erreurs.</p>
<p>Les informations disponibles sur le site sont fournies à titre informatif et ne constituent pas, à elles seules, une offre contractuelle, un devis ferme ou un engagement d’exécution.</p>

<h2>Devis et prestations</h2>
<p>Une demande transmise par l’intermédiaire du site internet ne constitue pas automatiquement la conclusion d’un contrat. Les conditions, l’étendue des travaux, les prix, les délais et les caractéristiques de chaque intervention sont définis individuellement au moyen d’une offre, d’un devis, d’une confirmation ou d’un contrat.</p>

<h2>Responsabilité</h2>
<p>Dans les limites autorisées par le droit applicable, V&V Swiss Services décline toute responsabilité pour les dommages pouvant résulter de l’accès, de l’utilisation, de l’impossibilité d’utiliser ou d’une interruption temporaire de ce site internet, sauf lorsqu’une responsabilité est imposée par des dispositions légales impératives.</p>

<h2>Liens externes</h2>
<p>Le site peut contenir des liens vers des sites internet, plateformes ou services exploités par des tiers. V&V Swiss Services ne contrôle pas nécessairement ces contenus et ne peut être tenue responsable de leur disponibilité, de leur sécurité, de leur contenu ou de leurs pratiques en matière de protection des données.</p>

<h2>Disponibilité du site</h2>
<p>V&V Swiss Services s’efforce d’assurer le bon fonctionnement du site internet, mais ne peut garantir une disponibilité permanente et sans interruption. Le site peut être temporairement indisponible en raison de travaux de maintenance, d’améliorations techniques, de mises à jour, de défaillances ou de circonstances indépendantes de notre volonté.</p>

<h2>Protection des données</h2>
<p>Le traitement des données personnelles effectué par l’intermédiaire de ce site internet est décrit dans notre déclaration relative à la protection des données accessible sur la page correspondante.</p>

<h2>Droit applicable</h2>
<p>Le présent site internet et les présentes mentions légales sont principalement soumis au droit suisse, sous réserve des dispositions légales impératives éventuellement applicables.</p>

<h2>Modifications</h2>
<p>V&V Swiss Services peut modifier ou actualiser les présentes mentions légales lorsque cela est nécessaire afin de tenir compte d’évolutions techniques, commerciales, organisationnelles ou juridiques.</p>
""",

                    "content_de": """
<h2>Zweck der Website</h2>
<p>Diese Website dient der Präsentation von V&V Swiss Services, ihrer Tätigkeiten und Dienstleistungen im Bereich Renovation und Bau sowie der Kontaktaufnahme mit Kunden, Eigentümern, Immobilienverwaltungen, Unternehmen und weiteren Interessierten.</p>

<h2>Geistiges Eigentum</h2>
<p>Sofern nicht anders angegeben, sind die Inhalte dieser Website, insbesondere Texte, Fotografien, Bilder, grafische Elemente, Logos, Dokumente, Struktur und Gestaltung, durch die anwendbaren Bestimmungen zum geistigen Eigentum geschützt.</p>
<p>Die vollständige oder teilweise Vervielfältigung, Verbreitung, Änderung, Veröffentlichung, Übertragung oder sonstige Nutzung dieser Inhalte bedarf der vorherigen Zustimmung des jeweiligen Rechteinhabers, soweit die anwendbare Gesetzgebung eine solche Nutzung nicht ausdrücklich erlaubt.</p>

<h2>Richtigkeit der Informationen</h2>
<p>V&V Swiss Services bemüht sich, die auf dieser Website veröffentlichten Informationen aktuell, klar und korrekt zu halten. Es kann jedoch nicht gewährleistet werden, dass sämtliche Inhalte jederzeit vollständig, aktuell oder fehlerfrei sind.</p>
<p>Die auf der Website bereitgestellten Informationen dienen der allgemeinen Information und stellen für sich allein kein verbindliches Vertragsangebot, keinen verbindlichen Kostenvoranschlag und keine Ausführungszusage dar.</p>

<h2>Offerten und Dienstleistungen</h2>
<p>Eine über die Website übermittelte Anfrage führt nicht automatisch zum Abschluss eines Vertrags. Leistungsumfang, Preise, Termine und weitere Bedingungen werden für jedes Projekt individuell durch eine Offerte, einen Kostenvoranschlag, eine Bestätigung oder einen Vertrag festgelegt.</p>

<h2>Haftung</h2>
<p>Soweit gesetzlich zulässig, übernimmt V&V Swiss Services keine Haftung für Schäden, die aus dem Zugriff auf diese Website, ihrer Nutzung, der Unmöglichkeit ihrer Nutzung oder vorübergehenden Unterbrechungen entstehen, soweit keine zwingende gesetzliche Haftung besteht.</p>

<h2>Externe Links</h2>
<p>Diese Website kann Links zu Websites, Plattformen oder Diensten Dritter enthalten. V&V Swiss Services hat nicht notwendigerweise Kontrolle über diese Inhalte und übernimmt keine Verantwortung für deren Verfügbarkeit, Sicherheit, Inhalt oder Datenschutzpraktiken.</p>

<h2>Verfügbarkeit der Website</h2>
<p>V&V Swiss Services bemüht sich um einen zuverlässigen Betrieb der Website, kann jedoch keine jederzeitige und unterbrechungsfreie Verfügbarkeit gewährleisten. Wartungsarbeiten, technische Verbesserungen, Aktualisierungen, Störungen oder andere Umstände können zu vorübergehenden Unterbrechungen führen.</p>

<h2>Datenschutz</h2>
<p>Informationen über die Bearbeitung personenbezogener Daten über diese Website finden Sie in unserer Datenschutzerklärung.</p>

<h2>Anwendbares Recht</h2>
<p>Diese Website und dieses Impressum unterstehen grundsätzlich schweizerischem Recht, vorbehaltlich zwingender gesetzlicher Bestimmungen.</p>

<h2>Änderungen</h2>
<p>V&V Swiss Services kann dieses Impressum bei Bedarf an technische, geschäftliche, organisatorische oder rechtliche Entwicklungen anpassen.</p>
""",

                    "content_it": """
<h2>Scopo del sito web</h2>
<p>Il presente sito web ha lo scopo di presentare V&V Swiss Services, le sue attività e i suoi servizi nel settore della ristrutturazione e dell’edilizia, nonché di facilitare il contatto con clienti, proprietari, amministrazioni immobiliari, imprese e altre persone interessate.</p>

<h2>Proprietà intellettuale</h2>
<p>Salvo diversa indicazione, i contenuti di questo sito web, inclusi testi, fotografie, immagini, elementi grafici, loghi, documenti, struttura e design, sono protetti dalle disposizioni applicabili in materia di proprietà intellettuale.</p>
<p>La riproduzione, distribuzione, modifica, pubblicazione, trasmissione o altro utilizzo, totale o parziale, richiede la previa autorizzazione del titolare dei diritti, salvo nei casi espressamente consentiti dalla legge applicabile.</p>

<h2>Accuratezza delle informazioni</h2>
<p>V&V Swiss Services si impegna a mantenere le informazioni pubblicate sul sito aggiornate, chiare e corrette. Non può tuttavia garantire che tutti i contenuti siano sempre completi, aggiornati o privi di errori.</p>
<p>Le informazioni presenti sul sito hanno carattere informativo e non costituiscono, da sole, un’offerta contrattuale, un preventivo vincolante o un impegno all’esecuzione di lavori.</p>

<h2>Preventivi e prestazioni</h2>
<p>Una richiesta inviata tramite il sito non comporta automaticamente la conclusione di un contratto. Condizioni, portata dei lavori, prezzi, termini e caratteristiche di ciascun intervento vengono definiti individualmente attraverso un’offerta, un preventivo, una conferma o un contratto.</p>

<h2>Responsabilità</h2>
<p>Nei limiti consentiti dalla legge applicabile, V&V Swiss Services non assume responsabilità per danni derivanti dall’accesso, dall’utilizzo, dall’impossibilità di utilizzare o da interruzioni temporanee del sito, salvo nei casi in cui una responsabilità sia imposta da disposizioni imperative.</p>

<h2>Collegamenti esterni</h2>
<p>Il sito può contenere collegamenti a siti web, piattaforme o servizi gestiti da terzi. V&V Swiss Services non controlla necessariamente tali contenuti e non assume responsabilità per la loro disponibilità, sicurezza, contenuto o pratiche in materia di protezione dei dati.</p>

<h2>Disponibilità del sito</h2>
<p>V&V Swiss Services si impegna a garantire il corretto funzionamento del sito, ma non può garantirne la disponibilità continua e senza interruzioni. Il sito può essere temporaneamente indisponibile per manutenzione, miglioramenti tecnici, aggiornamenti, guasti o circostanze indipendenti dalla nostra volontà.</p>

<h2>Protezione dei dati</h2>
<p>Il trattamento dei dati personali effettuato attraverso questo sito è descritto nella nostra dichiarazione sulla protezione dei dati.</p>

<h2>Diritto applicabile</h2>
<p>Il presente sito web e le presenti note legali sono principalmente soggetti al diritto svizzero, fatte salve eventuali disposizioni imperative applicabili.</p>

<h2>Modifiche</h2>
<p>V&V Swiss Services può modificare o aggiornare le presenti note legali per adeguarle a evoluzioni tecniche, commerciali, organizzative o giuridiche.</p>
""",

                    "content_en": """
<h2>Purpose of the website</h2>
<p>This website is intended to present V&V Swiss Services, its activities and its renovation and construction services, and to facilitate contact with clients, property owners, property management companies, businesses and other interested parties.</p>

<h2>Intellectual property</h2>
<p>Unless otherwise stated, the contents of this website, including texts, photographs, images, graphics, logos, documents, structure and design, are protected by applicable intellectual property laws.</p>
<p>Any reproduction, distribution, modification, publication, transmission or other use of such content, in whole or in part, requires the prior permission of the relevant rights holder unless expressly permitted by applicable law.</p>

<h2>Accuracy of information</h2>
<p>V&V Swiss Services endeavours to keep the information published on this website accurate, clear and up to date. However, we cannot guarantee that all content will at all times be complete, current or free from errors.</p>
<p>Information available on the website is provided for general information purposes and does not in itself constitute a binding contractual offer, quotation or commitment to carry out work.</p>

<h2>Quotations and services</h2>
<p>A request submitted through the website does not automatically create a contract. The scope of work, prices, deadlines and other conditions are determined individually by means of an offer, quotation, confirmation or contract.</p>

<h2>Liability</h2>
<p>To the extent permitted by applicable law, V&V Swiss Services accepts no liability for damage resulting from access to, use of, inability to use or temporary interruption of this website, except where liability is mandatory under applicable law.</p>

<h2>External links</h2>
<p>This website may contain links to websites, platforms or services operated by third parties. V&V Swiss Services does not necessarily control such content and accepts no responsibility for its availability, security, content or privacy practices.</p>

<h2>Website availability</h2>
<p>V&V Swiss Services endeavours to ensure that the website functions correctly but cannot guarantee permanent or uninterrupted availability. The website may temporarily be unavailable due to maintenance, technical improvements, updates, failures or circumstances beyond our control.</p>

<h2>Data protection</h2>
<p>The processing of personal data through this website is described in our data protection and privacy policy.</p>

<h2>Applicable law</h2>
<p>This website and this legal notice are primarily governed by Swiss law, subject to any mandatory legal provisions that may apply.</p>

<h2>Changes</h2>
<p>V&V Swiss Services may amend or update this legal notice where necessary to reflect technical, commercial, organisational or legal developments.</p>
""",

                    "is_active": True,
                    "is_indexable": True,
                },
            },

            {
                "slug_fr": "protection-des-donnees",
                "defaults": {
                    "title_es": "Protección de datos",
                    "title_fr": "Protection des données",
                    "title_de": "Datenschutzerklärung",
                    "title_it": "Protezione dei dati",
                    "title_en": "Privacy policy",

                    "slug_de": "datenschutzerklaerung",
                    "slug_it": "protezione-dei-dati",
                    "slug_en": "privacy-policy",

                    "seo_title_es": "Protección de datos | V&V Swiss Services",
                    "seo_title_fr": "Protection des données | V&V Swiss Services",
                    "seo_title_de": "Datenschutzerklärung | V&V Swiss Services",
                    "seo_title_it": "Protezione dei dati | V&V Swiss Services",
                    "seo_title_en": "Privacy policy | V&V Swiss Services",

                    "meta_description_es": "Información sobre la recopilación, utilización, conservación y protección de datos personales por V&V Swiss Services conforme al marco suizo de protección de datos.",
                    "meta_description_fr": "Informations sur la collecte, l’utilisation, la conservation et la protection des données personnelles par V&V Swiss Services dans le cadre du droit suisse de la protection des données.",
                    "meta_description_de": "Informationen zur Erhebung, Verwendung, Aufbewahrung und zum Schutz personenbezogener Daten durch V&V Swiss Services nach schweizerischem Datenschutzrecht.",
                    "meta_description_it": "Informazioni sulla raccolta, l’utilizzo, la conservazione e la protezione dei dati personali da parte di V&V Swiss Services secondo il diritto svizzero sulla protezione dei dati.",
                    "meta_description_en": "Information about the collection, use, retention and protection of personal data by V&V Swiss Services under the Swiss data protection framework.",

                    "content_es": """
<h2>Ámbito de aplicación</h2>
<p>Esta declaración explica cómo V&V Swiss Services recopila, utiliza, conserva y protege los datos personales cuando una persona visita este sitio web, envía una solicitud de contacto, solicita una visita técnica, adjunta fotografías o se comunica con nosotros por los canales disponibles.</p>
<p>Esta declaración está concebida teniendo en cuenta la legislación suiza aplicable en materia de protección de datos, incluida la Ley Federal de Protección de Datos.</p>

<h2>Datos personales que podemos recopilar</h2>
<p>Dependiendo de la forma en que utilice el sitio, podemos tratar las siguientes categorías de información:</p>
<ul>
<li>nombre y apellidos;</li>
<li>empresa, cuando se facilite;</li>
<li>dirección de correo electrónico;</li>
<li>número de teléfono;</li>
<li>servicio solicitado;</li>
<li>localización o localidad del proyecto;</li>
<li>contenido del mensaje enviado;</li>
<li>solicitud de visita técnica;</li>
<li>fecha y hora preferidas para una visita;</li>
<li>fotografías o imágenes del proyecto adjuntadas voluntariamente;</li>
<li>idioma utilizado;</li>
<li>dirección IP;</li>
<li>información técnica del navegador o dispositivo, como el User-Agent;</li>
<li>fecha de aceptación y versión de la política de privacidad aceptada.</li>
</ul>

<h2>Formulario de contacto</h2>
<p>Cuando utiliza nuestro formulario de contacto, tratamos los datos proporcionados con la finalidad de analizar su solicitud, responderle, preparar eventualmente un presupuesto, organizar una visita técnica y realizar el seguimiento de su proyecto.</p>

<h2>Fotografías y archivos adjuntos</h2>
<p>Cuando adjunta fotografías del proyecto, dichas imágenes se almacenan asociadas a su solicitud. Le recomendamos no enviar imágenes o documentos que contengan información personal innecesaria de terceros.</p>

<h2>Datos técnicos y seguridad</h2>
<p>El sitio puede registrar determinados datos técnicos, como la dirección IP y la información del navegador, con fines de seguridad, funcionamiento técnico, prevención de abusos, diagnóstico de errores y protección de nuestros sistemas.</p>

<h2>Finalidades del tratamiento</h2>
<p>Los datos personales pueden ser utilizados para:</p>
<ul>
<li>responder solicitudes de información;</li>
<li>preparar presupuestos y ofertas;</li>
<li>organizar visitas técnicas;</li>
<li>comunicarnos con clientes y potenciales clientes;</li>
<li>gestionar solicitudes y proyectos;</li>
<li>garantizar la seguridad técnica del sitio;</li>
<li>cumplir obligaciones legales y administrativas;</li>
<li>proteger nuestros derechos y documentar las solicitudes recibidas.</li>
</ul>

<h2>Correo electrónico, teléfono y WhatsApp</h2>
<p>Si decide comunicarse con nosotros por correo electrónico, teléfono o mediante un enlace a WhatsApp, los datos transmitidos serán tratados para gestionar la comunicación y responder a su solicitud.</p>
<p>Cuando utiliza servicios externos como WhatsApp, el proveedor correspondiente puede tratar información conforme a sus propias condiciones y políticas de privacidad.</p>

<h2>Google Maps</h2>
<p>El sitio puede integrar servicios cartográficos como Google Maps para mostrar nuestra ubicación o zona de servicio. Al utilizar o cargar dichos servicios, determinados datos técnicos pueden ser transmitidos al proveedor correspondiente, que trata la información conforme a sus propias políticas.</p>

<h2>Cookies y tecnologías técnicas</h2>
<p>El sitio puede utilizar cookies u otras tecnologías técnicamente necesarias para su funcionamiento, seguridad, preferencias o gestión de sesión. Si en el futuro se incorporan herramientas adicionales de análisis, publicidad o seguimiento que requieran medidas específicas de información o consentimiento, esta declaración y los mecanismos correspondientes deberán adaptarse.</p>

<h2>Destinatarios y proveedores</h2>
<p>Los datos pueden ser accesibles a proveedores técnicos y profesionales cuando sea necesario para operar el sitio, alojar la infraestructura, gestionar comunicaciones, mantener sistemas, prestar servicios o cumplir obligaciones legales. Dichos destinatarios reciben únicamente la información necesaria para su función.</p>

<h2>Transferencias internacionales</h2>
<p>Determinados proveedores tecnológicos pueden tratar datos desde países distintos de Suiza. Cuando se produzcan transferencias internacionales, se aplicarán las medidas de protección exigidas por la legislación aplicable, según corresponda.</p>

<h2>Conservación de los datos</h2>
<p>Conservamos los datos personales durante el tiempo necesario para atender la solicitud, gestionar la relación comercial, cumplir obligaciones legales o administrativas y proteger nuestros derechos. Los datos que ya no sean necesarios se eliminan o anonimizan cuando resulte razonablemente posible y procedente.</p>

<h2>Seguridad</h2>
<p>Aplicamos medidas técnicas y organizativas razonables destinadas a proteger los datos personales contra pérdida, acceso no autorizado, divulgación, modificación o utilización indebida. Ningún sistema electrónico puede garantizar una seguridad absoluta.</p>

<h2>Derechos de las personas</h2>
<p>Dentro de los límites y condiciones previstos por la legislación aplicable, puede solicitar información sobre sus datos personales, su rectificación, eliminación, entrega o limitación de determinados tratamientos cuando corresponda.</p>
<p>Para ejercer estos derechos puede utilizar los datos de contacto indicados en esta página.</p>

<h2>Obligación de facilitar datos</h2>
<p>La información marcada como obligatoria en nuestros formularios es necesaria para gestionar correctamente la solicitud. Si no se proporciona, es posible que no podamos responder o prestar el servicio solicitado.</p>

<h2>Modificaciones de esta declaración</h2>
<p>Podemos actualizar esta declaración cuando cambien nuestras actividades, el funcionamiento del sitio, los proveedores utilizados o el marco jurídico aplicable. La versión vigente será la publicada en esta página.</p>
""",

                    "content_fr": """
<h2>Champ d’application</h2>
<p>La présente déclaration explique comment V&V Swiss Services collecte, utilise, conserve et protège les données personnelles lorsqu’une personne consulte ce site internet, envoie une demande de contact, sollicite une visite technique, joint des photographies ou communique avec nous par les moyens mis à disposition.</p>
<p>Cette déclaration est conçue en tenant compte de la législation suisse applicable en matière de protection des données, notamment de la Loi fédérale sur la protection des données.</p>

<h2>Données personnelles que nous pouvons collecter</h2>
<p>Selon la manière dont vous utilisez le site, nous pouvons traiter notamment les catégories de données suivantes :</p>
<ul>
<li>nom et prénom ;</li>
<li>entreprise, lorsqu’elle est indiquée ;</li>
<li>adresse e-mail ;</li>
<li>numéro de téléphone ;</li>
<li>service demandé ;</li>
<li>lieu ou localité du projet ;</li>
<li>contenu du message transmis ;</li>
<li>demande de visite technique ;</li>
<li>date et heure souhaitées pour une visite ;</li>
<li>photographies ou images du projet transmises volontairement ;</li>
<li>langue utilisée ;</li>
<li>adresse IP ;</li>
<li>informations techniques relatives au navigateur ou à l’appareil, notamment le User-Agent ;</li>
<li>date d’acceptation et version de la politique de confidentialité acceptée.</li>
</ul>

<h2>Formulaire de contact</h2>
<p>Lorsque vous utilisez notre formulaire de contact, nous traitons les informations transmises afin d’examiner votre demande, de vous répondre, de préparer éventuellement un devis, d’organiser une visite technique et d’assurer le suivi de votre projet.</p>

<h2>Photographies et pièces jointes</h2>
<p>Lorsque vous joignez des photographies de votre projet, celles-ci sont enregistrées avec votre demande. Nous vous recommandons de ne pas transmettre d’images ou de documents contenant des données personnelles de tiers qui ne seraient pas nécessaires au traitement de votre demande.</p>

<h2>Données techniques et sécurité</h2>
<p>Le site peut enregistrer certaines informations techniques telles que l’adresse IP et les informations relatives au navigateur afin d’assurer la sécurité, le fonctionnement technique, la prévention des abus, le diagnostic des erreurs et la protection de nos systèmes.</p>

<h2>Finalités du traitement</h2>
<p>Les données personnelles peuvent notamment être utilisées afin de :</p>
<ul>
<li>répondre aux demandes d’information ;</li>
<li>préparer des offres et des devis ;</li>
<li>organiser des visites techniques ;</li>
<li>communiquer avec les clients et clients potentiels ;</li>
<li>gérer les demandes et projets ;</li>
<li>assurer la sécurité technique du site ;</li>
<li>respecter les obligations légales et administratives ;</li>
<li>protéger nos droits et documenter les demandes reçues.</li>
</ul>

<h2>E-mail, téléphone et WhatsApp</h2>
<p>Si vous choisissez de communiquer avec nous par e-mail, téléphone ou au moyen d’un lien vers WhatsApp, les données transmises sont traitées afin de gérer la communication et de répondre à votre demande.</p>
<p>Lorsque vous utilisez un service externe tel que WhatsApp, le fournisseur concerné peut traiter certaines informations conformément à ses propres conditions d’utilisation et politiques de confidentialité.</p>

<h2>Google Maps</h2>
<p>Le site peut intégrer un service cartographique tel que Google Maps afin de présenter notre localisation ou notre zone d’intervention. Lors du chargement ou de l’utilisation de ce service, certaines informations techniques peuvent être transmises au fournisseur concerné, qui traite les données selon ses propres règles de confidentialité.</p>

<h2>Cookies et technologies techniques</h2>
<p>Le site peut utiliser des cookies ou technologies similaires nécessaires à son fonctionnement, à sa sécurité, à la gestion des préférences ou aux sessions techniques. Si des outils supplémentaires d’analyse, de publicité ou de suivi nécessitant des mesures particulières d’information ou de consentement sont ajoutés ultérieurement, la présente déclaration et les mécanismes correspondants devront être adaptés.</p>

<h2>Destinataires et prestataires</h2>
<p>Les données peuvent être accessibles à des prestataires techniques ou professionnels lorsque cela est nécessaire pour exploiter le site, héberger l’infrastructure, gérer les communications, maintenir les systèmes, fournir les services ou respecter des obligations légales. Ces destinataires ne reçoivent que les informations nécessaires à leur mission.</p>

<h2>Transferts internationaux</h2>
<p>Certains prestataires technologiques peuvent traiter des données depuis des pays autres que la Suisse. Lorsque des données personnelles sont transférées à l’étranger, les mesures de protection requises par le droit applicable sont mises en œuvre lorsque cela est nécessaire.</p>

<h2>Durée de conservation</h2>
<p>Nous conservons les données personnelles pendant la durée nécessaire au traitement de la demande, à la gestion de la relation commerciale, au respect d’obligations légales ou administratives et à la protection de nos droits. Les données qui ne sont plus nécessaires sont supprimées ou anonymisées lorsque cela est raisonnablement possible et approprié.</p>

<h2>Sécurité</h2>
<p>Nous mettons en œuvre des mesures techniques et organisationnelles raisonnables destinées à protéger les données personnelles contre la perte, l’accès non autorisé, la divulgation, la modification ou l’utilisation abusive. Aucun système électronique ne peut toutefois garantir une sécurité absolue.</p>

<h2>Droits des personnes concernées</h2>
<p>Dans les limites et conditions prévues par le droit applicable, vous pouvez demander des informations sur les données personnelles vous concernant, leur rectification, leur suppression, leur remise ou la limitation de certains traitements lorsque ces droits sont applicables.</p>
<p>Pour exercer vos droits, vous pouvez utiliser les coordonnées indiquées sur cette page.</p>

<h2>Caractère obligatoire de certaines informations</h2>
<p>Les informations signalées comme obligatoires dans nos formulaires sont nécessaires afin de traiter correctement votre demande. Si elles ne sont pas fournies, nous pouvons ne pas être en mesure de répondre ou de fournir le service demandé.</p>

<h2>Modification de la présente déclaration</h2>
<p>Nous pouvons mettre à jour la présente déclaration lorsque nos activités, le fonctionnement du site, les prestataires utilisés ou le cadre juridique applicable évoluent. La version en vigueur est celle publiée sur cette page.</p>
""",

                    "content_de": """
<h2>Geltungsbereich</h2>
<p>Diese Datenschutzerklärung erläutert, wie V&V Swiss Services personenbezogene Daten erhebt, verwendet, aufbewahrt und schützt, wenn eine Person diese Website besucht, eine Kontaktanfrage sendet, eine technische Besichtigung anfragt, Fotografien hochlädt oder über die angebotenen Kontaktwege mit uns kommuniziert.</p>
<p>Diese Erklärung berücksichtigt die anwendbaren schweizerischen Datenschutzvorschriften, insbesondere das Bundesgesetz über den Datenschutz.</p>

<h2>Personenbezogene Daten, die wir bearbeiten können</h2>
<p>Je nach Nutzung der Website können insbesondere folgende Datenkategorien bearbeitet werden:</p>
<ul>
<li>Vor- und Nachname;</li>
<li>Unternehmen, sofern angegeben;</li>
<li>E-Mail-Adresse;</li>
<li>Telefonnummer;</li>
<li>gewünschte Dienstleistung;</li>
<li>Ort oder Standort des Projekts;</li>
<li>Inhalt der übermittelten Nachricht;</li>
<li>Anfrage für eine technische Besichtigung;</li>
<li>gewünschtes Datum und gewünschte Uhrzeit;</li>
<li>freiwillig übermittelte Fotografien oder Bilder des Projekts;</li>
<li>verwendete Sprache;</li>
<li>IP-Adresse;</li>
<li>technische Browser- oder Geräteinformationen, insbesondere der User-Agent;</li>
<li>Zeitpunkt der Zustimmung und Version der akzeptierten Datenschutzerklärung.</li>
</ul>

<h2>Kontaktformular</h2>
<p>Wenn Sie unser Kontaktformular verwenden, bearbeiten wir die übermittelten Daten, um Ihre Anfrage zu prüfen, Ihnen zu antworten, gegebenenfalls eine Offerte vorzubereiten, eine technische Besichtigung zu organisieren und Ihr Projekt weiterzuverfolgen.</p>

<h2>Fotografien und Anhänge</h2>
<p>Wenn Sie Fotografien Ihres Projekts hochladen, werden diese zusammen mit Ihrer Anfrage gespeichert. Bitte übermitteln Sie keine Bilder oder Dokumente mit unnötigen personenbezogenen Daten Dritter.</p>

<h2>Technische Daten und Sicherheit</h2>
<p>Die Website kann technische Informationen wie die IP-Adresse und Browserinformationen erfassen, um die technische Sicherheit, den Betrieb, die Missbrauchsprävention, die Fehlerdiagnose und den Schutz unserer Systeme zu gewährleisten.</p>

<h2>Zwecke der Datenbearbeitung</h2>
<p>Personenbezogene Daten können insbesondere für folgende Zwecke verwendet werden:</p>
<ul>
<li>Beantwortung von Informationsanfragen;</li>
<li>Erstellung von Offerten und Kostenvoranschlägen;</li>
<li>Organisation technischer Besichtigungen;</li>
<li>Kommunikation mit Kunden und Interessenten;</li>
<li>Bearbeitung von Anfragen und Projekten;</li>
<li>Gewährleistung der technischen Sicherheit;</li>
<li>Erfüllung gesetzlicher und administrativer Pflichten;</li>
<li>Schutz unserer Rechte und Dokumentation eingegangener Anfragen.</li>
</ul>

<h2>E-Mail, Telefon und WhatsApp</h2>
<p>Wenn Sie uns per E-Mail, Telefon oder über einen WhatsApp-Link kontaktieren, bearbeiten wir die übermittelten Daten zur Bearbeitung und Beantwortung Ihrer Anfrage.</p>
<p>Bei der Nutzung externer Dienste wie WhatsApp kann der jeweilige Anbieter Daten gemäss seinen eigenen Nutzungsbedingungen und Datenschutzbestimmungen bearbeiten.</p>

<h2>Google Maps</h2>
<p>Die Website kann Kartendienste wie Google Maps integrieren, um unseren Standort oder unser Einsatzgebiet darzustellen. Beim Laden oder Verwenden solcher Dienste können technische Informationen an den jeweiligen Anbieter übertragen werden.</p>

<h2>Cookies und technische Technologien</h2>
<p>Die Website kann Cookies oder vergleichbare Technologien verwenden, die für Betrieb, Sicherheit, Einstellungen oder technische Sitzungen erforderlich sind. Werden künftig zusätzliche Analyse-, Werbe- oder Trackingdienste eingesetzt, die besondere Informations- oder Einwilligungsmassnahmen erfordern, werden diese Datenschutzerklärung und die entsprechenden Mechanismen angepasst.</p>

<h2>Empfänger und Dienstleister</h2>
<p>Technische oder professionelle Dienstleister können Zugang zu Daten erhalten, soweit dies für den Betrieb der Website, das Hosting, die Kommunikation, die Wartung von Systemen, die Leistungserbringung oder die Erfüllung gesetzlicher Verpflichtungen erforderlich ist.</p>

<h2>Internationale Datenübermittlungen</h2>
<p>Einzelne Technologieanbieter können Daten ausserhalb der Schweiz bearbeiten. Bei internationalen Übermittlungen werden die nach anwendbarem Recht erforderlichen Schutzmassnahmen getroffen, sofern dies notwendig ist.</p>

<h2>Aufbewahrungsdauer</h2>
<p>Personenbezogene Daten werden so lange aufbewahrt, wie dies für die Bearbeitung einer Anfrage, die Geschäftsbeziehung, gesetzliche oder administrative Pflichten oder den Schutz unserer Rechte erforderlich ist. Nicht mehr benötigte Daten werden gelöscht oder anonymisiert, soweit dies vernünftigerweise möglich und angemessen ist.</p>

<h2>Sicherheit</h2>
<p>Wir treffen angemessene technische und organisatorische Massnahmen, um personenbezogene Daten vor Verlust, unbefugtem Zugriff, Offenlegung, Veränderung und missbräuchlicher Verwendung zu schützen. Eine absolute Sicherheit elektronischer Systeme kann jedoch nicht gewährleistet werden.</p>

<h2>Rechte betroffener Personen</h2>
<p>Im Rahmen der anwendbaren gesetzlichen Voraussetzungen können Sie Auskunft über Ihre personenbezogenen Daten sowie deren Berichtigung, Löschung, Herausgabe oder die Einschränkung bestimmter Bearbeitungen verlangen.</p>
<p>Zur Ausübung Ihrer Rechte können Sie die auf dieser Seite angegebenen Kontaktdaten verwenden.</p>

<h2>Erforderliche Angaben</h2>
<p>Als Pflichtfelder gekennzeichnete Angaben sind erforderlich, damit wir Ihre Anfrage ordnungsgemäss bearbeiten können. Ohne diese Angaben können wir möglicherweise nicht antworten oder die gewünschte Leistung erbringen.</p>

<h2>Änderungen dieser Datenschutzerklärung</h2>
<p>Wir können diese Datenschutzerklärung aktualisieren, wenn sich unsere Tätigkeiten, die Website, eingesetzte Dienstleister oder die anwendbaren rechtlichen Rahmenbedingungen ändern. Es gilt die jeweils auf dieser Seite veröffentlichte Fassung.</p>
""",

                    "content_it": """
<h2>Ambito di applicazione</h2>
<p>La presente informativa spiega come V&V Swiss Services raccoglie, utilizza, conserva e protegge i dati personali quando una persona visita questo sito, invia una richiesta di contatto, richiede una visita tecnica, allega fotografie o comunica con noi attraverso i canali messi a disposizione.</p>
<p>La presente informativa è predisposta tenendo conto della normativa svizzera applicabile in materia di protezione dei dati, in particolare della Legge federale sulla protezione dei dati.</p>

<h2>Dati personali che possiamo trattare</h2>
<p>A seconda dell’utilizzo del sito, possiamo trattare le seguenti categorie di dati:</p>
<ul>
<li>nome e cognome;</li>
<li>azienda, se indicata;</li>
<li>indirizzo e-mail;</li>
<li>numero di telefono;</li>
<li>servizio richiesto;</li>
<li>luogo o località del progetto;</li>
<li>contenuto del messaggio;</li>
<li>richiesta di visita tecnica;</li>
<li>data e ora preferite;</li>
<li>fotografie o immagini del progetto inviate volontariamente;</li>
<li>lingua utilizzata;</li>
<li>indirizzo IP;</li>
<li>informazioni tecniche del browser o del dispositivo, incluso lo User-Agent;</li>
<li>data di accettazione e versione dell’informativa sulla privacy accettata.</li>
</ul>

<h2>Modulo di contatto</h2>
<p>Quando utilizza il nostro modulo di contatto, trattiamo le informazioni fornite per analizzare la richiesta, rispondere, predisporre eventualmente un preventivo, organizzare una visita tecnica e seguire il progetto.</p>

<h2>Fotografie e allegati</h2>
<p>Le fotografie allegate al progetto vengono memorizzate insieme alla richiesta. Raccomandiamo di non inviare immagini o documenti contenenti dati personali di terzi non necessari.</p>

<h2>Dati tecnici e sicurezza</h2>
<p>Il sito può registrare informazioni tecniche quali indirizzo IP e dati del browser per finalità di sicurezza, funzionamento tecnico, prevenzione degli abusi, diagnosi degli errori e protezione dei sistemi.</p>

<h2>Finalità del trattamento</h2>
<p>I dati personali possono essere utilizzati per:</p>
<ul>
<li>rispondere alle richieste di informazioni;</li>
<li>preparare offerte e preventivi;</li>
<li>organizzare visite tecniche;</li>
<li>comunicare con clienti e potenziali clienti;</li>
<li>gestire richieste e progetti;</li>
<li>garantire la sicurezza tecnica del sito;</li>
<li>adempiere obblighi legali e amministrativi;</li>
<li>proteggere i nostri diritti e documentare le richieste ricevute.</li>
</ul>

<h2>E-mail, telefono e WhatsApp</h2>
<p>Se sceglie di contattarci tramite e-mail, telefono o un collegamento a WhatsApp, i dati trasmessi vengono trattati per gestire la comunicazione e rispondere alla richiesta.</p>
<p>Quando utilizza servizi esterni come WhatsApp, il relativo fornitore può trattare determinate informazioni secondo le proprie condizioni e politiche sulla privacy.</p>

<h2>Google Maps</h2>
<p>Il sito può integrare servizi cartografici come Google Maps per mostrare la nostra posizione o area di intervento. Quando tali servizi vengono caricati o utilizzati, alcune informazioni tecniche possono essere trasmesse al relativo fornitore.</p>

<h2>Cookie e tecnologie tecniche</h2>
<p>Il sito può utilizzare cookie o tecnologie analoghe necessarie per il funzionamento, la sicurezza, le preferenze o le sessioni tecniche. Qualora in futuro vengano introdotti strumenti aggiuntivi di analisi, pubblicità o tracciamento che richiedano specifiche misure informative o di consenso, la presente informativa e i relativi meccanismi saranno adeguati.</p>

<h2>Destinatari e fornitori</h2>
<p>I dati possono essere accessibili a fornitori tecnici o professionali quando ciò è necessario per il funzionamento del sito, l’hosting, le comunicazioni, la manutenzione dei sistemi, la fornitura dei servizi o l’adempimento di obblighi legali.</p>

<h2>Trasferimenti internazionali</h2>
<p>Alcuni fornitori tecnologici possono trattare dati al di fuori della Svizzera. In caso di trasferimenti internazionali saranno adottate, quando necessario, le misure di protezione previste dalla normativa applicabile.</p>

<h2>Conservazione dei dati</h2>
<p>I dati personali vengono conservati per il tempo necessario alla gestione della richiesta, della relazione commerciale, degli obblighi legali o amministrativi e alla tutela dei nostri diritti. I dati non più necessari vengono eliminati o anonimizzati quando ciò è ragionevolmente possibile e appropriato.</p>

<h2>Sicurezza</h2>
<p>Adottiamo misure tecniche e organizzative ragionevoli per proteggere i dati personali da perdita, accesso non autorizzato, divulgazione, modifica o uso improprio. Nessun sistema elettronico può tuttavia garantire una sicurezza assoluta.</p>

<h2>Diritti degli interessati</h2>
<p>Nei limiti e alle condizioni previste dalla normativa applicabile, può richiedere informazioni sui propri dati personali, la loro rettifica, cancellazione, consegna o la limitazione di determinati trattamenti.</p>
<p>Per esercitare tali diritti può utilizzare i dati di contatto indicati in questa pagina.</p>

<h2>Dati obbligatori</h2>
<p>Le informazioni indicate come obbligatorie nei nostri moduli sono necessarie per gestire correttamente la richiesta. In loro assenza potremmo non essere in grado di rispondere o fornire il servizio richiesto.</p>

<h2>Modifiche della presente informativa</h2>
<p>Possiamo aggiornare questa informativa quando cambiano le nostre attività, il funzionamento del sito, i fornitori utilizzati o il quadro giuridico applicabile. Fa fede la versione pubblicata su questa pagina.</p>
""",

                    "content_en": """
<h2>Scope</h2>
<p>This privacy policy explains how V&V Swiss Services collects, uses, retains and protects personal data when a person visits this website, submits a contact request, requests a technical visit, uploads photographs or communicates with us through the available contact channels.</p>
<p>This policy has been prepared with the applicable Swiss data protection framework in mind, including the Swiss Federal Act on Data Protection.</p>

<h2>Personal data we may collect</h2>
<p>Depending on how you use the website, we may process the following categories of information:</p>
<ul>
<li>first and last name;</li>
<li>company, where provided;</li>
<li>email address;</li>
<li>telephone number;</li>
<li>requested service;</li>
<li>project location;</li>
<li>content of the submitted message;</li>
<li>technical visit request;</li>
<li>preferred date and time;</li>
<li>photographs or images of the project voluntarily uploaded;</li>
<li>language used;</li>
<li>IP address;</li>
<li>technical browser or device information, including the User-Agent;</li>
<li>date of acceptance and version of the accepted privacy policy.</li>
</ul>

<h2>Contact form</h2>
<p>When you use our contact form, we process the information provided in order to review your request, reply to you, prepare a quotation where appropriate, organise a technical visit and follow up on your project.</p>

<h2>Photographs and attachments</h2>
<p>When you upload photographs of your project, they are stored together with your request. We recommend that you do not upload images or documents containing unnecessary personal data relating to third parties.</p>

<h2>Technical data and security</h2>
<p>The website may record technical information such as IP addresses and browser information for security, technical operation, abuse prevention, troubleshooting and system protection purposes.</p>

<h2>Purposes of processing</h2>
<p>Personal data may be used to:</p>
<ul>
<li>respond to information requests;</li>
<li>prepare quotations and offers;</li>
<li>organise technical visits;</li>
<li>communicate with clients and prospective clients;</li>
<li>manage requests and projects;</li>
<li>ensure the technical security of the website;</li>
<li>comply with legal and administrative obligations;</li>
<li>protect our rights and document requests received.</li>
</ul>

<h2>Email, telephone and WhatsApp</h2>
<p>If you choose to contact us by email, telephone or through a WhatsApp link, the information transmitted will be processed to manage the communication and respond to your request.</p>
<p>When using an external service such as WhatsApp, the relevant provider may process certain information under its own terms and privacy policies.</p>

<h2>Google Maps</h2>
<p>The website may integrate mapping services such as Google Maps to display our location or service area. When such services are loaded or used, certain technical information may be transmitted to the relevant provider.</p>

<h2>Cookies and technical technologies</h2>
<p>The website may use cookies or similar technologies that are technically necessary for operation, security, preferences or session management. If additional analytics, advertising or tracking tools requiring specific notice or consent measures are introduced in the future, this policy and the corresponding mechanisms will be updated accordingly.</p>

<h2>Recipients and service providers</h2>
<p>Personal data may be accessible to technical or professional service providers where necessary to operate the website, host infrastructure, manage communications, maintain systems, provide services or comply with legal obligations. Such recipients receive only the information required for their respective tasks.</p>

<h2>International transfers</h2>
<p>Certain technology providers may process data from countries outside Switzerland. Where international transfers occur, the safeguards required by applicable law will be implemented where necessary.</p>

<h2>Retention</h2>
<p>We retain personal data for as long as necessary to process requests, manage the business relationship, comply with legal or administrative obligations and protect our rights. Data that is no longer required is deleted or anonymised where reasonably possible and appropriate.</p>

<h2>Security</h2>
<p>We implement reasonable technical and organisational measures designed to protect personal data against loss, unauthorised access, disclosure, alteration or misuse. No electronic system can, however, guarantee absolute security.</p>

<h2>Your rights</h2>
<p>Subject to the conditions and limitations of applicable law, you may request information about your personal data, its correction, deletion, delivery or the restriction of certain processing activities where applicable.</p>
<p>You may use the contact details displayed on this page to exercise your rights.</p>

<h2>Required information</h2>
<p>Information marked as mandatory in our forms is required in order to process your request properly. If it is not provided, we may be unable to respond or provide the requested service.</p>

<h2>Changes to this policy</h2>
<p>We may update this policy when our activities, the operation of the website, the service providers used or the applicable legal framework change. The version published on this page is the current version.</p>
""",

                    "is_active": True,
                    "is_indexable": True,
                },
            },
        ]

        self.stdout.write("")
        self.stdout.write(self.style.MIGRATE_HEADING("V&V Swiss Services · Páginas legales"))
        self.stdout.write("")

        for page_data in legal_pages:
            page, created = InstitutionalPage.objects.update_or_create(slug_fr=page_data["slug_fr"], defaults=page_data["defaults"])

            if created:
                self.stdout.write(self.style.SUCCESS(f"CREADA: {page.title_fr}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"ACTUALIZADA: {page.title_fr}"))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Páginas legales creadas/actualizadas correctamente."))
        self.stdout.write("")