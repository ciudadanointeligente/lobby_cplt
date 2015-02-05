# -*- coding: utf-8 -*-
from django.test import TestCase
from lobby.models import Active, Audiencia
from lobby.csv_reader import ActivosCSVReader, AudienciasCSVReader
import uuid
import unicodedata


class CSVActivosReader(TestCase):
    def setUp(self):
        self.cabeceras = ["IDActivo", "Nombre_Institucion", "IDORPortal_Institucion", "Nombre_Activo", "Apellidos_Activo",
            "DocumentoPais_Activo", "CodigoNacionalidad_Activo", "FechaInicio_Activo", "FechaTermino_Activo", "Remunerado"]
        self.line = ['1243', 'SUBSECRETARIA DEL DEPORTE', 'BA001', 'Arturo', 'Barrios', 'CHL', 'CHL', '2014-12-04', '', 'False']
        self.line2 = ["1244", "SUBSECRETARIA DEL DEPORTE", "BA001", "Manuel", "Neira", "CHL", "CHL", "2014-12-04", "", "False"]
        self.all_lines = [self.cabeceras, self.line, self.line2]

    def atest_instanciate_and_parse_line(self):
        csv_reader = ActivosCSVReader()
        csv_reader.parse_line(self.line)

        the_seed = 'ArturoBarriosCHL2014-12-04'
        seed = unicodedata.normalize('NFKD', the_seed).encode('ascii', 'ignore')
        generated_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, seed)

        active = Active.objects.get(identifiers__identifier=generated_uuid)
        self.assertTrue(active)
        self.assertEquals(active.name, u'Arturo Barrios')


class CSVAudienciaReader(TestCase):
    def setUp(self):
        self.cabeceras = ["IDAudienciaReunion", "Cut", "Nombre_Institucion",
        "IDORPortal_Institucion", "Nombre_Comuna", "Nombre_TiposForma", "FechaInicio_Audiencia",
        "DuracionMinuto_Audiencia", "Lugar_Audiencia", "ObservacionesMateria_Audiencia",
        "Descripcion_Materia"]
        self.line1 = ["1", "13101", "CARABINEROS DE CHILE",
        "AD009", "Santiago", "Presencial",
        "2014-12-16 00:00:00", "30",
        "Avenida Libertador Bernardo O´Higgins 1196, Piso 9",
        "Se dieron a conocer los servicios de seguridad TI, vinculación de enlaces, Zimperium, soporte tecnológico, protección de ataques.",
        "Celebración, modificación o terminación a cualquier título, de contratos que realicen los sujetos pasivos y que sean necesarios para su funcionamiento."]
        self.line2 = ["2", "13101", "CARABINEROS DE CHILE", "AD009", "Santiago", "Presencial", "2014-12-29 00:00:00", "30",
        "Avenida Libertador Bernardo O´Higgins 1196, Piso 9", "Se expusieron los productos textiles y de confección",
        "Celebración, modificación o terminación a cualquier título, de contratos que realicen los sujetos pasivos y que sean necesarios para su funcionamiento."]
        self.all_lines = [self.cabeceras, self.line1, self.line2]

    def test_read_one_line(self):
        csv_reader = AudienciasCSVReader()
        csv_reader.parse_audiencia_line(self.line2)

        self.assertIn("2", csv_reader.audiencia_records)
        audiencia = csv_reader.audiencia_records['2']
        self.assertEquals(audiencia.observations,
             u"Se expusieron los productos textiles y de confección")
        self.assertIsNone(audiencia.id)
        self.assertEquals(audiencia.length, 30)
        self.assertEquals(audiencia.date.year, 2014)
        self.assertEquals(audiencia.date.month, 12)
        self.assertEquals(audiencia.date.day, 29)

    def test_get_several(self):
        csv_reader = AudienciasCSVReader()
        csv_reader.parse_several_lines(self.all_lines)
        self.assertIn("2", csv_reader.audiencia_records)
        self.assertIn("1", csv_reader.audiencia_records)
        self.assertEquals(len(csv_reader.audiencia_records), 2)

        self.assertIsInstance(csv_reader.audiencia_records['1'], Audiencia)
        self.assertIsInstance(csv_reader.audiencia_records['2'], Audiencia)

