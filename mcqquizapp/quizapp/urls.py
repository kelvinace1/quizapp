from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('quizzes/<int:course_id>/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', views.start_quiz, name='start_quiz'),
    path('section/<int:section_id>/', views.take_section, name='take_section'),
    path('submit/<int:section_id>/', views.submit_section, name='submit_section'),
    path('progress/', views.user_progress, name='user_progress'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='quizapp/login.html'), name='login'),
    path('create-course/', views.create_course_quizzes_sections, name='create_course'),
    

]
