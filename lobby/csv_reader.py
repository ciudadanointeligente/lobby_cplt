from lobby.models import Active, Audiencia
from popolo.models import Identifier
import uuid
import unicodedata
from datetime import datetime


class ActivosCSVReader():
    def parse_line(self, line):
        active = Active()
        active.name = unicode(line[3] + " " + line[4])
        active.save()
        seed = line[3] + line[4] + line[5] + line[7]
        i = Identifier(identifier=line[0])
        active.identifiers.add(i)


class AudienciasCSVReader():
    def __init__(self, *args, **kwargs):
        self.records = {

        }

    def parse_audiencia_line(self, line):
        audiencia = Audiencia()
        audiencia.observations = line[9].decode('utf-8').strip()
        audiencia.length = int(line[7])
        date = datetime.strptime(line[6], '%Y-%m-%d %H:%M:%S')
        audiencia.date = date

        self.records[line[0]] = audiencia

    def parse_several_lines(self, lines):
        lines.pop(0)
        for line in lines:
            self.parse_audiencia_line(line)
