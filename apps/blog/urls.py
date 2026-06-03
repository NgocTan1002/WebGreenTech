from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path("", views.PostListView.as_view(), name="list"),
    path("search/", views.PostSearchView.as_view(), name="search"),
    path("category/<slug:category_slug>/", views.CategoryPostListView.as_view(), name="category"),
    path("<slug:slug>/", views.PostDetailView.as_view(), name="detail"),
]