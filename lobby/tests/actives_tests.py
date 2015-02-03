from lobby.models import Active
from django.test import TestCase
from popolo.models import Identifier
from lobby.management.commands.scrape import ActiveScrapper
from lobby.tests import post_mock
from django.test.utils import override_settings
import json
import os


class ActiveTestCase(TestCase):
    def test_instanciate_one_with_name(self):
        active = Active.objects.create(name=u"Perico los palotes")

        self.assertTrue(active)
        self.assertEquals(active.name, u"Perico los palotes")

    def test_actives_have_tags(self):
        active = Active.objects.create(name=u"Perico los palotes")
        active.tags.add('Tag')
        self.assertTrue(active.tags.all())
        self.assertTrue(active.tags.count(), 1)

    def test_use_identifiers(self):
        active = Active.objects.create(name=u"Perico los palotes")

        identifier = Identifier(identifier="perico")
        active.identifiers.add(identifier)

        active2 = Active.objects.get(identifiers__identifier='perico')
        self.assertTrue(active2)
        self.assertEquals(active2.name, u"Perico los palotes")

    def test_use_two_identifiers(self):
        active = Active.objects.create(name=u"Perico los palotes")

        identifier = Identifier(identifier="perico")
        identifier2 = Identifier(identifier="condorito")
        active.identifiers.add(identifier)
        active.identifiers.add(identifier2)

        active_search_one = Active.objects.get(identifiers__identifier="perico")
        active_search_two = Active.objects.get(identifiers__identifier="condorito")
        self.assertTrue(active_search_one)
        self.assertTrue(active_search_two)
        self.assertEquals(active_search_one.name, u"Perico los palotes")
        self.assertEquals(active_search_two.name, u"Perico los palotes")


actives_query = 'SELECT DISTINCT * WHERE { ?s a foaf:Person; cplt:validoDurante ?p }'
sparql_url = 'http://preproduccion-datos.infolobby.cl:80/sparql'


@override_settings(SPARQL_ENDPOINT=sparql_url)
@override_settings(ACTIVES_QUERY=actives_query)
class ActiveScrapperTestCase(TestCase):
    def test_get_one(self):
        scraper = ActiveScrapper(requester=post_mock)
        scraper.get_one('http://preproduccion-datos.infolobby.cl:80/resource/temp/Activo/3905')

        active = Active.objects.filter(name="Alejandro Jimenez")
        self.assertTrue(active)

    def test_create_only_one(self):
        script_dir = os.path.dirname(__file__)
        f = open(os.path.join(script_dir, 'fixtures/alejandro.json'), 'r')
        alejandro_json = json.loads(f.read())

        scraper = ActiveScrapper()
        scraper.parse(alejandro_json, 'http://preproduccion-datos.infolobby.cl:80/resource/temp/Activo/3905')
        scraper.parse(alejandro_json, 'http://preproduccion-datos.infolobby.cl:80/resource/temp/Activo/3905')

        alejandros = Active.objects.filter(name="Alejandro Jimenez")
        self.assertEquals(alejandros.count(), 1)
