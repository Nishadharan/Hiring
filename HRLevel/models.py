from django.db import models
from HiringBackend.util import constants

class SourceMode(models.Model):
    name = models.CharField(unique=True, max_length=50, null=False)
    
    def __str__(self):
        return self.name

class Status(models.Model):
    status = models.CharField(unique=True, max_length=50, null=False)

    def __str__(self):
        return self.status
    
# class candidateInfo(models.Model):
    
    
    # resumeScore=models.PositiveIntegerField()
    # status like NOT_ASSIGNED, IN_ENTRY, IN_TECH, IN_FINAL, COMPLETED/
    
class candidate_info(models.Model):
    
    # resume = models.FileField()
    resumeId = models.CharField(unique=True, max_length=255)
    appliedDate=models.DateField(null=True)
    email = models.EmailField()
    assigned=models.CharField(max_length=50, null=True)
    assignedDate=models.DateField(null=True)
    interviewer=models.CharField(max_length=50, null=True)
    interviewerAssignedDate=models.DateField(null=True)
    currentStatus=models.CharField(default="NOT_ASSIGNED",max_length=50, null=True)
    shortlistStatus=models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=75,null=True)
    resumeScore = models.CharField(max_length=255)
    
    jobRole = models.CharField(max_length=75, null=True)
    yearsOfExperience = models.CharField(max_length=255)
    phoneNo = models.CharField(max_length = 100, null=True)
    yearOfGraduation = models.CharField(max_length=75, null=True)    
    
    location = models.CharField(max_length=100, null=True)
    qualification = models.CharField(max_length=100, null=True)
    domainExperience = models.IntegerField(null=True)
    reason = models.CharField(max_length=50, null=True)
    travelConstraint = models.CharField( max_length=100, null=True)
    sourceMode = models.ForeignKey(SourceMode, on_delete=models.CASCADE, null=True)
    referenceName = models.CharField(max_length=50, null=True)
    referenceEmail = models.EmailField(unique = True, null=True)
    notificationPeriod = models.CharField(max_length=50, null=True)
    fatherOccupation = models.CharField( max_length=50, null=True)
    motherOccupation = models.CharField( max_length=50, null=True)
    siblings = models.CharField(max_length=50, null=True)
    # status = models.ForeignKey(Status, on_delete=models.CASCADE)
    remarks = models.CharField(max_length=500, null=True)
    # SAVED SUBMITTED
    # submissionStatus=models.CharField(max_length=20, default=constants.SAVE, null=True)
    recruiterSubmissionStatus=models.CharField(max_length=20, null=True)
    #JSON DATA RECEIVED:
    # {'Name': 'Jane Smith', 'Email': 'janesmith@email.com', 'Resume_score': 69, 'Job_Role': 'Sales', 'Experience': 8, 'phone': '555-987-6543', 'Year_of_Graduation': 'N/A'}
    interviewerSubmissionStatus=models.CharField(max_length=20, null=True)
    
    resume_Link=models.CharField(max_length=1000, null=True)
    def __str__(self):
        return self.name
class evaluationdata(models.Model):
 
    resumeId = models.CharField(unique=True, max_length=255)
    longTermAssocaition = models.CharField(max_length=500,null=True)
    # joinDate = models.CharField(max_length=50,null=True)
    joinDate=models.DateField()
    specialRequest = models.CharField(max_length=100,null=True)
    hrFeedback = models.CharField(max_length=1000,null=True)
    shortlistStatus = models.CharField(max_length=50, null=True)
    remarks = models.CharField(max_length=1000,null=True)
    submissionStatus=models.CharField(max_length=50, null=True)

class meetingdata(models.Model):
    meetingURL = models.TextField()
    candidate = models.CharField(max_length = 100)
    date = models.DateField()
    startTime = models.CharField(max_length =20)
    endTime = models.CharField(max_length =20)
    description = models.TextField()
    