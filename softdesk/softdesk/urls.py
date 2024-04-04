from django.contrib import admin
from django.urls import path, include
from authentication.views import UserViewset
from rest_framework import routers

router = routers.SimpleRouter()
router.register('users', UserViewset, basename="users")

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls))
]
