from blog.models import Article
from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import Http404



class ArticleManagingMixin:

    def article_owner(self):
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Article, slug=slug)
        return self.request.user == article.owner


    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404("دسترسی لازم را ندارید.")
        else:
            if self.article_owner() == False and not request.user.is_superuser:
                raise Http404("دسترسی لازم را ندارید.")
            else:
                return super().dispatch(request, *args, **kwargs)





class AdminManagingMixin:

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404("دسترسی لازم را ندارید.")
        else:
            if not request.user.is_superuser:
                raise Http404("دسترسی لازم را ندارید.")
            else:
                return super().dispatch(request, *args, **kwargs)





class CategotyManagingMixin(AdminManagingMixin):
    pass





class ArticleAdminManagingMixin(AdminManagingMixin):
    pass



