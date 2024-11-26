import re
from django import forms
from .models import *
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from .models import QuizCreator

class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'confirm_password', 'placeholder': 'Confirm Password'}),
        max_length=128,
        label="Confirm Password"
    )

    class Meta:
        model = QuizCreator
        fields = ['name', 'email', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'id': 'name', 'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'id': 'email', 'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'id': 'password', 'placeholder': 'Password'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@gmail.com'):
            raise ValidationError("Email must be a valid Gmail address.")
        if QuizCreator.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 5:
            raise ValidationError("Password must be at least 5 characters long.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data.get("password"))
        if commit:
            user.save()
        return user

    
class QuizDetails1Form(forms.ModelForm):
    class Meta:
        model = QuizDetails1
        fields = ['title_quiz', 'description_quiz', 'quiz_img']

    def clean_title_quiz(self):
        title = self.cleaned_data.get('title_quiz')
        if not title or len(title) > 200:
            raise forms.ValidationError("Title cannot be empty or exceed 200 characters.")
        return title

    def clean_description_quiz(self):
        description = self.cleaned_data.get('description_quiz')
        if not description or len(description) > 1000:
            raise forms.ValidationError("Description cannot be empty or exceed 1000 characters.")
        return description


    def clean_quiz_img(self):
        image = self.cleaned_data.get('quiz_img')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file size should not exceed 5MB.")
            if not image.name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                raise forms.ValidationError("Please upload a valid image file (jpg, jpeg, png, gif).")
        return image


class QuizDetails2Form(forms.ModelForm):
    class Meta:
        model = QuizDetails2
        fields = ['question', 'option1', 'option2', 'option3', 'correct_option', 'points']

    def clean_question(self):
        question = self.cleaned_data.get('question')
        if not question or len(question) > 300:
            raise forms.ValidationError("Question cannot be empty or exceed 300 characters.")
        return question

    def clean_points(self):
        points = self.cleaned_data.get('points')
        if not isinstance(points, int) or points < 0:
            raise forms.ValidationError("Points must be a non-negative integer.")
        return points

    def clean_option1(self):
        option1 = self.cleaned_data.get('option1')
        if not option1 or len(option1) > 100:
            raise forms.ValidationError("Option 1 cannot be empty or exceed 100 characters.")
        return option1

    def clean_option2(self):
        option2 = self.cleaned_data.get('option2')
        if not option2 or len(option2) > 100:
            raise forms.ValidationError("Option 2 cannot be empty or exceed 100 characters.")
        return option2

    def clean_option3(self):
        option3 = self.cleaned_data.get('option3')
        if not option3 or len(option3) > 100:
            raise forms.ValidationError("Option 3 cannot be empty or exceed 100 characters.")
        return option3

    def clean_correct_option(self):
        correct_option = self.cleaned_data.get('correct_option')
        if correct_option not in ['option1', 'option2', 'option3']:
            raise forms.ValidationError("Correct option must be one of 'option1', 'option2', or 'option3'.")
        return correct_option
    
    
class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    