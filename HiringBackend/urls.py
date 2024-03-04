
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hiring/auth/', include('userManagement.urls')),
    
    path('hiring/entryLevel/',include('HRLevel.entryLevel.urls')),
    path('hiring/evaluationLevel/',include('HRLevel.evaluationLevel.urls')),
    path('hiring/interviewer/',include('technicalLevel.urls')),
    path('', TemplateView.as_view(template_name="index.html"), name="index")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
