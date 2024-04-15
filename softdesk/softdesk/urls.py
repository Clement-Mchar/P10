from django.contrib import admin
from django.urls import path, include
from authentication.views import UserViewset
from project.views import ProjectViewset, IssueViewset
from rest_framework import routers
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

router = routers.SimpleRouter()
router.register('users', UserViewset, basename="users")
router.register('projects', ProjectViewset, basename="projects")

projects_router = routers.NestedSimpleRouter(router, 'projects', lookup='project')
projects_router.register('issues', IssueViewset, basename='project-issues')
urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api/', include(projects_router.urls)),

]
