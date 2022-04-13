import imp
from itertools import count, product
from django.db import models
from django.urls import reverse
from category.models import Category
from accounts.models import Account
from django.db.models import Count


class Product(models.Model):
    book_name = models.CharField(max_length=200, blank=False)
    slug = models.SlugField(max_length=200, unique=True)
    writer = models.CharField(max_length=100, blank=False)
    # eita korar karon holo category delete korle oi category er sob product o delete hoye jabe
    genre = models.ForeignKey(Category, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='photos/store', blank=True)
    price = models.IntegerField()
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    description = models.TextField(max_length=500)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.genre.slug, self.slug])

    def __str__(self):
        return self.book_name


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    # rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
