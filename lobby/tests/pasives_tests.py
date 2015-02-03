from django.test import TestCase
from lobby.models import Passive
from django.core.management import call_command
from mock import patch
from django.test.utils import override_settings
from lobby.management.commands.scrape import PassiveScrapper, Scraper
from lobby.tests import PostMock
import os


class PassivePersonTestCase(TestCase):
    def test_instanciate(self):
        '''Instanciate a passive person'''
        passive = Passive.objects.create(name=u'The name')
        self.assertTrue(passive)
        self.assertEquals(passive.name, u'The name')

passives_query = 'SELECT DISTINCT ?instance WHERE { ?instance a <http://preproduccion-datos.infolobby.cl:80/resource/cplt/Persona> } ORDER BY ?instance'
sparql_url = 'http://preproduccion-datos.infolobby.cl:80/sparql'


@override_settings(SPARQL_ENDPOINT=sparql_url)
@override_settings(PASSIVES_QUERY=passives_query)
class PassiveScrapperTestCase(TestCase):
    def astest_it_creates_a_pasive(self):
        with patch('requests.post') as post:
            post.return_value = PostMock('passives.json')

            # result = requests.post('url')
            call_command('scrape', 'passives')
            post.assert_called_with(sparql_url, data={'query': passives_query, 'output': 'json'})

    def test_gets_several_passives(self):
        script_dir = os.path.dirname(__file__)
        f = open(os.path.join(script_dir, 'fixtures/passives.json'), 'r')
        passives_plain = f.read()
        f = open(os.path.join(script_dir, 'fixtures/leonor.json'), 'r')
        leonor_plain = f.read()
        f = open(os.path.join(script_dir, 'fixtures/tatiana.json'), 'r')
        tati_plain = f.read()

        with patch('requests.post') as post:
            post.return_value = PostMock()
            scraper = Scraper()
            scraper.parse(passives_plain)
            self.assertEquals(post.call_count, 2)

    def test_gets_one_passive(self):
        with patch('requests.post') as post:
            post.return_value = PostMock('leonor.json')

            scraper = PassiveScrapper()
            passive = scraper.get_one('http://preproduccion-datos.infolobby.cl:80/resource/URI/Persona/01000000000EC4A714E03B5E787C7BB13378FB26CDCC783038F1043B399A23046F478035')
            self.assertEquals(passive.name, 'Leonor Droguett Guerra')
            query = 'SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE { { <http://preproduccion-datos.infolobby.cl:80/resource/URI/Persona/01000000000EC4A714E03B5E787C7BB13378FB26CDCC783038F1043B399A23046F478035> ?property ?hasValue }  UNION { ?isValueOf ?property <http://preproduccion-datos.infolobby.cl:80/resource/URI/Persona/01000000000EC4A714E03B5E787C7BB13378FB26CDCC783038F1043B399A23046F478035> } } ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf'
            post.assert_called_with(sparql_url, data={'query': query, 'output': 'json'})

    def test_gets_one_but_not_replicates(self):
        with patch('requests.post') as post:
            post.return_value = PostMock('leonor.json')
            scraper = PassiveScrapper()
            scraper.get_one('http://preproduccion-datos.infolobby.cl:80/resource/URI/Persona/01000000000EC4A714E03B5E787C7BB13378FB26CDCC783038F1043B399A23046F478035')
            scraper.get_one('http://preproduccion-datos.infolobby.cl:80/resource/URI/Persona/01000000000EC4A714E03B5E787C7BB13378FB26CDCC783038F1043B399A23046F478035')

            leonores = Passive.objects.filter(name='Leonor Droguett Guerra')
            self.assertEquals(leonores.count(), 1)
