from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_problem, name='report_problem'),
    path('my-problems/', views.my_problems, name='my_problems'),
    path('problem/<int:problem_id>/', views.problem_detail, name='problem_detail'),
    path('all-problems/', views.all_problems, name='all_problems'),
    path('problem/<int:problem_id>/respond/', views.add_response, name='add_response'),
    path('problem/<int:problem_id>/update/', views.update_problem_status, name='update_problem_status'),
    path('stats/', views.problem_stats, name='problem_stats'),
]
