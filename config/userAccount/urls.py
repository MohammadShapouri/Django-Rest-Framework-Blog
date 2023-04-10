from django.urls import path
from . import views


urlpatterns = [
    path('signup', views.AddUserAccount.as_view(), name='AddUserAccount'),
    path('login', views.Login.as_view(), name='Login'),
    path('logout', views.Logout.as_view(), name='Logout'),
    path('edit-profile', views.EditUserAccount.as_view(), name='EditUserAccount'),
]