from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from subscription import models
from django.db import transaction


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        today = timezone.now().date()

        subscriptions = models.Subscription.objects.filter(
            next_billing_date__lte=today,
            status="active"
        )

        for sub in subscriptions:

            with transaction.atomic():

                already_billed = models.Payment.objects.filter(
                    subscription=sub,
                    status="success",
                    created_at__date=today
                ).exists()

                if already_billed:
                    continue

                plan_cost = models.PlanCost.objects.filter(plan=sub.plan).first()

                try:
                    payment_status = "success"
                except:
                    payment_status = "failed"

                models.Payment.objects.create(
                    subscription=sub,
                    amount=plan_cost.price,
                    status=payment_status
                )

                if sub.plan.billing_cycle == "monthly":
                    sub.next_billing_date = today + timedelta(days=30)
                else:
                    sub.next_billing_date = today + timedelta(days=365)                
                sub.save()

        print("Update Billing Date Success")