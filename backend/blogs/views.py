"""
views.py
=========================
该模块定义了博客系统的视图层（ViewSets），用于提供 RESTful API。

分为两类：
1. 前台接口（BlogViewSet、CategoryViewSet、TagViewSet）
   - 用于博客展示、分类列表、标签筛选、点赞、浏览量统计；
   - 允许匿名用户访问。
2. 管理端接口（AdminBlogViewSet）
   - 用于后台博客管理（增删改查）；
   - 仅限作者或管理员访问。

框架：Django REST framework
"""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Blog, Category, Tag
from .serializers import (
    BlogListSerializer, BlogDetailSerializer,
    CategorySerializer, TagSerializer, AdminBlogSerializer
)

# ===========================================================
#  前台接口（提供给 Vue 前端）
# ===========================================================

class BlogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    前台博客视图集：
    - GET /api/blogs/         → 博客列表
    - GET /api/blogs/{slug}/  → 博客详情
    - POST /api/blogs/{slug}/like/ → 点赞
    - POST /api/blogs/{slug}/view/ → 增加浏览量
    """
    queryset = Blog.objects.filter(status="published").select_related("author", "category").prefetch_related("tags")
    lookup_field = "slug"
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == "list":
            return BlogListSerializer
        return BlogDetailSerializer

    @action(detail=True, methods=["post"], permission_classes=[permissions.AllowAny])
    def like(self, request, slug=None):
        """前台点赞接口"""
        blog = self.get_object()
        blog.likes_count += 1
        blog.save(update_fields=["likes_count"])
        return Response({"message": "Liked", "likes_count": blog.likes_count})

    @action(detail=True, methods=["post"], permission_classes=[permissions.AllowAny])
    def view(self, request, slug=None):
        """前台浏览计数接口"""
        blog = self.get_object()
        blog.views_count += 1
        blog.save(update_fields=["views_count"])
        return Response({"message": "View counted", "views_count": blog.views_count})


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """前台分类接口"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """前台标签接口"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


# ===========================================================
#  后台管理接口（提供给管理端）
# ===========================================================

class AdminBlogViewSet(viewsets.ModelViewSet):
    """
    管理端博客视图集：
    - 仅管理员或作者可访问；
    - 支持创建、更新、删除博客。
    """
    queryset = Blog.objects.all().select_related("author", "category").prefetch_related("tags")
    serializer_class = AdminBlogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """自动绑定作者"""
        serializer.save(author=self.request.user)
