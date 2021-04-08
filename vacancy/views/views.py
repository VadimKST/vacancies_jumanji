from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView, DetailView

from vacancy.models import Vacancy, Company, Specialty
from vacancy.forms import AddApplicationForm


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')


def custom_handler404(request, exception):
    return HttpResponseNotFound('Страница не найдена!')


class HomeView(TemplateView):
    template_name = 'vacancy/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Джуманджи'
        context["specialties"] = Specialty.objects.annotate(vacancies_count=Count('vacancies'))
        context["companies"] = Company.objects.annotate(vacancies_count=Count('vacancies'))
        return context


class SpecialtyView(ListView):
    model = Vacancy
    template_name = 'vacancy/vacancies.html'
    context_object_name = 'Vacancies'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Вакансии | Джуманджи'
        context['specialty'] = get_object_or_404(Specialty, code=self.kwargs['spec'])
        return context

    def get_queryset(self):
        return Vacancy.objects.filter(specialty__code=self.kwargs['spec']).select_related('specialty')


class VacanciesView(ListView):
    model = Vacancy
    template_name = 'vacancy/vacancies.html'
    context_object_name = 'Vacancies'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Вакансии | Джуманджи'
        context['specialty'] = {'title': 'Все вакансии'}
        return context

    def get_queryset(self):
        return super().get_queryset().select_related('specialty')


class CompanyView(DetailView):
    model = Company
    template_name = 'vacancy/company.html'
    context_object_name = 'Company'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Компания | Джуманджи'
        context['vacancies'] = Vacancy.objects.filter(company=self.kwargs['pk']).select_related('specialty')
        return context


class VacancyView(DetailView):
    queryset = Vacancy.objects.all().select_related('company')
    template_name = 'vacancy/vacancy.html'
    context_object_name = 'Vacancy'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Вакансия | Джуманджи'
        context['form'] = AddApplicationForm
        return context

    @method_decorator(login_required)
    def post(self, request, pk):
        form = AddApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user_id = request.user.pk
            application.vacancy_id = pk
            application.save()
            return redirect('sent', pk=pk)
        self.object = self.get_object()
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class ApplicationSentView(LoginRequiredMixin, DetailView):
    model = Vacancy
    template_name = 'vacancy/sent.html'


class SearchView(ListView):
    model = Vacancy
    template_name = "vacancy/search.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            object_list = Vacancy.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(skills__icontains=query),
            )
        else:
            object_list = Vacancy.objects.all().select_related('specialty')
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "")
        context["search_string"] = query
        return context
