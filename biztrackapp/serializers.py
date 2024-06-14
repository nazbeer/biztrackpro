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
    
