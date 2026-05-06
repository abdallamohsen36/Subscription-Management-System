from rest_framework import serializers
from subscription import models

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Plan
        fields = '__all__'


class UserProfilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Customer
        fields = ('id', 'email')
    

class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Subscription
        fields = ('id', 'user', 'plan')



class SubscriptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subscription
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Payment
        fields = ('id', 'subscription', 'amount')
        read_only_fields = ('status', 'created_at')