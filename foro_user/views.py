#from rest_framework import status
from django.http import Http404
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework import status
from foro_user.models import Thread, Board, User, Post
from foro_user.serializers import ThreadSerializer, ThreadListSerializer, ThreadPostSerializer, BoardSerializer, UserSerializer, PostSerializer
from pprint import pprint


class BoardList(generics.ListCreateAPIView):
    """
    List and create operations for boards
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class BoardDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Get Board details and list its threads
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class UserList(generics.ListCreateAPIView):
    """
    List and create operations for users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    General operations for User model
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def put(self, request, pk, format=None):
        user = User.objects.get(pk=pk)
        print(request.data)
        serializer = UserSerializer(
            user, data=request.data, partial=True, context={'request': request})
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
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except User.DoesNotExist:
            raise Http404


class ThreadListCreate(APIView):
    """
    List and Create operations for Thread model
    """

    def get(self, request, format=None):
        threads = Thread.objects.all()
        board = self.request.query_params.get('board')
        if board:
            threads.filter(board_id=board)
        serializer = ThreadListSerializer(threads, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ThreadPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ThreadDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    General operations for Thread model
    """
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer


class PostList(generics.ListCreateAPIView):
    """
    List and Create operations for Post model
    """
    model = Post
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.all()
        thread = self.request.query_params.get('thread')
        if thread:
            queryset = queryset.filter(thread_id=thread)
        return queryset
