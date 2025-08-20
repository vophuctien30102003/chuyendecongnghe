from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=255)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - timezone.timedelta(days=1)
