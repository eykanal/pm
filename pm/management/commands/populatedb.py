from datetime import date
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from pm.models import Program, Project, Group, People, Worker, Task, TaskWorker, TaskDependency


class Command(BaseCommand):
    args = ''
    help = 'Populates data in the fresh database'

    def handle(self, *args, **options):
        n = []
        prg = {}
        pr = {}
        pe = {}
        gr = {}
        t = {}
        w = {}
        
        n = User.objects.create_superuser("admin", "admin@example.com", "admin")

        self.stdout.write("Added admin user")

        prg['none'] = Program.objects.create(name="None", description="Default program for projects.")

        self.stdout.write("Added default project")

        gr['maad'] = Group.objects.create(name="MAAD")
        gr['oar'] = Group.objects.create(name="OAR")
        gr['ods'] = Group.objects.create(name="ODS")

        self.stdout.write("Added ods groups")

        n = User.objects.create_user("anthony_garuccio", first_name="Anthony", last_name="Garuccio")
        People.objects.create(name=n, group=gr['maad'])
        n = User.objects.create_user("tom_keane", first_name="Tom", last_name="Keane")
        pe['tom'] = People.objects.create(name=n, group=gr['maad'])
        n = User.objects.create_user("steve_lettieri", first_name="Steve", last_name="Lettieri")
        People.objects.create(name=n, group=gr['maad'])
        n = User.objects.create_user("adam_miller", first_name="Adam", last_name="Miller")
        People.objects.create(name=n, group=gr['maad'])
        n = User.objects.create_user("jeff_narus", first_name="Jeff", last_name="Narus")
        pe['jeff'] = People.objects.create(name=n, group=gr['maad'])
        n = User.objects.create_user("matt_hall", first_name="Matt", last_name="Hall")
        People.objects.create(name=n, group=gr['maad'])
        n = User.objects.create_user("glenn_thompson", first_name="Glenn", last_name="Thompson")
        pe['glenn'] = People.objects.create(name=n, group=gr['maad'])
        n = User.objects.create_user("gene_may", first_name="Gene", last_name="May")
        People.objects.create(name=n, group=gr['maad'])
        n = User.objects.create_user("elli_kanal", first_name="Elli", last_name="Kanal")
        pe['elli'] = People.objects.create(name=n, group=gr['maad'])
        n = User.objects.create_user("ben_conrad", first_name="Ben", last_name="Conrad")
        People.objects.create(name=n, group=gr['oar'])
        n = User.objects.create_user("holly_dolan", first_name="Holly", last_name="Dolan")
        People.objects.create(name=n, group=gr['oar'])
        n = User.objects.create_user("judy_cullum", first_name="Judy", last_name="Cullum")
        People.objects.create(name=n, group=gr['oar'])
        n = User.objects.create_user("violeta_valenzuela", first_name="Violeta", last_name="Valenzuela")
        People.objects.create(name=n, group=gr['oar'])
        n = User.objects.create_user("nick_shope", first_name="Nick", last_name="Shope")
        People.objects.create(name=n, group=gr['oar'])
        n = User.objects.create_user("ted_houtz", first_name="Ted", last_name="Houtz")
        People.objects.create(name=n, group=gr['oar'])
        n = User.objects.create_user("todd_blouch", first_name="Todd", last_name="Blouch")
        People.objects.create(name=n, group=gr['oar'])
        n = User.objects.create_user("joe_roots", first_name="Joe", last_name="Roots")
        People.objects.create(name=n, group=gr['oar'])
        n = User.objects.create_user("jason_liggett", first_name="Jason", last_name="Liggett")
        People.objects.create(name=n, group=gr['oar'])
        n = User.objects.create_user("bill_irvin", first_name="Bill", last_name="Irvin")
        People.objects.create(name=n, group=gr['oar'])
        n = User.objects.create_user("dave_mishizen", first_name="Dave", last_name="Mishizen")
        People.objects.create(name=n, group=gr['oar'])
        n = User.objects.create_user("sharon_kilvington", first_name="Sharon", last_name="Kilvington")
        People.objects.create(name=n, group=gr['oar'])
        n = User.objects.create_user("scott_kinross", first_name="Scott", last_name="Kinross")
        People.objects.create(name=n, group=gr['ods'])
        n = User.objects.create_user("charlie_kannair", first_name="Charlie", last_name="Kannair")
        People.objects.create(name=n, group=gr['ods'])
        self.stdout.write("Added ods users")

        gr['s'] = Group.objects.create(name="Service")
        gr['cc'] = Group.objects.create(name="Command Center")
        self.stdout.write("Created additional groups")

        n = User.objects.create_user("michael_hall", first_name="Michael", last_name="Hall")
        pe['mike'] = People.objects.create(name=n, group=gr['s'])
        n = User.objects.create_user("melissa_lowery", first_name="Melissa", last_name="Lowery")
        pe['melissa'] = People.objects.create(name=n, group=gr['cc'])
        self.stdout.write("Created additional people")

        prg['cc'] = Program.objects.create(name="Command Center optimization", description="Improve processes and reporting in the command center.")
        prg['qa'] = Program.objects.create(name="QA overhaul", description="Update everything associated with QA.")

        pr['psr'] = Project.objects.create(
            name="Provider survey reporting",
            requester=pe['mike'],
            project_manager=pe['elli'],
            description="Set up reporting on IVR provider surveys. Gain access to IVR database, connect to CSR data, provide reporting.",
            start_date=date(2015, 2, 24),
            program=prg['none'],
        )
        pr['pg'] = Project.objects.create(
            name="PG dashboard",
            requester=pe['melissa'],
            project_manager=pe['elli'],
            description="Create a dashboard containing all PG metrics. Should show both month-to-date and for arbitrary historical date ranges. Also should contain detail reporting and executive summaries.",
            start_date=date(2014, 7, 1),
            program=prg['cc'],
        )
        pr['qa'] = Project.objects.create(
            name="QA inventory management",
            requester=pe['elli'],
            project_manager=pe['elli'],
            description="Centralize inventory management for the QA units",
            start_date=date(2015, 1, 19),
            program=prg['qa'],
        )

        self.stdout.write("Created projects")

        t[0] = Task.objects.create(
            project=pr['psr'],
            name="Create IVR survey table views",
            description="Create views of the IVR tables for reporting by ODS. This contains just IVR data, not agent data.",
            due_date=date(2015, 3, 10)
        )
        t[1] = Task.objects.create(
            project=pr['psr'],
            name="Connect IVR views to Avaya log tables",
            description="Connect the survey data containing customer survey responses to the Avaya log tables containing CSR login IDs.",
            start_date=date(2015, 3, 11),
            due_date=date(2015, 3, 18),
        )
        t[2] = Task.objects.create(
            project=pr['pg'],
            name="Add Enrollment PGs to dashboard",
            due_date=date(2015, 3, 31)
        )
        t[3] = Task.objects.create(
            project=pr['pg'],
            name="Add Claims Overpayment to dashboard",
            due_date=date(2015, 3, 31)
        )
        t[4] = Task.objects.create(
            project=pr['qa'],
            name="Create full query repository",
            due_date=date(2015, 3, 31)
        )
        t[5] = Task.objects.create(
            project=pr['qa'],
            name="Create dashboard demo",
            due_date=date(2015, 3, 31)
        )
        self.stdout.write("Created tasks")

        w['psr_tom'] = Worker.objects.create(project=pr['psr'], person=pe['tom'])
        w['pg_jeff'] = Worker.objects.create(project=pr['pg'], person=pe['jeff'])
        w['pg_glenn'] = Worker.objects.create(project=pr['pg'], person=pe['glenn'])
        w['qa_glenn'] = Worker.objects.create(project=pr['qa'], person=pe['glenn'])
        self.stdout.write("Created workers")

        TaskWorker.objects.create(task=t[1], worker=w['psr_tom'])
        TaskWorker.objects.create(task=t[2], worker=w['pg_jeff'])
        TaskWorker.objects.create(task=t[3], worker=w['pg_jeff'])
        TaskWorker.objects.create(task=t[3], worker=w['pg_glenn'])
        TaskWorker.objects.create(task=t[4], worker=w['pg_glenn'])
        TaskWorker.objects.create(task=t[5], worker=w['pg_glenn'])
        self.stdout.write("Created dummy taskworker")

        TaskDependency.objects.create(blocking_task=t[0], blocked_task=t[1])
        self.stdout.write("Created dummy taskdepencency")
