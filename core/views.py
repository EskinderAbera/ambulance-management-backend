from django.contrib.auth import login
from rest_framework import generics, mixins, status, permissions
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


class CreateDriver(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        res = self.create(request, *args, **kwargs)
        if res.status_code == 201:
            return Response({'msg': 'successfully created'}, status=status.HTTP_201_CREATED)


class ListDriver(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):

    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ActiveHospital(APIView):

    def get(self, request, format = None):
        drivers = Driver.objects.filter(isactive = True)
        Hospitales = []
        for driver in drivers:
            hospital = Hospital.objects.get(id = driver.hospital.id)
            serializer = HospitalSerializer(hospital)
            Hospitales.append(serializer.data)
        return Response(Hospitales, status=status.HTTP_200_OK)



class HospitalMessageView(APIView):
    def get(self, request, pk, format = None):
        try:
            message = SenderMessage.objects.filter(hospital = pk)
        except:
            return Response({"msg" : "No message is found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MessageSerializer(message, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format = None):
        serializer = LoginSerializer(data=request.data, context = {'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        profile = Profile.objects.get(user = user)
        if profile.role.rolename == 'hospitaluser':
            messages = SenderMessage.objects.filter(hospital = profile.hospital, isactive = True)
            activedrivers = Driver.objects.filter(hospital = profile.hospital, isactive = True)
            drivers = Driver.objects.filter(hospital = profile.hospital)
            messageserializer = MessageSerializer(messages, many = True)
            activedriverserialized = DriveSerializer(activedrivers, many=True)
            driverserialized = DriveSerializer(drivers, many = True)
            res = []
            res.append({"messages": messageserializer.data})
            res.append({"activedrivers": activedriverserialized.data})
            res.append({"drivers": driverserialized.data})
            return Response(res, status=status.HTTP_200_OK)


class LoginViewDriver(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format = None):
        serializer = LoginSerializer(data=request.data, context = {'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        driver = Driver.objects.get(user = user)
        message = SenderMessage.objects.filter(id = driver.sendermessage, isactive = True)
        serializer = MessageSerializer(message, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AssignMessage(APIView):

    def post(self, request, format = None):
        try: 
            driver = Driver.objects.get(id = request.data['id'])
        except Driver.DoesNotExist:
            return Response({"msg" : "driver does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        serializer = DriverSerializer(driver, data=request.data)
        if serializer.is_valid():
            serializer.validated_data['isactive'] = False
            serializer.save()
            # SenderMessage.objects.get(id = request.data['msg_id']).update(isactive = False)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # SenderMessage.objects.filter(id = driver.sendermessage).update(isactive = False)
        # return Response({"msg": "Successfully assign message to driver"}, status=status.HTTP_202_ACCEPTED)
        




