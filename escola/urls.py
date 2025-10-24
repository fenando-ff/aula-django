from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_aluno, name='aluno_list'),
    path('create/', views.aluno_create, name='aluno_create'),
    path('update/<int:aluno_id>/', views.aluno_update, name='aluno_update'),
    path('delete/<int:aluno_id>/', views.aluno_delete, name='aluno_delete'),
]
