from django.urls import path
from . import views
from .views import invite_user, accept_invitation

urlpatterns = [
    path('invite/', invite_user, name='invite_user'),
    path('accept-invitation/<uuid:token>/', accept_invitation, name='accept_invitation'),
]
