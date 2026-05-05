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
        merchant = models.Merchant.objects.get(user=request.user)
        plans = models.Plan.objects.filter(merchant=merchant)
        serializer = self.serializer_class(plans, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            merchant = models.Merchant.objects.get(user=request.user)
            serializer.save(merchant=merchant)
            return Response({"message": "Plan created successfully"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CreateUserAPIView(APIView):
    serializer_class = serializers.UserProfilesSerializer

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

            if plan.merchant != request.user.merchant:
                return Response({"error": "Invalid plan"}, status=400)
            
            with transaction.atomic():

                subscription = serializer.save(
                    status="active",
                    next_billing_date=date.today() + timedelta(days=30)
                )

                models.Payment.objects.create(
                    subscription=subscription,
                    amount=subscription.plan.price,
                    status="success"
                )
            return Response({"message": "Subscribe User created successfully"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionListAPIView(APIView):
    serializer_class = serializers.SubscriptionListSerializer

    def get(self, request):
        merchant = request.user.merchant
        subscriptions = models.Subscription.objects.filter(user__merchant=merchant)
        serializer = self.serializer_class(subscriptions, many=True)
        return Response(serializer.data)