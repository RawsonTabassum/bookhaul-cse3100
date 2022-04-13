from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from accounts.models import Account
from store.models import Product


class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    # user er phone number, er sathe date concatenate kore diboni :3
    payment_id = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    # this is extra i tried to add.
    # phone_number = models.CharField(max_length=11, null=True)

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    SHIPPING = (
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    email = models.EmailField(max_length=50)
    city = models.CharField(max_length=20)
    postcode = models.CharField(max_length=20)
    zilla = models.CharField(max_length=20)
    division = models.CharField(max_length=20)
    order_note = models.CharField(max_length=100)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=100, choices=STATUS, default='New')
    shipping = models.CharField(
        max_length=100, choices=SHIPPING, default='Shipped')
    ip = models.CharField(max_length=20, blank=True)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # zilla mane upazilla :3
    # division mane zilla :3 hehe sorry

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        return f'{self.city}, {self.zilla}-{self.postcode}, {self.division}'

    def __str__(self):
        return self.first_name


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(
        Payment, on_delete=SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.book_name
