from django.urls import path

from hello import views

# URL routes for the main pages in the hello app.
urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("reviews/", views.review, name="review"),
    path("product/", views.product, name="product"),
]