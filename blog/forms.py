from django import forms

class CommentForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    comment_text = forms.CharField(widget = forms.Textarea(attrs={'class':"form-control", 'rows':"3"}))