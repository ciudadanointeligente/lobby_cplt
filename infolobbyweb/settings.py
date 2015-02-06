"""
Django settings for infolobbyweb project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'tmv$_uhmtxxg*uch=bo$xffww2-f^6r^t9mg(i+cd4d8ct9$0('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ## Testing
    'django_nose',
    ## Popolo things
    'popolo',
    ## Own Applications
    'lobby',
    'taggit'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'infolobbyweb.urls'

WSGI_APPLICATION = 'infolobbyweb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'


INFOLOBBY_BASE_URL = 'http://preproduccion-datos.infolobby.cl:80'

try:
    from local_settings import * # noqa
except ImportError:
    pass

# Project specific
SPARQL_ENDPOING = '{base_url}/sparql'.format(base_url=INFOLOBBY_BASE_URL)
PASSIVES_QUERY = u'''
PREFIX db: <{base_url}/resource/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX org: <http://www.w3.org/ns/org#>
PREFIX bcngeo: <http://datos.bcn.cl/ontologies/bcn-geographics#>
PREFIX gn: <http://www.geonames.org/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX time: <http://www.w3.org/2006/time#>
PREFIX d2r: <http://sites.wiwiss.fu-berlin.de/suhl/bizer/d2r-server/config.rdf#>
PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX map: <{base_url}/resource/#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX cplt: <{base_url}/resource/cplt/>
SELECT DISTINCT * WHERE {{ ?instancia a foaf:Person;
cplt:correpondeA ?instance; org:hasMember ?p }} '''.format(base_url=INFOLOBBY_BASE_URL)
ACTIVES_QUERY = u'''
PREFIX db: <{base_url}/resource/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX org: <http://www.w3.org/ns/org#>
PREFIX bcngeo: <http://datos.bcn.cl/ontologies/bcn-geographics#>
PREFIX gn: <http://www.geonames.org/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX time: <http://www.w3.org/2006/time#>
PREFIX d2r: <http://sites.wiwiss.fu-berlin.de/suhl/bizer/d2r-server/config.rdf#>
PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX map: <{base_url}/resource/#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX cplt: <{base_url}/resource/cplt/>
SELECT DISTINCT ?nombreActivo ?instance ?ReunionregistradaPor ?ReunionesDeTipo ?descripcion ?lugar ?observaciones ?materia WHERE {{

?s a cplt:Activo;

foaf:name ?nombreActivo;

cplt:correpondeA ?instance;

cplt:participa ?reunion.

?reunion cplt:registradoPor ?ReunionregistradaPor;

cplt:esDeTipo ?ReunionesDeTipo;

cplt:descripcion ?descripcion;

cplt:lugar ?lugar;

cplt:observaciones ?observaciones;

cplt:materia ?materia;

}}'''.format(base_url=INFOLOBBY_BASE_URL)

AUDIENCIAS_QUERY = '''
PREFIX db: <{base_url}/resource/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX org: <http://www.w3.org/ns/org#>
PREFIX bcngeo: <http://datos.bcn.cl/ontologies/bcn-geographics#>
PREFIX gn: <http://www.geonames.org/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX time: <http://www.w3.org/2006/time#>
PREFIX d2r: <http://sites.wiwiss.fu-berlin.de/suhl/bizer/d2r-server/config.rdf#>
PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX map: <{base_url}/resource/#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX cplt: <{base_url}/resource/cplt/>
SELECT DISTINCT ?instance WHERE {{ ?instance a <{base_url}/resource/cplt/RegistroAudiencia> }} ORDER BY ?instance'''.format(base_url=INFOLOBBY_BASE_URL)

INSTITUCIONES_QUERY = '''
PREFIX db: <{base_url}/resource/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX org: <http://www.w3.org/ns/org#>
PREFIX bcngeo: <http://datos.bcn.cl/ontologies/bcn-geographics#>
PREFIX gn: <http://www.geonames.org/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX time: <http://www.w3.org/2006/time#>
PREFIX d2r: <http://sites.wiwiss.fu-berlin.de/suhl/bizer/d2r-server/config.rdf#>
PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX map: <{base_url}/resource/#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX cplt: <{base_url}/resource/cplt/>
SELECT DISTINCT ?instance WHERE {{ ?instance a <{base_url}/resource/cplt/Institucion> }} ORDER BY ?instance'''.format(base_url=INFOLOBBY_BASE_URL)

ENTIDADES_QUERY = '''
PREFIX db: <{base_url}/resource/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX org: <http://www.w3.org/ns/org#>
PREFIX bcngeo: <http://datos.bcn.cl/ontologies/bcn-geographics#>
PREFIX gn: <http://www.geonames.org/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX time: <http://www.w3.org/2006/time#>
PREFIX d2r: <http://sites.wiwiss.fu-berlin.de/suhl/bizer/d2r-server/config.rdf#>
PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX map: <{base_url}/resource/#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX cplt: <{base_url}/resource/cplt/>
SELECT DISTINCT ?instance
WHERE {{ ?instance a <{base_url}/resource/cplt/Entidad> }}
ORDER BY ?instance
'''.format(base_url=INFOLOBBY_BASE_URL)

MEMBERSHIP_QUERY = '''
PREFIX db: <{base_url}/resource/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX org: <http://www.w3.org/ns/org#>
PREFIX bcngeo: <http://datos.bcn.cl/ontologies/bcn-geographics#>
PREFIX gn: <http://www.geonames.org/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX time: <http://www.w3.org/2006/time#>
PREFIX d2r: <http://sites.wiwiss.fu-berlin.de/suhl/bizer/d2r-server/config.rdf#>
PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX map: <{base_url}/resource/#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX cplt: <{base_url}/resource/cplt/>
SELECT DISTINCT ?instance WHERE {{ ?instance a <http://www.w3.org/ns/org#Membership> }} ORDER BY ?instance
'''.format(base_url=INFOLOBBY_BASE_URL)
