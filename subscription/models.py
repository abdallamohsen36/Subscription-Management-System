from django.db import models
from django.contrib.auth.models import User as DjangoUser

# Create your models here.

class Merchant(models.Model):
    name = models.CharField(max_length=150)
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, null=True, blank=True)

class Customer(models.Model):
    email = models.EmailField()
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='users', null=True, blank=True)


class Plan(models.Model):
    name = models.CharField(max_length=150)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = models.CharField(max_length=20, default="monthly")


class Subscription(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, default="active")
    next_billing_date = models.DateTimeField()


class Payment(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="success")
    created_at = models.DateTimeField(auto_now_add=True)