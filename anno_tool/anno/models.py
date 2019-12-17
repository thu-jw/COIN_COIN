from django.db import models

class Video(models.Model):
    # name of video
    video_name = models.CharField(max_length=200)
    # cut points, seprated by comma. e.g. 1,3,5,10
    cut_points = models.CharField(max_length=200)
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
    state = models.SmallIntegerField(default=0, choices=STATE_CHOICES)

    checkpoint = models.SmallIntegerField(default=0)

    def __init__(self):
        return self.video_name
# Create your models here.
