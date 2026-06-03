from django.urls import path
from . import views

app_name="categories"
urlpatterns=[
    path("", views.CategoryListView.as_view(), name="list"),
    path("brand/<slug:slug>/", views.BrandDetailView.as_view(), name="brand"),
    path("<slug:slug>", views.CategoryDetailView.as_view(), name="detail"),
]