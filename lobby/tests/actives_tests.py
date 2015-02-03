from lobby.models import Active
from django.test import TestCase
from popolo.models import Identifier


class ActiveTestCase(TestCase):
    def test_instanciate_one_with_name(self):
        active = Active.objects.create(name=u"Perico los palotes")

        self.assertTrue(active)
        self.assertEquals(active.name, u"Perico los palotes")

    def test_use_identifiers(self):
        active = Active.objects.create(name=u"Perico los palotes")

        identifier = Identifier(identifier="perico")
        active.identifiers.add(identifier)

        active2 = Active.objects.get(identifiers__identifier='perico')
        self.assertTrue(active2)
        self.assertEquals(active2.name, u"Perico los palotes")
