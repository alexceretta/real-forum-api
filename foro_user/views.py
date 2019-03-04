#from rest_framework import status
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from foro_user.models import Thread, Board
from foro_user.serializers import ThreadSerializer, BoardSerializer

@api_view(['GET'])
def thread_list(request):
    """
    List all the threads on the forum
    """
    if request.method == 'GET':
        threads = Thread.objects.all()
        serializer = ThreadSerializer(threads, many=True)        

        return Response(serializer.data)

class BoardDetail(APIView):
    """
    Get Board details and list its threads
    """
    def get_object(self, pk):
        try:
            return Board.objects.prefetch_related('threads').get(pk=pk)
        except Board.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        board = self.get_object(pk)
        serializer = BoardSerializer(board)
        return Response(serializer.data)
