from django.urls import path
from .views import checkout, OrderList

urlpatterns = [
    path('checkout/', checkout),
    path('orders/', OrderList.as_view()),
]
