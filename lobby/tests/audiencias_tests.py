from django.test import TestCase
from lobby.models import Audiencia
from django.utils import timezone


class AudienciasTestCase(TestCase):
    def test_instanciate(self):
        date = timezone.localtime(timezone.now())
        audiencia = Audiencia()
        audiencia.description = "Description"
        audiencia.length = 60
        audiencia.date = date
        audiencia.place = 13101
        audiencia.observations = "Esto puede ser extenso"
        audiencia.save()
        self.assertTrue(audiencia)
        audiencia = Audiencia.objects.get(id=audiencia.id)
        self.assertEquals(audiencia.length, 60)
        self.assertEquals(audiencia.date, date)
        self.assertEquals(audiencia.place, 13101)
        self.assertEquals(audiencia.observations, "Esto puede ser extenso")