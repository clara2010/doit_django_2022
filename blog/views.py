from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView


# def index(request):
#     # posts = Post.objects.all() # 모든 post를 다 가져온다.
#     posts = Post.objects.all().order_by('-pk') # 모든 post를 다 가져온다. 역순으로
#     return render(
#         request,
#         'blog/index.html',
#         {
#             'posts' : posts, # 위에서 가져온걸 딕셔너리 형태로 posts라는 이름으로 돌려준다.
#         }
#
#     )


# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#     return render(
#         request,
#         'blog/single_page.html',
#         {
#             'post' : post,
#         }
#     )


class PostList(ListView):
    model = Post
    ordering = '-pk'
    # template_name = 'blog/index.html'
    # 자동으로 post_list.html 보여줌 따로 지정하고 싶다면 위에 코드드


class PostDetail(DetailView):
    model = Post
    # template_name = 'blog/single_page.html'

