from django.urls import path,include
from HRLevel.entryLevel.views import (assign_resume_with_out_constraints, GetUnAssignedCandidates,
                              GetAUnassignedCandidate, updatedata, getCandidateForRecruiter,postMeetingData,getallMeetingData,getspecificMeetingData,getEmail,sendEmail
                              )
# getCandidateForInterviewer

urlpatterns = [
    # path('userrolelist/',userrolelist.as_view(),name='user-list'),
    # path('store/',storedata.as_view(),name='store-data'),
    # path('retrivedata/<int:pk>/',retrivedata.as_view(),name='entryleveldatauprt-id'),
    # path('updatedata/<int:pk>/',updatedata.as_view(),name='entryleveldatauprt-id'),
    # path('llmcandidatedata/',llmcandidatedatas.as_view(),name='entryleveldata-list'),
    path('assignRole/',assign_resume_with_out_constraints.as_view(),name='assign_resume_with_out_constraints'),
    path('getAllCandidates/',GetUnAssignedCandidates.as_view(),name='GetUnAssignedCandidates'),
    path('getACandidate/<int:id>',GetAUnassignedCandidate.as_view(),name='GetAUnassignedCandidate'),
    path('updatedata/<str:resumeId>/',updatedata.as_view(),name='entryleveldatauprt-id'),
    path('getCandidateForRecruiter/',getCandidateForRecruiter.as_view(),name='getCandidateForRecruiter'),
    path('createMeeting/', postMeetingData.as_view(), name='createMeeting'),
    path('getallMeetingdata', getallMeetingData.as_view(), name = 'getallMeetingdata'),
    path('getspecificMeetingdata', getspecificMeetingData.as_view(), name = 'getspecificMeetingdata'),
    path('getemail',getEmail.as_view(),name= 'getemailapi'),
    path('sendemail',sendEmail.as_view(),name= 'sendemailapi'),

    # path('sendMail/',SendEmailView.as_view(),name='SendEmailView'),
]
