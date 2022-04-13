from math import prod
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    quantity = product.stock

    if current_user.is_authenticated:
        is_cart_item_exists = CartItem.objects.filter(
            product=product, user=current_user).exists()

        if is_cart_item_exists:
            # filter diye hocchena, get ii use kora lagbe
            cart_item = CartItem.objects.get(
                product=product, user=current_user)
            # cart_item.quantity += 1
            if cart_item.quantity < quantity:
                cart_item.quantity += 1

            cart_item.save()

        elif CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                user=current_user,
                product=product,
                quantity=1
            )
            cart_item.save()
        return redirect('cart')

    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request),
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(
            product=product, cart=cart).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(
                product=product, cart=cart)  # get chilo, filter use korsi
            cart_item.quantity += 1
            cart_item.save()

        elif CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                cart=cart,
                quantity=1
            )
            cart_item.save()

        return redirect('cart')


def remove_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                product=product, user=request.user)

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass

    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total = total + cart_item.product.price * cart_item.quantity
            quantity = quantity + cart_item.quantity
        tax = int((2 * total)/100)
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, "store/cart.html", context)


def remove_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user)

    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)

    cart_item.delete()
    return redirect('cart')


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total = total + cart_item.product.price * cart_item.quantity
            quantity = quantity + cart_item.quantity
        tax = int((2 * total)/100)
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'store/checkout.html', context)
