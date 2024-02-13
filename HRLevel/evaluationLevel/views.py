from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from HiringBackend.util import constants
from HRLevel.models import candidate_info
from HRLevel.entryLevel.serializer import AllcandidateSerializer
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
        serializer = AllcandidateSerializer(candidates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class finalEvaluation(generics.ListCreateAPIView):
    queryset = evaluationdata.objects.all()
    serializer_class = evaluationserializer
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        payload=request.data
        if payload.get('submissionStatus', None)==constants.SUBMIT:
            changeStatus(payload, constants.COMPLETED)
        # else:
        #     changeStatus(payload, constants.INFINAL)
        
    
class finalEvalById(generics.RetrieveAPIView):
    serializer_class = evaluationserializer
    permission_classes = [IsAuthenticated]
 
    def get_object(self):
        pk = self.kwargs.get('pk')
        candidate = get_object_or_404(evaluationdata, pk=pk)
        return candidate
            