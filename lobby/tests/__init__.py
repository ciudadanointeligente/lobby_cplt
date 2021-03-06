import os
from django.http import HttpResponse
from django.conf import settings


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
        settings.PASSIVES_QUERY:
        read_fixture('passives.json'),
        u'SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE {  { <http://preproduccion-datos.infolobby.cl:80/resource/temp/AudienciaInicio/2204> ?property ?hasValue }  UNION  { ?isValueOf ?property <http://preproduccion-datos.infolobby.cl:80/resource/temp/AudienciaInicio/2204> }} ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf':
        read_fixture('audiencia_2204_inicia.json'),
        u'SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE {  { <http://preproduccion-datos.infolobby.cl:80/resource/URI/Institucion/AF001> ?property ?hasValue }  UNION  { ?isValueOf ?property <http://preproduccion-datos.infolobby.cl:80/resource/URI/Institucion/AF001> }} ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf':
        read_fixture('subsecretaria_general_de_la_republica.json'),
        settings.INSTITUCIONES_QUERY:
        read_fixture('instituciones.json'),
        u'SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE {  { <http://preproduccion-datos.infolobby.cl:80/resource/URI/Institucion/AM001> ?property ?hasValue }  UNION  { ?isValueOf ?property <http://preproduccion-datos.infolobby.cl:80/resource/URI/Institucion/AM001> }} ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf':
        read_fixture('subsecretaria_obras_publicas.json'),
        settings.ENTIDADES_QUERY:
        read_fixture('entidades.json'),
        u'SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE {{ <http://preproduccion-datos.infolobby.cl:80/resource/URI/Entidad/769818200> ?property ?hasValue } UNION {?isValueOf ?property <http://preproduccion-datos.infolobby.cl:80/resource/URI/Entidad/769818200> }} ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf':
        read_fixture('azerta.json'),
        u'SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE {{ <http://preproduccion-datos.infolobby.cl:80/resource/URI/Entidad/700026604> ?property ?hasValue } UNION {?isValueOf ?property <http://preproduccion-datos.infolobby.cl:80/resource/URI/Entidad/700026604> }} ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf':
        read_fixture('cpc.json'),
        settings.MEMBERSHIP_QUERY:
        read_fixture('memberships.json'),
        u'SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE {{ <http://preproduccion-datos.infolobby.cl:80/resource/temp/MembershipPasivo/40213> ?property ?hasValue } UNION { ?isValueOf ?property <http://preproduccion-datos.infolobby.cl:80/resource/temp/MembershipPasivo/40213> }} ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf':
        read_fixture('membership_40213.json'),
        u'SELECT DISTINCT ?property ?hasValue ?isValueOf WHERE {{ <http://preproduccion-datos.infolobby.cl:80/resource/temp/MembershipPasivo/40214> ?property ?hasValue } UNION { ?isValueOf ?property <http://preproduccion-datos.infolobby.cl:80/resource/temp/MembershipPasivo/40214> }} ORDER BY (!BOUND(?hasValue)) ?property ?hasValue ?isValueOf':
        read_fixture('membership_40214.json'),
        u'''SELECT ?instance ?registradoPor ?esDeTipo ?descripcion ?lugar ?observaciones ?inicia ?duracion ?materia

        WHERE { ?instance a cplt:RegistroAudiencia;

        cplt:registradoPor ?registradoPor;

        cplt:esDeTipo ?esDeTipo;

        cplt:descripcion ??descripcion;

        cplt:lugar ?lugar;

        cplt:observaciones ?observaciones;

        cplt:materia ?materia;

        cplt:inicia ?tiempoInicia.

        ?tiempoInicia time:hasBeginning ?inicia.

        ?instance cplt:duracion ?duracionI.

        ?duracionI time:minutes ?duracion.


        }
        ''':
        read_fixture('audiencias_2.json')
        }

    if data:
        if 'query' in data:
            return HttpResponse(responses_array[data["query"]])
