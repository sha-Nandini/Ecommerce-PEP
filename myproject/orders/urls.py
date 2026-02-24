
from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('place/', views.place_order, name='place_order'),
    path('history/', views.order_history, name='order_history'),
    path('track/<int:order_id>/', views.order_tracking, name='order_tracking'),
    path('detail/<int:order_id>/', views.order_detail, name='order_detail'),
]
