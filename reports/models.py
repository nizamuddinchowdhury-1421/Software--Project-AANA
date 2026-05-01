from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ProblemReport(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    PROBLEM_TYPES = [
        ('engine', 'Engine Problem'),
        ('tire', 'Tire Issue'),
        ('battery', 'Battery Problem'),
        ('brake', 'Brake Issue'),
        ('electrical', 'Electrical Problem'),
        ('fuel', 'Fuel System'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='problem_reports')
    title = models.CharField(max_length=200, help_text='Brief description of the problem')
    description = models.TextField(help_text='Detailed description of the problem')
    problem_type = models.CharField(max_length=20, choices=PROBLEM_TYPES, default='other')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    

    location = models.CharField(max_length=200, help_text='Current location where the problem occurred')
    latitude = models.FloatField(null=True, blank=True, help_text='GPS latitude')
    longitude = models.FloatField(null=True, blank=True, help_text='GPS longitude')
    

    phone_number = models.CharField(max_length=15, help_text='Contact number for assistance')
    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    assigned_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                     related_name='assigned_reports', limit_choices_to={'groups__name': 'Agents'})
    assigned_center = models.ForeignKey('centers.ServiceCenter', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.user.username} ({self.status})"
    
    class Meta:
        ordering = ['-created_at']

class ProblemPhoto(models.Model):
    problem_report = models.ForeignKey(ProblemReport, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='problem_photos/%Y/%m/%d/', help_text='Upload photos of the problem')
    description = models.CharField(max_length=200, blank=True, help_text='Optional description of this photo')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Photo for {self.problem_report.title}"
    
    class Meta:
        ordering = ['uploaded_at']

class ProblemResponse(models.Model):
    problem_report = models.ForeignKey(ProblemReport, on_delete=models.CASCADE, related_name='responses')
    responder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='problem_responses')
    message = models.TextField(help_text='Response message to the user')
    is_solution = models.BooleanField(default=False, help_text='Is this a solution to the problem?')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Response to {self.problem_report.title} by {self.responder.username}"
    
    class Meta:
        ordering = ['created_at']