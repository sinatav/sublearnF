
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.views.generic import TemplateView

from users import views

app_name = "users"

urlpatterns = [
    path('', views.user_home, name='home'),
    path(r'register/', views.signup, name="register"),
    path(r'profile/', views.user_profile, name="profile"),
    path(r'exam', views.get_exam, name="exam"),
    path(r'login/', auth_views.LoginView.as_view(template_name='users/login.html'), name="login"),
    path(r'logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name="logout"),
    path(r'confirm/', TemplateView.as_view(template_name='users/confirm.html'), name="confirm"),
    path(r'quize/', views.get_quiz, name="quiz"),
    path(r'index', TemplateView.as_view(template_name='index.html'), name="home"),
    path(r'', views.user_index, name='index'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('quiz_result/', views.quiz_result, name='quiz_rez'),
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html',
            email_template_name='users/password_reset_email.html', subject_template_name='users/password_reset_subject.txt',
            success_url = '/users/password_reset/done'),
        name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                                success_url='/users/reset/done'),
        name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name='password_reset_complete'),
    url(r'buy_premium/', views.buy_premium, name='buy_premium'),
]
