from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import modelformset_factory

from .models import Course, Quiz, Section, Question

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['course', 'title']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }

QuizFormSet = modelformset_factory(Quiz, form=QuizForm, extra=1, can_delete=False)

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['quiz', 'difficulty']
        widgets = {
            'quiz': forms.Select(attrs={'class': 'form-select'}),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
        }

SectionFormSet = modelformset_factory(Section, form=SectionForm, extra=1, can_delete=False)

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['section', 'text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option']
        widgets = {
            'section': forms.Select(attrs={'class': 'form-select'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'option_a': forms.TextInput(attrs={'class': 'form-control'}),
            'option_b': forms.TextInput(attrs={'class': 'form-control'}),
            'option_c': forms.TextInput(attrs={'class': 'form-control'}),
            'option_d': forms.TextInput(attrs={'class': 'form-control'}),
            'correct_option': forms.Select(attrs={'class': 'form-select'}),
        }

QuestionFormSet = modelformset_factory(Question, form=QuestionForm, extra=1, can_delete=False)
