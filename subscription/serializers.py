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

    def create(self, validated_data):
        merchant = self.context.get('merchant')

        user = models.Customer.objects.create(
            email=validated_data['email'],
            merchant=merchant
        )
        return user
    

class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Subscription
        fields = ('id', 'user', 'plan', 'status', 'next_billing_date')



class SubscriptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subscription
        fields = '__all__'