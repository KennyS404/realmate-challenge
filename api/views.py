from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
import uuid

class WebhookView(APIView):

    def post(self, request, *args, **kwargs):
        event_type = request.data.get('type')
        data = request.data.get('data', {})

        if not event_type:
            return Response({"detail": "Campo 'type' não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        if event_type == "NEW_CONVERSATION":
            return self.handle_new_conversation(data)

        elif event_type == "NEW_MESSAGE":
            return self.handle_new_message(data)

        elif event_type == "CLOSE_CONVERSATION":
            return self.handle_close_conversation(data)

        else:
            return Response({"detail": "Tipo de evento inválido."}, status=status.HTTP_400_BAD_REQUEST)

    def handle_new_conversation(self, data):
        conversation_id = data.get('id')
        if not conversation_id:
            return Response({"detail": "ID da conversa não fornecido."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            conversation_uuid = uuid.UUID(conversation_id)
        except ValueError:
            return Response({"detail": "ID de conversa inválido (não é UUID)."}, status=status.HTTP_400_BAD_REQUEST)

        if Conversation.objects.filter(id=conversation_uuid).exists():
            return Response({"detail": "Conversa já existe."}, status=status.HTTP_400_BAD_REQUEST)

        Conversation.objects.create(id=conversation_uuid, state=Conversation.OPEN)
        return Response({"detail": f"Conversa {conversation_id} criada com sucesso."}, status=status.HTTP_201_CREATED)

    def handle_new_message(self, data):
        message_id = data.get('id')
        direction = data.get('direction')
        content = data.get('content')
        conversation_id = data.get('conversation_id')

        if not message_id or not direction or not content or not conversation_id:
            return Response({"detail": "Campos obrigatórios faltando em data."}, status=status.HTTP_400_BAD_REQUEST)


        if direction not in [Message.SENT, Message.RECEIVED]:
            return Response({"detail": "Direção da mensagem inválida."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            conversation_uuid = uuid.UUID(conversation_id)
        except ValueError:
            return Response({"detail": "ID de conversa inválido."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            conversation = Conversation.objects.get(id=conversation_uuid)
        except Conversation.DoesNotExist:
            return Response({"detail": "Conversa não encontrada."}, status=status.HTTP_400_BAD_REQUEST)

      
        if conversation.state == Conversation.CLOSED:
            return Response({"detail": "Conversa está fechada e não pode receber mensagens."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            message_uuid = uuid.UUID(message_id)
        except ValueError:
            return Response({"detail": "ID da mensagem inválido (não é UUID)."}, status=status.HTTP_400_BAD_REQUEST)

        if Message.objects.filter(id=message_uuid).exists():
            return Response({"detail": "Mensagem com esse ID já existe."}, status=status.HTTP_400_BAD_REQUEST)
        
        Message.objects.create(
            id=message_uuid,
            direction=direction,
            content=content,
            conversation=conversation
        )

        return Response({"detail": "Mensagem criada com sucesso."}, status=status.HTTP_201_CREATED)

    def handle_close_conversation(self, data):
        conversation_id = data.get('id')
        if not conversation_id:
            return Response({"detail": "ID da conversa não fornecido."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            conversation_uuid = uuid.UUID(conversation_id)
        except ValueError:
            return Response({"detail": "ID de conversa inválido (não é UUID)."}, status=status.HTTP_400_BAD_REQUEST)

     
        conversation = get_object_or_404(Conversation, id=conversation_uuid)

        if conversation.state == Conversation.CLOSED:
            return Response({"detail": "Conversa já estava fechada."}, status=status.HTTP_200_OK)


        conversation.state = Conversation.CLOSED
        conversation.save()
        return Response({"detail": f"Conversa {conversation_id} fechada com sucesso."}, status=status.HTTP_200_OK)


class ConversationDetailView(APIView):
    def get(self, request, conversation_id, *args, **kwargs):
        conversation = get_object_or_404(Conversation, id=conversation_id)
        
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
def front_view(request):
    return render(request, 'front.html')

class ConversationListView(APIView):
    def get(self, request, *args, **kwargs):
        conversations = Conversation.objects.all().order_by('-created_at')
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)