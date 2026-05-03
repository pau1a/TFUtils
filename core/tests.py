from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


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

    def test_admin_tools_dashboard_is_staff_only(self):
        url = reverse("admin_tools_index")
        readiness_url = reverse("admin_tools_adsense_readiness")

        anonymous = self.client.get(url)
        self.assertEqual(anonymous.status_code, 302)
        self.assertIn("/admin/login/", anonymous["Location"])

        user_model = get_user_model()
        normal_user = user_model.objects.create_user(username="normal", password="testpass123")
        self.client.force_login(normal_user)
        normal_response = self.client.get(url)
        self.assertEqual(normal_response.status_code, 302)
        self.assertIn("/admin/login/", normal_response["Location"])

        staff_user = user_model.objects.create_user(
            username="staff",
            password="testpass123",
            is_staff=True,
            is_superuser=True,
        )
        self.client.force_login(staff_user)
        staff_response = self.client.get(url)
        self.assertEqual(staff_response.status_code, 200)
        self.assertContains(staff_response, "Technofatty Tools")
        self.assertContains(staff_response, "AdSense Readiness")
        self.assertContains(staff_response, "Content Inventory")
        self.assertContains(staff_response, readiness_url)

        admin_response = self.client.get(reverse("admin:index"))
        self.assertEqual(admin_response.status_code, 200)
        self.assertContains(admin_response, "Technofatty Tools")
        self.assertContains(admin_response, readiness_url)
        self.assertContains(admin_response, reverse("admin_tools_content_inventory"))
        self.assertNotContains(admin_response, ">Admin tools<")

        readiness_response = self.client.get(readiness_url)
        self.assertEqual(readiness_response.status_code, 200)
        self.assertContains(readiness_response, "AdSense Readiness Dashboard")
        self.assertContains(readiness_response, 'id="nav-sidebar"')
        self.assertContains(readiness_response, "Technofatty Tools")
        self.assertContains(readiness_response, "Authentication and Authorization")
        self.assertContains(readiness_response, "View site")
        self.assertNotContains(readiness_response, ">Admin tools<")

        for route_name in [
            "admin_tools_content_inventory",
            "admin_tools_seo_metadata",
            "admin_tools_ymyl_safety",
            "admin_tools_internal_links",
        ]:
            queued_response = self.client.get(reverse(route_name))
            self.assertEqual(queued_response.status_code, 200)
            self.assertContains(queued_response, "Technofatty Tools")
