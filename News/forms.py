from django import forms
from .models import Author, News,Category, Comment,  Banneradd
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
        self.fields['image'].widget.attrs.update({
            'class':'form-control',
            'onchange':'loadFile(event)',
        })
        # self.fields['category'].widget.attrs.update({
        #     'class': 'form-control select2'
        # })
 

class NewsForm(forms.ModelForm):
    details=forms.CharField(widget=CKEditorWidget())
    class Meta:
        model=News
        fields=['author','category','title','image','details']

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
        self. fields['image'].widget.attrs.update({
            'class': 'form-control',
            'onchange' : 'loadFile(event)'
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

class BanneraddForm(forms.ModelForm):
    class Meta:
        model = Banneradd
        fields = ['title', 'image' ,'is_active']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class':'form-control',
            'placeholder':'Enter your title'
        })
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class':'form-control',
            })
        self.fields['image'].widget.attrs.update({
            'class': 'form-control',
            'onchange': 'loadFile(event)'
        })
            
