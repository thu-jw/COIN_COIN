from django.db import models


class Video(models.Model):
    video_name = models.CharField(max_length=200, default="")
    video_class = models.CharField(max_length=200, default="")
    # cut points, seprated by comma. e.g. 1,3,5,10
    cut_points = models.CharField(max_length=200, default="")
    """state of the video
    0: not annotated
    1: annotating
    2: finished
    """
    STATE_CHOICES = [
        (0, 'NOT ANNOTATED'),
        (1, 'ANNOTATING'),
        (2, 'FINISHED'),
    ]
    state = models.PositiveSmallIntegerField(default=0, choices=STATE_CHOICES)

    checkpoint = models.PositiveSmallIntegerField(default=0)

    # total steps
    steps = models.PositiveSmallIntegerField(default=0)

    train = models.BooleanField(default=True)

    action_ids = models.CharField(max_length=300, default="")

    prev_vid = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.video_name
# Create your models here.
