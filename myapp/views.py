from django.shortcuts import render,redirect
from django.http import HttpResponse 
from django.core.cache import cache
from myapp.models import Book
from django.http import JsonResponse
from .tasks import import_books_from_csv, send_confirmation_email
from celery.result import AsyncResult
from .models import Author, Book, Review
from django.db.models import Avg, Count
from django.db import connection
from pymongo import MongoClient


def login_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')

        response = redirect('greeting')
        response.set_cookie('name', name, max_age=60 * 15)  

        request.session['age'] = age
        return response

    return render(request, 'login.html')

def greeting_view(request):
    name = request.COOKIES.get('name')
    age = request.session.get('age')

    if not name or not age:
        return redirect('login')
    """Автоподовження cookies"""
    response = render(request, 'greeting.html', {'name': name, 'age': age})
    response.set_cookie('name', name, max_age=60 * 60 * 24 * 7) 
    return response

def logout_view(request):
    """Видаляємо cookies"""
    response = redirect('login')
    response.delete_cookie('name')
    
    """Видаляємо сесійні дані"""
    request.session.flush()
    return response

def book_list_view(request):
    """Відображаємо список книг з авторами"""
    books = cache.get('book_list')

    if not books:
        books = list(Book.objects.select_related('author').all())
        cache.set('book_list', books, 60*15) 

    return render(request, 'book_list.html', {'books': books})

def start_import_task(request):
    file_path = 'myproject\books.csv'
    import_books_from_csv.delay(file_path)
    send_confirmation_email.delay('test@test.com')
    return JsonResponse({'message': 'Task started!'})

def task_status_view(request, task_id):
    task = AsyncResult(task_id)
    return render(request, 'task_status.html', {'task_id': task_id, 'status': task.status})

def books_statistics_view(request):
    authors = Author.objects.annotate(
        avg_rating=Avg('book__review__rating'),  
    )

    books = Book.objects.annotate(
        review_count=Count('review'),         
        avg_rating=Avg('review__rating'),      
    ).order_by('-review_count', '-avg_rating')  

    context = {
        'authors': authors,
        'books': books,
    }
    return render(request, 'books_statistics.html', context)

def raw_sql_view(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT a.id, a.name, COUNT(r.id) AS review_count
            FROM myapp_author a
            JOIN myapp_book b ON a.id = b.author_id
            JOIN myapp_review r ON b.id = r.book_id
            GROUP BY a.id, a.name
            HAVING COUNT(r.id) > 10
        """)
        authors = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) FROM myapp_book")
        total_books = cursor.fetchone()[0]

    context = {
        'authors': authors,
        'total_books': total_books,
    }
    return render(request, 'raw_sql.html', context)

def save_books_to_mongodb(request):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['mydatabase']
    books_collection = db['books']

    books = Book.objects.all()
    for book in books:
        books_collection.insert_one({
            'title': book.title,
            'author': book.author.name,
        })

    return HttpResponse("Books saved to MongoDB")