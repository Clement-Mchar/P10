from django.contrib import admin
from django.urls import path, include
from authentication.views import UserViewset
from project.views import ProjectViewset
from rest_framework import routers

router = routers.SimpleRouter()
router.register('users', UserViewset, basename="users")
router.register('projects', ProjectViewset, basename="projects")

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls))
]
