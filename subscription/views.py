from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from subscription import models, serializers
from subscription.utils import for_merchant
from subscription.services.billing_service import create_payment, create_plan
from subscription.services.subscription_service import create_subscription, cancel_subscription
from subscription.services.tenant_service import create_user, get_plan_for_merchant, get_subscription_for_merchant
from subscription.api_response import success_response, error_response

# Create your views here.
class PlanAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PlanSerializer

    def get(self, request):
        plans = for_merchant(models.Plan.objects.all(), request.user)
        serializer = self.serializer_class(plans, many=True)
        return success_response(
            data=serializer.data
        )
    
    def post(self, request):
        merchant = request.user.merchant

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            plan = create_plan(
                merchant=request.user.merchant,
                name=serializer.validated_data["name"],
                price=serializer.validated_data.get("price"),
                currency=serializer.validated_data.get("currency"),
            )
            
            return success_response(
                message="Plan created successfully"
            )

        return error_response(
            message="Failed to create plan",
            errors=serializer.errors
        )



class UserAPIView(APIView):
    serializer_class = serializers.UserProfilesSerializer

    def get(self, request):
        users = for_merchant(models.User.objects.all(), request.user)
        serializer = self.serializer_class(users, many=True)
        return success_response(
            data=serializer.data
        )


    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            create_user(
                merchant=request.user.merchant,
                email=serializer.validated_data["email"]
            )
            return success_response(
                message="User created successfully"
            )
        else:
            return error_response(
                message="Failed to create plan",
                errors=serializer.errors
            )


class SubscribeUserAPIView(APIView):
    serializer_class = serializers.SubscriptionSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)        

        if serializer.is_valid():
            plan = get_plan_for_merchant(
                plan_id=serializer.validated_data["plan"],
                merchant=request.user.merchant
            )

            subscription = create_subscription(
                user=request.user,
                plan=plan
            )          
            return success_response(
                message="Subscription created successfully"
            )
        else :
            return error_response(
                message="Failed to create subscription",
                errors=serializer.errors
            )



class CancelSubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        subscription = get_subscription_for_merchant(
            subscription_id=pk,
            merchant=request.user.merchant
        )

        cancel_subscription(
            subscription=subscription,
            merchant=request.user.merchant
        )

        return success_response(
            message="Subscription canceled successfully"
        )



class SubscriptionListAPIView(APIView):
    serializer_class = serializers.SubscriptionListSerializer

    def get(self, request):
        subscriptions = models.Subscription.objects.filter(
            user__merchant=request.user.merchant
        )
        serializer = self.serializer_class(subscriptions, many=True)
        return success_response(
            data=serializer.data
        )


class PaymentAPIView(APIView):
    serializer_class = serializers.PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payments = models.Payment.objects.filter(
            subscription__user__merchant=request.user.merchant
        )

        serializer = self.serializer_class(payments, many=True)
        return success_response(
            data=serializer.data
        )

    def post(self, request):
        subscription = get_subscription_for_merchant(
            subscription_id=request.data.get("subscription"),
            merchant=request.user.merchant
        )

        create_payment(
            subscription=subscription,
            merchant=request.user.merchant
        )

        return success_response(
            message="Payment recorded successfully"
        )