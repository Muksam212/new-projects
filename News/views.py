from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


from .models import Author, News, Category, Comment
from .forms import AuthorForm, NewsForm, CategoryForm, CommentForm


#creating the process
class DashboardTemplate(TemplateView):
    template_name='dashboard/base.html'
    success_url=reverse_lazy('News:dashboard')


class IndexView(TemplateView):
    template_name='admin/index.html'
    

#author
class AuthorList(ListView):
    context_object_name='author_list'
    model=Author
    template_name='Author/author_list.html'
    success_url=reverse_lazy("News:list-author")
    paginate_by=1
    

    def get_queryset(self):
        queryset=Author.objects.all()
        query=self.request.GET.get('q')

        if query:
            author_list=self.model.objects.filter(
                Q(name__icontains=query)|
                Q(address__icontains=query)
            )
        else:
            author_list=queryset
        return author_list


class AuthorCreate(SuccessMessageMixin, CreateView):
    ajax_template_name='Author/author_create_ajax.html'
    form_class=AuthorForm
    success_url=reverse_lazy("News:create-author")
    success_message='Author information is created'

    def get_template_names(self):
        return self.ajax_template_name

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def form_invalid(self, form):
        errors=form.errors.as_json()
        return JsonResponse({'errors':errors},status=400)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data

        

class AuthorUpdate(LoginRequiredMixin,SuccessMessageMixin, UpdateView):
    ajax_template_name='Author/author_update_ajax.html'
    model=Author
    form_class=AuthorForm
    success_url=reverse_lazy("News:list-author")
    success_message='Author information is updated'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        errors=form.errors.as_json()
        return JsonResponse({'errors':errors},status=400)
        
    def get_template_names(self):
        return self.ajax_template_name

    def get_object(self, **kwargs):
        id=self.kwargs.get('id')
        return get_object_or_404(Author,id=id)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


class AuthorDelete(LoginRequiredMixin,SuccessMessageMixin, DeleteView):
    ajax_template_name='Author/author_delete_ajax.html'
    success_url=reverse_lazy("News:list-author")
    success_message="Author information is deleted"

    def get_template_names(self):
        return self.ajax_template_name

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data

    def get_object(self, **kwargs):
        id=self.kwargs.get('id')
        return get_object_or_404(Author,id=id)



#New details with crud
class NewList(ListView):
    template_name='news/new_list.html'
    model=News
    context_object_name='new_list'
    success_url=reverse_lazy("News:new-list")

    def get_queryset(self):
        queryset=News.objects.all()
        query=self.request.GET.get('q')

        if query:
            new_list=self.model.objects.filter(title__icontains=query)
        else:
            new_list=queryset
        return new_list


class NewsCreate(SuccessMessageMixin, CreateView):
    template_name='news/new_create.html'
    form_class=NewsForm
    success_url=reverse_lazy("News:create-news")
    success_message='News is created'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


class NewsUpdate(SuccessMessageMixin, UpdateView):
    ajax_template_name='news/new_update_ajax.html'
    form_class=NewsForm
    success_url=reverse_lazy("News:new-list")
    success_message="News has been updated"

    def get_object(self, **kwargs):
        id=self.kwargs.get('id')
        return get_object_or_404(News,id=id)

    def get_template_names(self):
        return self.ajax_template_name

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


class NewsDelete(SuccessMessageMixin, DeleteView):
    ajax_template_name='news/new_delete_ajax.html'
    model=News
    success_url=reverse_lazy("News:delete-news")
    success_message="News information is deleted"

    def get_object(self, **kwargs):
        id=self.kwargs.get('id')
        return get_object_or_404(News, id=id)

    def get_template_names(self):
        return self.ajax_template_name

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


#category crud
class CategoryList(ListView):
    ajax_template_name='category/category_list_ajax.html'
    model=Category
    context_object_name='category_list'

    def get_template_names(self):
        return self.ajax_template_name

    def get_queryset(self):
        queryset=Category.objects.all()
        query=self.request.GET.get('q')

        if query:
            category_list=self.model.objects.filter(title__icontains=query)
        else:
            category_list=queryset
        return category_list
    
class CategoryCreate(SuccessMessageMixin, CreateView):
    ajax_template_name='category/category_create_ajax.html'
    form_class=CategoryForm
    success_message="Category information is created"
    success_url=reverse_lazy("News:create-category")
    
    def get_template_names(self):
        return self.ajax_template_name

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


class CategoryUpdate(SuccessMessageMixin, UpdateView):
    ajax_template_name='category/category_update_ajax.html'
    form_class=CategoryForm
    success_message="Category is updated"
    success_url=reverse_lazy("News:category-list")

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)
        
    def get_template_names(self):
        return self.ajax_template_name

    def get_object(self, **kwargs):
        id=self.kwargs.get('id')
        return get_object_or_404(Category, id=id)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


class CategoryDelete(SuccessMessageMixin, DeleteView):
    ajax_template_name='category/category_delete_ajax.html'
    model=Category
    success_message="Category is deleted"
    success_url=reverse_lazy("News:category-list")

    def get_template_names(self):
        return self.ajax_template_name

    def get_object(self, **kwargs):
        id=self.kwargs.get('id')
        return get_object_or_404(Category, id=id)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data



#comment

class CommentList(ListView):
    ajax_template_name='comment/comment_list_ajax.html'
    context_object_name='comment_list'
    model=Comment

    def get_template_names(self):
        return self.ajax_template_name

    def get_queryset(self):
        queryset=Comment.objects.all()
        query=self.request.GET.get('q')

        if query:
            comment_list=self.model.objects.filter(name__icontains=query)
        else:
            comment_list=queryset
        return comment_list


class CommentCreate(SuccessMessageMixin,CreateView):
    ajax_template_name='comment/comment_create_ajax.html'
    form_class=CommentForm
    success_message="Comment is added"
    success_url=reverse_lazy("News:comment-create")

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_template_names(self):
        return self.ajax_template_name

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


class CommentUpdate(SuccessMessageMixin, UpdateView):
    ajax_template_name='comment/comment_update_ajax.html'
    form_class=CommentForm
    model=Comment
    success_message="Comment is updated"
    success_url=reverse_lazy("News:comment-update")
    
    def get_object(self, **kwargs):
        id=self.kwargs.get('id')
        return get_object_or_404(Comment, id=id)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_template_names(self):
        return self.ajax_template_name