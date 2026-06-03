from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('',           views.DashboardHomeView.as_view(),      name='home'),
    path('products/',  views.DashboardProductsView.as_view(),  name='products'),
    path('orders/',    views.DashboardOrdersView.as_view(),    name='orders'),
    path('quotes/',    views.DashboardQuotesView.as_view(),    name='quotes'),
    path('contacts/',  views.DashboardContactsView.as_view(),  name='contacts'),
    path('analytics/', views.DashboardAnalyticsView.as_view(), name='analytics'),
]