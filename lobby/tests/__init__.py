import os
from django.http import HttpResponse


def read_fixture(fixture_name=''):
    script_dir = os.path.dirname(__file__)
    f = open(os.path.join(script_dir, 'fixtures/' + fixture_name), 'r')
    return f.read()


def post_mock(url, data=None, json=None, **kwargs):
    responses_array = {
        u'SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE { { <http://preproduccion-datos.infolobby.cl:80/resource/temp/RegistroAudiencia/2204> ?property ?hasValue } UNION { ?isValueOf ?property <http://preproduccion-datos.infolobby.cl:80/resource/temp/RegistroAudiencia/2204> } } ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf':
        read_fixture('audiencia_2204.json'),
        u'SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE {  { <http://preproduccion-datos.infolobby.cl:80/resource/temp/AudienciaMinutos/2204> ?property ?hasValue } UNION { ?isValueOf ?property <http://preproduccion-datos.infolobby.cl:80/resource/temp/AudienciaMinutos/2204> }} ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf':
        read_fixture('audienci_2204_minutes.json'),
        u"SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE { { <http://preproduccion-datos.infolobby.cl:80/resource/temp/Activo/3905> ?property ?hasValue } UNION { ?isValueOf ?property <http://preproduccion-datos.infolobby.cl:80/resource/temp/Activo/3905> }} ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf":
        read_fixture('alejandro.json'),
        u'SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE { { <http://preproduccion-datos.infolobby.cl:80/resource/URI/Persona/01000000006B61E3BE8531376237CA91EA5D76962CE44CFB210C4289CF99155ADD7A118A> ?property ?hasValue }  UNION { ?isValueOf ?property <http://preproduccion-datos.infolobby.cl:80/resource/URI/Persona/01000000006B61E3BE8531376237CA91EA5D76962CE44CFB210C4289CF99155ADD7A118A> } } ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf':
        read_fixture('leonor.json'),
        u'SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE { { <http://preproduccion-datos.infolobby.cl:80/resource/URI/Pasivo/01000000E31C39D004051B319923430929BF486C807689D6527AF079ABF9CCC3346867C99FA310BA17B2573DB988A4B811F299618A98C6A57C22BC327A009EC766D54292016380CCB9A89F39> ?property ?hasValue }  UNION { ?isValueOf ?property <http://preproduccion-datos.infolobby.cl:80/resource/URI/Pasivo/01000000E31C39D004051B319923430929BF486C807689D6527AF079ABF9CCC3346867C99FA310BA17B2573DB988A4B811F299618A98C6A57C22BC327A009EC766D54292016380CCB9A89F39> } } ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf':
        read_fixture('tatiana.json'),
        u'SELECT oassuves':
        read_fixture('passives.json'),
        u'SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE {  { <http://preproduccion-datos.infolobby.cl:80/resource/temp/AudienciaInicio/2204> ?property ?hasValue }  UNION  { ?isValueOf ?property <http://preproduccion-datos.infolobby.cl:80/resource/temp/AudienciaInicio/2204> }} ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf':
        read_fixture('audiencia_2204_inicia.json')
        }

    if data:
        if 'query' in data:
            return HttpResponse(responses_array[data["query"]])
