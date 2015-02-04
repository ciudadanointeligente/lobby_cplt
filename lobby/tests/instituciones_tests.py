# -*- coding: UTF-8 -*-
from django.test import TestCase
from popolo.models import Identifier, Organization
import json
from lobby.management.commands.scrape import InstitucionesScraper, Scraper
from lobby.tests import post_mock, read_fixture
from django.conf import settings


class InstitucionesScraperTestCase(TestCase):
    def test_parse_one(self):
        sgr_json = json.loads(read_fixture('subsecretaria_general_de_la_republica.json'))
        id = 'http://preproduccion-datos.infolobby.cl:80/resource/URI/Institucion/AF001'
        scraper = InstitucionesScraper(requester=post_mock)
        scraper.parse(sgr_json, id)
        institucion = Organization.objects.get(identifiers__identifier=id)
        self.assertEquals(institucion.name, u"SUBSECRETARÍA GENERAL DE LA PRESIDENCIA")

    def test_get_one(self):
        id = 'http://preproduccion-datos.infolobby.cl:80/resource/URI/Institucion/AF001'
        scraper = InstitucionesScraper(requester=post_mock)
        scraper.get_one(id)
        institucion = Organization.objects.get(identifiers__identifier=id)
        self.assertEquals(institucion.name, u"SUBSECRETARÍA GENERAL DE LA PRESIDENCIA")

    def test_get_all(self):
        response = post_mock(settings.SPARQL_ENDPOING, data={'query': settings.INSTITUCIONES_QUERY, 'output': 'json'})
        instituciones_scraper = Scraper(InstitucionesScraper, requester=post_mock)
        instituciones_scraper.parse(response.content)

        self.assertEquals(Organization.objects.count(), 2)
