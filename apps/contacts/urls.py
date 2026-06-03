from django.urls import path
from . import views
 
app_name = 'contacts'
urlpatterns = [
    path('',              views.ContactView.as_view(),      name='contact'),
    path('success/',      views.ContactSuccessView.as_view(), name='success'),
    path('demo/',         views.DemoRequestView.as_view(),  name='demo_request'),
    path('demo/success/', views.DemoSuccessView.as_view(),  name='demo_success'),
]