from django import forms
from .models import Article, Category, ArticleReturn, ArticleReport
from django.utils.html import format_html


class ArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)

        STATUS_CHOICES = (
            ('d',  "پیش نویس"),
            ('p', "منتشر شده"),
        )
        self.fields['status'] = forms.ChoiceField(choices=STATUS_CHOICES, label="وضعیت")
        self.fields['category'].required = False
        
    class Meta:
        model = Article
        fields = ['title', 'category', 'description', 'thumbnail', 'status']





class CategoryForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.form_request = kwargs.pop('request', None)
        super(CategoryForm, self).__init__(*args, **kwargs)

        if self.form_request.user.is_superuser == False:
            self.fields['status'].disabled = True
            self.fields['status'].initial = 'd'
            self.fields['status'].help_text = format_html("<ul>  <li>{}</li>  </ul>".format("این بخش تنها توسط ادمین اصلاح می شود."))

    class Meta:
        model = Category
        fields = ['parent', 'title', 'status']







class ArticleReturnForm(forms.ModelForm):
    class Meta:
        model = ArticleReturn
        fields = ['reason', 'description']







class ArticleReportForm(forms.ModelForm):
    class Meta:
        model = ArticleReport
        fields = ['reason', 'description']
