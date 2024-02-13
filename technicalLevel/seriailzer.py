from rest_framework import serializers
from .models import TechnicalInterviewTable, SkillsTable

class TechnicalInterviewSerializer(serializers.ModelSerializer):
    id =serializers.IntegerField(required=False)
    class Meta:
        model = TechnicalInterviewTable
        fields = '__all__'
        
class SkillsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SkillsTable
        fields = '__all__'
        # fields = ['id','skills', 'proficiency', 'ratingoutof10', 'comments']

class updateSkillsSerializer(serializers.ModelSerializer):
    id =serializers.IntegerField(required=False)
    class Meta:
        model = SkillsTable
        # fields = '__all__'
        fields = ['id','skills', 'proficiency', 'ratingoutof10', 'comments']
        
class getTechnicalInterviewSerializer(serializers.ModelSerializer):
    skills = updateSkillsSerializer(many=True)  # Nested serializer for SkillsTable
    id=serializers.IntegerField(required=False)
    class Meta:
        model = TechnicalInterviewTable
        fields = ['id','candidateName', 'resumeId', 'strength', 'weakness', 'shortlistStatus', 'submissionStatus', 'overall_comments', 'overall_rating', 'remarks', 'skills']
        
    def update(self, instance, validated_data):
        techId=validated_data.pop('id', None)
        skills_data = validated_data.pop('skills', [])
        if techId:
            instance = super().update(instance, validated_data)
        for skill_data in skills_data:
            child_id = skill_data.pop('id', None)
            print(child_id)
            if child_id:
                child = instance.skills.get(id=child_id)
                updateSkillsSerializer().update(child, skill_data)
            else:
                instance.skills.create(**skill_data)
        return instance
