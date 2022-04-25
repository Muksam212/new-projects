from django import forms
from .models import Author, News,Category, Comment
from ckeditor.widgets import CKEditorWidget

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name','email','address','image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class' : 'form-control',
            'placeholder':'enter your name'
        })
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
        # self.fields['category'].widget.attrs.update({
        #     'class': 'form-control select2'
        # })
 

class NewsForm(forms.ModelForm):
    details=forms.CharField(widget=CKEditorWidget())
    class Meta:
        model=News
        fields=['category','title','image','details','subcategory']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class' : 'form-control',
            'placeholder':'enter your title'
        })
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })

 
class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['title']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class' : 'form-control',
            'placeholder':'enter your title'
        })
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })


class CommentForm(forms.ModelForm):
    comment=forms.CharField(widget=CKEditorWidget, label='Comment')
    class Meta:
        model=Comment
        fields=['author','news','user','email','comment','status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget.attrs.update({
            'class' : 'form-control',
            'placeholder':'enter your name'
        })
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })