from django.shortcuts import render

from store.models import Product
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def home(request):
    books = Product.objects.all().filter(is_available=True)
    paginator = Paginator(books, 12)
    page = request.GET.get('page')
    paged_book = paginator.get_page(page)

    context = {
        'books': paged_book,
    }
    return render(request, 'home.html', context)
