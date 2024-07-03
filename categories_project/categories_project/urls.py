from django.contrib import admin
from django.urls import path, include
from categories.views import main_page

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", main_page, name="main-page"),
    path("api/", include("categories.urls")),
]
