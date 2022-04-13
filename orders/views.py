from email.message import EmailMessage
import json
from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse

from carts.models import CartItem
from .forms import OrderForm
from .models import Order, OrderProduct, Payment
from store.models import Product

import datetime
from django.template.loader import render_to_string
import stripe
stripe.api_key = 'sk_test_51Kn6TZGOatzjLsRhCf25WzWF5SYojVTCL2AoeYr3do3UxqZdfwW3SrlcmvnwyKPo33uHrrh7H38aqLcjQDFXWgsU00F29Ggwj7'


def payments(request):

    if request.method == 'POST':
        print('Data:', request.POST)
        amount = int(request.POST.get('amount'))

        customer = stripe.Customer.create(
            email=request.user.email,
            name=request.user.username,
            source=request.POST['stripeToken'],
        )

        charge = stripe.Charge.create(
            customer=customer,
            amount=amount*100,
            currency='BDT',
            description='Bookhaul Payment',
        )

        order = Order.objects.get(
            user=request.user, is_ordered=False, order_number=request.POST['orderID'])

        payment = Payment(
            user=request.user,
            payment_id=request.POST['stripeToken'],
            amount_paid=amount,
            status='COMPLETED',
        )

        payment.save()
        order.payment = payment
        order.is_ordered = True
        order.save()

        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:
            order_product = OrderProduct()
            order_product.order_id = order.id
            order_product.payment = payment
            order_product.user_id = request.user.id
            order_product.product_id = item.product_id
            order_product.quantity = item.quantity
            order_product.product_price = item.product.price
            order_product.ordered = True

            order_product.save()

            # move the cart items to order products and reduce sold product quantity

            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

        # clearing cart
        CartItem.objects.filter(user=request.user).delete()

        return render(request, 'orders/order_success.html')
    else:
        return render(request, 'orders/failure.html')


def place_order(request, total=0, quantity=0,):
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = int((2 * total)/100)
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)

        # print(form)

        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.city = form.cleaned_data['city']
            data.postcode = form.cleaned_data['postcode']
            data.zilla = form.cleaned_data['zilla']
            data.division = form.cleaned_data['division']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # generating order number
            year = int(datetime.date.today().strftime('%Y'))
            date = int(datetime.date.today().strftime('%d'))
            month = int(datetime.date.today().strftime('%m'))
            d = datetime.date(year, month, date)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number

            # id = str(data.phone) + current_date
            # data.payment = id
            data.save()

            order = Order.objects.get(
                user=current_user, is_ordered=False, order_number=order_number)

            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
                'date': d,
            }
            return render(request, 'orders/payments.html', context)
        # else:
        #     return HttpResponse('oh no')

    return redirect('checkout')


def order_success(request):
    return render(request, 'orders/order_success.html')


def failure(request):
    return render(request, 'orders/failure.html')
