from django.db import models

class Assignment(models.Model):
    assigned_marks = models.IntegerField(choices=[(60, '60'), (50, '50'), (30, '30')])
    obtained_marks = models.IntegerField()

    def __str__(self):
        return f"Assignment ({self.assigned_marks}) - Obtained: {self.obtained_marks}"
