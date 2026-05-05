from django.contrib import admin
from .models import Merchant, Customer, Plan, Subscription, Payment

# Register your models here.

admin.site.register(Merchant)
admin.site.register(Customer)
admin.site.register(Plan)
admin.site.register(Subscription)
admin.site.register(Payment)