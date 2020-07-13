from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

# REST FRAMEWORK
router = routers.DefaultRouter()

# ------------------------------------------------

urlpatterns = [
    path('api/v1/rest_api/', include('rest_api.urls')),
    path('admin/', admin.site.urls),
    # REST FRAMEWORK
    # path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # --------------------------------
]
