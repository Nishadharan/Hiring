from django.urls import path
from HRLevel.evaluationLevel.views import (CandidateForFinalEval, finalEvaluation, finalEvalById)

urlpatterns = [
    path('CandidateForFinalEval/',CandidateForFinalEval.as_view(),name='getCandidateForFinalEval'),
    path('finalEvaluation/',finalEvaluation.as_view(),name='finalEvaluation'),
    path('finalEvalById/<int:pk>',finalEvalById.as_view(),name='finalEvalById'),
]
