from django.db import models

LENGTH = 30
MAX_USERS = 20
USERNAME_LENGTH = 16

class QA(models.Model):
    """questions
    [start_frame, end_frame]
    """
    question = models.CharField(max_length=2 * LENGTH)
    choices = models.CharField(max_length=LENGTH * 6 * 4)
    """answers from users"""
    answers = models.CharField(max_length=MAX_USERS, default='')
    answerers = models.CharField(max_length=MAX_USERS * USERNAME_LENGTH)
    correct_answer = models.PositiveSmallIntegerField(default=5)

    phase = models.CharField(default='test', max_length=10)
    setting = models.CharField(max_length=20, default='')
 #
# Create your models here.
