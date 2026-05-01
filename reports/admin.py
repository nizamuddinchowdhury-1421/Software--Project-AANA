from django.contrib import admin
from .models import ProblemReport, ProblemPhoto, ProblemResponse

class ProblemPhotoInline(admin.TabularInline):
    model = ProblemPhoto
    extra = 0
    readonly_fields = ['uploaded_at']

class ProblemResponseInline(admin.TabularInline):
    model = ProblemResponse
    extra = 0
    readonly_fields = ['created_at']

@admin.register(ProblemReport)
class ProblemReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'problem_type', 'priority', 'status', 'created_at', 'assigned_agent']
    list_filter = ['status', 'priority', 'problem_type', 'created_at', 'assigned_agent']
    search_fields = ['title', 'description', 'user__username', 'location']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ProblemPhotoInline, ProblemResponseInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'title', 'description', 'problem_type', 'priority')
        }),
        ('Location', {
            'fields': ('location', 'latitude', 'longitude')
        }),
        ('Contact', {
            'fields': ('phone_number',)
        }),
        ('Assignment', {
            'fields': ('assigned_agent', 'assigned_center', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ProblemPhoto)
class ProblemPhotoAdmin(admin.ModelAdmin):
    list_display = ['problem_report', 'description', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['problem_report__title', 'description']

@admin.register(ProblemResponse)
class ProblemResponseAdmin(admin.ModelAdmin):
    list_display = ['problem_report', 'responder', 'is_solution', 'created_at']
    list_filter = ['is_solution', 'created_at', 'responder']
    search_fields = ['problem_report__title', 'message', 'responder__username']
