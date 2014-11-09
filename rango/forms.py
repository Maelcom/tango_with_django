from django import forms
from rango.models import Page, Category, UserProfile


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")

    class Meta:
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")

    class Meta:
        model = Page
        fields = ('title', 'url')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')


class MailerForm(forms.Form):
    login = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={'placeholder': 'From:'}))
    to = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={'placeholder': 'To:'}))
    pwd = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your email password'}))

    class Meta:
        fields = ('login', 'to', 'pwd')
