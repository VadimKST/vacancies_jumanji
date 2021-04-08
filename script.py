import os
import django

os.environ["DJANGO_SETTINGS_MODULE"] = 'stepik_vacancies.settings'
django.setup()

from vacancy.models import Vacancy, Company, Specialty
from vacancy.data import jobs, companies, specialties

if __name__ == '__main__':
    for company in companies:
        comp = Company.objects.create(
            name=company['title'],
            location=company['location'],
            description=company['description'],
            employee_count=company['employee_count'],
        )

    for specialty in specialties:
        spec = Specialty.objects.create(
            code=specialty['code'],
            title=specialty['title'],
        )

    for job in jobs:
        vacancy = Vacancy.objects.create(
            title=job['title'],
            specialty=Specialty.objects.get(code=job["specialty"]),
            company=Company.objects.get(pk=job['company']),
            skills=job['skills'],
            description=job['description'],
            salary_min=job['salary_from'],
            salary_max=job['salary_to'],
            published_at=job['posted'],
        )
