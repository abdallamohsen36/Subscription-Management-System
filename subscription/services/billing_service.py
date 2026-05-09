from datetime import timedelta
from django.utils import timezone
from django.db import transaction

from subscription import serializers, models
from subscription.services.tenant_service import get_subscription_for_merchant
def create_plan(*, merchant, name, price=100, currency="EGP"):

    plan = models.Plan.objects.create(
        name=name,
        merchant=merchant
    )

    models.PlanCost.objects.create(
        plan=plan,
        price=price,
        currency=currency
    )

    return plan


def create_payment(*, subscription, merchant):

    subscription = get_subscription_for_merchant(
        subscription_id=subscription.id,
        merchant=merchant
    )

    plan_cost = models.PlanCost.objects.get(plan=subscription.plan)

    payment = models.Payment.objects.create(
        subscription=subscription,
        amount=plan_cost.price,
        status="success"
    )

    return payment


def process_recurring_billing():
    today = timezone.now().date()

    subscriptions = models.Subscription.objects.filter(
        next_billing_date__lte=today,
        status="active"
    )

    results = []

    for subscription in subscriptions:

        with transaction.atomic():

            already_billed = models.Payment.objects.filter(
                subscription=subscription,
                created_at__date=today,
                status="success"
            ).select_for_update().exists()

            if already_billed:
                continue

            payment = create_payment(
                subscription=subscription,
                merchant=subscription.user.merchant
            )

            if subscription.plan.billing_cycle == "monthly":
                subscription.next_billing_date = today + timedelta(days=30)
            else:
                subscription.next_billing_date = today + timedelta(days=365)

            subscription.save()

            results.append(payment)

    return results
