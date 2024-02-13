from django.urls import path,include
from .views import SaveInterviewerData, getInterviewerDataById, getCandidateForInterviewer

urlpatterns = [
    path('SaveInterviewerData/',SaveInterviewerData.as_view(),name='SaveInterviewerData'),
    path('getInterviewerDataById/<int:pk>',getInterviewerDataById.as_view(),name='getInterviewerDataById'),
    path('getCandidateForInterviewer/',getCandidateForInterviewer.as_view(),name='getCandidateForInterviewer'),
]
