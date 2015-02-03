from django.db import models
from popolo.models import Person
from taggit.managers import TaggableManager


# Create your models here.
class Passive(Person):
    tags = TaggableManager()


class Active(Person):
    tags = TaggableManager()
