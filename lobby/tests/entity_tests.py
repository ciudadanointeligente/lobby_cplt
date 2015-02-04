from django.test import TestCase
from popolo.models import Organization
from lobby.models import Entidad
from lobby.tests import read_fixture, post_mock
from lobby.management.commands.scrape import EntidadScraper, Scraper
import json
from django.conf import settings


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

    def test_get_one(self):
        id = "http://preproduccion-datos.infolobby.cl:80/resource/URI/Entidad/769818200"
        scraper = EntidadScraper(requester=post_mock)
        scraper.get_one(id)
        e = Entidad.objects.get(identifiers__identifier=id)
        self.assertEquals(e.name, 'Azerta Comunicaciones')
        self.assertEquals(e.rut, '769818200')

    def test_get_several(self):
        response = post_mock(settings.SPARQL_ENDPOING, data={'query': settings.ENTIDADES_QUERY, 'output': 'json'})
        entidades_scrapper = Scraper(EntidadScraper, requester=post_mock)
        entidades_scrapper.parse(response.content)

        self.assertEquals(Entidad.objects.count(), 2)
