from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("calculators/", views.calculators_index, name="calculators_index"),
    path("calculators/<slug:slug>/", views.calculator_detail, name="calculator_detail"),
    path("categories/<slug:slug>/", views.category_detail, name="category_detail"),
    path("guides/<slug:slug>/", views.guide_detail, name="guide_detail"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("privacy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),
]
