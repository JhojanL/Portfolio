"""FINAL_PROJECT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Project import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("exams", views.get_exams, name="exams"),
    path("start_exam/<int:exam_id>", views.start_exam, name="start_exam"),
    path("exam/<int:exam_id>", views.exam_view, name="exam"),
    path('exam/<int:exam_id>/save/', views.save_exam, name='save_exam'),
    path("exam_edit/<int:exam_id>/<str:filter>", views.exam_edit, name="exam_edit"),
    path("question_update/<int:question_id>", views.question_update, name="question_update"),
    path("new_question/<int:exam_id>", views.new_question, name="new_question"),
    path("question_delete/<int:question_id>/<int:exam_id>", views.question_delete, name="question_delete"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("exam_result/<int:result_id>", views.exam_result, name="exam_result"),
]
