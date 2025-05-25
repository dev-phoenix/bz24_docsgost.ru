"""dg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
# from django.urls import path
from django.urls import path, include, re_path, reverse_lazy
from django.views.generic.base import RedirectView


from projectTempl.urls import project_urls as pu
from user.urls import project_urls

from django.conf import settings
from django.conf.urls.static import static

import json
from dg.color import color
from dg.lib import dump

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/',include('debug_toolbar.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static('downloads/', document_root=settings.DOWNLOADS_ROOT)
urlpatterns += pu
# urlpatterns += project_urls
# print('urlpatterns \n',json.dumps( urlpatterns , indent=4))
# dump('urlpatterns', urlpatterns )
# dump('urlpatterns',json.dumps([ str(url) for url in urlpatterns] , indent=4))
# dump('TEMPLATE_DIRS',json.dumps([ str(url) for url in settings.TEMPLATE_DIRS] , indent=4))


# urlpatterns +=[
#     re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),
#     # re_path(r'^.*$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),
#     # re_path(r'^.*$', RedirectView.as_view(url=reverse_lazy('api/admin/'), permanent=False)),
# ]