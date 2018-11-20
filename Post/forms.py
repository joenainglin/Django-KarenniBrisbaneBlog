from django import forms
from .models import * 
from tinymce import TinyMCE


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    body = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )
    class Meta:
        model = Comment
        fields = ( 'email', 'body')


class SearchForm(forms.Form):
    query = forms.CharField()



class CreatePostForm(forms.ModelForm):
    body = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )
    class Meta:
        model = Post
        fields = ('title', 'body', 'status','category','tags', 'image' )



class EditPost(forms.ModelForm):
    body = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )
    class Meta:
        model = Post
        fields = ('title', 'body', 'tags', 'image', 'status')