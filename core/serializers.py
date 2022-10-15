from rest_framework import serializers
from .models import *

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


