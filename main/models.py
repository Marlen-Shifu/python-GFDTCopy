from django.db import models

import uuid


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    goal = models.CharField(max_length = 255)
    deadline = models.DateField()
    payment = models.PositiveIntegerField()
    user_name = models.CharField(max_length=255, default='')
    user_email = models.EmailField()
    verificator_name = models.CharField(max_length=255, default='')
    verificator_email = models.EmailField()
    verified = models.BooleanField(default = False)
    closed = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    #card_info

    def __str__(self):
        return f'Goal: {self.goal}, user: {self.user_email}'

