from django.contrib import admin

from .models import Vacancy, Company, Specialty


class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'specialty', 'company', 'salary_min', 'salary_max', 'published_at')


class CompanyAdmin(admin.ModelAdmin):
    pass
    list_display = ('name', 'location', 'employee_count')


class SpecialtyAdmin(admin.ModelAdmin):
    pass
    list_display = ('code', 'title', 'picture')


admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Specialty, SpecialtyAdmin)
