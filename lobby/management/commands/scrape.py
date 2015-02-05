from django.core.management.base import BaseCommand
import requests
from django.conf import settings
from lobby.models import Passive, Active, Audiencia, Entidad
from string import Template
import json
from popolo.models import Identifier, Organization
from datetime import datetime


class RequesterMixin():
    def __init__(self, requester=requests.post, *args, **kwargs):
        self.requester = requester


class PersonScrapperMixin(RequesterMixin):
    def get_one(self, id):
        query = Template(self.query)
        query_s = query.substitute(id=id)
        response = self.requester(settings.SPARQL_ENDPOING, data={'query': query_s, 'output': 'json'})
        try:
            response_json = json.loads(response.content)
        except ValueError:
            return

        return self.post_processor(self.parse(response_json, id))

    def post_processor(self, response):
        return response

    def extra_processor(self, result, instance):
        return instance

    def parse(self, response_json, id):
        previous_persons = self.model.objects.filter(identifiers__identifier=id)
        if previous_persons:
            return None

        person = self.model()
        for result in response_json['results']['bindings']:
            person = self.extra_processor(result, person)

            if result['property']['value'] == "http://xmlns.com/foaf/0.1/name":
                person.name = result["hasValue"]["value"]
        person.save()
        identifier = Identifier(identifier=id)
        person.identifiers.add(identifier)
        return person


class InstitucionesScraper(PersonScrapperMixin):
    model = Organization
    query = 'SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE {  { <$id> ?property ?hasValue }  UNION  { ?isValueOf ?property <$id> }} ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf'


class EntidadScraper(PersonScrapperMixin):
    model = Entidad
    query = 'SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE {{ <$id> ?property ?hasValue } UNION {?isValueOf ?property <$id> }} ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf'

    def extra_processor(self, result, entidad):
        if result['property']['value'].endswith('resource/cplt/rut'):
            entidad.rut = result["hasValue"]["value"]
        return entidad


class MembershipScraper(PersonScrapperMixin):
    query = 'SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE {{ <$id> ?property ?hasValue } UNION { ?isValueOf ?property <$id> }} ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf'

    def parse(self, response_json, id=None):
        person = None
        organization = None
        for result in response_json['results']['bindings']:
            if result['property']['value'] == "http://www.w3.org/ns/org#member":
                person = Passive.objects.get(identifiers__identifier=result["hasValue"]["value"])
            if result['property']['value'] == "http://www.w3.org/ns/org#organization":
                organization = Organization.objects.get(identifiers__identifier=result["hasValue"]["value"])
        person.add_membership(organization)


class PassiveScrapper(PersonScrapperMixin):
    model = Passive
    query = u'SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE { { <$id> ?property ?hasValue }  UNION { ?isValueOf ?property <$id> } } ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf'


class ActiveScrapper(PersonScrapperMixin):
    model = Active
    query = u'SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE { { <$id> ?property ?hasValue } UNION { ?isValueOf ?property <$id> }} ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf'


class Scraper(RequesterMixin):
    def __init__(self, scraper, requester=requests.post, *args, **kwargs):
        self.scraper = scraper
        self.requester = requester

    def parse(self, content):
        response_json = json.loads(content)
        scraper = self.scraper(requester=self.requester)
        for result in response_json['results']['bindings']:
            scraper.get_one(result['instance']['value'])


class SingleValueScraperMixin(RequesterMixin, PersonScrapperMixin):
    def parse(self, response_json, id=None):
        for result in response_json['results']['bindings']:
            if result['property']['value'] == self.property_value:
                return result['hasValue']['value']


class MinutesScraper(SingleValueScraperMixin):
    query = u'SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE {  { <$id> ?property ?hasValue } UNION { ?isValueOf ?property <$id> }} ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf'
    property_value = 'http://www.w3.org/2006/time#minutes'

    def post_processor(self, response):
        return int(response)


class IniciaScraper(SingleValueScraperMixin):
    query = u'SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE {  { <$id> ?property ?hasValue }  UNION  { ?isValueOf ?property <$id> }} ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf'
    property_value = 'http://www.w3.org/2006/time#hasBeginning'

    def post_processor(self, response):
        date = datetime.strptime(response, '%Y-%m-%dT%H:%M:%S')
        return date


class AudienciasScraper(PersonScrapperMixin):
    query = 'SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE { { <$id> ?property ?hasValue } UNION { ?isValueOf ?property <$id> } } ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf'

    def parse(self, response_json, id):
        all_audiencias = Audiencia.objects.filter(identifiers__identifier=id)
        if all_audiencias:
            return
        audiencia = Audiencia()
        active = []
        for result in response_json['results']['bindings']:
            if result['property']['value'].endswith('resource/cplt/descripcion'):
                audiencia.description = result['hasValue']['value']

            if result['property']['value'].endswith('resource/cplt/observaciones'):
                audiencia.observations = result['hasValue']['value']

            if result['property']['value'].endswith("resource/cplt/duracion"):
                minutes_scraper = MinutesScraper(requester=self.requester)
                audiencia.length = minutes_scraper.get_one(result['hasValue']['value'])

            if result['property']['value'].endswith("resource/cplt/registradoPor"):
                organization = Organization.objects.get(identifiers__identifier=result['hasValue']['value'])
                audiencia.registering_organization = organization

            if result['property']['value'].endswith("resource/cplt/inicia"):
                date_scraper = IniciaScraper(requester=self.requester)
                audiencia.date = date_scraper.get_one(result['hasValue']['value'])

            if result['property']['value'].endswith('resource/cplt/participa'):
                person = result['isValueOf']['value']
                try:
                    audiencia.passive = Passive.objects.get(identifiers__identifier=person)
                except Passive.DoesNotExist:
                    active.append(Active.objects.get(identifiers__identifier=person))

        audiencia.save()
        for a in active:
            audiencia.actives.add(a)

        identifier = Identifier(identifier=id)
        audiencia.identifiers.add(identifier)


class Command(BaseCommand):
    def handle(self, *args, **options):
        # response = requests.post(settings.SPARQL_ENDPOING, data={'query': settings.PASSIVES_QUERY, 'output': 'json'})
        # passives_scrarper = Scraper(PassiveScrapper)
        # passives_scrarper.parse(response.content)

        response = requests.post(settings.SPARQL_ENDPOING, data={'query': settings.ACTIVES_QUERY, 'output': 'json'})
        actives_scraper = Scraper(ActiveScrapper)
        actives_scraper.parse(response.content)

        # response = requests.post(settings.SPARQL_ENDPOING, data={'query': settings.INSTITUCIONES_QUERY, 'output': 'json'})
        # instituciones_scraper = Scraper(InstitucionesScraper)
        # instituciones_scraper.parse(response.content)

        # response = requests.post(settings.SPARQL_ENDPOING, data={'query': settings.ENTIDADES_QUERY, 'output': 'json'})
        # entidades_scrapper = Scraper(EntidadScraper)
        # entidades_scrapper.parse(response.content)

        # response = requests.post(settings.SPARQL_ENDPOING, data={'query': settings.AUDIENCIAS_QUERY, 'output': 'json'})
        # audiencias_scraper = Scraper(AudienciasScraper)
        # audiencias_scraper.parse(response.content)

        # response = requests.post(settings.SPARQL_ENDPOING, data={'query': settings.MEMBERSHIP_QUERY, 'output': 'json'})
        # memberships_scraper = Scraper(MembershipScraper)
        # memberships_scraper.parse(response.content)
