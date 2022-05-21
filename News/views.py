from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, JsonResponse
from django.contrib.staticfiles import finders
from django.contrib.auth import login, logout
from django.utils import timezone

from news.filters import AuthorFilter,CategoryFilter, NewsFilter, VideoFilter, CommentFilter
from news.mixins import GroupRequiredMixin
from xhtml2pdf import pisa
from news.utils import render_to_pdf, link_callback
import xlwt


from .models import Author, News, Category, Comment, Video
from .forms import AuthorForm, NewsForm, CategoryForm, CommentForm, VideoForm
import csv



class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            pass
        else:
            return redirect('accounts:login')
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class ChartDetails(TemplateView):
    def get(self, *args, **kwargs):
        author = Author.objects.all().count()
        category = Category.objects.all().count()
        news = News.objects.all().count()
        comment = Comment.objects.all().count()
        video = Video.objects.all().count()
        context = {'author':author,'category':category,'news':news,'comment':comment,'video':video}
        return render(self.request,'dashboard/chart.html', context)

#creating the process
class DashboardTemplate(LoginRequiredMixin,TemplateView):
    template_name='dashboard/base.html'

class IndexView(TemplateView):
    template_name='admin/index.html'


#author
class AuthorList(GroupRequiredMixin,ListView):
    model = Author
    template_name = 'Author/author_list.html'
    paginate_by = 4
    group_required = ['Author']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author_filter'] = AuthorFilter(self.request.GET, queryset=self.get_queryset())
        return context


class AuthorCreate(GroupRequiredMixin,LoginRequiredMixin,SuccessMessageMixin, CreateView):
    template_name = 'Author/author_create.html'
    form_class = AuthorForm
    success_url = reverse_lazy("news:create-author")
    success_message = 'Author information is created'
    group_required = ['Author']

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data

    #setup the initial values 
    def get_initial(self):
        return {'name':'abc','address':'self','email':'asdf@gmail.com'}


class AuthorUpdate(GroupRequiredMixin,LoginRequiredMixin,SuccessMessageMixin, UpdateView):
    template_name = 'Author/author_update.html'
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy("news:list-author")
    success_message = 'Author information is updated'
    group_required = ['Author']


    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_object(self, **kwargs):
        id=self.kwargs.get('id')
        return get_object_or_404(Author,id=id)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data

class AuthorDelete(GroupRequiredMixin,LoginRequiredMixin,SuccessMessageMixin, DeleteView):
    template_name = 'Author/author_delete.html'
    success_url = reverse_lazy("news:list-author")
    success_message = "Author information is deleted"
    group_required = ['Author']

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data

    def get_object(self, **kwargs):
        id=self.kwargs.get('id')
        return get_object_or_404(Author,id=id)


