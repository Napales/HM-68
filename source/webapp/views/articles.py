from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.utils.http import urlencode
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import ArticleForm, SearchForm

from webapp.models import Article


class ArticleListView(ListView):
    template_name = 'articles/index.html'
    model = Article
    context_object_name = "articles"
    ordering = ['-created_at']
    paginate_by = 12

    def dispatch(self, request, *args, **kwargs):
        print(request.user)
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(Q(title__icontains=self.search_value) | Q(author__icontains=self.search_value))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        result = super().get_context_data(**kwargs)
        result['search_form'] = self.form
        if self.search_value:
            result["query"] = urlencode({"search": self.search_value})
            result['search'] = self.search_value
        return result

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']


class CreateArticleView(LoginRequiredMixin, CreateView):
    template_name = 'articles/create_article.html'
    # model = Article
    # fields = ['title', 'author', 'content', 'tags']
    form_class = ArticleForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateArticleView(PermissionRequiredMixin ,UpdateView):
    template_name = 'articles/update_article.html'
    form_class = ArticleForm
    model = Article

    permission_required = 'webapp.change_article'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

    # def dispatch(self, request, *args, **kwargs):
    #     user = request.user
    #     if not user.is_authenticated:
    #         return redirect('webapp:index')
    #     if not user.has_perm('webapp.change_article'):
    #         raise PermissionDenied
    #     return super().dispatch(request, *args, **kwargs)


class DeleteArticleView(PermissionRequiredMixin, DeleteView):
    model = Article
    template_name = 'articles/delete_article.html'
    success_url = reverse_lazy('webapp:index')

    permission_required = "webapp.delete_article"

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author



class DetailArticleView(DetailView):
    template_name = 'articles/detail_article.html'
    model = Article


    def get_context_data(self, **kwargs):
        result = super().get_context_data(**kwargs)
        result['comments'] = self.object.comments.order_by('-created_at')
        return result


class LikeArticleView(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if request.user in article.like_users.all():
            article.like_users.remove(request.user)
            like = False
        else:
            article.like_users.add(request.user)
            like = True
        return JsonResponse({'like': like, 'likes_count': article.like_users.count()})

def sec_index(request):
    return render(request,  'second_index.html')

