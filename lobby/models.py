from django.db import models
from popolo.models import Person, Identifier, Organization
from taggit.managers import TaggableManager
from django.contrib.contenttypes import generic


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
    passive = models.ForeignKey(Passive)
    actives = models.ManyToManyField(Active)
    identifiers = generic.GenericRelation(Identifier, help_text="Issued identifiers")
    registering_organization = models.ForeignKey(Organization, null=True)
    tags = TaggableManager()


class Entidad(Organization):
    rut = models.CharField(max_length=64)
