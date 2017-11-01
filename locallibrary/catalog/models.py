from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import uuid

# Create your models here.
class Genre(models.Model):
 name = models.CharField(max_length=200, help_text="Enter a Book Genre")

 def __str__(self):
  return self.name

class Book(models.Model):
    """
    Model for Book
    """
    title   = models.CharField(max_length=200, help_text="Book Name")
    author  = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)  
    summary = models.CharField(max_length=1000, help_text='brief book')
    isbn    = models.CharField('ISBN', max_length=13, help_text='13 chapters <a href="https://www.isbn-international.org/content/what-isbn">ISBN Numner</a>')
    genre   = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    def __str__(self):
     return self.title

    def get_absolute_url(self):
    
     return reverse('book-detail', args=[str(self.id)])

class Author(models.Model):
 first_name    = models.CharField(max_length=200)
 last_name     = models.CharField(max_length=200)
 date_of_birth = models.DateField(null=True, blank=True)
 date_of_death = models.DateField('died', null=True, blank=True)

 def get_absolute_url(self):
  return reverse('author-detail', args=[str(self.id)])
 
 def __str__(self):

  return '%s , %s' % (self.last_name, self.first_name) 


class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True) 
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["due_back"]

    def __str__(self):
        """
        String for representing the Model object
        """
        return '%s (%s)' % (self.id,self.book.title)
    