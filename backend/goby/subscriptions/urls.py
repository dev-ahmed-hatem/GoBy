from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, include

router = DefaultRouter()
router.register("subscription-plan", SubscriptionPlanViewSet, basename="subscription-plan")
router.register("subscription", SubscriptionViewSet, basename="subscription")
router.register("invitation", InvitationViewSet, basename="invitation")

urlpatterns = [
    path("", include(router.urls)),
    path("subscription-invitations/", subscription_invitations, name="subscription-invitations"),
    path("send-invitation-mail/", send_invitation_mail, name="send-invitation-mail"),
    path("invitation-data/", invitation_data, name="invitation-data"),
    path("create-invitation/", create_invitation, name="create-invitation"),
]
