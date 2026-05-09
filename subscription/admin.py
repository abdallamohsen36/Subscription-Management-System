from django.contrib import admin
from .models import Merchant, User, Plan, Subscription, Payment

# Register your models here.

admin.site.register(Merchant)
admin.site.register(User)
admin.site.register(Plan)
admin.site.register(Subscription)
admin.site.register(Payment)