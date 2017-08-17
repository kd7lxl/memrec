from django.core.management.base import BaseCommand
from django.db.models import Q
from member.models import Person

import datetime, xlrd


def iterable_map(functions, values):
    function_it, value_it = iter(functions), iter(values)
    while function_it and value_it:
        yield next(function_it)(next(value_it))


def get_date(val):
    return datetime.datetime(*xlrd.xldate_as_tuple(val, 0)).date()


class Command(BaseCommand):
    args = '<filename>'
    help = 'Adds DEM numbers from an Excel spreadsheet to Members.'

    def handle(self, *args, **options):
        filename = args[0]
        workbook = xlrd.open_workbook(filename=filename)
        sheet = workbook.sheet_by_name('Sheet1')
        for rownum in range(1, sheet.nrows, 2):
            if not any(sheet.row_values(rownum)):
                print "Done."
                break
            try:
                record = Record(*sheet.row_values(rownum))
                person = record.get_person()
                person.dem_exp = record.dem_exp
                print person, person.dem_exp
                person.save()
            except Person.DoesNotExist:
                continue
                self.stderr.write("%s %s %s NOT FOUND" % (
                    record.first_name, record.last_name, record.dem_number))
                try:
                    self.stderr.write("SIMILAR: %s" % (
                        Person.objects.get(dem_number=record.dem_number)))
                except:
                    pass



class Record:
    def __init__(self, dem_number, name, active, unknown, dem_exp, work_phone):
        self.dem_number = str(int(dem_number))
        self.last_name, first_name = name.split(', ', 1)
        self.first_name, middle_name = first_name.split(' ', 1)
        self.middle_initial = middle_name and middle_name[0]
        self.active = bool(active)
        self.dem_exp = get_date(dem_exp)
        self.work_phone = work_phone

    def __repr__(self):
        return 'Record(%s, %s, %s)' % (
            self.last_name, self.first_name, self.dem_number)

    def get_person(self):
        return Person.objects.get(dem_exp=None, dem_number=self.dem_number)
        return Person.objects.get(
            Q(first_name=self.first_name) | Q(first_nick=self.first_name),
            Q(last_name=self.last_name) | Q(last_nick=self.last_name),
            dem_number=self.dem_number,
        )
