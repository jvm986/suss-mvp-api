from django.urls import include, path
from rest_framework import routers
from . import views
from .views import AcceptFormResponse, CheckNewUser, SetUserPassword, CustomTokenObtainPairView
from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()
router.register(r'values', views.ValueViewSet)
router.register(r'brands', views.BrandViewSet)
router.register(r'claim_categories', views.ClaimCategoryViewSet)
router.register(r'claims', views.ClaimViewSet)
router.register(r'product_categories', views.ProductCategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'product_images', views.ProductImageViewSet)
router.register(r'form_responses', views.FormResponseViewSet)
router.register(r'responder_value_weight', views.ResponderValueWeightViewSet)
router.register(r'product_value_weight', views.ProductValueWeightViewSet)
router.register(r'responders', views.ResponderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('accounts/authenticate',
         CustomTokenObtainPairView.as_view(), name='token_create'),
    path('token/obtain/', CustomTokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('accept_form_response/', AcceptFormResponse, name='register'),
    path('check_new_user/<str:typeform_id>/', CheckNewUser, name='new_user'),
    path('set_user_password/<str:typeform_id>/',
         SetUserPassword, name='new_user')
]
