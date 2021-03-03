from rest_framework import permissions, viewsets, response, decorators, status
from .models import (Value, Brand, ClaimCategory, Claim, ProductCategory,
                     Product, ProductImage, FormResponse, ResponderValueWeight,
                     ProductValueWeight, Responder)
from .serializers import (ValueSerializer, BrandSerializer, ClaimCategorySerializer,
                          ClaimSerializer, ProductCategorySerializer, ProductSerializer, ProductImageSerializer,
                          FormResponseSerializer, ResponderValueWeightSerializer,
                          ProductValueWeightSerializer, CustomTokenObtainPairSerializer, ResponderSerializer)
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework.exceptions import PermissionDenied


User = get_user_model()


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        else:
            return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.user == request.user
        else:
            return request.user.is_staff


class IsOwnerOrAdminEditable(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        else:
            return obj.responder == request.user


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        else:
            return request.user.is_staff


class ValueViewSet(viewsets.ModelViewSet):
    queryset = Value.objects.all()
    serializer_class = ValueSerializer
    permission_classes = (permissions.AllowAny,)


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = (IsAdminOrReadOnly,)


class ClaimCategoryViewSet(viewsets.ModelViewSet):
    queryset = ClaimCategory.objects.all()
    serializer_class = ClaimCategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class ClaimViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    permission_classes = (IsAdminOrReadOnly,)


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly,)


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = (IsAdminOrReadOnly,)


class FormResponseViewSet(viewsets.ModelViewSet):
    queryset = FormResponse.objects.all()
    serializer_class = FormResponseSerializer
    permission_classes = (IsOwnerOrAdmin,)

    def get_queryset(self):
        return FormResponse.objects.filter(user=self.request.user)


class ResponderValueWeightViewSet(viewsets.ModelViewSet):
    queryset = ResponderValueWeight.objects.all()
    serializer_class = ResponderValueWeightSerializer
    permission_classes = (IsOwnerOrAdminEditable,)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return ResponderValueWeight.objects.all()
        elif user.is_authenticated:
            return ResponderValueWeight.objects.filter(responder=user)
        raise PermissionDenied()


class ProductValueWeightViewSet(viewsets.ModelViewSet):
    queryset = ProductValueWeight.objects.all()
    serializer_class = ProductValueWeightSerializer
    permission_classes = (IsOwnerOrAdmin,)


class ResponderViewSet(viewsets.ModelViewSet):
    queryset = Responder.objects.all()
    serializer_class = ResponderSerializer
    permission_classes = (IsOwnerOrAdmin,)

    def get_queryset(self):
        return Responder.objects.filter(user=self.request.user)


@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def AcceptFormResponse(request):
    typeform_id = request.data['event_id']
    for i in request.data['form_response']['answers']:
        if i['field']['id'] == "Ta8dtdbEA5pP":
            values = i['choices']
        if i['field']['id'] == "pE0XkQCk0MwG":
            email = i['email']

    for i in request.data['form_response']['definition']['fields']:
        if i['id'] == 'Ta8dtdbEA5pP':
            for choice in i['choices']:
                try:
                    Value.objects.create(
                        typeform_id=choice['id'], value=choice['label']).save()
                except IntegrityError:
                    Value.objects.filter(typeform_id=choice['id']).update(
                        value=choice['label'])

    try:
        responder = User.objects.get(username=email)
    except ObjectDoesNotExist:
        responder = User.objects.create(username=email)
        responder.set_unusable_password()
        responder.save()

    try:
        FormResponse.objects.create(
            typeform_id=typeform_id, responder=responder, response_data=request.data).save()
    except IntegrityError:
        return(response.Response({"400": "id already exists"}, status.HTTP_400_BAD_REQUEST))

    for value in values["labels"]:
        value = Value.objects.get(value=value)
        ResponderValueWeight.objects.create(
            value=value, responder=responder, weight=1).save()

    return response.Response({"thanks": "for the form"}, status.HTTP_201_CREATED)


@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.AllowAny])
def CheckNewUser(request, typeform_id):
    try:
        formResponse = FormResponse.objects.get(typeform_id=typeform_id)
        responder = formResponse.responder
    except ObjectDoesNotExist:
        return response.Response({"404": "id does not exists"}, status.HTTP_404_NOT_FOUND)
    if responder.has_usable_password():
        return response.Response({"403": "user has password"}, status.HTTP_403_FORBIDDEN)
    return response.Response({"email": responder.email}, status.HTTP_202_ACCEPTED)


@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def SetUserPassword(request, typeform_id):
    try:
        formResponse = FormResponse.objects.get(typeform_id=typeform_id)
        responder = formResponse.responder
    except ObjectDoesNotExist:
        return response.Response({"404": "id does not exists"}, status.HTTP_404_NOT_FOUND)
    if responder.has_usable_password():
        return response.Response({"403": "user has password"}, status.HTTP_403_FORBIDDEN)
    responder.set_password(request.data['password'])
    responder.save()
    return response.Response({"200": "password added"}, status.HTTP_202_ACCEPTED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
