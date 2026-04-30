from django.test import TestCase
from django.urls import reverse


class SiteRoutesTests(TestCase):
    def test_homepage_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Technofatty")

    def test_random_calculator_redirects_to_tool_page(self):
        response = self.client.get(reverse("random_calculator"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/calculators/", response["Location"])

    def test_ask_podge_page_loads(self):
        response = self.client.get(reverse("ask_podge"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Start with the awkward question")

    def test_live_calculator_pages_load(self):
        slugs = [
            "percentage-change-calculator",
            "vat-calculator",
            "room-area-calculator",
            "days-between-dates",
            "should-i-send-that-message-gauge",
            "main-character-risk-calculator",
            "subscription-shame-index",
            "vaguepost-decoder",
            "parent-phone-hypocrisy-meter",
            "fake-fan-detector",
            "parental-phone-treaty-generator",
            "fancy-version-justification-engine",
            "future-embarrassment-gauge",
            "sale-suspicion-gauge",
        ]
        for slug in slugs:
            with self.subTest(slug=slug):
                response = self.client.get(reverse("calculator_detail", args=[slug]))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Answer crunched")

    def test_missing_calculator_returns_404(self):
        response = self.client.get(reverse("calculator_detail", args=["not-a-real-tool"]))
        self.assertEqual(response.status_code, 404)

    def test_category_page_shows_live_tools(self):
        response = self.client.get(reverse("category_detail", args=["money"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "VAT Engine")
        self.assertContains(response, "Percentage Change Engine")
