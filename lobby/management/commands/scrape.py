from django.core.management.base import BaseCommand
import requests
from django.conf import settings
from lobby.models import Passive
from string import Template
import json


class PassiveScrapper():
    def get_one(self, id):
        query = Template(u'SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE { { <$id> ?property ?hasValue }  UNION { ?isValueOf ?property <$id> } } ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf')
        query_s = query.substitute(id=id)
        response = requests.post(settings.SPARQL_ENDPOING, data={'query': query_s, 'output': 'json'})
        response_json = json.loads(response.content)
        passive = Passive()
        for result in response_json['results']['bindings']:
            if result['property']['value'] == "http://xmlns.com/foaf/0.1/name":
                passive.name = result["hasValue"]["value"]
        return passive


class Command(BaseCommand):
    def handle(self, *args, **options):
        response = requests.post(settings.SPARQL_ENDPOING, data={'query': settings.PASSIVES_QUERY, 'output': 'json'})
