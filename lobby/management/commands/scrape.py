from django.core.management.base import BaseCommand
import requests
from django.conf import settings
from lobby.models import Passive, Active, Audiencia
from string import Template
import json
from popolo.models import Identifier


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

        return self.parse(response_json, id)

    def parse(self, response_json, id):
        previous_persons = self.model.objects.filter(identifiers__identifier=id)
        if previous_persons:
            return None

        person = self.model()
        identifier_alt = None
        for result in response_json['results']['bindings']:

            if result['property']['value'] == "http://xmlns.com/foaf/0.1/name":
                person.name = result["hasValue"]["value"]

            if result['property']['value'] == 'http://preproduccion-datos.infolobby.cl:80/resource/cplt/correpondeA':
                if 'hasValue' in result:
                    identifier_alt = Identifier(identifier=result["hasValue"]["value"])
                if 'isValueOf' in result:
                    identifier_alt = Identifier(identifier=result["isValueOf"]["value"])
        person.save()
        identifier = Identifier(identifier=id)
        person.identifiers.add(identifier)
        if identifier_alt:
            person.identifiers.add(identifier_alt)
        else:
            print person, id
        return person


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


class AudienciasScraper(PersonScrapperMixin):
    query = 'SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE { { <$id> ?property ?hasValue } UNION { ?isValueOf ?property <$id> } } ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf'

    def parse(self, response_json, id):
        all_audiencias = Audiencia.objects.filter(identifiers__identifier=id)
        if all_audiencias:
            return
        audiencia = Audiencia()
        active = []
        for result in response_json['results']['bindings']:
            if result['property']['value'] == 'http://preproduccion-datos.infolobby.cl:80/resource/cplt/descripcion':
                audiencia.description = result['hasValue']['value']

            if result['property']['value'] == 'http://preproduccion-datos.infolobby.cl:80/resource/cplt/observaciones':
                audiencia.observations = result['hasValue']['value']

            if result['property']['value'] == 'http://preproduccion-datos.infolobby.cl:80/resource/cplt/participa':
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
        response = requests.post(settings.SPARQL_ENDPOING, data={'query': settings.PASSIVES_QUERY, 'output': 'json'})
        passives_scrarper = Scraper(PassiveScrapper)
        passives_scrarper.parse(response.content)

        response = requests.post(settings.SPARQL_ENDPOING, data={'query': settings.ACTIVES_QUERY, 'output': 'json'})
        actives_scraper = Scraper(ActiveScrapper)
        actives_scraper.parse(response.content)

        response = requests.post(settings.SPARQL_ENDPOING, data={'query': settings.AUDIENCIAS_QUERY, 'output': 'json'})
        audiencias_scraper = Scraper(AudienciasScraper)
        audiencias_scraper.parse(response.content)
