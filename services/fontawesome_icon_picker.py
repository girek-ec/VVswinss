"""Font Awesome icon picker for the Django Services admin (English only).
Existing CSS classes stay unchanged. No database or model migrations.
"""
from django import forms

# ICON CATALOG | (Category, display name, Font Awesome class, search keywords)
ICON_CATALOG = (
    ('Buildings', 'House', 'fa-solid fa-house', 'house home residential property dwelling'),
    ('Buildings', 'House with chimney', 'fa-solid fa-house-chimney', 'home house chimney residential housing'),
    ('Buildings', 'Building', 'fa-solid fa-building', 'building apartment property estate housing'),
    ('Buildings', 'City', 'fa-solid fa-city', 'city urban buildings skyline'),
    ('Buildings', 'Hotel', 'fa-solid fa-hotel', 'hotel accommodation residence hospitality'),
    ('Buildings', 'Office', 'fa-solid fa-briefcase', 'office business company workplace'),
    ('Buildings', 'Closed door', 'fa-solid fa-door-closed', 'door closed entrance entry access'),
    ('Buildings', 'Open door', 'fa-solid fa-door-open', 'door open entrance exit access'),
    ('Buildings', 'Window (grid)', 'fa-solid fa-table-cells-large', 'window glass glazing panes grid'),
    ('Buildings', 'Stairs', 'fa-solid fa-stairs', 'stairs steps staircase access'),
    ('Buildings', 'Location', 'fa-solid fa-location-dot', 'location address map pin place'),
    ('Buildings', 'Map', 'fa-solid fa-map', 'map location directions area site'),
    ('Construction', 'Hammer', 'fa-solid fa-hammer', 'hammer building construction repair works'),
    ('Construction', 'Tools', 'fa-solid fa-screwdriver-wrench', 'hand tools maintenance repair renovation'),
    ('Construction', 'Wrench', 'fa-solid fa-wrench', 'wrench spanner repair maintenance plumbing'),
    ('Construction', 'Screwdriver', 'fa-solid fa-screwdriver', 'screwdriver tool fixing installation'),
    ('Construction', 'Toolbox', 'fa-solid fa-toolbox', 'toolbox tools hardware maintenance construction'),
    ('Construction', 'Safety helmet', 'fa-solid fa-helmet-safety', 'safety helmet hard hat protection site'),
    ('Construction', 'Construction worker', 'fa-solid fa-person-digging', 'construction worker builder worksite masonry'),
    ('Construction', 'Ruler', 'fa-solid fa-ruler', 'ruler measuring dimensions measurement'),
    ('Construction', 'Ruler and square', 'fa-solid fa-ruler-combined', 'ruler square measurement floor plan dimensions'),
    ('Construction', 'Drafting compass', 'fa-solid fa-compass-drafting', 'drafting compass architecture design blueprints plans'),
    ('Construction', 'Cube', 'fa-solid fa-cube', 'cube blocks building materials structure'),
    ('Construction', 'Blocks', 'fa-solid fa-cubes', 'blocks masonry materials bricks construction'),
    ('Construction', 'Layers', 'fa-solid fa-layer-group', 'layers insulation cladding coating drywall'),
    ('Construction', 'Gear', 'fa-solid fa-gear', 'gear mechanism machinery maintenance operation'),
    ('Finishes', 'Paint roller', 'fa-solid fa-paint-roller', 'paint roller painting walls finishing coating'),
    ('Finishes', 'Paintbrush', 'fa-solid fa-paintbrush', 'paintbrush painting decorating wall finish'),
    ('Finishes', 'Brush', 'fa-solid fa-brush', 'brush painting decorating finishing'),
    ('Finishes', 'Colour palette', 'fa-solid fa-palette', 'colour palette design decoration painting'),
    ('Finishes', 'Droplet', 'fa-solid fa-droplet', 'droplet water humidity moisture leaks'),
    ('Finishes', 'Water', 'fa-solid fa-water', 'water moisture dampness liquid humidity'),
    ('Finishes', 'Tiles (grid)', 'fa-solid fa-border-all', 'tiles grid tiling ceramic floor bathroom'),
    ('Finishes', 'Wall (outline)', 'fa-solid fa-border-none', 'wall outline partition renovation drywall'),
    ('Insulation', 'Thermometer', 'fa-solid fa-temperature-half', 'heat temperature thermometer thermal insulation'),
    ('Insulation', 'Snowflake', 'fa-solid fa-snowflake', 'snow cold winter frost insulation'),
    ('Insulation', 'Sun', 'fa-solid fa-sun', 'sun sunlight heat thermal energy'),
    ('Insulation', 'Wind', 'fa-solid fa-wind', 'wind air ventilation airflow insulation'),
    ('Insulation', 'Leaf', 'fa-solid fa-leaf', 'leaf sustainability green ecology energy'),
    ('Insulation', 'Tree', 'fa-solid fa-tree', 'tree environment nature ecology sustainability'),
    ('Insulation', 'Protective shield', 'fa-solid fa-shield-halved', 'protective shield safety insulation protection'),
    ('Insulation', 'Fire', 'fa-solid fa-fire', 'fire heat resistance fireproof safety'),
    ('Insulation', 'Energy', 'fa-solid fa-bolt', 'energy power electricity efficiency consumption'),
    ('Insulation', 'Performance gauge', 'fa-solid fa-gauge-high', 'performance gauge efficiency meter monitoring'),
    ('Cleaning', 'Broom', 'fa-solid fa-broom', 'broom cleaning post construction site cleaning'),
    ('Cleaning', 'Soap', 'fa-solid fa-soap', 'soap washing cleaning sanitation'),
    ('Cleaning', 'Spray can', 'fa-solid fa-spray-can-sparkles', 'spray cleaner cleaning disinfecting surfaces'),
    ('Cleaning', 'Sparkles', 'fa-solid fa-sparkles', 'sparkles shine clean polishing cleanliness'),
    ('Cleaning', 'Bucket', 'fa-solid fa-bucket', 'bucket pail cleaning washing equipment'),
    ('Cleaning', 'Recycling', 'fa-solid fa-recycle', 'recycling waste environment eco disposal'),
    ('Cleaning', 'Waste bin', 'fa-solid fa-trash-can', 'waste bin trash rubbish garbage cleaning'),
    ('Cleaning', 'Handwashing', 'fa-solid fa-hands-bubbles', 'handwashing hygiene cleanliness hand wash'),
    ('Management', 'Checked checklist', 'fa-solid fa-clipboard-check', 'checked checklist inspection quality control'),
    ('Management', 'Task list', 'fa-solid fa-list-check', 'task list scheduling planning management'),
    ('Management', 'Document', 'fa-solid fa-file-lines', 'document report file paperwork documentation'),
    ('Management', 'Checklist', 'fa-solid fa-clipboard-list', 'checklist clipboard tasks supervision management'),
    ('Management', 'Calendar', 'fa-solid fa-calendar-days', 'calendar schedule dates appointment planning'),
    ('Management', 'Clock', 'fa-solid fa-clock', 'clock time punctuality working hours deadlines'),
    ('Management', 'Team', 'fa-solid fa-users', 'team people staff workers crew group'),
    ('Management', 'User', 'fa-solid fa-user', 'user client customer person account'),
    ('Management', 'Handshake', 'fa-solid fa-handshake', 'handshake trust agreement partnership contract'),
    ('Management', 'Medal', 'fa-solid fa-medal', 'medal certificate quality award excellence'),
    ('Management', 'Award', 'fa-solid fa-award', 'award excellence achievement quality recognition'),
    ('Management', 'Star', 'fa-solid fa-star', 'star rating review quality satisfaction'),
    ('Management', 'Verified', 'fa-solid fa-circle-check', 'verified approval confirmed completed checked'),
    ('Management', 'Shield', 'fa-solid fa-shield', 'shield security protection insurance safety'),
    ('Management', 'Truck', 'fa-solid fa-truck', 'truck transportation logistics delivery supplies'),
    ('Management', 'Fast delivery', 'fa-solid fa-truck-fast', 'fast delivery express shipping transportation logistics'),
    ('Contact', 'Phone', 'fa-solid fa-phone', 'phone call telephone contact support'),
    ('Contact', 'Envelope', 'fa-solid fa-envelope', 'email envelope message mail contact'),
    ('Contact', 'Comment', 'fa-solid fa-comment-dots', 'comment feedback message inquiry review'),
    ('Contact', 'Messages', 'fa-solid fa-comments', 'messages communication conversations chat support'),
    ('Contact', 'Information', 'fa-solid fa-circle-info', 'information help assistance details guidance'),
    ('Contact', 'Question', 'fa-solid fa-circle-question', 'question help faq frequently asked questions'),
    ('Contact', 'Link', 'fa-solid fa-link', 'link website url hyperlink online'),
    ('Contact', 'Globe', 'fa-solid fa-globe', 'globe internet web world languages translation'),
    ('Masonry', 'Bricks and trowel', 'fa-solid fa-trowel-bricks', 'bricks trowel masonry bricklaying wall construction'),
    ('Masonry', 'Mason', 'fa-solid fa-person-digging', 'mason bricklayer builder construction worksite'),
    ('Masonry', 'Materials', 'fa-solid fa-cubes', 'materials building blocks bricks construction'),
    ('Masonry', 'Hammer', 'fa-solid fa-hammer', 'hammer tools construction masonry worksite'),
    ('Thermal insulation', 'Temperature', 'fa-solid fa-temperature-half', 'temperature warm cold thermal heat insulation'),
    ('Thermal insulation', 'Layers', 'fa-solid fa-layer-group', 'layers insulation cladding thermal wall protection'),
    ('Thermal insulation', 'Energy efficiency', 'fa-solid fa-leaf', 'energy efficiency sustainable insulation saving'),
    ('Painting', 'Paint roller', 'fa-solid fa-paint-roller', 'paint roller painting wall decorating finishes'),
    ('Painting', 'Paintbrush', 'fa-solid fa-paintbrush', 'paintbrush painting finishes coating decoration'),
    ('Painting', 'Colours', 'fa-solid fa-palette', 'colours colour palette painting decorating design'),
    ('Property management', 'Managed building', 'fa-solid fa-building', 'managed building property estate apartments facilities'),
    ('Property management', 'Inspection', 'fa-solid fa-clipboard-check', 'inspection assessment control maintenance checklist'),
    ('Property management', 'Keys', 'fa-solid fa-key', 'keys access property tenancy locks management'),

)


class FontAwesomeIconPickerWidget(forms.TextInput):
    """Text input with an English-only visual icon gallery."""
    template_name = "services/admin/widgets/fontawesome_icon_picker_en.html"

    class Media:
        css = {"all": (
            "antra/assets/css/fontawesome.min.css",
            "services/admin/fontawesome_icon_picker.css",
        )}
        js = ("services/admin/fontawesome_icon_picker_en.js",)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        widget = context["widget"]
        css = widget["attrs"].get("class", "")
        widget["attrs"]["class"] = (css + " vv-fa-class-input").strip()
        widget["catalog"] = (
            {"category": group, "label": label, "css": css_class, "keywords": keywords}
            for group, label, css_class, keywords in ICON_CATALOG
        )
        widget["categories"] = tuple(dict.fromkeys(item[0] for item in ICON_CATALOG))
        return context


class FontAwesomeIconPickerMixin:
    """Enhance the existing icon CharField without affecting other fields."""

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "icon":
            kwargs["widget"] = FontAwesomeIconPickerWidget
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == "icon" and formfield is not None:
            formfield.label = "Icon"
            # Replaces legacy model help text in the Admin only.
            formfield.help_text = "Select an icon or enter its Font Awesome CSS class."
        return formfield
