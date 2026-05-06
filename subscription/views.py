from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import transaction

from datetime import date, timedelta

from subscription import serializers, models

# Create your views here.

class PlanAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PlanSerializer
    def get(self, request):
        print("USER:", request.user.username)
        print("MERCHANT:", request.user.merchant.id)

        plans = models.Plan.objects.filter(merchant=request.user.merchant)
        serializer = self.serializer_class(plans, many=True)
        return Response(serializer.data)
    def post(self, request):
        merchant = request.user.merchant

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            plan = serializer.save(merchant=merchant)
            models.PlanCost.objects.create(
                plan=plan,
                price=request.data.get("price", 100),  # default لو مش مبعوت
                currency=request.data.get("currency", "EGP")
            )
            return Response({"message": "Plan created successfully"})

        return Response(serializer.errors, status=400)

class UserAPIView(APIView):
    serializer_class = serializers.UserProfilesSerializer

    def get(self, request):
        merchant = models.Merchant.objects.get(user=request.user)
        customers = models.Customer.objects.filter(merchant=merchant)
        serializer = self.serializer_class(customers, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            merchant = models.Merchant.objects.get(user=request.user)
            serializer.save(merchant=merchant)
            return Response({"message": "User created successfully"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscribeUserAPIView(APIView):
    serializer_class = serializers.SubscriptionSerializer

    def post(self, request):
        data = request.data.copy()
        
        merchant = models.Merchant.objects.get(user=request.user)
        
        serializer = self.serializer_class(data = data)

        if serializer.is_valid():
            plan = serializer.validated_data['plan']

            if plan.merchant != merchant:
                return Response({"error": "Invalid plan"}, status=400)
            
            if plan.billing_cycle == "monthly":
                next_date = date.today() + timedelta(days=30)
            else:
                next_date = date.today() + timedelta(days=365)
            
            with transaction.atomic():

                subscription = serializer.save(
                    status="pending",
                    next_billing_date=next_date
                )

                plan_cost = models.PlanCost.objects.get(plan=subscription.plan)
                payment = models.Payment.objects.create(
                    subscription=subscription,
                    amount=plan_cost.price,
                    status="success"
                )
                subscription.status = "active"
                subscription.save()

            return Response({"message": "Subscribe User created successfully"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CancelSubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        merchant = models.Merchant.objects.get(user=request.user)
        subscription = models.Subscription.objects.get(id=pk, user__merchant=merchant)

        if subscription.user.merchant != merchant:
            return Response({"error": "Not allowed"}, status=403)

        subscription.status = "canceled"
        subscription.end_date = date.today()
        subscription.save()

        return Response({"message": "Subscription canceled successfully"})
    

class SubscriptionListAPIView(APIView):
    serializer_class = serializers.SubscriptionListSerializer

    def get(self, request):
        merchant = models.Merchant.objects.get(user=request.user)
        subscriptions = models.Subscription.objects.filter(user__merchant=merchant)
        serializer = self.serializer_class(subscriptions, many=True)
        return Response(serializer.data)
    

class PaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PaymentSerializer

    def get(self, request):
        merchant = models.Merchant.objects.get(user=request.user)
        payments = models.Payment.objects.filter(subscription__user__merchant=merchant)
        serializer = self.serializer_class(payments, many=True)
        return Response(serializer.data)

    def post(self, request):
        merchant = models.Merchant.objects.get(user=request.user)
        subscription_id = request.data.get("subscription")
        subscription = models.Subscription.objects.get(id=subscription_id)

        if subscription.user.merchant != merchant:
            return Response({"error": "Not allowed"}, status=403)
            
        plan_cost = models.PlanCost.objects.get(plan=subscription.plan)

        payment = models.Payment.objects.create(
            subscription=subscription,
            amount=plan_cost.price,
            status="success"
        )

        return Response({"message": "Payment recorded successfully"})