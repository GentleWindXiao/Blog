# Register your models here.
from django.contrib import admin
from .models import Blog, Category, Tag

# ===========================================================
# 博客后台管理注册
# ===========================================================

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """
    Blog 模型的后台管理配置：
    - list_display: 在列表页显示的字段
    - list_filter: 右侧筛选栏，可按状态、分类、标签过滤
    - search_fields: 搜索框可搜索的字段
    """
    list_display = ('title', 'author', 'status', 'created_at')  # 列表页显示标题、作者、状态和创建时间
    list_filter = ('status', 'category', 'tags')               # 侧边栏可筛选文章状态、分类和标签
    search_fields = ('title', 'content_markdown')             # 搜索框可搜索文章标题和 Markdown 内容

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Category 模型的后台管理配置：
    - list_display: 在列表页显示名称、slug 和创建时间
    - search_fields: 搜索框可搜索分类名称
    """
    list_display = ('name', 'slug', 'created_at')  # 列表页显示分类名称、slug、创建时间
    search_fields = ('name',)                     # 搜索框可搜索分类名称

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Tag 模型的后台管理配置：
    - list_display: 在列表页显示名称、slug 和创建时间
    - search_fields: 搜索框可搜索标签名称
    """
    list_display = ('name', 'slug', 'created_at')  # 列表页显示标签名称、slug、创建时间
    search_fields = ('name',)                     # 搜索框可搜索标签名称
