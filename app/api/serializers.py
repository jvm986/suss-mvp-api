from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .models import (Value, Brand, ClaimCategory, Claim,
                     ProductCategory, Product, ProductImage, FormResponse,
                     ResponderValueWeight, ProductValueWeight, Responder)


User = get_user_model()


class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ResponderValueWeightSerializer(serializers.ModelSerializer):
    value_name = serializers.ReadOnlyField(source='value.value')

    class Meta:
        model = ResponderValueWeight
        fields = ('id', 'weight', 'value', 'responder', 'value_name')


class ProductValueWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductValueWeight
        fields = '__all__'


class ClaimCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimCategory
        fields = '__all__'


class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = '__all__'


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = '__all__'


class FormResponseSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    recomendations = ProductSerializer(many=True)

    class Meta:
        model = FormResponse
        fields = '__all__'


class ResponderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responder
        fields = '__all__'


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        token['is_staff'] = user.is_staff
        return token
