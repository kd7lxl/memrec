from django.core.management.base import BaseCommand
from import_xls_signin import Mission
from member.models import Person
from mission import models
from os.path import basename


class Command(BaseCommand):
    args = '<filename filename ...>'
    help = 'Imports the specified xls file into the mission database'

    def handle(self, *args, **options):
        passed, failed, total = 0, 0, 0

        for filename in args:
            mission = Mission(filename)
            total += 1
            if mission.validate():
                passed += 1
                print basename(filename), "Passed Validation"
                new_mission = models.Mission(
                    mission_number=mission.mission_number,
                    mission_type='mission',
                    category=models.MissionCategory.objects.get(pk=1),
                    mission_name=mission.mission_name,
                    county=mission.county,
                    date_start=mission.date_from,
                    date_end=mission.date_to,
                    day1=mission.day1 or mission.date_from,
                    day2=mission.day2,
                    day3=mission.day3,
                    total_personnel=mission.total_personnel,
                    total_hours=mission.total_hours,
                    total_miles=mission.total_miles,
                    signed=mission.signed,
                )
                new_mission.save()
                for signin in mission.signins:
                    try:
                        person = Person.objects.get(pk=signin.namematch[3])
                    except Person.DoesNotExist:
                        new_mission.delete()
                        print signin.namematch
                        raise
                    new_signin = models.Signin(
                        mission=new_mission,
                        person=person,
                        assignment=signin.assignment,
                        time1_in=signin.day1_in,
                        time1_out=signin.day1_out,
                        time2_in=signin.day2_in,
                        time2_out=signin.day2_out,
                        time3_in=signin.day3_in,
                        time3_out=signin.day3_out,
                        hours=signin.hours,
                        miles_driven=signin.miles,
                    )
                    try:
                        new_signin.save()
                    except:
                        new_mission.delete()
                        print signin
                        raise
            else:
                failed += 1
                print basename(filename), "Failed Validation"
                for error in mission.errors:
                    print " -", error
            print

        print "%d passed, %d failed, of %d total" % (passed, failed, total)
