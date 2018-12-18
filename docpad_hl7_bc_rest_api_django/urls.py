"""dp_bc_rest_api_django_project URL Configuration

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

from django.urls import re_path,path, include
from django.contrib import admin
import oauth2_provider.views as oauth2_views
from django.conf import settings
from docpad_hl7_bc_rest_api_django_app.views import ApiEndpoint
from docpad_hl7_bc_rest_api_django_app import urls
from rest_framework.routers import DefaultRouter
from docpad_hl7_bc_rest_api_django_app.views import TransactionViewSet

router = DefaultRouter()
router.register('transaction', TransactionViewSet)

app_name = "docpad_hl7_bc_rest_api_django_app"
# OAuth2 provider endpoints
oauth2_endpoint_views = [
    re_path(r'authorize/$', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    re_path(r'token/$', oauth2_views.TokenView.as_view(), name="token"),
    re_path(r'revoke-token/$', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

if settings.DEBUG:
    # OAuth2 Application Management endpoints
    oauth2_endpoint_views += [
        re_path(r'applications/$', oauth2_views.ApplicationList.as_view(), name="list"),
        re_path(r'applications/register/$', oauth2_views.ApplicationRegistration.as_view(), name="register"),
        re_path(r'applications/(?P<pk>\d+)/$', oauth2_views.ApplicationDetail.as_view(), name="detail"),
        re_path(r'applications/(?P<pk>\d+)/delete/$', oauth2_views.ApplicationDelete.as_view(), name="delete"),
        re_path(r'applications/(?P<pk>\d+)/update/$', oauth2_views.ApplicationUpdate.as_view(), name="update"),
    ]

    # OAuth2 Token Management endpoints
    oauth2_endpoint_views += [
        re_path(r'authorized-tokens/$', oauth2_views.AuthorizedTokensListView.as_view(), name="authorized-token-list"),
        re_path(r'authorized-tokens/(?P<pk>\d+)/delete/$', oauth2_views.AuthorizedTokenDeleteView.as_view(),
            name="authorized-token-delete"),
    ]

    urlpatterns = [
        # OAuth 2 endpoints:
        path('admin/', admin.site.urls),
        re_path(r'o/', include(oauth2_endpoint_views)),
        re_path(r'api/hello', ApiEndpoint.as_view()),  # an example resource endpoint
        path('authentication/', include(urls)),
        path('v1/', include(router.urls)),
    ]


#from django.contrib import admin
#from django.urls import path
#from django.conf.urls import include


#urlpatterns = [
 #   path('admin/', admin.site.urls),
 #   path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
#]

#urlpatterns = [
 #   path('admin/', admin.site.urls),
   # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
  #  url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    #path(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),
    #re_path(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # Logged-in user profile endpoint
    #re_path(r'^profile/$', views.profile),
   # url(r'^authorize/$', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    #url(r'^token/$', oauth2_views.TokenView.as_view(), name="token"),
    #url(r'^revoke-token/$', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
#]
