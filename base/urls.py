from django.urls import path

from . import views

urlpatterns = [
    path("user-login/", views.applicant_login_view, name="user-login"),
    path("user-register/", views.applicant_registration_view, name="user-register"),
    path("company-register/", views.company_registration_view, name="company-register"),
    path("company-login/", views.company_login_view, name="company-login"),
    path("", views.index, name="index"),
    path("company-dashboard/", views.create_job, name="company-dashboard"),
    path("company-dashboard/update-job/<str:pk>/", views.update_job, name="update-job"),
    path("company-dashboard/delete-job/<str:pk>/", views.delete_job, name="delete-job"),
]