from lobby.models import Audiencia
import uuid
import unicodedata
from popolo.models import Identifier


class AudienciasScraper2():
    def get_one(self, response_json):
        observaciones = response_json['observaciones']['value']
        fecha = response_json['inicia']['value']
        seed = observaciones + fecha
        normalized_seed = unicodedata.normalize('NFKD', seed).encode('ascii', 'ignore')
        generated_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, normalized_seed)
        audiencia = Audiencia()
        audiencia.observaciones = observaciones
        audiencia.length = int(response_json['duracion']['value'])
        audiencia.save()
        i = Identifier(identifier=generated_uuid)
        audiencia.add(i)
