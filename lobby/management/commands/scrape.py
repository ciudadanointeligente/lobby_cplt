from django.core.management.base import BaseCommand
import requests
from django.conf import settings
from lobby.models import Passive, Active
from string import Template
import json
from popolo.models import Identifier


class PassiveScrapper():
    def get_one(self, id):
        query = Template(u'SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE { { <$id> ?property ?hasValue }  UNION { ?isValueOf ?property <$id> } } ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf')
        query_s = query.substitute(id=id)
        response = requests.post(settings.SPARQL_ENDPOING, data={'query': query_s, 'output': 'json'})
        response_json = json.loads(response.content)

        previous_passives = Passive.objects.filter(identifiers__identifier=id)
        if previous_passives:
            return None

        passive = Passive()
        for result in response_json['results']['bindings']:

            if result['property']['value'] == "http://xmlns.com/foaf/0.1/name":
                passive.name = result["hasValue"]["value"]
        passive.save()
        identifier = Identifier(identifier=id)
        passive.identifiers.add(identifier)
        print passive.name
        return passive


class Command(BaseCommand):
    def handle(self, *args, **options):
        response = requests.post(settings.SPARQL_ENDPOING, data={'query': settings.PASSIVES_QUERY, 'output': 'json'})
        response_json = json.loads(response.content)
        passive_scrapper = PassiveScrapper()
        for result in response_json['results']['bindings']:
            passive_scrapper.get_one(result['instance']['value'])


class ActiveScrapper():
    def get_one(self, id):
        query = Template(u'SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE { { <$id> ?property ?hasValue } UNION { ?isValueOf ?property <$id> }} ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf')
        query_s = query.substitute(id=id)
        response = requests.post(settings.SPARQL_ENDPOING, data={'query': query_s, 'output': 'json'})
        response_json = json.loads(response.content)

        active = Active()
        for result in response_json['results']['bindings']:

            if result['property']['value'] == "http://xmlns.com/foaf/0.1/name":
                active.name = result["hasValue"]["value"]
        active.save()

    def parse(self, response_json, id):

        previous_actives = Active.objects.filter(identifiers__identifier=id)
        if previous_actives:
            return None

        active = Active()

        for result in response_json['results']['bindings']:

            if result['property']['value'] == "http://xmlns.com/foaf/0.1/name":
                active.name = result["hasValue"]["value"]

            if result['property']['value'] == 'http://preproduccion-datos.infolobby.cl:80/resource/cplt/correpondeA':
                identifier_alt = Identifier(identifier=result["hasValue"]["value"])
        active.save()
        identifier = Identifier(identifier=id)
        active.identifiers.add(identifier)
        active.identifiers.add(identifier_alt)
