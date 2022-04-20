from unicodedata import category
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.staticfiles import finders

from xhtml2pdf import pisa
from news.utils import render_to_pdf, link_callback
import xlwt


from .models import Author, News, Category, Comment
from .forms import AuthorForm, NewsForm, CategoryForm, CommentForm
import csv

class ChartDetails(TemplateView):
    def get(self, *args, **kwargs):
        author = Author.objects.all().count()
        category = Category.objects.all().count()
        news = News.objects.all().count()
        comment = Comment.objects.all().count()
        context = {'author':author,'category':category,'news':news,'comment':comment}
        return render(self.request,'dashboard/chart.html', context)

#creating the process
class DashboardTemplate(TemplateView):
    template_name='dashboard/base.html'
    success_url=reverse_lazy('news:dashboard')


class IndexView(TemplateView):
    template_name='admin/index.html'

    
    
    

#author
class AuthorList(ListView):
    context_object_name='author_list'
    model=Author
    template_name='Author/author_list.html'
    success_url=reverse_lazy("news:list-author")
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
    success_url=reverse_lazy("news:create-author")
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
    success_url=reverse_lazy("news:list-author")
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
    success_url=reverse_lazy("news:list-author")
    success_message="Author information is deleted"

    def get_template_names(self):
        return self.ajax_template_name

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data

    def get_object(self, **kwargs):
        id=self.kwargs.get('id')
        return get_object_or_404(Author,id=id)


class AuthorDetailsPdf(View):
    def get(self, request, *args, **kwargs):
        author=Author.objects.all()
        data = {
            'count':author.count(),
            'author':author
        }
        pdf = render_to_pdf('Author/author_pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

class AuthorDetailsCSV(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/csv')

        writer=csv.writer(response)
        writer.writerow(['id','name','address','email','image'])
        image = request.FILES.get('image')

        for author in Author.objects.all().values_list('id','name','address','email','image'):
            writer.writerow(author)

        response['Content-Disposition']='attachment; filename="author.csv"'

        return response


class AuthorDetailsExcel(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Author.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Author')

    # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['id','name','address','email','image']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = Author.objects.all().values_list('id','name','address','email','image')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response

#New details with crud
class NewList(ListView):
    template_name='news/new_list.html'
    model=News
    context_object_name='new_list'
    success_url=reverse_lazy("news:new-list")
    paginate_by=1

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
    success_url=reverse_lazy("news:create-news")
    success_message='News is created'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


class NewsUpdate(SuccessMessageMixin, UpdateView):
    ajax_template_name='news/new_update_ajax.html'
    form_class=NewsForm
    success_url=reverse_lazy("news:new-list")
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
<<<<<<< HEAD
    success_url=reverse_lazy("News:new-list")
=======
    success_url=reverse_lazy("news:delete-news")
>>>>>>> f9a27a9ef065607026a9dcac40798f1780bfc1ce
    success_message="News information is deleted"

    def get_object(self, **kwargs):
        id=self.kwargs.get('id')
        return get_object_or_404(News, id=id)

    def get_template_names(self):
        return self.ajax_template_name

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


class NewsDetailsPdf(View):
    def get(self, request, *args, **kwargs):
        new=News.objects.all()
        data = {
            'count':new.count(),
            'new':new,
        }
        pdf = render_to_pdf('news/new_pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


class NewsDetailsCSV(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/csv')

        writer=csv.writer(response)
        writer.writerow(['category','title','details'])

        for new in News.objects.all().values_list('category','title','details'):
            writer.writerow(new)

        response['Content-Disposition']='attachment; filename="news.csv"'

        return response

class NewsDetailsExcel(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="News.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('News')

    # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['category','title','details']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows =News.objects.all().values_list('category','title','details')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response



#category crud
class CategoryList(ListView):
    ajax_template_name='category/category_list_ajax.html'
    model=Category
    context_object_name='category_list'
    paginate_by=1

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
    success_url=reverse_lazy("news:create-category")
    
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
    success_url=reverse_lazy("news:category-list")

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
    success_url=reverse_lazy("news:category-list")

    def get_template_names(self):
        return self.ajax_template_name

    def get_object(self, **kwargs):
        id=self.kwargs.get('id')
        return get_object_or_404(Category, id=id)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data

class CategoryDetailsPdf(View):
    def get(self, request, *args, **kwargs):
        category=Category.objects.all()
        data = {
            'count':category.count(),
            'category':category
        }
        pdf = render_to_pdf('category/category_pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')



class CategoryDetailsCSV(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/csv')

        writer=csv.writer(response)
        writer.writerow(['title','details'])

        for category in Category.objects.all().values_list('title','details'):
            writer.writerow(category)

        response['Content-Disposition']='attachment; filename="category.csv"'

        return response

class CategoryDetailsExcel(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Category.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Category')

    # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['title']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = Category.objects.all().values_list('title')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response

#comment

class CommentList(ListView):
    ajax_template_name='comment/comment_list_ajax.html'
    context_object_name='comment_list'
    model=Comment
    paginate_by=1

    def get_template_names(self):
        return self.ajax_template_name

    def get_queryset(self):
        queryset=Comment.objects.all()
        query=self.request.GET.get('q')

        if query:
            comment_list=self.model.objects.filter(email__icontains=query)
        else:
            comment_list=queryset
        return comment_list


class CommentCreate(SuccessMessageMixin,CreateView):
    ajax_template_name='comment/comment_create_ajax.html'
    form_class=CommentForm
    success_message="Comment is added"
    success_url=reverse_lazy("news:comment-create")

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
    success_url=reverse_lazy('news:comment-list')
    success_message="Comment updated successfully"

    def get_template_names(self):
        return self.ajax_template_name

    def get_object(self, **kwargs):
        id=self.kwargs.get('id')
        return get_object_or_404(Comment, id=id)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data

class CommentDelete(SuccessMessageMixin, DeleteView):
    ajax_template_name='comment/comment_delete_ajax.html'
    model=Comment
    success_url=reverse_lazy('news:comment-list')
    success_message="Comment Delete Successfully"

    def get_template_names(self):
        return self.ajax_template_name
    
    def get_object(self, **kwargs):
        id=self.kwargs.get('id')
        return get_object_or_404(Comment, id=id)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data

class CommentDetailsPdf(View):
    def get(self, request, *args, **kwargs):
        comments=Comment.objects.all()
        data = {
            'count':comments.count(),
            'comments':comments
        }
        pdf = render_to_pdf('comment/comment_pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

class CommentDetailsCSV(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/csv')

        writer=csv.writer(response)
        writer.writerow(['author','news','user','email','comment','status'])

        for comment in Comment.objects.all().values_list('author','news','user','email','comment','status'):
            writer.writerow(comment)

        response['Content-Disposition']='attachment; filename="comment.csv"'

        return response


class CommentDetailsExcel(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Comment.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Comment')

    # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['user','author','news','email','comment','status']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = Comment.objects.all().values_list('user','author','news','email','comment','status')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response
