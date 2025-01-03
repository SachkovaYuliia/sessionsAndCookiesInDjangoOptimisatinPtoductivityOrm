from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    published_date = models.DateField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['title']),
        ]

    def __str__(self):
        return self.title

class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(null=True, blank=True) 

    class Meta:
        indexes = [
            models.Index(fields=['rating']),
        ]

    def __str__(self):
        return f"Review for {self.book.title}"
