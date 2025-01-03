from django.urls import path
from . import views
from .views import start_import_task, task_status_view

urlpatterns = [
    path('', views.login_view, name='login'),
    path('greeting/', views.greeting_view, name='greeting'),
    path('logout/', views.logout_view, name='logout'),
    path('books/', views.book_list_view, name='book_list'),
    path('start-task/', views.start_import_task, name='start-task'),
    path('task-status/<str:task_id>/', views.task_status_view, name='task-status'),
    path('statistics/', views.books_statistics_view, name='books_statistics'),
    path('raw-sql/', views.raw_sql_view, name='raw_sql'),
    path('save-books-to-mongodb/', views.save_books_to_mongodb, name='save_books_to_mongodbl'),
]
