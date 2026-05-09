from datetime import date, timedelta
from django.db import transaction

from subscription import models
from subscription.services.billing_service import create_payment
from subscription.services.tenant_service import get_plan_for_merchant, get_plan_for_merchant, get_subscription_for_merchant


def create_subscription(*, user, plan):
    user = models.User.objects.get(id=user.id)
    merchant = user.merchant

    plan = get_plan_for_merchant(
        plan_id=plan.id,
        merchant=merchant
    )


    if plan.billing_cycle == "monthly":
        next_date = date.today() + timedelta(days=30)
    else:
        next_date = date.today() + timedelta(days=365)

    with transaction.atomic():

        subscription = models.Subscription.objects.create(
            user=user,
            plan=plan,
            status="pending",
            next_billing_date=next_date
        )

        create_payment(
            subscription=subscription,
            merchant=merchant
        )

        subscription.status = "active"
        subscription.save()

    return subscription



def cancel_subscription(*, subscription, merchant):

    subscription = get_subscription_for_merchant(
        subscription_id=subscription.id,
        merchant=merchant
    )

    subscription.status = "canceled"
    subscription.end_date = date.today()
    subscription.save()

    return subscription