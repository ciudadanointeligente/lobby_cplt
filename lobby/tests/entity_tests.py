from django.test import TestCase
from popolo.models import Organization
from lobby.models import Entidad
from lobby.tests import read_fixture, post_mock
from lobby.management.commands.scrape import EntidadScraper
import json


class EntityTestCase(TestCase):
    def test_instanciate(self):
        instance = Entidad.objects.create(name=u'The name', rut=u'12345')
        self.assertIsInstance(instance, Organization)


class EntidadScraperTestCase(TestCase):
    def test_parse(self):
        azerta_json = json.loads(read_fixture('azerta.json'))
        scraper = EntidadScraper(requester=post_mock)
        scraper.parse(azerta_json, "http://preproduccion-datos.infolobby.cl:80/resource/URI/Entidad/769818200")

        e = Entidad.objects.get(identifiers__identifier="http://preproduccion-datos.infolobby.cl:80/resource/URI/Entidad/769818200")
        self.assertEquals(e.name, 'Azerta Comunicaciones')
        self.assertEquals(e.rut, '769818200')
