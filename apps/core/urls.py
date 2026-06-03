from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = "core"
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('autocomplete/', views.autocomplete_view, name='autocomplete'),
    path(
        'chinh-sach-bao-hanh.html',
        TemplateView.as_view(template_name='policies/warranty.html'),
        name='policy_warranty',
    ),
    path(
        'chinh-sach-van-chuyen.html',
        TemplateView.as_view(template_name='policies/shipping.html'),
        name='policy_shipping',
    ),
    path(
        'chinh-sach-doi-tra.html',
        TemplateView.as_view(template_name='policies/returns.html'),
        name='policy_returns',
    ),
    path(
        'chinh-sach-bao-mat.html',
        TemplateView.as_view(template_name='policies/privacy.html'),
        name='policy_privacy',
    ),
]
