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

        self.assertIn("2", csv_reader.records)
        audiencia = csv_reader.records['2']
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
        self.assertIn("2", csv_reader.records)
        self.assertIn("1", csv_reader.records)
        self.assertEquals(len(csv_reader.records), 2)

        self.assertIsInstance(csv_reader.records['1'], Audiencia)
        self.assertIsInstance(csv_reader.records['2'], Audiencia)
