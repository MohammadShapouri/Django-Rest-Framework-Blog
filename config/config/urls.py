"""config URL Configuration

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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views
from api.views import AccountConfirmEmail
from dj_rest_auth.views import PasswordResetConfirmView
from rest_framework_simplejwt import views as jwt_views
# from django.views.generic import TemplateView
# from api.views import RevokeToken


urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('account/', include('userAccount.urls')),
    # path('api-auth/', include('rest_framework.urls')),
    path('api/', include('api.urls')),

    # Standard Token urls...
    # path('api-token-auth/', views.obtain_auth_token),
    # path('api/revoke', RevokeToken.as_view()),

    # dj-rest-auth urls with optimization...
    path('api/dj-rest-auth/', include('dj_rest_auth.urls')),
    path('api/dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    # path('api/dj-rest-auth/registration/', CustomRegisterView.as_view() ),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    re_path(
        r'^api/dj-rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$', AccountConfirmEmail.as_view(),
        name='account_confirm_email',
    ),

    # JWT urls...
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root= settings.STATIC_ROOT)
