from django.db import models
from popolo.models import Person
from taggit.managers import TaggableManager


# Create your models here.
class Passive(Person):
    tags = TaggableManager()


class Active(Person):
    tags = TaggableManager()


class Audiencia(models.Model):
    description = models.CharField(max_length=1024)
    length = models.IntegerField(null=True)
    date = models.DateTimeField(null=True)
    place = models.IntegerField(null=True)
    observations = models.TextField(null=True)
