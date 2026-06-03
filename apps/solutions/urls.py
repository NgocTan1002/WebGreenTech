from django.urls import path
from . import views

app_name = "solutions"
urlpatterns = [
    path("", views.SolutionListView.as_view(), name="list"),
    path('category/<slug:category_slug>/', views.SolutionListView.as_view(), name='by_category'),
    path("<slug:slug>/", views.SolutionDetailView.as_view(), name="detail"),
]