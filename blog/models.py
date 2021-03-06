from django.db import models
from django.contrib.auth.models import User
import os

from markdownx.utils import markdown
from markdownx.models import MarkdownxField

from datetime import timedelta

class Category(models.Model):
    # 카테고리는 유니크 해야한다
    name = models.CharField(max_length=50, unique=True)

    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'

    class Meta:
        verbose_name_plural = "Categories"


class Tag(models.Model):
    # 카테고리는 유니크 해야한다
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'


class Post(models.Model):
    title = models.CharField(max_length=50) # 짧은내용
    hook_text = models.CharField(max_length=100, blank=True)
    content = MarkdownxField()  #긴 내용

    #blank=True : 폼이 있을때 잘 입력됐는지 봐주는것 True로 되어 있으면 없어도 폼입력 화면에서 넘어감..
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    # 카테고리가 지워지더라도 포스트가 지워지지는 않도록 ....
    # null=True : DB 안에 없어도 된다..
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'[{self.pk}] {self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]

    def get_content_markdown(self):
        return markdown(self.content)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'

    def is_updated(self):
        return self.updated_at - self.create_at > timedelta(seconds=1)

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else :
            return f'https://doitdjango.com/avatar/id/705/174d5e2969cf0d1c/svg/{self.author.email}'