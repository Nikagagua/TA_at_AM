from django.urls import path
from .views import CategoryCreateView, CategoryDetailView

urlpatterns = [
    path("categories/", CategoryCreateView.as_view(), name="category-create"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
]