#convert text data into pdf format data
class AuthorDetailsPdf(View):
    def get(self, request, *args, **kwargs):
        author = Author.objects.all()
        data = {
            'count':author.count(),
            'author':author
        }
        pdf = render_to_pdf('Author/author_pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

class AuthorDetailsCSV(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/csv')

        writer = csv.writer(response)
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

        columns = ['id','name','addrFess','email','image']

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
class NewList(GroupRequiredMixin,ListView):
    template_name = 'news/new_list.html'
    model = News
    success_url = reverse_lazy("news:new-list")
    paginate_by = 4
    group_required = ['Author']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context

class NewsCreate(GroupRequiredMixin,LoginRequiredMixin,SuccessMessageMixin, CreateView):
    template_name = 'news/new_create.html'
    form_class = NewsForm
    success_url = reverse_lazy("news:create-news")
    success_message = 'News is created'
    group_required = ['Author']

    def form_valid(self, form):
        form.instance.date_created = timezone.now()
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


    def get_initial(self):
        return {'title':'awe','details':'wradd'}


class NewsUpdate(GroupRequiredMixin,LoginRequiredMixin,SuccessMessageMixin, UpdateView):
    template_name = 'news/new_update.html'
    form_class = NewsForm
    success_url = reverse_lazy("news:new-list")
    success_message = "News has been updated"
    group_required = ['Author']

    def get_object(self, **kwargs):
        id=self.kwargs.get('id')
        return get_object_or_404(News,id=id)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


class NewsDelete(GroupRequiredMixin,LoginRequiredMixin,SuccessMessageMixin, DeleteView):
    template_name = 'news/new_delete.html'
    model = News
    success_url = reverse_lazy("news:new-list")
    success_message = "News information is deleted"
    group_required = ['Author']

    def get_object(self, **kwargs):
        id = self.kwargs.get('id')
        return get_object_or_404(News, id=id)



    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data

class NewsDetailsCSV(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/csv')

        writer=csv.writer(response)
        writer.writerow(['author','category','subcategory','title','image','details','is_published','date_created'])

        for new in News.objects.all().values_list('author','category','subcategory','title','image','details','is_published','date_created'):
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

        rows =News.objects.all().values_list('author','category','subcategory','title','image','details','is_published','date_created')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response



#category crud
class CategoryList(ListView):
    template_name = 'category/category_list.html'
    model = Category
    paginate_by=4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_filter']=CategoryFilter(self.request.GET, self.get_queryset())
        return context


class CategoryCreate(SuccessMessageMixin, CreateView):
    template_name = 'category/category_create.html'
    form_class = CategoryForm
    success_message = "Category information is created"
    success_url = reverse_lazy("news:create-category")

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data

    def get_initial(self):
        return {'title':'asdfas'}


class CategoryUpdate(SuccessMessageMixin, UpdateView):
    template_name = 'category/category_update.html'
    form_class = CategoryForm
    success_message = "Category is updated"
    success_url = reverse_lazy("news:category-list")

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_object(self, **kwargs):
        id=self.kwargs.get('id')
        return get_object_or_404(Category, id=id)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


class CategoryDelete(SuccessMessageMixin, DeleteView):
    template_name='category/category_delete.html'
    model=Category
    success_message="Category is deleted"
    success_url=reverse_lazy("news:category-list")

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
class CommentList(GroupRequiredMixin,ListView):
    template_name = 'comment/comment_list.html'
    context_object_name = 'comment_list'
    model = Comment
    paginate_by = 2
    group_required = ['Reader']

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['comment_filter']=CommentFilter(self.request.GET, queryset=self.get_queryset())
        return context


class CommentCreate(GroupRequiredMixin,LoginRequiredMixin,SuccessMessageMixin,CreateView):
    template_name = 'comment/comment_create.html'
    form_class = CommentForm
    success_message = "Comment is added"
    success_url = reverse_lazy("news:comment-create")
    group_required = ['Reader']

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data

    def get_initial(Self):
        return {'email':'asdf@gmail.com'}


class CommentUpdate(GroupRequiredMixin,LoginRequiredMixin,SuccessMessageMixin, UpdateView):
    template_name = 'comment/comment_update.html'
    form_class = CommentForm
    model = Comment
    success_url = reverse_lazy('news:comment-list')
    success_message = "Comment updated successfully"
    group_required = ['Reader']

    def get_object(self, **kwargs):
        id = self.kwargs.get('id')
        return get_object_or_404(Comment, id=id)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data

class CommentDelete(GroupRequiredMixin,LoginRequiredMixin,SuccessMessageMixin, DeleteView):
    template_name = 'comment/comment_delete.html'
    model = Comment
    success_url = reverse_lazy('news:comment-list')
    success_message = "Comment Delete Successfully"
    group_required = ['Reader']

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


class VideoCreate(GroupRequiredMixin,SuccessMessageMixin, CreateView):
    template_name = 'video/create_video.html'
    form_class = VideoForm
    success_message = "Video is created"
    success_url = reverse_lazy('news:create-video')
    group_required = ['Author']

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


class VideoList(GroupRequiredMixin,ListView):
    template_name = 'video/video_list.html'
    model = Video
    paginate_by = 2
    group_required = ['Author']

    #search garne query
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['video_filter']=VideoFilter(self.request.GET, queryset=self.get_queryset())
        return context

class VideoUpdate(GroupRequiredMixin,SuccessMessageMixin, UpdateView):
    template_name = 'video/video_update.html'
    form_class = VideoForm
    success_url = reverse_lazy('news:video-list')
    success_message = 'Video Update Successfully'
    group_required = ['Author']

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_object(self, **kwargs):
        id = self.kwargs.get('id')
        return get_object_or_404(Video, id=id)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data

class VideoDelete(GroupRequiredMixin,SuccessMessageMixin, DeleteView):
    template_name = 'video/video_delete.html'
    success_message = 'Video deleted successfull'
    success_url = reverse_lazy('news:video-list')
    group_required = ['Author','Reader']


    def get_object(self, **kwargs):
        id = self.kwargs.get('id')
        return get_object_or_404(Video, id=id)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data