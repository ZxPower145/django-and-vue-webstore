from io import BytesIO
from PIL import Image
from django.core.files import File
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models

DOMAIN = 'http://127.0.0.1:8000'


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}'


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def get_image(self):
        if self.image:
            return DOMAIN + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return DOMAIN + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return DOMAIN + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(1000, 1000)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'PNG', quality=100)

        thumbnail = File(thumb_io, name=image.name)
        return thumbnail


class AccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, phone, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address!')
        if not username:
            raise ValueError('Users must have an username!')

        model = User

        user = model(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            phone=phone,
            **extra_fields
            )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password):
        model = User

        user = model(
            username=username,
            is_staff=1,
            is_active=1,
            is_superuser=1
        )

        user.set_password(password)
        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True, max_length=250)
    first_name = models.CharField(max_length=240)
    last_name = models.CharField(max_length=250)
    username = models.CharField(max_length=60, unique=True)
    phone = models.CharField(max_length=50)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
