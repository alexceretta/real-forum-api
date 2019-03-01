#from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from foro_user.models import Thread
from foro_user.serializers import ThreadSerializer

@api_view(['GET'])
def thread_list(request):
    """
    List all the threads on the forum
    """
    if request.method == 'GET':
        threads = Thread.objects.all()
        serializer = ThreadSerializer(threads, many=True)
        return Response(serializer.data)
