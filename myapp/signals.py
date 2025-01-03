from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from myapp.models import Book

@receiver([post_save, post_delete], sender=Book)
def update_cache(sender, **kwargs):
    books = list(Book.objects.select_related('author').all())
    cache.set('book_list', books, 60*15)
