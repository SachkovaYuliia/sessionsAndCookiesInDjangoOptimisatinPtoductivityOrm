from celery import shared_task
from django.core.mail import send_mail
import csv
from .models import Book  

@shared_task
def import_books_from_csv(file_path):
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            Book.objects.create(
                title=row['title'],
                author=row['author'],
                published_date=row['published_date']
            )
    return "Books imported successfully!"

@shared_task
def send_confirmation_email(email):
    send_mail(
        'Task Completed',
        'Your task of importing books has been completed successfully!',
        'noreply@example.com',
        [email],
    )
