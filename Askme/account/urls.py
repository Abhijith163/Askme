
from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.index),
    path('registration/',views.registraion,name="reg"),
    path('login/',views.User_login,name="login"),
    path('logout_user/',views.logout_user,name="logout"),
    path('home',views.home, name="h"),
    path('ask_questions/', views.ask_question, name='ask_question'),
    path('answers/<int:id>', views.answers, name='answer'),
    path('like_answer/<int:id>', views.like_answer, name='like_answer'),
]
