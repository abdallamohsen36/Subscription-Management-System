from subscription import models


def create_user(*, merchant, email):

    user = models.User.objects.create(
        merchant=merchant,
        email=email
    )

    return user


def get_plan_for_merchant(*, plan_id, merchant):

    return models.Plan.objects.get(
        id=plan_id,
        merchant=merchant
    )


def get_subscription_for_merchant(*, subscription_id, merchant):

    return models.Subscription.objects.get(
        id=subscription_id,
        user__merchant=merchant
    )