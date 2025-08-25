from django.urls import path
from . import views

urlpatterns = [ 
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path('signup_step1/', views.signup_step1, name='signup_step1'),
    path('signup_step2/', views.signup_step2, name='signup_step2'),

    path('profile/', views.profile_view, name='profile'),

    path('career_quiz/', views.career_quiz, name='career_quiz'),
    path('career_result/<str:user>/', views.career_result, name='career_result'),
    # path('ai-recommendation/', views.ai_recommendation, name='ai_recommendation'),
]