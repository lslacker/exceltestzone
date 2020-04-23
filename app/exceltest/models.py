from django.db import models
from django.utils import timezone


class Question(models.Model):
    id = models.IntegerField(primary_key=True)
    text = models.TextField()
    hint = models.TextField()
    type = models.TextField(max_length=50)
    test_id = models.IntegerField()
    category = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text or self.hint


class Stimulus(models.Model):

    text = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    filename = models.TextField(null=True, blank=True)
    question_id = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="stimulus")
    order = models.PositiveSmallIntegerField()
    created_date = models.DateTimeField(default=timezone.now)


class Review(models.Model):
    column_1_text = models.TextField(null=True, blank=True)
    column_2_text = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    filename = models.TextField(null=True, blank=True)
    question_id = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="reviews")
    order = models.PositiveSmallIntegerField()
    created_date = models.DateTimeField(default=timezone.now)


class Choice(models.Model):
    label = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    filename = models.TextField(null=True, blank=True)
    question_id = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices")
    order = models.PositiveSmallIntegerField()
    created_date = models.DateTimeField(default=timezone.now)
    correct = models.BooleanField(default=False)
