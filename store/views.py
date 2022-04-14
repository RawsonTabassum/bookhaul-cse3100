from email import message
from django.core.exceptions import ObjectDoesNotExist
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls.base import is_valid_path

from carts.models import CartItem
from store.forms import ReviewForms
from .models import Product, ReviewRating
from category.models import Category
from orders.models import OrderProduct
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib import messages


def store(request, category_slug=None):
    categories = None
    books = None

    if category_slug != None:
        # genre thakle seta return korbe, na thakle 404 return korbe
        categories = get_object_or_404(Category, slug=category_slug)
        books = Product.objects.filter(genre=categories, is_available=True)
        paginator = Paginator(books, 8)
        page = request.GET.get('page')
        paged_book = paginator.get_page(page)
        book_count = books.count()
    else:
        books = Product.objects.all().filter(is_available=True)
        paginator = Paginator(books, 8)
        page = request.GET.get('page')
        paged_book = paginator.get_page(page)
        book_count = books.count()

    context = {
        'books': paged_book,
        'cat': categories,
        'book_count': book_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            genre__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(
            cart__cart_id=_cart_id(request), product=single_product)
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            order_product = OrderProduct.objects.filter(
                user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            order_product = None
    else:
        order_product = None

    reviews = ReviewRating.objects.filter(
        product_id=single_product.id, status=True)

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'order_product': order_product,
        'reviews': reviews,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    context = {}
    books = []
    book_count = 0
    if 'keyword' in request.GET:
        key = request.GET['keyword']

        if key:
            books = Product.objects.order_by('-created_date').filter(Q(writer__icontains=key) | Q(
                slug__icontains=key) | Q(genre__category_name__icontains=key))
            book_count = books.count()

        context = {
            'books': books,
            'book_count': book_count
        }

    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(
                user__id=request.user.id, product__id=product_id)
            form = ReviewForms(request.POST, instance=reviews)

            form.save()
            messages.success(request, 'Your review has been updated')

        except ReviewRating.DoesNotExist:
            form = ReviewForms(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()

                messages.success(request, 'Your review has been posted')
                # return redirect(url)

    return redirect(url)
