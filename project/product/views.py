from django.db.models import Q
from django.http import Http404
from rest_framework import status
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Product, Category, User, AccountManager
from .serializers import ProductSerializer, CategorySerializer, UserSerializer, UserGetSerializer, UserGetIdSerializer


class LatestProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[:3]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class AllProducts(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug=category_slug, product_slug=product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class CreateUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.is_valid():
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            phone = serializer.validated_data['phone']
            password = serializer.validated_data['password']

            AM = AccountManager()
            AM.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                phone=phone,
                password=password
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUser(APIView):
    def get_object(self, id_slug):
        try:
            return User.objects.get(id=id_slug)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, id_slug, format=None):
        user = self.get_object(id_slug=id_slug)
        serializer = UserGetSerializer(user)
        return Response(serializer.data)


class GetUserId(APIView):
    def get_object(self, username_slug):
        try:
            return User.objects.get(username=username_slug)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, username_slug, format=None):
        user = self.get_object(username_slug=username_slug)
        serializer = UserGetIdSerializer(user)
        return Response(serializer.data)


class CheckPasswordView(APIView):
    def post(self, request, pk, format=None):
        user = User.objects.get(pk=pk)
        password = request.data.get('password')
        # Use Django's built-in authentication to check the password
        if user.check_password(password):
            return Response({'password_match': True})
        else:
            return Response({'password_match': False})


class UpdateUser(APIView):
    def post(self, request, id_slug):
        user = User.objects.get(id=id_slug)
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.username = request.data.get('username', user.username)
        user.email = request.data.get('email', user.email)
        user.phone = request.data.get('phone', user.phone)

        if 'password' in request.data:
            user.set_password(raw_password=request.data['password'])

        user.save()

        serializer = UserGetSerializer(user)
        return Response(serializer.data)


class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug=category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({"products": []})
