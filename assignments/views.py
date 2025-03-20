from django.shortcuts import render, redirect
from .models import Assignment
from .forms import AssignmentForm

def assignment_submission(request):
    assignments = Assignment.objects.all()
    total_submissions = assignments.count()
    total_assigned_marks = sum(a.assigned_marks for a in assignments)
    total_obtained_marks = sum(a.obtained_marks for a in assignments)
    
    # Calculate average marks
    average_marks = (total_obtained_marks / total_submissions) if total_submissions > 0 else 0
    
    # Calculate required marks to maintain minimum 48 average across 12 assignments
    required_total_marks = 48 * 12  # Total required marks across 12 assignments
    remaining_needed = max(0, (required_total_marks - total_obtained_marks) / (12 - total_submissions)) if total_submissions < 12 else 0
    
    # Check last two assignments' requirement
    last_two_required = "N/A"
    if total_submissions >= 2:
        last_two_assignments = assignments.order_by('-id')[:2]
        last_two_required = all(a.obtained_marks >= (0.7 * a.assigned_marks) for a in last_two_assignments)
    
    if request.method == "POST":
        if "clear_data" in request.POST:
            assignments.delete()
            return redirect('assignment_submission')
        
        form = AssignmentForm(request.POST)
        if form.is_valid():
            new_assignment = form.save()
            return redirect('assignment_submission')
    else:
        form = AssignmentForm()
    
    context = {
        'form': form,
        'assignments': assignments,
        'average_marks': round(average_marks, 2),
        'remaining_needed': round(remaining_needed, 2),
        'last_two_required': "Yes" if last_two_required else "No",
    }
    
    return render(request, 'assignment_submission.html', context)
