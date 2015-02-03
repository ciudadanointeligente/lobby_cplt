from django.test import TestCase
from lobby.models import Audiencia, Passive, Active
from django.utils import timezone


class AudienciasTestCase(TestCase):
    def setUp(self):
        self.passive = Passive.objects.create(name=u'The name')

    def test_instanciate(self):
        date = timezone.localtime(timezone.now())
        audiencia = Audiencia()
        audiencia.description = "Description"
        audiencia.length = 60
        audiencia.date = date
        audiencia.place = 13101
        audiencia.observations = "Esto puede ser extenso"
        audiencia.passive = self.passive
        audiencia.save()
        self.assertTrue(audiencia)
        audiencia = Audiencia.objects.get(id=audiencia.id)
        self.assertEquals(audiencia.length, 60)
        self.assertEquals(audiencia.date, date)
        self.assertEquals(audiencia.place, 13101)
        self.assertEquals(audiencia.observations, "Esto puede ser extenso")
        self.assertEquals(audiencia.passive, self.passive)

    def test_audiencia_several_actives(self):
        audiencia = Audiencia()
        audiencia.description = "Description"
        audiencia.passive = self.passive
        audiencia.save()

        active1 = Active.objects.create(name=u"Perico los palotes")
        active2 = Active.objects.create(name=u"Perico los palotes2")

        audiencia.actives.add(active1)
        audiencia.actives.add(active2)

        audiencia = Audiencia.objects.get(id=audiencia.id)
        self.assertTrue(audiencia.actives.all())
        self.assertEqual(audiencia.actives.count(), 2)
        self.assertIn(active1, audiencia.actives.all())
        self.assertIn(active2, audiencia.actives.all())
