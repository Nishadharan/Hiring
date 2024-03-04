from rest_framework import serializers
from HRLevel.models import evaluationdata

class evaluationserializer(serializers.ModelSerializer):
    class Meta:
        model = evaluationdata
        fields = '__all__'
        
    def update(self, instance, validated_data):
        instance=super().update(instance, validated_data)
        return instance
        
        