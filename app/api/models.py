from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext as _
from django.contrib.postgres.fields import JSONField
from django.db import models


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Value(models.Model):
    typeform_id = models.CharField(max_length=80, unique=True)
    value = models.CharField(max_length=80, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.value


class Brand(models.Model):
    brand = models.CharField(max_length=80, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.brand


class ClaimCategory(models.Model):
    claim_category = models.CharField(max_length=80, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.claim_category


class Claim(models.Model):
    claim = models.CharField(max_length=80, unique=True)
    claim_category = models.ForeignKey(
        ClaimCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.claim


class ProductCategory(models.Model):
    product_category = models.CharField(max_length=80, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_category


class Product(models.Model):
    product = models.CharField(max_length=80, unique=True)
    product_category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    claims = models.ManyToManyField(Claim, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to='products', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.image)


class FormResponse(models.Model):
    typeform_id = models.CharField(max_length=80, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    response_data = JSONField(blank=True)
    recomendations = models.ManyToManyField(
        Product, related_name='recomendation')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)


class ResponderValueWeight(models.Model):
    value = models.ForeignKey(
        Value, on_delete=models.CASCADE, related_name='value_to_responder')
    responder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='responder_to_value')
    weight = models.IntegerField()

    class Meta:
        unique_together = ('value', 'responder',)


class ProductValueWeight(models.Model):
    value = models.ForeignKey(
        Value, on_delete=models.CASCADE, related_name='value_to_product')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_to_value')
    weight = models.IntegerField()


class Responder(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    form_responses = models.ManyToManyField(FormResponse, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
