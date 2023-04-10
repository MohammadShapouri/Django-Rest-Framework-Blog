from django.urls import path, include
from api import views
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'articles', views.ArticleViewSet, basename='article')
router.register(r'users', views.UserViewSet, basename='user')
# urlpatterns = router.urls
urlpatterns = [
    path('', include(router.urls))
]





# appname = 'api'

# urlpatterns = [
#     path('article', views.ArticleList.as_view(), name='ArticleList'),
#     path('article/<slug:slug>', views.ArticleDetail.as_view(), name='ArticleDetail'),
#     path('account', views.UserAccountList.as_view(), name='UserAccountList'),
#     path('account/<str:username>', views.UserAccountDetail.as_view(), name='UserAccountDetail'),
#     ]