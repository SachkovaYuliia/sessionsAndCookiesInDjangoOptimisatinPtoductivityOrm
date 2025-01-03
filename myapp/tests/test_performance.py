import time
from django.test import TestCase
from .query_tests import get_books_without_optimization, get_books_with_optimization
from myapp.models import Author, Book, Review
import random
from datetime import datetime, timedelta


class PerformanceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Створення даних для тестів."""
        authors = [Author.objects.create(name=f"Author {i}") for i in range(10)]
        for i in range(1000):  # 1000 книг для тестування продуктивності
            book = Book.objects.create(
                title=f"Book {i}",
                author=random.choice(authors),
                published_date=datetime.now() - timedelta(days=random.randint(1, 1000))
            )
            for _ in range(random.randint(1, 5)):
                Review.objects.create(
                    book=book,
                    content=f"Review content for {book.title}",
                    rating=random.randint(1, 5)
                )

    def measure_execution_time(self, func):
        """Допоміжний метод для вимірювання часу виконання."""
        start_time = time.time()
        func()
        return time.time() - start_time

    def test_performance_without_optimization(self):
        """Тест продуктивності без оптимізації."""
        duration = self.measure_execution_time(get_books_without_optimization)
        print(f"Time without optimization: {duration:.2f} seconds")

    def test_performance_with_optimization(self):
        """Тест продуктивності з оптимізацією."""
        duration = self.measure_execution_time(get_books_with_optimization)
        print(f"Time with optimization: {duration:.2f} seconds")
