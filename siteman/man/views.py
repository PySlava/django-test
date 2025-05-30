from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import AddPostForm, UploadFileForm
from .models import Man, TagPost, UploadFiles
from .utils import DataMixin

class ManHome(DataMixin, ListView):
    template_name = 'man/index.html'
    context_object_name = 'posts'
    title_page = 'Main Page'
    cat_selected = 0
    paginate_by = 3

    def get_queryset(self):
        return Man.published.all().select_related('cat')


@login_required
def about(request):
    contact_list = Man.published.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'man/about.html', {'title': 'О сайте', 'page_obj': page_obj})

class ShowPost(DataMixin, DetailView):
    # model = Man
    template_name = 'man/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Man.published, slug=self.kwargs[self.slug_url_kwarg])

class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'man/addpage.html'
    title_page = 'Added Page'
    login_url = '/admin/'
    permission_required = 'women.add_women'

    def form_valid(self, form):
        m = form.save(commit=False)
        m.author = self.request.user
        return super().form_valid(form)

class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Man
    fields = ['title', 'content', 'photo', 'is_active', 'cat']
    template_name = 'man/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Changed Posts'
    permission_required = 'women.change_women'


@permission_required(perm='women.view_women', raise_exception=True)
def contact(request):
    return HttpResponse("Feedback")


def login(request):
    return HttpResponse("Authorization")

class ManCategory(DataMixin, ListView):
    template_name = 'man/index.html'
    context_object_name = 'posts'
    allow_empty = False
    paginate_by = 3

    def get_queryset(self):
        return Man.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title=f'Category - {cat.name}', cat_selected=cat.pk)

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")

class TagPostList(DataMixin, ListView):
    template_name = 'man/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Man.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title=f'Category - {tag.tag}')
