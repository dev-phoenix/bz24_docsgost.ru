
# from django.urls import path
# from .views import GenericUserAPIView,UserAPIView, CustomRegisterView
# from .views import UserViewSet, GroupViewSet
from .views import \
    index, loginView, logoutView, _404View, \
    tplnew, tplstatistic, templateList, removeFile
# from .views import *
from django.urls import path, include, re_path, reverse_lazy
# from rest_framework import routers

# from knox import views as knox_views
# from api.project.views import LoginView, LogoutView as LogoutotherView, LogoutAllView

# project_router_urls = routers.DefaultRouter()
# project_router_urls.register(r'login', login)
# project_router_urls.register(r'logout', logout)

project_urls = [
    path('', index, name='index'),
    path('404', _404View, name='404'),
    path('login', loginView, name='login'),
    path('logout', logoutView, name='logout'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    
    re_path(r'tplnew/?', tplnew, name='tplnew'),
    re_path(r'tpl/<int:tplid>/?', tplnew, name='tplget'),
    path(r'tpl/<int:tplid>/', tplnew, name='tplget'),
    path(r'tpl/<int:tplid>', tplnew, name='tplget'),
    path(r'tpls', templateList, name='templateList'),
    path(r'tpls/', templateList, name='templateList'),
    path(r'tpls/<int:page>/', templateList, name='templateList'),
    path(r'tpls/<int:page>/<int:limit>/', templateList, name='templateList'),
    path(r'filerem/<int:fid>', removeFile, name='removeFile'),
    path(r'filerem/<int:fid>/', removeFile, name='removeFile'),
    path('tplstatistic', tplstatistic, name='tplstatistic'),
    # path(r'/', IndexWiew.as_view(), name='index'),
    # path(r'templates/', TemplatesView.as_view(), name='templates'),
    # path(r'statistic/', StatisticView.as_view(), name='statistic'),

    # path(r'login/', LoginView.as_view(), name='knox_login'),
    # path(r'logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    
    # path('api/v1/', include(project_router_urls.urls)),
    # path('api/token-auth/', CustomAuthToken.as_view()),
    # path('api/drf-token-auth/', drfauthtokenviews.obtain_auth_token),

    # path(r'api/auth/login/', LoginView.as_view(), name='knox_login'),
    # path(r'api/auth/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
]