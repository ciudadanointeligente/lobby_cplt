from django.test import TestCase
from lobby.models import Passive
from django.test.utils import override_settings
from lobby.management.commands.scrape import PassiveScrapper, Scraper
from lobby.tests import post_mock
import os


class PassivePersonTestCase(TestCase):
    def test_instanciate(self):
        '''Instanciate a passive person'''
        passive = Passive.objects.create(name=u'The name')
        self.assertTrue(passive)
        self.assertEquals(passive.name, u'The name')

    def test_passive_have_tags(self):
        passive = Passive.objects.create(name=u"Perico los palotes")
        passive.tags.add('Tag')
        self.assertTrue(passive.tags.all())
        self.assertTrue(passive.tags.count(), 1)

passives_query = 'SELECT DISTINCT ?instance WHERE { ?instance a <http://preproduccion-datos.infolobby.cl:80/resource/cplt/Persona> } ORDER BY ?instance'
sparql_url = 'http://preproduccion-datos.infolobby.cl:80/sparql'


@override_settings(SPARQL_ENDPOINT=sparql_url)
@override_settings(PASSIVES_QUERY=passives_query)
class PassiveScrapperTestCase(TestCase):

    def test_gets_several_passives(self):
        script_dir = os.path.dirname(__file__)
        f = open(os.path.join(script_dir, 'fixtures/passives.json'), 'r')
        passives_plain = f.read()

        scraper = Scraper(PassiveScrapper, requester=post_mock)
        scraper.parse(passives_plain)
        self.assertEquals(Passive.objects.filter(name='Leonor Droguett Guerra').count(), 1)
        self.assertEquals(Passive.objects.filter(name="Tatiana Aceituno Flores").count(), 1)

    def test_create_leo(self):
        script_dir = os.path.dirname(__file__)
        f = open(os.path.join(script_dir, 'fixtures/single_passive.json'), 'r')
        passives_plain = f.read()
        scraper = Scraper(PassiveScrapper, requester=post_mock)
        scraper.parse(passives_plain)

        leonores = Passive.objects.all()
        self.assertEquals(leonores.count(), 1)

    def test_gets_one_passive(self):
        scraper = PassiveScrapper(requester=post_mock)
        passive = scraper.get_one('http://preproduccion-datos.infolobby.cl:80/resource/URI/Persona/01000000006B61E3BE8531376237CA91EA5D76962CE44CFB210C4289CF99155ADD7A118A')
        self.assertEquals(passive.name, 'Leonor Droguett Guerra')

    def test_gets_one_but_not_replicates(self):
        scraper = PassiveScrapper(requester=post_mock)
        scraper.get_one('http://preproduccion-datos.infolobby.cl:80/resource/URI/Persona/01000000006B61E3BE8531376237CA91EA5D76962CE44CFB210C4289CF99155ADD7A118A')
        scraper.get_one('http://preproduccion-datos.infolobby.cl:80/resource/URI/Persona/01000000006B61E3BE8531376237CA91EA5D76962CE44CFB210C4289CF99155ADD7A118A')

        leonores = Passive.objects.filter(name='Leonor Droguett Guerra')
        self.assertEquals(leonores.count(), 1)
