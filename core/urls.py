from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("calculators/", views.calculators_index, name="calculators_index"),
    path("admin-tools/", views.admin_tools_index, name="admin_tools_index"),
    path("admin-tools/adsense-readiness/", views.admin_tools_adsense_readiness, name="admin_tools_adsense_readiness"),
    path("admin-tools/content-inventory/", views.admin_tools_content_inventory, name="admin_tools_content_inventory"),
    path("admin-tools/seo-metadata/", views.admin_tools_seo_metadata, name="admin_tools_seo_metadata"),
    path("admin-tools/ymyl-safety/", views.admin_tools_ymyl_safety, name="admin_tools_ymyl_safety"),
    path("admin-tools/internal-links/", views.admin_tools_internal_links, name="admin_tools_internal_links"),
    path("calculators/random/", views.random_calculator, name="random_calculator"),
    path("calculators/<slug:slug>/", views.calculator_detail, name="calculator_detail"),
    path("categories/<slug:slug>/", views.category_detail, name="category_detail"),
    path("ask-podge/", views.ask_podge, name="ask_podge"),
    path("guides/<slug:slug>/", views.guide_detail, name="guide_detail"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("privacy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path("ads.txt", views.ads_txt, name="ads_txt"),
    path("sitemap.xml", views.sitemap_xml, name="sitemap_xml"),
]
