from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('confirmation/<str:order_number>/', views.OrderConfirmationView.as_view(), name='confirmation'),
    path('my-orders/', views.OrderListView.as_view(), name='list'),
    path('my-orders/<str:order_number>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('quote/', views.QuoteRequestView.as_view(), name='quote_request'),
    path('quote/success/', views.QuoteSuccessView.as_view(), name='quote_success'),
]
