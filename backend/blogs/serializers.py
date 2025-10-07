"""
serializers.py
=========================
该模块定义了 Blog、Category、Tag 三个模型的序列化器。

主要功能：
1. 将数据库模型转换为 JSON 数据格式，供前端 API 使用；
2. 定义前台与后台不同视图所需的字段集合；
3. 统一管理字段显示逻辑。

本文件包含以下序列化器：
- CategorySerializer：分类信息；
- TagSerializer：标签信息；
- BlogListSerializer：博客列表视图；
- BlogDetailSerializer：博客详情视图；
- AdminBlogSerializer：后台管理使用的完整博客序列化器。
"""

from rest_framework import serializers
from .models import Blog, Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    """博客分类序列化器（前台/后台通用）"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']


class TagSerializer(serializers.ModelSerializer):
    """博客标签序列化器（前台/后台通用）"""
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class BlogListSerializer(serializers.ModelSerializer):
    """博客列表序列化器（前台）"""
    author = serializers.StringRelatedField()
    category = CategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'slug', 'excerpt', 'featured_image',
            'author', 'category', 'tags', 'status', 'is_featured',
            'views_count', 'likes_count', 'created_at', 'updated_at'
        ]


class BlogDetailSerializer(serializers.ModelSerializer):
    """博客详情序列化器（前台）"""
    author = serializers.StringRelatedField()
    category = CategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Blog
        fields = '__all__'


class AdminBlogSerializer(serializers.ModelSerializer):
    """博客管理序列化器（后台）"""
    class Meta:
        model = Blog
        fields = '__all__'
