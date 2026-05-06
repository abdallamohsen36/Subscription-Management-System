from django.db import models
from django.contrib.auth.models import User as DjangoUser

# Create your models here.
class Merchant(models.Model):
    name = models.CharField(max_length=150)
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Customer(models.Model):
    email = models.EmailField(unique=True)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)


class Plan(models.Model):
    name = models.CharField(max_length=150)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    billing_cycle = models.CharField(max_length=20, choices=[
        ("monthly", "Monthly"),
        ("yearly", "Yearly")
    ])


class PlanCost(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)


class Subscription(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("active", "Active"),
        ("canceled", "Canceled")
    ], default="Pending")
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    next_billing_date = models.DateTimeField()


class Payment(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ("success", "Success"),
        ("failed", "Failed")
    ], default="success")
    created_at = models.DateTimeField(auto_now_add=True)