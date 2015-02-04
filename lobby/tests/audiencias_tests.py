from django.test import TestCase
from lobby.models import Audiencia, Passive, Active
from django.utils import timezone
from popolo.models import Identifier, Organization
from django.test.utils import override_settings
import json
from lobby.management.commands.scrape import AudienciasScraper, MinutesScraper, IniciaScraper
from lobby.tests import post_mock, read_fixture


class AudienciasTestCase(TestCase):
    def setUp(self):
        self.passive = Passive.objects.create(name=u'The name')

    def test_instanciate(self):
        organization = Organization.objects.create(name=u"The organization")
        date = timezone.localtime(timezone.now())
        audiencia = Audiencia()
        audiencia.description = "Description"
        audiencia.length = 60
        audiencia.date = date
        audiencia.place = 13101
        audiencia.registering_organization = organization
        audiencia.observations = "Esto puede ser extenso"
        audiencia.passive = self.passive
        audiencia.save()
        identifier = Identifier(identifier='perrito')
        audiencia.identifiers.add(identifier)
        self.assertTrue(audiencia)
        audiencia = Audiencia.objects.get(id=audiencia.id)
        self.assertEquals(audiencia.length, 60)
        self.assertEquals(audiencia.date, date)
        self.assertEquals(audiencia.place, 13101)
        self.assertEquals(audiencia.registering_organization, organization)
        self.assertEquals(audiencia.observations, "Esto puede ser extenso")
        self.assertEquals(audiencia.passive, self.passive)
        self.assertTrue(audiencia.identifiers.all())
        self.assertEquals(audiencia.identifiers.count(), 1)

    def test_audiencia_several_actives(self):
        organization = Organization.objects.create(name=u"The organization")
        audiencia = Audiencia()
        audiencia.description = "Description"
        audiencia.passive = self.passive
        audiencia.registering_organization = organization
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

    def test_audiencia_have_a_tag(self):
        organization = Organization.objects.create(name=u"The organization")
        audiencia = Audiencia()
        audiencia.description = "Description"
        audiencia.passive = self.passive
        audiencia.registering_organization = organization
        audiencia.save()
        audiencia.tags.add('Tag')
        self.assertTrue(audiencia.tags.all())
        self.assertTrue(audiencia.tags.count(), 1)

audiencias_query = 'SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE { { <$id> ?property ?hasValue } UNION { ?isValueOf ?property <$id> } } ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf'
sparql_url = 'http://preproduccion-datos.infolobby.cl:80/sparql'


@override_settings(SPARQL_ENDPOINT=sparql_url)
@override_settings(AUDIENCIAS_QUERY=audiencias_query)
class AudienciasScraperTestCase(TestCase):
    fixtures = ['persons']

    def setUp(self):
        self.organization = Organization.objects.create(name=u"The org")
        i = Identifier(identifier="http://preproduccion-datos.infolobby.cl:80/resource/URI/Institucion/AF001")
        self.organization.identifiers.add(i)

    def test_loads_an_audiencia(self):
        audiencia_2204_json = json.loads(read_fixture('audiencia_2204.json'))

        scraper = AudienciasScraper(requester=post_mock)
        scraper.parse(audiencia_2204_json, 'http://preproduccion-datos.infolobby.cl:80/resource/temp/RegistroAudiencia/2204')

        audiencias = Audiencia.objects.filter(identifiers__identifier='http://preproduccion-datos.infolobby.cl:80/resource/temp/RegistroAudiencia/2204')
        self.assertTrue(audiencias)
        self.assertEquals(audiencias.count(), 1)
        audiencia = audiencias[0]
        self.assertEquals(audiencia.description, "Oficina subsecretaria")
        self.assertEquals(audiencia.length, 60)
        self.assertEquals(audiencia.date.year, 2014)
        self.assertEquals(audiencia.date.month, 12)
        self.assertEquals(audiencia.date.day, 3)
        self.assertTrue(audiencia.observations)
        paty = Passive.objects.get(pk=305)
        self.assertEquals(audiencia.passive, paty)

        a1 = Active.objects.get(pk=480)
        a2 = Active.objects.get(pk=481)
        a3 = Active.objects.get(pk=482)

        self.assertIn(a1, audiencia.actives.all())
        self.assertIn(a2, audiencia.actives.all())
        self.assertIn(a3, audiencia.actives.all())

    def test_scrape_twice_audiencias(self):
        audiencia_2204_json = json.loads(read_fixture('audiencia_2204.json'))

        scraper = AudienciasScraper(requester=post_mock)
        scraper.parse(audiencia_2204_json, 'http://preproduccion-datos.infolobby.cl:80/resource/temp/RegistroAudiencia/2204')
        scraper.parse(audiencia_2204_json, 'http://preproduccion-datos.infolobby.cl:80/resource/temp/RegistroAudiencia/2204')

        audiencias = Audiencia.objects.filter(identifiers__identifier='http://preproduccion-datos.infolobby.cl:80/resource/temp/RegistroAudiencia/2204')

        self.assertEquals(audiencias.count(), 1)

    def test_get_one_audiencia(self):
        scraper = AudienciasScraper(requester=post_mock)
        scraper.get_one('http://preproduccion-datos.infolobby.cl:80/resource/temp/RegistroAudiencia/2204')
        audiencias = Audiencia.objects.filter(identifiers__identifier='http://preproduccion-datos.infolobby.cl:80/resource/temp/RegistroAudiencia/2204')

        self.assertEquals(audiencias.count(), 1)


class MinutesParserTestCase(TestCase):
    def test_the_scraper_parses_one(self):
        minutes_json = json.loads(read_fixture('audienci_2204_minutes.json'))

        scraper = MinutesScraper()
        minutes = scraper.parse(minutes_json)
        self.assertEquals(minutes, '60')

    def test_get_one_minute(self):
        scraper = MinutesScraper(requester=post_mock)
        minutes = scraper.get_one("http://preproduccion-datos.infolobby.cl:80/resource/temp/AudienciaMinutos/2204")

        self.assertEquals(minutes, 60)


class IniciaParserTestCasse(TestCase):
    def test_the_scraper_parses_one(self):
        inicia_json = json.loads(read_fixture('audiencia_2204_inicia.json'))

        scraper = IniciaScraper()
        date = scraper.parse(inicia_json)
        self.assertEquals(date, '2014-12-03T00:00:00')

    def test_get_one(self):
        scraper = IniciaScraper(requester=post_mock)
        date = scraper.get_one('http://preproduccion-datos.infolobby.cl:80/resource/temp/AudienciaInicio/2204')
        self.assertEquals(date.year, 2014)
        self.assertEquals(date.month, 12)
        self.assertEquals(date.day, 3)
