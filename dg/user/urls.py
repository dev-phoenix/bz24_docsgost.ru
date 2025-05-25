
from django.urls import path
# from .views import GenericUserAPIView,UserAPIView, CustomRegisterView
# from .views import UserViewSet, GroupViewSet
from .views import *
from django.urls import path, include, re_path, reverse_lazy
# from rest_framework import routers

# from knox import views as knox_views
# from api.project.views import LoginView, LogoutView as LogoutotherView, LogoutAllView

# project_router_urls = routers.DefaultRouter()
# project_router_urls.register(r'login', login)
# project_router_urls.register(r'logout', logout)

project_urls = [
    # path('api/v1/', include(project_router_urls.urls)),
    # path('api/token-auth/', CustomAuthToken.as_view()),
    # path('api/drf-token-auth/', drfauthtokenviews.obtain_auth_token),

    # path(r'api/auth/login/', LoginView.as_view(), name='knox_login'),
    # path(r'api/auth/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
]