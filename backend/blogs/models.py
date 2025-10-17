from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

class Category(models.Model):
    """博客分类"""
    name = models.CharField(max_length=100, unique=True, verbose_name="分类名称")
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name="URL标识")
    description = models.TextField(blank=True, verbose_name="分类描述")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "博客分类"
        verbose_name_plural = "博客分类"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """博客标签"""
    name = models.CharField(max_length=50, unique=True, verbose_name="标签名称")
    slug = models.SlugField(max_length=50, unique=True, blank=True, verbose_name="URL标识")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "博客标签"
        verbose_name_plural = "博客标签"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Blog(models.Model):
    """博客文章"""
    STATUS_CHOICES = [
        ("draft", "草稿"),
        ("published", "已发布"),
        ("archived", "已归档"),
    ]

    title = models.CharField(max_length=200, verbose_name="标题")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="URL标识")
    content_markdown = models.TextField(verbose_name="Markdown内容")
    excerpt = models.TextField(max_length=500, blank=True, verbose_name="摘要")
    featured_image = models.ImageField(upload_to="blogs/", blank=True, null=True, verbose_name="特色图片")

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs", verbose_name="作者")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="分类")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="标签")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft", verbose_name="状态")
    is_featured = models.BooleanField(default=False, verbose_name="是否推荐")

    views_count = models.PositiveIntegerField(default=0, verbose_name="浏览次数")
    likes_count = models.PositiveIntegerField(default=0, verbose_name="点赞次数")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="发布时间")

    class Meta:
        verbose_name = "博客文章"
        verbose_name_plural = "博客文章"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
