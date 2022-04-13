from django.db.models.query import RawQuerySet
from .models import Cart, CartItem
from .views import _cart_id


def counter(request):
    count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id = _cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user =  request.user)
            
            else:
                cart_items = CartItem.objects.all().filter(cart = cart[:1],)

            for cartitem in cart_items:
                count += cartitem.quantity

        except Cart.DoesNotExist:
            count = 0
    return dict(cart_count = count)