from __future__ import unicode_literals
from django.db import models
from django.utils import timezone

class Node(models.Model):
    location = models.CharField(max_length=20)
    current = models.IntegerField(default=0)

    def __str__(self):
        return self.location

class Reading(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    db_level = models.IntegerField(default=0)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s - %s' % (self.node.location, self.time)
