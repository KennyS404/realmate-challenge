from django.urls import path
from .views import (
    WebhookView,
    ConversationDetailView,
    ConversationListView, 
    front_view,         
)

urlpatterns = [
    path('webhook/', WebhookView.as_view(), name='webhook'),
    
    path('conversations/<uuid:conversation_id>/', ConversationDetailView.as_view(), name='conversation-detail'),
    path('conversations/', ConversationListView.as_view(), name='conversation-list'),
    
    path('front/', front_view, name='front'),
]
