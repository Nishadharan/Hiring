from django.db import models

# Create your models here.
class TechnicalInterviewTable(models.Model):
   
    candidateName = models.CharField(max_length=100, null=True)
    resumeId = models.CharField(max_length=100, null=True)
    # resume = models.FileField(null=True)
    strength = models.CharField(max_length=150, null=True)
    weakness = models.CharField(max_length=150, null=True)
    shortlistStatus = models.CharField(max_length=50, null=True)
    submissionStatus=models.CharField(max_length=50, null=True)
    overall_comments = models.CharField(max_length=280, null=True)
    overall_rating = models.FloatField(null=True)
    remarks = models.CharField(max_length=50,null=True)
    
    def __str__(self):
        return self.resumeId
    
class SkillsTable(models.Model):

    skills = models.CharField(max_length = 100, null =True)
    proficiency = models.CharField(max_length = 100, null =True)
    ratingoutof10 = models.PositiveIntegerField(null=True)
    comments = models.CharField(max_length = 150, null =True)
    techReview=models.ForeignKey(TechnicalInterviewTable, on_delete=models.CASCADE, null=True, related_name="skills")
    
    # sourceMode = models.ForeignKey(SourceMode, on_delete=models.CASCADE, null=True)