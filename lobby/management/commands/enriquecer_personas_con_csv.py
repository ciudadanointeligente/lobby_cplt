from django.core.management.base import BaseCommand
from lobby.models import Passive, Active, Entidad
import csv
from lobby.csv_reader import AudienciasCSVReader
from popolo.models import Identifier
import unicodedata


class Command(BaseCommand):
    def get_count(self, klass, name):
        elements = klass.objects.filter(name__icontains=name)
        return elements

    def get_errors_in_line(self, lines, klass):
        pass

    def parse_persons(self, *args):
        passives_csv_reader = open(args[1], 'rb')
        actives_csv_reader = open(args[2], 'rb')

        lines_for_passives_loader = csv.reader(passives_csv_reader, delimiter=';')
        lines_for_actives_loader = csv.reader(actives_csv_reader, delimiter=';')
        passives_lines = []
        actives_lines = []
        for line in lines_for_passives_loader:
            passives_lines.append(line)

        for line in lines_for_actives_loader:
            actives_lines.append(line)

        klass = Passive
        lines = passives_lines
        things_again, problems = self.get_things_from_lines_and_klasses(klass, lines, "passive_")

        print "=========================Problemas con pasivos========================="
        print len(problems)
        for pro in problems:
            print pro['name'], pro['count']

        klass = Active
        lines = actives_lines
        things_again, problems = self.get_things_from_lines_and_klasses(klass, lines, "active_")
        print "=========================Problemas con activos========================="
        print len(problems)
        for pro in problems:
            print pro['name'], pro['count']

    def parse_audiencias(self, *args):
        au_csv_reader = open(args[1], 'rb')
        lines_for_au_loader = csv.reader(au_csv_reader, delimiter=';')
        au_lines = []
        for line in lines_for_au_loader:
            au_lines.append(line)
        reader = AudienciasCSVReader()
        au_lines.pop(0)
        for line in au_lines:
            try:
                reader.parse_audiencia_line(line)
            except Exception, e:
                print line, e

        asistencia_pasivo_csv_reader = open(args[2], 'rb')
        lines_for_asistencia_pasivo_loader = csv.reader(asistencia_pasivo_csv_reader, delimiter=';')
        asis_pas_lines = []
        for line in lines_for_asistencia_pasivo_loader:
            asis_pas_lines.append(line)
        print '===pasivos=='
        for line in asis_pas_lines:
            try:
                audiencia = reader.audiencia_records[line[0]]
                q = Passive.objects.filter(identifiers__identifier='passive_' + line[1])
                if q:
                    audiencia.passive = q[0]
                else:
                    print audiencia.observations, line[0]
            except Exception, e:
                print "Error en los datos de audiencias con el IDAudienciaReunion " + line[0]
                pass
            audiencia.save()
        print '===activos=='
        asistencia_activo_csv_reader = open(args[3], 'rb')
        lines_for_asistencia_activo_loader = csv.reader(asistencia_activo_csv_reader, delimiter=';')
        asis_act_lines = []
        for line in lines_for_asistencia_activo_loader:
            asis_act_lines.append(line)
        asis_act_lines.pop(0)
        counter = 0
        for line in asis_act_lines:
            counter += 1
            try:
                audiencia = reader.audiencia_records[line[2]]
                q = Active.objects.filter(identifiers__identifier='active_' + line[1])
                if q:
                    if q.count() == 1:
                        activo = q[0]
                    else:
                        print "Error en los datos con ", q, "que tienen el id Activo igual", line[1]
                else:
                    if not line[1].strip():
                        es = Entidad.objects.filter(identifiers__identifier="entidad_"+line[0].strip())
                        if not es:
                            q = Active.objects.filter(identifiers__identifier='active_' + line[0])
                            if not q:
                                print line
                    else:
                        print "Error en los datos de AsistenciaActivos.cs con", line[1].strip(), "en la linea", counter + 1, line, q
            except Exception, e:
                print "Error en los datos de audiencias con el IDAudienciaReunion " + line[2], e


    def handle(self, *args, **options):

        if args[0] == 'persons':
            self.parse_persons(*args)
        if args[0] == 'audiencias':
            self.parse_audiencias(*args)
        if args[0] == 'entidades':
            self.parse_entidades(*args)

    def parse_entidades(self, *args):
        entidades = {}
        entidades_csv_reader = open(args[1], 'rb')

        lines_for_entidades_loader = csv.reader(entidades_csv_reader, delimiter=',')
        entidades_lines = []
        for line in lines_for_entidades_loader:
            entidades_lines.append(line)

        for line in entidades_lines:
            entidad = Entidad()
            entidad.rut = line[1].decode('utf-8').strip()
            entidad.name = line[3].decode('utf-8').strip()
            try:
                if line[14] == "True":
                    entidad.remunerado = True
                if line[14] == "False":
                    entidad.remunerado = False
            except:
                pass

            entidad.giro = line[5].decode('utf-8').strip()
            slug = unicodedata.normalize('NFKD', entidad.name).encode('ascii', 'ignore').lower().replace(" ", "")
            id = "entidad_" + line[0]
            if slug in entidades:
                if id not in entidades[slug]['ids']:
                    entidades[slug]['ids'].append(id)
            else:
                entidades[slug] = {
                    'entidad': entidad,
                    'ids': [id]
                }

        for slug in entidades:
            e = entidades[slug]
            e['entidad'].save()
            for iden in e['ids']:
                i = Identifier(identifier=iden)
                e['entidad'].identifiers.add(i)

    def get_things_from_lines_and_klasses(self, klass, lines, pre_):
        things = []
        problems = []
        for line in lines:
            original_name = name = line[3].decode('utf-8').strip() + u" " + line[4].decode('utf-8').strip()
            ps = self.get_count(klass, name)
            if ps.count() > 1:
                problems.append({
                    'name': name,
                    'count': ps.count()
                    })
            if not ps:
                name2 = line[3].decode('utf-8').strip() + u"  " + line[4].decode('utf-8').strip()
                ps = self.get_count(klass, name2)
                if not ps:
                    apellidos = line[4].decode('utf-8').strip().split(" ")
                    if len(apellidos) == 2:
                        apellidos_ = apellidos[0] + " " + apellidos[1]
                        name3 = line[3].decode('utf-8').strip() + u"  " + apellidos_
                        ps = self.get_count(klass, name3)
                        if not ps:
                            nombres = line[3].decode('utf-8').strip().split(" ")
                            name4 = nombres[0] + u"  " + apellidos_
                            ps = self.get_count(klass, name4)
                            if not ps:
                                instance = klass.objects.create(name=original_name)
                                i = Identifier(identifier=pre_ + line[0])
                                instance.identifiers.add(i)
                                continue
            if ps.count() == 1:
                i = Identifier(identifier=pre_ + line[0])
                q = ps[0].identifiers.filter(identifier=i.identifier)
                if not q:
                    ps[0].identifiers.add(i)
                else:
                    if q.count() > 1:
                        print q.count()
                        q.exclude(id=q[0].id).delete()
                things.append(ps[0])
        return things, problems
