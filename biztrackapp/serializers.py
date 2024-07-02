from rest_framework import serializers
from .models import *
class ReportFilterSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)

class DailyCollectionReportFilterSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)
    # category = serializers.ChoiceField(choices=[('A', 'Category A'), ('B', 'Category B')], required=False)


class BankStatementReportFilterSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)
    bank = serializers.PrimaryKeyRelatedField(queryset=AllBank.objects.all())
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'country_code','phone_number','is_admin','is_employee']
   

class CustomTokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)