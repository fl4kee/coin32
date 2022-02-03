from django.db import models


# Create your models here.
class Url(models.Model):
    long_url = models.CharField(max_length=2000)
    short_url = models.CharField(max_length=200, default=None, null=True)
    subpart = models.CharField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.long_url
