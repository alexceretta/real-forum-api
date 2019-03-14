#from rest_framework import status
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from foro_user.models import Thread, Board, User
from foro_user.serializers import ThreadSerializer, BoardSerializer, UserSerializer

class BoardDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Get Board details and list its threads
    """
    queryset = Board.objects.prefetch_related('threads').all()
    serializer_class = BoardSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    General operations for User model
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer