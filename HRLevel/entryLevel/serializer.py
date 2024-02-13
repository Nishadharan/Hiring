from rest_framework import serializers
from HRLevel.models import candidate_info

class candidateInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=candidate_info
        fields='__all__'
    
class AllcandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model=candidate_info
        fields=('id','name', 'jobRole', 'resumeScore', 'resumeId', 'currentStatus')
        
class llmcandidateInfoserializer(serializers.ModelSerializer):
    class Meta:
        model = candidate_info
        fields = '__all__'
    