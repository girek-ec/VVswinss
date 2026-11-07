from django.test import TestCase
from django.urls import reverse
from django.utils import translation
from .models import ProfessionalSitePage, ProfessionalNeedItem


class ProfessionalsV2Tests(TestCase):
    def setUp(self):
        self.page = ProfessionalSitePage.objects.create(slug="main", hero_title_fr="Solutions pour professionnels")

    def test_all_public_language_routes(self):
        for lang in ("fr", "de", "it", "en"):
            with self.subTest(language=lang), translation.override(lang):
                response = self.client.get(reverse("core:professionals"))
                self.assertEqual(response.status_code, 200)

    def test_new_models_render(self):
        ProfessionalNeedItem.objects.create(page=self.page, key="coordination", title_fr="Coordination de plusieurs corps de métier", order=1)
        with translation.override("fr"):
            response = self.client.get(reverse("core:professionals"))
        self.assertContains(response, "Coordination de plusieurs corps de métier")
