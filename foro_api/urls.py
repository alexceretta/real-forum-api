"""foro_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework import routers
from foro_user import views
from foro_api import settings

# Routers provide an easy way of automatically determining the URL conf.
ROUTER = routers.DefaultRouter()

urlpatterns = [
    path('', include(ROUTER.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('boards/<int:pk>', views.BoardDetail.as_view()),
    path('threads/', views.ThreadList.as_view()),
    path('threads/<int:pk>', views.ThreadDetail.as_view()),
    path('users/<int:pk>', views.UserDetail.as_view(), name="users"),
    path('users/auth/<authId>', views.UserAuthViewSet.as_view({ 'get': 'get_from_auth' }), name="users-auth"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
