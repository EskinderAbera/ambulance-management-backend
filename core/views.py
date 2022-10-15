from rest_framework import generics, mixins, status
from rest_framework.response import Response
from core.models import *
from .serializers import *
from rest_framework.views import APIView

# Create your views here.

class CreateMessage(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    queryset = SenderMessage.objects.all()
    serializer_class = MessageSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        res = self.create(request, *args, **kwargs)
        if res.status_code == 201:
            return Response({'msg': 'successfully created'}, status=status.HTTP_201_CREATED)


class ActiveHospital( mixins.ListModelMixin, generics.GenericAPIView):

    queryset = Driver.objects.filter(isactive = True)
    serializer_class = DriverSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)

    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)

class HospitalMessageView(APIView):
    def get(self, request, pk, format = None):
        try:
            message = SenderMessage.objects.filter(hospital = pk)
        except:
            return Response({"msg" : "No message is found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MessageSerializer(message, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

