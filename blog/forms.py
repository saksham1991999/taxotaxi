from django import forms

class CommentForm(forms.Form):
    comment_text = forms.CharField(widget = forms.Textarea(attrs={'class':"form-control", 'rows':"3"}))