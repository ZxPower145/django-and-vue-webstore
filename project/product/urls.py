from django.urls import path, include
from .views import *

urlpatterns = [
    path('latest-products/', LatestProductsList.as_view()),
    path('products/all', AllProducts.as_view()),
    path('products/search', search),
    path('products/<slug:category_slug>/<slug:product_slug>/', ProductDetail.as_view()),
    path('products/<slug:category_slug>/', CategoryDetail.as_view()),
    path('users/create', CreateUser.as_view()),
    path('users/get/<slug:id_slug>/', GetUser.as_view()),
    path('users/getid/<slug:username_slug>/', GetUserId.as_view()),
    path('users/checkpass/<int:pk>/', CheckPasswordView.as_view()),
    path('users/update/<int:id_slug>/', UpdateUser.as_view()),
]
