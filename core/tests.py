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
            "astroturf-detector",
            "algorithm-tax-calculator",
            "ai-emotional-dependency-gauge",
            "should-i-be-proud-of-this-plate",
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
        self.assertContains(response, "What this category does")

    def test_calculators_index_shows_newer_live_tools(self):
        response = self.client.get(reverse("calculators_index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Should I Be Proud Of This Plate?")
        self.assertContains(response, "AI Emotional Dependency Gauge")

    def test_new_guide_pages_have_real_sections(self):
        response = self.client.get(reverse("guide_detail", args=["how-to-spot-fake-hype-online"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Real excitement is usually messier")
        self.assertContains(response, "Fake Fan Detector")

    def test_robots_and_sitemap_load(self):
        robots = self.client.get(reverse("robots_txt"))
        self.assertEqual(robots.status_code, 200)
        self.assertContains(robots, "Sitemap: https://technofatty.com/sitemap.xml")

        ads = self.client.get(reverse("ads_txt"))
        self.assertEqual(ads.status_code, 200)
        self.assertContains(ads, "real publisher ID")

        sitemap = self.client.get(reverse("sitemap_xml"))
        self.assertEqual(sitemap.status_code, 200)
        self.assertContains(sitemap, "https://technofatty.com/calculators/should-i-be-proud-of-this-plate/")
        self.assertContains(sitemap, "https://technofatty.com/guides/how-to-spot-fake-hype-online/")
        self.assertContains(sitemap, "https://technofatty.com/privacy/")
