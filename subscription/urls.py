from django.urls import path

from . import views


urlpatterns = [
    path("user/",views.UserAPIView.as_view()),
    path("plan/",views.PlanAPIView .as_view()),
    path('subscribe/', views.SubscribeUserAPIView.as_view()),
    path('subscriptionslist/', views.SubscriptionListAPIView.as_view()),
    path('subscriptions/<int:pk>/', views.CancelSubscriptionAPIView.as_view(), name='cancel-subscription'),
    path('payments/', views.PaymentAPIView.as_view(), name='payments'),
]
