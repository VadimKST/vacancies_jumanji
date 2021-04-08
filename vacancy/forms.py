from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Company, Vacancy, Application, Resume


class AddCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'location', 'description', 'employee_count']


class AddVacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = [
            'title',
            'specialty',
            'skills',
            'description',
            'salary_min',
            'salary_max',
            'published_at',
        ]


class AddApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['username', 'phone', 'cover_letter']
        labels = {
            'username': "Ваше имя",
            'phone': "Ваш номер телефона",
            'cover_letter': "О себе",
        }


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class AddResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = [
            'name',
            'surname',
            'status',
            'salary',
            'specialty',
            'grade',
            'education',
            'experience',
            'portfolio',
        ]
        labels = {
            'name': 'Имя',
            'surname': 'Фамилия',
            'status': 'Готовность к работе',
            'salary': 'Ожидаемая зарплата',
            'specialty': 'Специализация',
            'grade': 'Квалификация',
            'education': 'Образование',
            'experience': 'Опыт работы',
            'portfolio': 'Ссылка на портфолио',
        }
