from rest_framework import serializers
from .models import CSVFile

class CSVUploadSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    content = serializers.CharField()
        
        
class CSVFileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=CSVFile
        fields='__all__'