from django.urls import path
from . import views


urlpatterns = [
    path('article/add', views.AddArticle.as_view(), name='addArticle'),
    path('article/list', views.ArticleList.as_view(), name='ArticleList'),
    path('article/<slug:slug>', views.ArticleDetail.as_view(), name='ArticleDetail'),
    path('article/<slug:slug>/edit', views.EditArticle.as_view(), name='EditArticle'),
    path('article/<slug:slug>/delete', views.DeleteArticle.as_view(), name='DeleteArticle'),
    path('category/add', views.AddCategory.as_view(), name='AddCategory'),
    path('category/<str:status>/list', views.CategoryList.as_view(), name='CategoryList'),
    path('category/<str:status>/<slug:slug>', views.CategoryDetail.as_view(), name='CategoryDetail'),
    #path('category/<slug:slug>/edit', views.EditCategory.as_view(), name='EditCategory'),
    path('category/<str:status>/<slug:slug>/edit', views.EditCategory.as_view(), name='EditCategory'),
    path('article/<slug:slug>/return', views.ArticleReturn.as_view(), name='ArticleReturn'),
    path('article/<slug:slug>/report', views.ArticleReport.as_view(), name='ArticleReport')
]