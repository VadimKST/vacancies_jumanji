from django.contrib.auth import get_user_model
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class Vacancy(models.Model):
    title = models.CharField(max_length=120)
    specialty = models.ForeignKey('Specialty', on_delete=models.CASCADE, related_name="vacancies")
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name="vacancies")
    skills = models.CharField(max_length=300)
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'


class Company(models.Model):
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=30)
    logo = models.URLField(default='https://place-hold.it/100x60')
    description = models.TextField()
    employee_count = models.IntegerField()
    owner = models.OneToOneField(get_user_model(), on_delete=models.PROTECT, related_name="company", null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class Specialty(models.Model):
    code = models.CharField(max_length=15, unique=True)
    title = models.CharField(max_length=120)
    picture = models.URLField(default='https://place-hold.it/100x60')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'


class Application(models.Model):
    username = models.CharField(max_length=30, unique=True)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    cover_letter = models.TextField(max_length=500)
    vacancy = models.ForeignKey('Vacancy', on_delete=models.CASCADE, related_name="applications")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="applications")

    def __str__(self):
        return self.username


class Resume(models.Model):
    STATUS_CHOICES = [
        ('not_looking', 'Не ищу работу'),
        ('taking_offers', 'Рассматриваю предложения'),
        ('looking', 'Ищу работу'),
    ]
    GRADE_CHOICES = [
        ('intern', 'Стажер'),
        ('junior', 'Джуниор'),
        ('middle', 'Миддл'),
        ('senior', 'Синьор'),
        ('lead', 'Лид'),
    ]
    user = models.OneToOneField(get_user_model(), null=True, on_delete=models.CASCADE, related_name="resume")
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    salary = models.IntegerField(default=0)
    specialty = models.ForeignKey(Specialty, null=True, blank=True, on_delete=models.SET_NULL, related_name='resume')
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES)
    education = models.TextField()
    experience = models.TextField()
    portfolio = models.URLField(max_length=120, default='', blank=True)

    def __str__(self):
        return self.name
