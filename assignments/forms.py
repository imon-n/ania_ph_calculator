from django import forms
from .models import Assignment

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['assigned_marks', 'obtained_marks']

    def clean_obtained_marks(self):
        obtained_marks = self.cleaned_data.get('obtained_marks')
        assigned_marks = self.cleaned_data.get('assigned_marks')
        total_submissions = Assignment.objects.count()
        
        if obtained_marks > assigned_marks:
            raise forms.ValidationError("Obtained marks cannot be greater than assigned marks.")
        
        required_percentage = 0.5 if total_submissions < 10 else 0.7
        if obtained_marks < (required_percentage * assigned_marks):
            raise forms.ValidationError(f"You must score at least {int(required_percentage * 100)}% of the assigned marks.")
        
        return obtained_marks