from django.db import models

class AnalysisResult(models.Model):
    input_text = models.TextField()
    positive_percent = models.FloatField(default=0.0)
    negative_percent = models.FloatField(default=0.0)
    neutral_percent = models.FloatField(default=0.0)
    analysis_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Analysis on {self.analysis_date}'