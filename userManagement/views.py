from django.shortcuts import render
from userManagement.serializer import (RegisterSerializer, loginSerializer, userRolesSerializer, 
                                       allUserSerializer,UpdateallUserSerializer, getUserSerializer,
                                       ListOfInterviewerSerializer)
from rest_framework import generics, status, views, permissions, parsers
from .models import user, UserRoles
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from HRLevel.models import candidate_info
from HiringBackend.util import constants
from django.core.mail import EmailMessage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from HiringBackend.util.email import sendMail
from HiringBackend.util.emailHtmlLoader import emailHtmlLoader
# Create your views here.
class RegistrationView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    # renderer_classes = (UserRenderer,)

    def post(self, request):
        userpayload = request.data
        serializer = self.serializer_class(data=userpayload)
        serializer.is_valid(raise_exception=True)  # this is going to run a method called
        serializer.save()
        user_data = serializer.data
        user_obj = user.objects.get(email=user_data.get('email'))
        token = RefreshToken.for_user(user_obj).access_token
        mail=sendMail()
        content=emailHtmlLoader.userCreatedMail(userpayload)
        subject='User created'
        receipient=[]
        receipient.append(userpayload.get('email', None))
        mail.sendMailtoReceipients(content, subject, receipient)
    
        return Response(user_data, status=status.HTTP_201_CREATED)
    
class updateUser(generics.UpdateAPIView):
    queryset = user.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateallUserSerializer
    
    
class activeInactiveUser(APIView):
    def put(self, request, pk):
        try:
            existUser=user.objects.get(pk=pk)
        except user.DoesNotExist:
            return Response({'message':'Object no found'}, status=status.HTTP_404_NOT_FOUND) 
        existUser.is_active=request.data.get('is_active', None)
        # existUser.pause=request.data.get('pause', None)
        existUser.save()
        return Response({'message':'updated successfully'}, status = status.HTTP_200_OK)
    
class pauseResumeUser(APIView):
    def put(self, request, pk):
        try:
            existUser=user.objects.get(pk=pk)
        except user.DoesNotExist:
            return Response({'message':'Object no found'}, status=status.HTTP_404_NOT_FOUND) 
        existUser.pause=request.data.get('pause', None)
        # existUser.pause=request.data.get('pause', None)
        existUser.save()
        return Response({'message':'updated successfully'}, status = status.HTTP_200_OK)

class LoginView(generics.GenericAPIView):
    serializer_class=loginSerializer
    def post(self, request):
         user = request.data
         serializer = self.serializer_class(data=user)
         serializer.is_valid(raise_exception=True)
         return Response(serializer.data, status=status.HTTP_200_OK)
     
class GetAllUsersView(generics.ListAPIView):
    serializer_class=allUserSerializer
    queryset=user.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]
    
class GetUser(APIView):
    def get(self, request, *args, **kwargs):
        userId=request.query_params.get('userId', None)
        try:
            users=user.objects.get(pk=userId)
        except user.DoesNotExist:
            return Response({'message':f'user does not exist with this {userId}'})
        serializer=getUserSerializer(users)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetAllRolesView(generics.ListAPIView):
    serializer_class=userRolesSerializer
    queryset=UserRoles.objects.all()
    permission_classes = [IsAuthenticated]
    
    # status like NOT_ASSIGNED,ASSIGNED, IN_ENTRY, IN_TECH, IN_FINAL, COMPLETED/
class statusOfCandidate(views.APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user=request.query_params.get('user', None)
        if user is None:
            return Response({'message':'username is required'})
        totalCandidate=candidate_info.objects.filter(currentStatus=constants.NOTASSIGNED).count()
        numberOfNewApplicants=candidate_info.objects.filter(assigned=user, currentStatus=constants.ASSIGNED).count()
        verfied=candidate_info.objects.filter(assigned=user, currentStatus=constants.INENTRY).count()
        assignedToTech=candidate_info.objects.filter(assigned=user, currentStatus=constants.INTECH).count()
        approvalWaiting=candidate_info.objects.filter(assigned=user, currentStatus=constants.INFINAL).count()
        completed=candidate_info.objects.filter(assigned=user, currentStatus=constants.COMPLETED).count()
        
        jsonResponse={
            'Total Candidates':totalCandidate,
            'Number Of New Applicants':numberOfNewApplicants,
            'Verified':verfied,
            'Assigned To Tech':assignedToTech,
            'Approval Waiting':approvalWaiting,
            'completed':completed
        }
        return Response(jsonResponse)
    
class getListOfInterviewer(APIView):
    def get(self, request, *args, **kwargs):
        auser=user.objects.filter(roles__id=3)
        serializer=ListOfInterviewerSerializer(auser, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