from lobby.models import Passive


class PersonsReaderCsV(TestCase):
    def setUp(self):
        self.cabeceras = ["IDPasivo", "Nombre_Institucion", "CategoriaCargo_Nombre", "Nombre_Pasivo", "Apellidos_Pasivo", "CodigoNacionalidadIso_Pasivo", "DocumentoPaisIso_Pasivo", "FechaInicio_Pasivo", "FechaTermino_Pasivo", "LinkAudienciaReunion_Pasivo", "LinkViajes_Pasivo", "LinkDonativos_Pasivo", "CargoFuncion_Pasivo", "IDORPortal_Institucion"]
        self.line1 = ["34602", "SUBSECRETARÍA DE RELACIONES EXTERIORES", "Embajador ", "James Sidney", "Sinclair Manley", "CHL", "CHL", "2014-11-27", "", "https://www.leylobby.gob.cl/instituciones/124/cargos-pasivos/745/audiencias", "https://www.leylobby.gob.cl/instituciones/124/cargos-pasivos/745/viajes", "https://www.leylobby.gob.cl/instituciones/124/cargos-pasivos/745/donativos", "Embajador de Chile en Singapur", "AC001"]
        self.line2 = ["34623", "EJÉRCITO DE CHILE", "Encargado de adquisiciones en las Fuerzas Armadas y de Orden y Seguridad Pública", "GUIDO ENZO", "MONTINI GÓMEZ", "CHL", "CHL", "2014-11-25", "", "https://www.leylobby.gob.cl/instituciones/130/cargos-pasivos/425/audiencias", "https://www.leylobby.gob.cl/instituciones/130/cargos-pasivos/425/viajes", "https://www.leylobby.gob.cl/instituciones/130/cargos-pasivos/425/donativos", "Comandante de Industria Militar e Ingeniería", "AD006"]
        self.all_lines = [self.cabeceras, self.line1, self.line2]
        self.passive1 = Passive.objects.create(name=u"James Sidney Sinclair Manley")
        self.passive2 = Passive.objects.create(name=u"GUIDO ENZO MONTINI GÓMEZ")

    def test_persons_reader(self):
        csv_reader = AudienciasCSVReader()
        csv_reader.parse_one_passive_lines(self.line1)

        p1 = Passive.objects.get(identifiers__identifier='passive_34602')

        self.assertEquals(p1, self.passive1)

    def test_persons_readers(self):
        csv_reader = AudienciasCSVReader()
        csv_reader.parse_several_passives_lines(self.all_lines)

        p1 = Passive.objects.get(identifiers__identifier='passive_34602')
        p2 = Passive.objects.get(identifiers__identifier="passive_34623")

        self.assertEquals(p1, self.passive1)
        self.assertEquals(p2, self.passive2)

    def test_get_parse_activos(self):
        cabeceras = ["IDActivo", "Nombre_Institucion", "IDORPortal_Institucion", "Nombre_Activo", "Apellidos_Activo", "DocumentoPais_Activo", "CodigoNacionalidad_Activo", "", "FechaInicio_Activo", "FechaTermino_Activo", "Remunerado"]
        line1 = ["1243", "SUBSECRETARIA DEL DEPORTE", "BA001", "Arturo", "Barrios", "CHL", "CHL", "2014-12-04", "", "False"]
        line2 = ["1244", "SUBSECRETARIA DEL DEPORTE", "BA001", "Manuel", "Neira", "CHL", "CHL", "2014-12-04", "", "False"]
        all_lines = [cabeceras, line1, line2]

        a1 = Active.objects.create(name=u"Arturo Barrios")
        csv_reader = AudienciasCSVReader()
        csv_reader.parse_one_active_lines(line1)
        self.assertEquals(a1, Active.objects.get(identifiers__identifier='active_1243'))