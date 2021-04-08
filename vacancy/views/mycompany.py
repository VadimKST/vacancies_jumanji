from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, UpdateView, ListView

from vacancy.forms import AddCompanyForm, AddVacancyForm, AddResumeForm
from vacancy.models import Application, Vacancy


class LetsStartCompanyView(LoginRequiredMixin, TemplateView):
    template_name = 'vacancy/company-create.html'


class CompanyCreateView(LoginRequiredMixin, CreateView):
    form_class = AddCompanyForm
    template_name = 'vacancy/company-form.html'
    extra_context = {'page_title': 'Моя компания | Джуманджи'}

    def get_success_url(self):
        return reverse('company', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        company = form.save(commit=False)
        user = self.request.user
        company.owner = user
        return super().form_valid(form)


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    form_class = AddCompanyForm
    template_name = 'vacancy/company-form.html'
    extra_context = {'page_title': 'Моя компания | Джуманджи'}

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return redirect('letsstart')

    def get_object(self, queryset=None):
        return self.request.user.company

    def get_success_url(self):
        return reverse('company', kwargs={'pk': self.object.pk})


class VacancyCreateView(LoginRequiredMixin, CreateView):
    form_class = AddVacancyForm
    template_name = 'vacancy/vacancy_edit.html'
    extra_context = {'page_title': 'Моя компания | Джуманджи'}

    def get_success_url(self):
        return reverse('vacancy', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        vacancy = form.save(commit=False)
        company = self.request.user.company
        vacancy.company = company
        return super().form_valid(form)


class VacancyUpdateView(LoginRequiredMixin, UpdateView):
    form_class = AddVacancyForm
    template_name = 'vacancy/vacancy_edit.html'
    context_object_name = 'Vacancy'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Моя компания | Джуманджи'
        context['applications'] = Application.objects.filter(vacancy=self.object.pk)
        return context

    def get_queryset(self):
        return (
            Vacancy.objects.filter(company__owner=self.request.user).
            select_related('specialty').
            annotate(application_count=Count('applications'))
                 )

    def get_success_url(self):
        return reverse('vacancy', kwargs={'pk': self.object.pk})


class MyVacancyView(LoginRequiredMixin, ListView):
    model = Vacancy
    template_name = 'vacancy/vacancy_list.html'
    context_object_name = 'MyVacancies'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Мои вакансии | Джуманджи'
        return context

    def get_queryset(self):
        return (
            Vacancy.objects.
            filter(company__owner=self.request.user.id).
            annotate(application_count=Count('applications'))
        )


class LetsStartResumeView(LoginRequiredMixin, TemplateView):
    template_name = 'vacancy/resume-create.html'


class ResumeCreateView(LoginRequiredMixin, CreateView):
    form_class = AddResumeForm
    template_name = 'vacancy/resume-edit.html'
    extra_context = {'page_title': 'Моё резюме | Джуманджи'}

    def get_success_url(self):
        return reverse('myresume')

    def form_valid(self, form):
        resume = form.save(commit=False)
        owner = self.request.user
        resume.user = owner
        return super().form_valid(form)


class ResumeUpdateView(LoginRequiredMixin, UpdateView):
    form_class = AddResumeForm
    template_name = 'vacancy/resume-edit.html'
    context_object_name = 'Resume'
    extra_context = {'page_title': 'Моё резюме | Джуманджи'}

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return redirect('letsstart_resume')

    def get_object(self, queryset=None):
        return self.request.user.resume

    def get_success_url(self):
        return reverse('myresume')
