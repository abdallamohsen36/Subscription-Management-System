from django.urls import path

from . import views


urlpatterns = [
    path("user/",views.CreateUserAPIView.as_view()),
    path("plan/",views.PlanAPIView .as_view()),
    path('subscribe/', views.SubscribeUserAPIView.as_view()),
    path('subscriptionslist/', views.SubscriptionListAPIView.as_view()),
]
