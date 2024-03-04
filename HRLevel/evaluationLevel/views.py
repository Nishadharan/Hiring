from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from HiringBackend.util import constants
from HRLevel.models import candidate_info, evaluationdata
from HRLevel.entryLevel.serializer import AllcandidateSerializer, candidateInfoSerializer
from rest_framework.response import Response
from rest_framework import status, generics
from .serializer import evaluationserializer
from HRLevel.models import evaluationdata
from django.shortcuts import get_object_or_404
from technicalLevel.views import changeStatus

class CandidateForFinalEval(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user_id=request.user.empId
        print(user_id)
        candidates=candidate_info.objects.filter(currentStatus=constants.INFINAL, assigned=user_id)
        serializer = candidateInfoSerializer(candidates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class finalEvaluation(generics.ListCreateAPIView):
    queryset = evaluationdata.objects.all()
    serializer_class = evaluationserializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        payload=request.data
        if payload.get('submissionStatus', None)==constants.SUBMIT:
            changeStatus(payload, constants.COMPLETED)
            return Response(payload, status=status.HTTP_200_OK)
        return Response(payload, status=status.HTTP_200_OK)
    
        # else:
        #     changeStatus(payload, constants.INFINAL)
        
        
class finalEvaluation(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        payload=request.data
        id=payload.get('id', None)
        if id:
            evaluation = evaluationdata.objects.get(id=id)
            updateserializer=evaluationserializer(evaluation, data=payload)
            if updateserializer.is_valid():
                updateserializer.save()
                if payload.get('submissionStatus', None)==constants.SUBMIT:
                    changeStatus(payload, constants.COMPLETED)
                # changeStatus(payload, constants.COMPLETED)
                return Response(updateserializer.data, status=status.HTTP_200_OK)
            return Response(updateserializer.errors, status=status.HTTP_200_OK)
        else:
            
            serializer=evaluationserializer(data=payload)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            
    
class finalEvalById(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        resumeId = self.kwargs.get('pk')
        try:
            candidate = evaluationdata.objects.get(resumeId= resumeId)
        except evaluationdata.DoesNotExist:
            return Response({'message':'data with this is id does not exist!'})
        serializer = evaluationserializer(candidate)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

# class finalEvalById(generics.RetrieveAPIView):
#     serializer_class = evaluationserializer
#     permission_classes = [IsAuthenticated]
 
#     def get_object(self):
#         pk = self.kwargs.get('pk')
#         # candidate = get_object_or_404(evaluationdata, resumeId=pk)
#         try:
#             candidate=evaluationdata.objects.get(resumeId=pk)
#         except:
#             return evaluationdata()
            
#         return candidate
    
    
    
# class finalEvalById(APIView):
#     def get(self, request, *args, **kwargs):
#         permission_classes = [IsAuthenticated]
#         resumeId = self.kwargs.get('pk')
#         evaluationData=evaluationdata.objects.get(resumeId)
#         # print(evaluationData)
#         serializer=evaluationserializer(evaluationData)
#         return serializer.data
