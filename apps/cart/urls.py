from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path("", views.CartDetailView.as_view(), name="detail"),
    path("add/", views.CartAddView.as_view(), name="add"),
    path("add/<slug:slug>/", views.CartAddView.as_view(), name="add_product"),
    path("update/<int:item_id>/", views.CartUpdateView.as_view(), name="update"),
    path("remove/<int:item_id>/", views.CartRemoveView.as_view(), name="remove"),
    path("clear/", views.CartClearView.as_view(), name="clear"),
]