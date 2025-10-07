from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Notebook(models.Model):
    """笔记本"""
    name = models.CharField(max_length=100, verbose_name='笔记本名称')
    description = models.TextField(blank=True, verbose_name='描述')
    color = models.CharField(max_length=7, default='#3B82F6', verbose_name='颜色')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notebooks', verbose_name='所有者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '笔记本'
        verbose_name_plural = '笔记本'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Note(models.Model):
    """笔记"""
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
        ('archived', '已归档'),
    ]

    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    summary = models.TextField(max_length=500, blank=True, verbose_name='摘要')
    
    notebook = models.ForeignKey(Notebook, on_delete=models.CASCADE, related_name='notes', verbose_name='笔记本')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes', verbose_name='作者')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='状态')
    is_pinned = models.BooleanField(default=False, verbose_name='是否置顶')
    
    views_count = models.PositiveIntegerField(default=0, verbose_name='浏览次数')
    likes_count = models.PositiveIntegerField(default=0, verbose_name='点赞次数')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='发布时间')

    class Meta:
        verbose_name = '笔记'
        verbose_name_plural = '笔记'
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title
