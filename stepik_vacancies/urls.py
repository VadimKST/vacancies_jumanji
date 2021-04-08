from django.contrib import admin
from django.urls import path, include

from stepik_vacancies import settings
from vacancy.views.login import RegisterUser, LoginUser, logout_user

from vacancy.views.views import (
    custom_handler404, custom_handler500, HomeView, SpecialtyView,
    VacanciesView, CompanyView, VacancyView, ApplicationSentView, SearchView,
)
from vacancy.views.mycompany import (
                                     LetsStartCompanyView, CompanyCreateView, CompanyUpdateView,
                                     MyVacancyView, VacancyCreateView, VacancyUpdateView,
                                     LetsStartResumeView, ResumeUpdateView, ResumeCreateView,
                                     )

handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('vacancies/', VacanciesView.as_view(), name='vacancies'),
    path('vacancies/cat/<str:spec>', SpecialtyView.as_view(), name='specialty'),
    path('companies/<int:pk>', CompanyView.as_view(), name='company'),
    path('vacancies/<int:pk>', VacancyView.as_view(), name='vacancy'),
    path('vacancies/<int:pk>/sent', ApplicationSentView.as_view(), name='sent'),
    path('search/', SearchView.as_view(), name='search'),

    path('mycompany/letsstart/', LetsStartCompanyView.as_view(), name='letsstart'),
    path('mycompany/', CompanyUpdateView.as_view(), name='mycompany'),
    path('mycompany/create/', CompanyCreateView.as_view(), name='create_company'),

    path('mycompany/vacancies/', MyVacancyView.as_view(), name='myvacancies'),
    path('mycompany/vacancies/create/', VacancyCreateView.as_view(), name='create_vacancy'),
    path('mycompany/vacancies/<int:pk>/', VacancyUpdateView.as_view(), name='update_vacancy'),

    path('myresume/letsstart/', LetsStartResumeView.as_view(), name='letsstart_resume'),
    path('myresume/', ResumeUpdateView.as_view(), name='myresume'),
    path('myresume/create/', ResumeCreateView.as_view(), name='create_resume'),

    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('companies/<int:comp_id>', CompanyView.as_view(), name='company'),
    path('vacancies/<int:vac_id>', VacancyView.as_view(), name='vacancy'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
