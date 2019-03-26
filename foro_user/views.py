#from rest_framework import status
from django.http import Http404
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import generics, viewsets
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

class UserDetail(APIView):
    """
    General operations for User model
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)        
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAuthViewSet(viewsets.ModelViewSet):
    """
    ViewSet for additional user requests
    """    

    @action(detail=False)
    def get_from_auth(self, request, authId):
        try:
            user = User.objects.get(auth0Id=authId)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            raise Http404

class ThreadList(generics.ListCreateAPIView):
    """
    List and Create operations for Thread model
    """
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer


class ThreadDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    General operations for Thread model
    """
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer