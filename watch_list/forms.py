# -*- coding: utf-8 -*-
from django import forms


class WatchListForm(forms.Form):
    total = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    type = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class': "form-control"}))
    publication_date = forms.CharField(required=False, max_length=20, widget=forms.TextInput(attrs={'class': "form-control"}))
    watch_num_of_chapter = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    cover = forms.ImageField(required=False)
    origin_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    media_type = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    url = forms.CharField(max_length=300, required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    summary = forms.CharField(max_length=2000, required=False,widget=forms.Textarea(attrs={'rows': 8, 'class': "form-control"}))


class WatchAddForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    total = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    type = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    publication_date = forms.CharField(required=False, max_length=20, widget=forms.TextInput(attrs={'class': "form-control"}))
    watch_last_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    watch_num_of_chapter = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    origin_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    media_type = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    url = forms.CharField(max_length=300, required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    summary = forms.CharField(max_length=2000, required=False, widget=forms.Textarea(attrs={'rows': 8, 'class': "form-control"}))
    cover = forms.ImageField(required=False)


# ===for test, need remove===
class photoForm(forms.Form):
    image = forms.ImageField(required=False)


class AddForm(forms.Form):
    a = forms.IntegerField()
    b = forms.IntegerField()


class CommentForm(forms.Form):
    user = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=20, required=False)
    content = forms.CharField(max_length=200)
    publication_date = forms.DateField(required=False)

# ===
