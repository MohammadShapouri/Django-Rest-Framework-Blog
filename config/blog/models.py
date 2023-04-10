from django.db import models
from django.utils import timezone
from extentions.utils import jalali_converter
from django.utils.text import slugify
# Create your models here.


# ***Manager***
# Custom manager which has the same functionality as     filter(status = 'p'). Use it for Article table. => Article.objects.published_article()
class BlogManager(models.Manager):

    def published_article(self):
        return self.filter(status = 'p')



class CategoryManager(models.Manager):

    def completed_cateogry(self):
        return self.filter(status = True)









# *** MODELS ***

class Category(models.Model):
    
    STATUS_CHOICES = (
        ('d',"پیش نویس"),
        ('p',"منتشر شده"),
    )

    parent      = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, verbose_name="والد", related_name='child')
    title       = models.CharField(max_length=200, verbose_name="عنوان")
    slug        = models.SlugField(max_length=100, unique=True, verbose_name="آدرس عنوان")
    status      = models.CharField(choices=STATUS_CHOICES, max_length=1, default='d', verbose_name="وضعیت")

    class Meta:
        ordering = ['parent__id']
        verbose_name =  "دسته بندی"
        verbose_name_plural =  "دسته بندی ها"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)


    objects = BlogManager()








class Article(models.Model):

    STATUS_CHOICES = (
        ('d',  "پیش نویس"),
        ('p', "منتشر شده"),
        ('r', "برگشت داده شده"),
    )

    owner           = models.ForeignKey('userAccount.UserAccount', on_delete=models.CASCADE, verbose_name="مالک")
    title           = models.CharField(max_length=200, verbose_name="عنوان")
    slug            = models.SlugField(max_length=100, unique=True, verbose_name="آدرس عنوان")
    category        = models.ManyToManyField(Category, verbose_name="دسته بندی", related_name='article')
    description     = models.TextField(max_length=2000, verbose_name="توضیحات")
    thumbnail       = models.ImageField(default='image/article-image/default/article-default.jpg', upload_to='image/article-image', verbose_name='عکس')
    publish_date    = models.DateTimeField(default=timezone.now, verbose_name="زمان ")
    creation_date   = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    update_date     = models.DateTimeField(auto_now=True)
    status          = models.CharField(choices=STATUS_CHOICES, max_length=1, verbose_name="وضعیت")

    class Meta:
        verbose_name =  "مقاله"
        verbose_name_plural =  "مقالات"

    def __str__(self):
        return self.title

    def jalali_publish_date(self):
        return jalali_converter(self.publish_date)
    jalali_publish_date.short_description =  "زمان انتشار" # It has the same functionality as '   verbose_name=""  '.

    def jalali_creation_date(self):
        return jalali_converter(self.creation_date)
    jalali_creation_date.short_description =  "زمان ایجاد"

    def jalali_update_date(self):
        return jalali_converter(self.update_date)
    jalali_update_date.short_description =  "زمان به روز رسانی"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    # Use it in template for getting TRUE categories. Put it after article object. => articleObject.completed_cateogry
    def completed_cateogry(self):
        return self.category.filter(status=True)

    
    objects = BlogManager()






class ArticleHistory(models.Model):
    
    STATUS_CHOICES = (
        ('d',  "پیش نویس"),
        ('p', "منتشر شده"),
        ('r', "برگشت داده شده"),
    )
    CHANGE_CHOICES = (
        ('+',"افزودن"),
        ('-',"حذف کردن"),
        ('∼',"آپدیت کردن"),
        ('r', "برگشت دادن"),
    )

    article                 = models.ForeignKey('Article', blank=True, null=True, on_delete=models.SET_NULL, related_name='articleHistory', verbose_name="مقاله مربوط")
    article_after_delete    = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, related_name='articleHistoryAfterDelete', verbose_name="مقاله مربوط (حذف شده)")
    # ...
    title                   = models.CharField(max_length=200, verbose_name="عنوان")
    slug                    = models.SlugField(max_length=100, unique=True, verbose_name="آدرس عنوان")
    category                = models.ManyToManyField(Category, verbose_name="دسته بندی")
    description             = models.TextField(max_length=2000, verbose_name="توضیحات", blank=True, null=True)
    thumbnail               = models.ImageField(default='image/article-image/default/article-default.jpg', upload_to='image/article-image', verbose_name='عکس')
    creation_date           = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    publish_date            = models.DateTimeField(default=timezone.now, verbose_name="زمان ")
    update_date             = models.DateTimeField(auto_now=True)
    status                  = models.CharField(choices=STATUS_CHOICES, max_length=1, verbose_name="وضعیت")
    # ...
    return_title              = models.CharField(max_length=100, blank=True, null=True, verbose_name="عنوان اخطار")
    return_description        = models.CharField(max_length=500, blank=True, null=True, verbose_name="توضیحات")
    # ...
    history_creation_date   = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد تاریخچه")
    change                  = models.CharField(choices=CHANGE_CHOICES, max_length=1, verbose_name="نوع تغییر")


    class Meta:
        verbose_name =  "تاریخچه مقاله"
        verbose_name_plural =  "تاریخچه مقالات"

    def __str__(self):
        return str(self.title)

    def jalali_publish_date(self):
        return jalali_converter(self.publish_date)
    jalali_publish_date.short_description =  "زمان انتشار" # It has the same functionality as '   verbose_name=""  '.

    def jalali_creation_date(self):
        return jalali_converter(self.creation_date)
    jalali_creation_date.short_description =  "زمان ایجاد"

    def jalali_update_date(self):
        return jalali_converter(self.update_date)
    jalali_update_date.short_description =  "زمان به روز رسانی"

    # Use it in template for getting TRUE categories. Put it after article object. => articleObject.completed_cateogry
    def completed_cateogry(self):
        return self.category.filter(status=True)





class ArticleReturn(models.Model):

    REASON_CHOICES = (
        ('m',"اطلاعات علمی نادرست"),
        ('r',"محتوای نامناسب و توهین آمیز"),
        ('o', "موارد دیگر"),
    )

    article     = models.ForeignKey('Article', on_delete=models.CASCADE, verbose_name="مقاله مربوط")
    reason      = models.CharField(choices=REASON_CHOICES, max_length=1, verbose_name="دلیل")
    description = models.TextField(max_length=500, verbose_name="توضیحات", blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_checked  = models.BooleanField(default=False, verbose_name="رویت شده است؟")

    class Meta:
        verbose_name = "مقاله برگشت خورده"
        verbose_name_plural = "مقالات برگشت خورده"

    def __str__(self):
        return self.title


    def jalali_creation_date(self):
        return jalali_converter(self.creation_date)






        


class ArticleReport(models.Model):

    REASON_CHOICES = (
        ('m',"اطلاعات علمی نادرست"),
        ('r',"محتوای نامناسب و توهین آمیز"),
        ('o', "موارد دیگر"),
    )
    
    IS_CHECKED_CHOICES = (
        ('y',"بررسی شده است"),
        ('n',"بررسی نشده است"),
    )

    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='articleReport', verbose_name="مقاله")
    reason = models.CharField(choices=REASON_CHOICES, max_length=1, verbose_name="دلیل")
    description = models.TextField(max_length=500, verbose_name="توضیحات", blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_checked = models.CharField(choices=IS_CHECKED_CHOICES, default='n', max_length=1, verbose_name="بررسی شده است؟")

    class Meta:
        verbose_name = "مقاله گزارش داده شده"
        verbose_name_plural = "مقالات گزارش داده شده"

    def __str__(self):
        return self.reason

    def jalali_creation_date(self):
        return jalali_converter(self.creation_date)
