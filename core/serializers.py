from pyexpat import model
from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    # Hospital = serializers.SerializerMethodField()

    class Meta:
        model = SenderMessage
        fields = '__all__'

    # def get_accounts_items(self, obj):
    #     hospital_query = models.Hospital.objects.get(
    #         id = obj.id)
    #     serializer = AccountSerializer(customer_account_query, many=True)


class DriverSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer()

    class Meta:
        model = Driver
        fields = ['hospital']

class DriveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Driver
        fields = '__all__'
        

class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs


