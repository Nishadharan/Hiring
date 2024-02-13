
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hiring/auth/', include('userManagement.urls')),
    
    path('hiring/entryLevel/',include('HRLevel.entryLevel.urls')),
    path('hiring/evaluationLevel/',include('HRLevel.evaluationLevel.urls')),
    path('hiring/interviewer/',include('technicalLevel.urls')),
]
