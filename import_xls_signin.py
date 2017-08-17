#!/usr/bin/env python

import xlrd
import pprint
from datetime import date, datetime, timedelta
from os.path import basename

from namecache import names

pp = pprint.PrettyPrinter(indent=2)
p = pp.pprint


DATE_FORMATS = [
    "%m/%d/%y",
    "%m/%d/%Y",
    "%m-%d-%y",
    "%m-%d-%Y",
    "%d %b %y",
    "%d %b %Y",
    "%m-%d",
    "%m/%d",
]


def is_numeric(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def parse_date(datestr):
    if isinstance(datestr, float):
        return datetime(*xlrd.xldate_as_tuple(datestr, 0)).date()
    for format in DATE_FORMATS:
        try:
            return datetime.strptime(datestr, format).date()
        except ValueError:
            continue
    raise ValueError("%s not matched" % datestr)


def td_to_hours(td):
    return td.days * 24 + td.seconds / 3600.


class Signin:
    def __init__(self, row, day1, day2, day3):
        self.first = None
        self.last = None
        self.card_num = None
        self.assignment = None
        self.day1_in = None
        self.day1_out = None
        self.day2_in = None
        self.day2_out = None
        self.day3_in = None
        self.day3_out = None
        self.hours = None
        self.miles = None
        self.errors = []
        self.namematch = None

        self.import_row(row, day1, day2, day3)
        self.validate()

    def import_row(self, row, day1, day2, day3):
        self.import_name(row)
        self.import_card_num(row)
        self.import_assignment(row)
        try:
            self.import_days(row, day1, day2, day3)
        except ValueError, msg:
            self.errors.append(str(msg))
        self.import_hours(row)
        self.import_miles(row)

    def import_name(self, row):
        name = row[1].value
        if ',' in name:
            self.last, self.first = name.split(", ", 1)
        elif ' ' in name:
            self.first, self.last = name.split(" ", 1)
            if ' ' in self.last:
                self.last, extra = self.last.split(" ", 1)
                self.first += " " + extra
        else:
            self.errors.append("could not split first/last name")

    def import_card_num(self, row):
        if row[2].value == '':
            self.card_num = ''
        else:
            self.card_num = "%d" % int(row[2].value)

    def import_assignment(self, row):
        self.assignment = row[3].value

    def import_days(self, row, day1, day2, day3):
        def make_datetime(date, time):
            try:
                if int(time) == 2400:
                    return datetime(date.year, date.month, date.day) + \
                           timedelta(days=1)
            except ValueError:
                return None
            return datetime(date.year, date.month, date.day,
                            int(time) / 100, int(time) % 100)

        if day1 is not None:
            self.day1_in  = make_datetime(day1, row[5].value)
            self.day1_out = make_datetime(day1, row[6].value)
        if day2 is not None:
            self.day2_in  = make_datetime(day2, row[8].value)
            self.day2_out = make_datetime(day2, row[9].value)
        if day3 is not None:
            self.day3_in  = make_datetime(day3, row[11].value)
            self.day3_out = make_datetime(day3, row[12].value)

    def import_hours(self, row):
        self.hours = row[14].value or None
        if self.hours == u" ":
            self.hours = self.hours.strip() or None        

    def import_miles(self, row):
        self.miles = row[15].value or None

    def match_name(self, force=False):
        if self.namematch is not None and not force:
            return self.namematch

        if self.first is None and self.last is None:
            return False

        first, last = self.first.title(), self.last.title()

        low_certainty = 0

        for name in names:
            # match last name
            if last == name[0].title():
                # match first name
                if first == name[1]:
                    self.namematch = name
                    return self.namematch
                # match DEM number
                elif is_numeric(self.card_num) and self.card_num == name[2]:
                    self.namematch = name
                    # match first part of first name
                    if ' ' in first and first.split()[0] != name[1]:
                        self.errors.append("check first name (%s)" % name[1])
                    return self.namematch
                # match first part of first name (leave out Jr/Sr/nickname)
                elif ' ' in first and first.split()[0] == name[1]:
                    self.namematch = name
                    low_certainty += 1
                # match only last name
                else:
                    self.namematch = name
                    low_certainty += 1
            # first name match
            elif first == name[1]:
                # match DEM number
                if is_numeric(self.card_num) and self.card_num == name[2]:
                    self.namematch = name
                    self.errors.append("check last name (%s)" % name[0])
                    return self.namematch
            # match last name to first name position
            elif (first, last) == (name[0], name[1]):
                self.namematch = name
                self.errors.append("first and last name swapped")
                return self.namematch
            # match first few characters of first name, possible nickname
            elif first == name[1][:len(self.first)]:
                # match DEM number
                if is_numeric(self.card_num) and self.card_num == name[2]:
                    self.namematch = name
                    self.errors.append("check name (%s)" % ' '.join(name))
                    return self.namematch

        if low_certainty >= 1:
            self.errors.append("low certainty on name match (%s)" % ' '.join(self.namematch))

        return self.namematch

    def sum_hours(self):
        try:
            day1_hours = self.day1_out - self.day1_in
        except TypeError:
            day1_hours = timedelta()

        try:
            day2_hours = self.day2_out - self.day2_in
        except TypeError:
            day2_hours = timedelta()

        try:
            day3_hours = self.day3_out - self.day3_in
        except TypeError:
            day3_hours = timedelta()

        return td_to_hours(day1_hours + day2_hours + day3_hours)

    def validate(self):
        self.validate_name()
        self.validate_card_num()

        if self.hours is None:
            self.errors.append("hours missing")
        elif self.sum_hours() != self.hours:
            self.errors.append("hours don't add up")

        return not bool(self.errors)

    def validate_card_num(self):
        if not self.card_num:
            if self.namematch and is_numeric(self.namematch[2]):
                self.errors.append("no DEM number (should be %s)" % self.namematch[2])
            # else:
            #     self.errors.append("no DEM number")

        elif self.match_name():
            if self.namematch[2] == self.card_num:
                return True
            else:
                self.errors.append("DEM number mismatch (should be %s)" % self.namematch[2])
                return False
        
        return False

    def validate_name(self):
        if self.match_name():
            return True

        self.errors.append("unrecognized name")
        return False

    def __repr__(self):
        return '%s(%s %s, %s)' % (
            self.__class__.__name__, self.first, self.last, self.card_num)


class Mission:
    def __init__(self, filename):
        self.county = None
        self.mission_number = None
        self.mission_name = None
        self.date_from = None
        self.date_to = None
        self.unit_name = None
        self.unit_address = None
        self.day1 = None
        self.day2 = None
        self.day3 = None
        self.signins = []
        self.total_personnel = None
        self.total_hours = None
        self.total_miles = None
        self.signed = None
        self.errors = []

        try:
            self.import_xls(filename)
        except:
            print filename
            raise

    def import_xls(self, filename):
        workbook = xlrd.open_workbook(filename=filename)
        firstsheet = True
        for sheet in workbook.sheets():
            row = sheet.row(11)
            try:
                if row[0].value != u"1.":
                    raise ValueError("Names do not start in normal cell B11")
            except IndexError:
                # ignore missing data from Sheets2 and 3. This is normal.
                if sheet.name not in ["Sheet2", "Sheet3"]:
                    raise
                continue # skip sheet

            if firstsheet:
                self.import_county(sheet)
                self.import_mission_number(sheet)
                self.import_mission_name(sheet)
                self.import_date_from(sheet)
                self.import_date_to(sheet)
                self.import_unit_name(sheet)
                self.import_unit_address(sheet)
                self.import_days(sheet)
                self.import_total_personnel(sheet)
                self.import_total_hours(sheet)
                self.import_total_miles(sheet)
                self.import_signed(sheet)
                firstsheet = False

            self.import_signins(sheet)

    def import_county(self, sheet):
        self.county = sheet.cell(3, 5).value or sheet.cell(3, 4).value or None
        if self.county is not None:
            self.county = self.county.title()

    def import_mission_number(self, sheet):
        self.mission_number = sheet.cell(3, 14).value or \
                              sheet.cell(3, 15).value or \
                              sheet.cell(3, 13).value or None

    def import_mission_name(self, sheet):
        self.mission_name = sheet.cell(4, 3).value or None

    def import_date_from(self, sheet):
        self.date_from = parse_date(sheet.cell(4, 9).value)

    def import_date_to(self, sheet):
        try:
            self.date_to = parse_date(sheet.cell(4, 14).value or \
                                      sheet.cell(4, 13).value)
        except ValueError:
            pass

    def import_unit_name(self, sheet):
        self.unit_name = sheet.cell(5, 2).value

    def import_unit_address(self, sheet):
        self.unit_address = sheet.cell(6, 2).value

    def import_days(self, sheet):
        try:
            self.day1 = parse_date(sheet.cell(8, 5).value or \
                                   sheet.cell(8, 6).value or \
                                   sheet.cell(7, 6).value)
            if self.day1.year == 1900:
                self.day1 = date(self.date_from.year,
                                 self.day1.month,
                                 self.day1.day)
        except ValueError:
            pass

        try:
            self.day2 = parse_date(sheet.cell(8, 8).value or \
                                   sheet.cell(8, 9).value or \
                                   sheet.cell(7, 9).value)
            if self.day2.year == 1900:
                self.day2 = date(self.date_from.year,
                                 self.day2.month,
                                 self.day2.day)
        except ValueError:
            pass

        try:
            self.day3 = parse_date(sheet.cell(8, 11).value or \
                                   sheet.cell(8, 12).value or \
                                   sheet.cell(7, 12).value)
            if self.day3.year == 1900:
                self.day3 = date(self.date_to.year,
                                 self.day3.month,
                                 self.day3.day)
        except ValueError:
            pass

    def import_total_personnel(self, sheet):
        self.total_personnel = sheet.cell(42, 2).value or \
                               sheet.cell(42, 3).value or \
                               sheet.cell(43, 2).value or None
        if self.total_personnel is not None:
            self.total_personnel = int(self.total_personnel)

    def import_total_hours(self, sheet):
        self.total_hours = sheet.cell(42, 8).value or \
                           sheet.cell(42, 9).value or \
                           sheet.cell(43, 8).value or None
        if self.total_hours is not None:
            self.total_hours = float(self.total_hours)
    
    def import_total_miles(self, sheet):
        self.total_miles = sheet.cell(42, 14).value or \
                           sheet.cell(42, 15).value or \
                           sheet.cell(43, 14).value or None
        if self.total_miles is not None:
            self.total_miles = int(self.total_miles)

    def import_signed(self, sheet):
        self.signed = sheet.cell(46, 1).value or \
                      sheet.cell(47, 1).value or None

    def import_signins(self, sheet):
        for rownum in xrange(11,42):
            row = sheet.row(rownum)
            if row[1].ctype != xlrd.XL_CELL_EMPTY:
                try:
                    signin = Signin(row,
                        self.day1 or self.date_from, self.day2, self.day3)
                except:
                    print row
                    raise
                self.signins.append(signin)
            elif row[6].value.startswith("*The time a person"):
                break

    def validate(self):
        if self.county is None:
            self.errors.append("No county.")

        if self.mission_number[2] != '-':
            self.errors.append("Mission number is wrong format: %s" % self.mission_number)

        if self.mission_name is None:
            self.errors.append("No mission name.")

        if self.date_from is None:
            self.errors.append("No date from.")

        if self.date_to is None:
            self.errors.append("No date to.")
        elif self.date_from > self.date_to:
            self.errors.append("Date from (%s) is greater than date to (%s)." % (
                self.date_from, self.date_to))

        if self.unit_name != "Washington Explorer Search And Rescue - Pierce County Unit":
            self.errors.append("Unexpected unit name: %s" % self.unit_name)

        if self.unit_address != "P.O. Box 11322, Tacoma, WA  98411-0322":
            self.errors.append("Unexpected unit address: %s" % self.unit_address)

        if self.day1 is None:
            # only care if search is longer than one day
            if self.date_from != self.date_to and self.date_to is not None:
                self.errors.append("Day 1 is empty.")
        elif self.day1 != self.date_from:
            self.errors.append("Day 1 (%s) must be the same as Date From (%s)." % (
                self.day1, self.date_from))

        # multi-day searches
        if self.day3 is not None:
            if self.day3 != self.date_to:
                self.errors.append("Day 3 (%s) doesn't match Date To (%s)." % (
                    self.day3, self.date_to))
        elif self.day2 is not None:
            if self.day2 != self.date_to:
                self.errors.append("Day 2 (%s) doesn't match Date To (%s) and Day 3 is blank." % (
                    self.day2, self.date_to))

        for signin in self.signins:
            if signin.errors:
                self.errors.append("%s %s: %s" % (
                    signin.first, signin.last, ', '.join(signin.errors)))

        if self.total_personnel is None:
            self.errors.append("Personnel count missing.")
        elif self.total_personnel != len(self.signins):
            self.errors.append("Personnel count doesn't add up (%d vs %d)." % (
                self.total_personnel, len(self.signins)))

        if self.total_hours is None:
            self.errors.append("Total hours is missing.")
        elif self.total_hours != sum([signin.sum_hours() for signin in self.signins]):
            self.errors.append("Total hours don't add up.")

        if self.total_miles is None:
            self.errors.append("Total miles is missing.")
        elif self.total_miles != sum([signin.miles or 0 for signin in self.signins]):
            self.errors.append("Total miles don't add up.")

        return not bool(self.errors)
      

def main():
    import sys

    passed, failed, total = 0, 0, 0

    filenames = sys.argv[1:]
    for filename in filenames:
        mission = Mission(filename)
        total += 1
        if mission.validate():
            passed += 1
            print basename(filename), "Passed Validation"
        else:
            failed += 1
            print basename(filename), "Failed Validation"
            for error in mission.errors:
                print " -", error
        print

    print "%d passed, %d failed, of %d total" % (passed, failed, total)


if __name__ == '__main__':
    main()