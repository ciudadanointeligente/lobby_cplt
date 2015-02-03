from django.core.management.base import BaseCommand
import requests
from django.conf import settings
from lobby.models import Passive, Active
from string import Template
import json
from popolo.models import Identifier


class PersonScrapperMixin():
    def get_one(self, id):
        query = Template(self.query)
        query_s = query.substitute(id=id)
        response = requests.post(settings.SPARQL_ENDPOING, data={'query': query_s, 'output': 'json'})
        response_json = json.loads(response.content)

        return self.parse(response_json, id)

    def parse(self, response_json, id):

        previous_persons = self.model.objects.filter(identifiers__identifier=id)
        if previous_persons:
            return None

        person = self.model()

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
        person.identifiers.add(identifier_alt)
        print person
        return person


class PassiveScrapper(PersonScrapperMixin):
    model = Passive
    query = u'SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE { { <$id> ?property ?hasValue }  UNION { ?isValueOf ?property <$id> } } ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf'


class ActiveScrapper(PersonScrapperMixin):
    model = Active
    query = u'SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE { { <$id> ?property ?hasValue } UNION { ?isValueOf ?property <$id> }} ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf'


class Command(BaseCommand):
    def handle(self, *args, **options):
        response = requests.post(settings.SPARQL_ENDPOING, data={'query': settings.PASSIVES_QUERY, 'output': 'json'})
        response_json = json.loads(response.content)
        passive_scrapper = PassiveScrapper()
        for result in response_json['results']['bindings']:
            passive_scrapper.get_one(result['instance']['value'])

        response = requests.post(settings.SPARQL_ENDPOING, data={'query': settings.ACTIVES_QUERY, 'output': 'json'})
        response_json = json.loads(response.content)
        active_scraper = ActiveScrapper()
        for result in response_json['results']['bindings']:
            active_scraper.get_one(result['instance']['value'])
