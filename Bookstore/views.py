from django.shortcuts import render

from store.models import Product
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def home(request):
    books = Product.objects.all().filter(is_available=True)
    new_books = []

    for book in books:
        new_books = [book] + new_books

    paginator = Paginator(new_books, 18)
    page = request.GET.get('page')
    paged_book = paginator.get_page(page)
    # paged_book.reverse()

    context = {
        'books': paged_book,
        # 'books': books,
    }
    return render(request, 'home.html', context)
