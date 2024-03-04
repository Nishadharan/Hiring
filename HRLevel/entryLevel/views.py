from rest_framework import views, status
from userManagement.models import user
from HRLevel.models import candidate_info
from rest_framework.views import APIView
from .serializer import (candidateInfoSerializer, AllcandidateSerializer, llmcandidateInfoserializer)
from rest_framework.response import Response
from HiringBackend.util import constants
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
# mail
from django.core.mail import EmailMessage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from HiringBackend.util.email import sendMail
from HiringBackend.util.emailHtmlLoader import emailHtmlLoader
from django.shortcuts import get_object_or_404
from HiringBackend.util.apiResponse import APIResponse
from django.shortcuts import render

def index(request):
    return render(request, 'resource/frontend.html')


def applicants_without_any_constraints():
    objects = candidate_info.objects.filter(assigned=None)
    serializer = candidateInfoSerializer(objects ,many=True)
    return serializer.data

class assign_resume_with_out_constraints(APIView):
    def post(self, request):
        users = user.objects.filter(roles=2, pause=False)
        users_id = [user.empId for user in users]
        count = 0
        sorted_resumes = applicants_without_any_constraints()
        for resume_data in sorted_resumes:
            if count < len(users_id):
                existing_resume = candidate_info.objects.get(resumeId=resume_data['resumeId'])
                existing_resume.assigned = users_id[count]
                # for mainting status like not assigned assigned verified   
                existing_resume.currentStatus=constants.ASSIGNED
                
                existing_resume.save()
                count += 1
            else:
                count = 0
        return Response({'message':'successfully created!'})
                    
class GetUnAssignedCandidates(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        candidates=candidate_info.objects.filter(currentStatus=constants.NOTASSIGNED)
        serializer = AllcandidateSerializer(candidates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetAUnassignedCandidate(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, *args, **kwargs):
        candidate_id = self.kwargs.get('id')
        try:
            candidate=candidate_info.objects.get(id=candidate_id)
        except candidate_info.DoesNotExist:
            return Response({'message':f'no data found with this id {candidate_id}'})
            # return Response(APIResponse("uanble to get data"))
        
        serializer=candidateInfoSerializer(candidate)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# class updatedata(generics.UpdateAPIView):
#     queryset = candidate_info.objects.all()
#     serializer_class = llmcandidateInfoserializer
#     permission_classes = [IsAuthenticated]
    
class updatedata(generics.UpdateAPIView):
    serializer_class = llmcandidateInfoserializer
    permission_classes = [IsAuthenticated]
 
    def get_object(self):
        resume_id = self.kwargs.get('resumeId')
        candidate = get_object_or_404(candidate_info, resumeId=resume_id)
        return candidate
    
    def perform_update(self, serializer):
        instance=self.get_object()
        userPayload = serializer.validated_data
        # unless submit, it need not move to technical interviewer
        if userPayload.get('recruiterSubmissionStatus', None)=="SUBMITTED":
            # instance.currentStatus="IN_TECH"
            serializer.validated_data['currentStatus']='IN_TECH'
        else:
            # instance.currentStatus="IN_ENTRY"
            serializer.validated_data['currentStatus']='ASSIGNED'
        
        # print(submissionStatus)
        # instance.save()
        serializer.save()
        # print(type(userPayload))
        
        subject=f' Application Status - {userPayload.get("jobRole", None)}'
        receipient=[]
        receipient.append(userPayload.get('email', None))
        content=None
        if userPayload.get('shortlistStatus')==constants.NOTSHORTLISTED:
            subject=f' Application Status - {userPayload.get("jobRole", None)}'
            content=emailHtmlLoader.HrNotShortistedMail(userPayload)
            
        elif userPayload.get('shortlistStatus')==constants.SHORTLISTED:
            subject=f'Congratulations! You have Been Shortlisted - {userPayload.get("jobRole", None)}'
            content=emailHtmlLoader.HrShortistedMail(userPayload)
        mail=sendMail()
        mail.sendMailtoReceipients(content, subject, receipient) 
         
    # mail.send(content, subject, receipient)

class getCandidateForRecruiter(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        empId=request.user.empId
        print(empId)
        candidates=candidate_info.objects.filter(assigned=empId, shortlistStatus=(constants.SHORTLISTED))
        serializer = candidateInfoSerializer(candidates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

        