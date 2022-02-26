from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin



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

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

    # template_name = 'blog/index.html'
    # 자동으로 post_list.html 보여줌 따로 지정하고 싶다면 위에 코드드


class PostDetail(DetailView):
    model = Post
    # ordefing = '-pk'

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context
    # template_name = 'blog/single_page.html'


class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        # 로그인 여부 체크 and (staff or superuser 체크)
        # ==> 로그인한 계정이 권한이 있는지...
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_sueruser):
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else :
            return redirect('/blog/')


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']
    template_name = 'blog/post_update_form.html'

    # get/post 방식 구분해주는 역할. 해당포스트에서 권한이 있는지 확인가능
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list= Post.objects.filter(category=None)
    else :
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list':post_list,
            'categories':Category.objects.all(),
            'no_category_post_count':Post.objects.filter(category=None).count(),
            'category':category
        }
    )


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'tag': tag,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),

        }
    )

