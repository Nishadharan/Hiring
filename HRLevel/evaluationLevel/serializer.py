from rest_framework import serializers
from HRLevel.models import evaluationdata

class evaluationserializer(serializers.ModelSerializer):
    class Meta:
        model = evaluationdata
        fields = '__all__'