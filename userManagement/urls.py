
from django.urls import path
from .views import (RegistrationView, LoginView, GetAllUsersView, 
                    GetAllRolesView, statusOfCandidate, updateUser, GetUser,
                    pauseResumeUser,activeInactiveUser, getListOfInterviewer)
urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('updateUser/<int:pk>', updateUser.as_view(), name='updateUser'),
    path('signin/', LoginView.as_view(), name='login'),
    path('getAllUsers/', GetAllUsersView.as_view(), name='getAllUsers'),
    path('getUser/', GetUser.as_view(), name='getUser'),
    path('getAllRoles/', GetAllRolesView.as_view(), name='getAllRoles'),
    path('getDetails/', statusOfCandidate.as_view(), name='status'),
    path('activeInactiveUser/<int:pk>', activeInactiveUser.as_view(), name='activeInactiveUser'),
    path('pauseResumeUser/<int:pk>', pauseResumeUser.as_view(), name='pauseResumeUser'),
    path('getListOfInterviewer/', getListOfInterviewer.as_view(), name='getListOfInterviewer'),
]
