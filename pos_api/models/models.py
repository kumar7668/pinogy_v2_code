from django.db import models
from solo.models import SingletonModel


class PoApiSession(SingletonModel):
    token = models.CharField("token", max_length=255, default="", blank=True)
