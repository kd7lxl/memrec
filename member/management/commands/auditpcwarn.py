from django.core.management.base import BaseCommand
from member.models import Person

import codecs, csv


def allbutlast(iterable):
    it = iter(iterable)
    current = it.next()
    for i in it:
        yield current
        current = i


class Command(BaseCommand):
    args = '<filename>'
    help = 'Checks an Everbridge-format CSV against memrec database.'

    def handle(self, *args, **options):
        member_cache = {}
        for member in Person.objects.all():
            member_cache[(member.first_name.lower(), member.last_name.lower())] = member
        pcwarn_contacts = self.parse_csv(args[0])
        for contact in pcwarn_contacts:
            name = contact['First Name'].lower(), contact['Last Name'].lower()
            
            if name not in member_cache:
                print name, 'not found.'
            elif member_cache[name].drop_date:
                print name, 'dropped.'
            else:
                print name, 'ok.', member_cache[name].last_reup

    def parse_csv(self, filename):
        with codecs.open(filename, 'rb', encoding='utf-8-sig') as csvfile:
            everbridgereader = csv.reader(csvfile)
            header = next(everbridgereader)
            return map(lambda row: dict(zip(header, row)), everbridgereader)
