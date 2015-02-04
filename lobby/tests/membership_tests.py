from django.test import TestCase
from popolo.models import Organization, Identifier
from lobby.models import Entidad, Passive
from lobby.tests import read_fixture, post_mock
from lobby.management.commands.scrape import MembershipScraper, Scraper
import json
from django.conf import settings


class EntidadScraperTestCase(TestCase):
    def setUp(self):
        self.passive = Passive.objects.create(name=u'leonor')
        i = Identifier(identifier='http://preproduccion-datos.infolobby.cl:80/resource/URI/Pasivo/0100000035FBA8A3489DC55B38F2412000ECD823B7B037613D60FA221702F4025EF216475E4450578C83800A796A265767CF60B10C5D1C0A3D55C867E588683B758B4B6C684FD3391E2B0601')
        self.passive.identifiers.add(i)

        self.organization = Organization.objects.create(name=u'organization')
        i2 = Identifier(identifier='http://preproduccion-datos.infolobby.cl:80/resource/URI/Institucion/AF001')
        self.organization.identifiers.add(i2)

    def test_parse(self):
        m_40213 = json.loads(read_fixture('membership_40213.json'))
        scraper = MembershipScraper(requester=post_mock)

        scraper.parse(m_40213)

        self.assertTrue(self.passive.memberships.all())
        self.assertEqual(self.passive.memberships.count(), 1)
        self.assertEqual(self.passive.memberships.all()[0].organization, self.organization)
