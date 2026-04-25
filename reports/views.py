from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .models import ProblemReport, ProblemPhoto, ProblemResponse
from .forms import ProblemReportForm, ProblemResponseForm, ProblemReportUpdateForm

def is_agent_or_admin(user):

    return user.is_staff or user.groups.filter(name='Agents').exists()

@login_required
def report_problem(request):

    if request.method == 'POST':
        form = ProblemReportForm(request.POST, request.FILES)
        if form.is_valid():

            problem_report = form.save(commit=False)
            problem_report.user = request.user
            

            if not problem_report.phone_number and hasattr(request.user, 'profile'):
                problem_report.phone_number = request.user.profile.phone_number or ""
            
            problem_report.save()
            

            photos = request.FILES.getlist('photos')
            for photo in photos:
                ProblemPhoto.objects.create(
                    problem_report=problem_report,
                    photo=photo
                )
            
            messages.success(request, 'Your problem has been reported successfully! Our team will review it and get back to you soon.')
            return redirect('problem_detail', problem_id=problem_report.id)
    else:
        form = ProblemReportForm()
    
    return render(request, 'reports/report_problem.html', {'form': form})

@login_required
def my_problems(request):

    problems = ProblemReport.objects.filter(user=request.user).order_by('-created_at')
    

    paginator = Paginator(problems, 10)
    page_number = request.GET.get('page')
    problems = paginator.get_page(page_number)
    
    return render(request, 'reports/my_problems.html', {'problems': problems})

@login_required
def problem_detail(request, problem_id):

    problem = get_object_or_404(ProblemReport, id=problem_id)
    

    if not (problem.user == request.user or is_agent_or_admin(request.user)):
        messages.error(request, 'You do not have permission to view this problem report.')
        return redirect('home')
    
    responses = problem.responses.all().order_by('created_at')
    photos = problem.photos.all()
    

    response_form = None
    if is_agent_or_admin(request.user):
        response_form = ProblemResponseForm()
    
    return render(request, 'reports/problem_detail.html', {
        'problem': problem,
        'responses': responses,
        'photos': photos,
        'response_form': response_form,
    })

@login_required
@user_passes_test(is_agent_or_admin)
def all_problems(request):

    problems = ProblemReport.objects.all().order_by('-created_at')
    

    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')
    problem_type_filter = request.GET.get('problem_type')
    search_query = request.GET.get('search')
    
    if status_filter:
        problems = problems.filter(status=status_filter)
    if priority_filter:
        problems = problems.filter(priority=priority_filter)
    if problem_type_filter:
        problems = problems.filter(problem_type=problem_type_filter)
    if search_query:
        problems = problems.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(user__username__icontains=search_query)
        )
    

    paginator = Paginator(problems, 15)
    page_number = request.GET.get('page')
    problems = paginator.get_page(page_number)
    
    return render(request, 'reports/all_problems.html', {
        'problems': problems,
        'status_choices': ProblemReport.STATUS_CHOICES,
        'priority_choices': ProblemReport.PRIORITY_CHOICES,
        'problem_type_choices': ProblemReport.PROBLEM_TYPES,
    })

@login_required
@user_passes_test(is_agent_or_admin)
def add_response(request, problem_id):

    problem = get_object_or_404(ProblemReport, id=problem_id)
    
    if request.method == 'POST':
        form = ProblemResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.problem_report = problem
            response.responder = request.user
            response.save()
            

            if response.is_solution:
                problem.status = 'resolved'
                problem.save()
            
            messages.success(request, 'Your response has been added successfully!')
            return redirect('problem_detail', problem_id=problem.id)
    else:
        form = ProblemResponseForm()
    
    return render(request, 'reports/add_response.html', {
        'form': form,
        'problem': problem
    })

@login_required
@user_passes_test(is_agent_or_admin)
def update_problem_status(request, problem_id):

    problem = get_object_or_404(ProblemReport, id=problem_id)
    
    if request.method == 'POST':
        form = ProblemReportUpdateForm(request.POST, instance=problem)
        if form.is_valid():
            form.save()
            messages.success(request, 'Problem status updated successfully!')
            return redirect('problem_detail', problem_id=problem.id)
    else:
        form = ProblemReportUpdateForm(instance=problem)
    
    return render(request, 'reports/update_problem.html', {
        'form': form,
        'problem': problem
    })

@login_required
def problem_stats(request):

    if not is_agent_or_admin(request.user):
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('home')
    
    total_problems = ProblemReport.objects.count()
    pending_problems = ProblemReport.objects.filter(status='pending').count()
    in_progress_problems = ProblemReport.objects.filter(status='in_progress').count()
    resolved_problems = ProblemReport.objects.filter(status='resolved').count()
    

    problem_types = {}
    for choice in ProblemReport.PROBLEM_TYPES:
        problem_types[choice[1]] = ProblemReport.objects.filter(problem_type=choice[0]).count()
    

    priority_dist = {}
    for choice in ProblemReport.PRIORITY_CHOICES:
        priority_dist[choice[1]] = ProblemReport.objects.filter(priority=choice[0]).count()
    
    return render(request, 'reports/problem_stats.html', {
        'total_problems': total_problems,
        'pending_problems': pending_problems,
        'in_progress_problems': in_progress_problems,
        'resolved_problems': resolved_problems,
        'problem_types': problem_types,
        'priority_dist': priority_dist,
    })