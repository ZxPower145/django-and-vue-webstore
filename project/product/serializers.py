from rest_framework import serializers
from .models import Category, Product, User


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "name",
            "get_absolute_url",
            "description",
            "price",
            "get_image",
            "get_thumbnail"
        )


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "products",
        )


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "username", "email", "phone", "password")
        extra_kwargs = {'password': {'write_only': True}}

    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.IntegerField()
    password = serializers.CharField(write_only=True)

    def to_representation(self, instance):
        # Customize representation for rendering in browsable API
        representation = super().to_representation(instance)
        representation['password'] = ''
        return representation


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "phone",
        )


class UserGetIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
        )
