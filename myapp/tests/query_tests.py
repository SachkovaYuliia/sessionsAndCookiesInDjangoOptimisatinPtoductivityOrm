from myapp.models import Book

def get_books_without_optimization():
    """Запит без оптимізації."""
    books = Book.objects.all()
    data = []
    for book in books:
        author = book.author
        reviews = book.reviews.all()
        data.append({
            'title': book.title,
            'author': author.name,
            'reviews': [{'content': review.content} for review in reviews]
        })
    return data

def get_books_with_optimization():
    """Запит з оптимізацією."""
    books = Book.objects.select_related('author').prefetch_related('reviews')
    data = []
    for book in books:
        reviews = book.reviews.all()
        data.append({
            'title': book.title,
            'author': book.author.name,
            'reviews': [{'content': review.content} for review in reviews]
        })
    return data
