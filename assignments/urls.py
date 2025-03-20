from django.urls import path
from .views import assignment_submission

urlpatterns = [
    path('', assignment_submission, name='assignment_submission'),
]