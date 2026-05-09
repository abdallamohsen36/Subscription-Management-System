from celery import shared_task
from subscription.services.billing_service import process_recurring_billing


@shared_task
def renew_billing_task():
    process_recurring_billing()
    return "Billing completed"