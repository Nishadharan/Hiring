from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework  import status
from .seriailzer import SkillsSerializer, TechnicalInterviewSerializer, getTechnicalInterviewSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import TechnicalInterviewTable, SkillsTable
from rest_framework.permissions import IsAuthenticated
from HiringBackend.util import constants
from HRLevel.models import candidate_info
from HRLevel.entryLevel.serializer import AllcandidateSerializer

class getCandidateForInterviewer(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user_id=request.user.empId
        candidates=candidate_info.objects.filter(currentStatus=constants.INTECH,interviewer=user_id, submissionStatus=constants.SUBMIT)
        serializer = AllcandidateSerializer(candidates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SaveInterviewerData(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        payload=request.data
        id=payload.get('id', None)
        
        if id:
            interview = TechnicalInterviewTable.objects.get(id=id)
            serializer = getTechnicalInterviewSerializer(interview, data=payload)
            if serializer.is_valid():
                serializer.save()
                changeStatus(payload, constants.INFINAL)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            tech_interview_serializer = TechnicalInterviewSerializer(data=payload)
            if tech_interview_serializer.is_valid():
                tech_interview_instance = tech_interview_serializer.save()
                
                skills_data = request.data.get('skills', [])
                skills_serializer = SkillsSerializer(data=skills_data, many=True)
                if skills_serializer.is_valid():
                    skills_serializer.save(techReview=tech_interview_instance)
                    changeStatus(payload, constants.INFINAL)
                    # need to change status for a candidate resume
                    return Response({"message": "Data saved successfully."}, status=201)
                else:
                    tech_interview_instance.delete()  # Rollback if skills data is invalid
                    return Response(skills_serializer.errors, status=400)
            else:
                return Response(tech_interview_serializer.errors, status=400)
        

def changeStatus(payload, statusMessage):
    permission_classes = [IsAuthenticated]
    if payload.get('submissionStatus',None)==constants.SUBMIT:
            try:
                candidate=candidate_info.objects.get(resumeId=payload.get('resumeId', None))
            except candidate_info.DoesNotExist:
                return Response({'Message':'no data with this resumeId'})
            candidate.currentStatus=statusMessage
            candidate.save()  
        
            
            
            
            
            
        
         
        
                
    def get(self, request):
        interviews = TechnicalInterviewTable.objects.all()  # Fetch all technical interviews
        # interviews = TechnicalInterviewTable.objects.prefetch_related('skills').all() 
        serializer = getTechnicalInterviewSerializer(interviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class getInterviewerDataById(APIView):
    
    def get(self, request, *args, **kwargs):
    # def get(self, request):
        techId=self.kwargs.get('pk')
        try:
            interview = TechnicalInterviewTable.objects.get(id=techId)
            serializer = getTechnicalInterviewSerializer(interview)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TechnicalInterviewTable.DoesNotExist:
            return Response({"message":"Interviewer data with this id does not exist!"})
        
    # def put(self, request, pk, format=None):
    #     interview = TechnicalInterviewTable.objects.get(id=pk)
    #     serializer = getTechnicalInterviewSerializer(interview, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)