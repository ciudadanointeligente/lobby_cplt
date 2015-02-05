from lobby.models import Active, Audiencia, Passive
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
        self.audiencia_records = {

        }

    def parse_audiencia_line(self, line):
        audiencia = Audiencia()
        audiencia.observations = line[9].decode('utf-8').strip()
        audiencia.length = int(line[7])
        date = datetime.strptime(line[6], '%Y-%m-%d %H:%M:%S')
        audiencia.date = date

        self.audiencia_records[line[0]] = audiencia

    def parse_several_lines(self, lines):
        lines.pop(0)
        for line in lines:
            self.parse_audiencia_line(line)

    def parse_several_passives_lines(self, line):
        name = line[3].decode('utf-8').strip() + u" " + line[4].decode('utf-8').strip()
        p = Passive.objects.get(name=name)
        i = Identifier(identifier=u"passive_" + line[0].decode('utf-8').strip())
        p.identifiers.add(i)