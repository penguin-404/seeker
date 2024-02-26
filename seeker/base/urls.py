from django.urls import path

from . import views

urlpatterns = [
    path("user-login/", views.applicant_login_view, name="user-login"),
    path("logout/", views.logoutpage, name="logout"),
    path("user-register/", views.applicant_registration_view, name="user-register"),
    path("company-register/", views.company_registration_view, name="company-register"),
    path("company-login/", views.company_login_view, name="company-login"),
    path("", views.index, name="index"),
    path("profile/<str:pk>/", views.profile_view, name="profile"),
    path("find-work/", views.find_work, name="find-work"),
    path('apply/', views.apply_for_job, name='apply_for_job'),
    path("bid/", views.process_bid, name="bid"),
    path('create-profile/', views.create_profile, name='create-profile'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path("user-dashboard/", views.user_dashboard, name="user-dashboard"),
    path("company-dashboard/", views.create_job, name="company-dashboard"),
    path("company-dashboard/update-job/<str:pk>/", views.update_job, name="update-job"),
    path("company-dashboard/delete-job/<str:pk>/", views.delete_job, name="delete-job"),
]