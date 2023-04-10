from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from .forms import ArticleForm, CategoryForm, ArticleReturnForm, ArticleReportForm
from .models import Article, Category, ArticleReturn, ArticleReport
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import ArticleManagingMixin, CategotyManagingMixin
# Create your views here.



class AddArticle(LoginRequiredMixin, CreateView):
    template_name = 'blog/article-add.html'
    form_class = ArticleForm
    model = Article
    success_url = reverse_lazy('ArticleList')





class ArticleList(ListView):
    model = Article
    template_name = 'blog/article-list.html'
    paginate_by = 8

    def get_queryset(self):
        return get_list_or_404(Article.objects.published_article())
         




class ArticleDetail(DetailView):
    model = Article
    template_name = 'blog/article-detail.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Article, status='p', slug=slug)





class EditArticle(ArticleManagingMixin, UpdateView):
    model = Article
    template_name = 'blog/article-edit.html'
    form_class = ArticleForm
    success_url = reverse_lazy('ArticleList')

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Article, slug=slug)





class DeleteArticle(ArticleManagingMixin, DeleteView):
    model = Article
    template_name = 'blog/article-delete.html'
    success_url = reverse_lazy('ArticleList')





class CategoryList(ListView):
    model = Category
    template_name = 'blog/category-list.html'
    paginate_by = 15

    def get_queryset(self):
        status = self.kwargs.get('status')
        return get_list_or_404(Category.objects.filter(status=status))





class CategoryDetail(ListView):
    model = Article
    template_name = 'blog/category-detail.html'
    paginate_by = 8

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        status = self.kwargs.get('status')
        global category
        category = get_object_or_404(Category, status=status, slug=slug)
        return get_list_or_404(Article.objects.published_article(), category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context





class AddCategory(CreateView):
    model = Category
    template_name = 'blog/category-add.html'
    form_class = CategoryForm
    success_url = reverse_lazy('ArticleList')

    def get_form_kwargs(self):
        kwargs = super(AddCategory, self).get_form_kwargs()
        kwargs.update({ 'request' : self.request })
        return kwargs





class EditCategory(CategotyManagingMixin, UpdateView):
    model = Category
    template_name = 'blog/category-edit.html'
    form_class = CategoryForm
    success_url = reverse_lazy('ArticleList')

    def get_object(self):
        slug = self.kwargs.get('slug')
        status = self.kwargs.get('status') 
        """ In normal situation line 126 and line 130 are not required and line129 can 
         handle the operation but now I have to use line 126 and 130 instead og 129."""
        #return get_object_or_404(Category, slug=slug)
        return get_object_or_404(Category, status=status, slug=slug)

    def get_form_kwargs(self):
        kwargs = super(EditCategory, self).get_form_kwargs()
        kwargs.update({ 'request' : self.request })
        return kwargs





class ArticleReturn(CreateView):
    model = ArticleReturn
    template_name = 'blog/article-return.html'
    form_class = ArticleReturnForm
    success_url = reverse_lazy('ArticleList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        global returnedArticle
        returnedArticle = get_object_or_404(Article, status='p', slug=slug)
        context['article'] = returnedArticle
        return context

    def form_valid(self, form):
        returnedArticle.status = 'r'
        returnedArticle.save()
        form.instance.article = returnedArticle
        return super().form_valid(form)






class ArticleReport(CreateView):
    model = ArticleReport
    template_name = 'blog/article-report.html'
    form_class = ArticleReportForm
    success_url = reverse_lazy('ArticleList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        global reportedArticle
        reportedArticle = get_object_or_404(Article, status='p', slug=slug)
        context['article'] = reportedArticle
        return context

    def form_valid(self, form):
        form.instance.article = reportedArticle
        return super().form_valid(form)
