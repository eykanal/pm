from datetime import date

from django.core.management.base import BaseCommand, CommandError
from pm.models import Program, Project, Group, People, Worker, Task, TaskWorker, TaskDependency


class Command(BaseCommand):
    args = ''
    help = 'Populates data in the fresh database'

    def handle(self, *args, **options):
        prg = {}
        pr = {}
        pe = {}
        gr = {}
        t = {}
        w = {}
        
        prg['none'] = Program.objects.create(name="None", description="Default program for projects.")

        self.stdout.write("Added default project")

        gr['maad'] = Group.objects.create(name="MAAD")
        gr['oar'] = Group.objects.create(name="OAR")
        gr['ods'] = Group.objects.create(name="ODS")

        self.stdout.write("Added ods groups")

        People.objects.create(name="Anthony Garuccio", group=gr['maad'])
        pe['tom'] = People.objects.create(name="Tom Keane", group=gr['maad'])
        People.objects.create(name="Steve Lettieri", group=gr['maad'])
        People.objects.create(name="Adam Miller", group=gr['maad'])
        pe['jeff'] = People.objects.create(name="Jeff Narus", group=gr['maad'])
        People.objects.create(name="Matt Hall", group=gr['maad'])
        pe['glenn'] = People.objects.create(name="Glenn Thompson", group=gr['maad'])
        People.objects.create(name="Gene May", group=gr['maad'])
        pe['elli'] = People.objects.create(name="Elli Kanal", group=gr['maad'])
        People.objects.create(name="Ben Conrad", group=gr['oar'])
        People.objects.create(name="Holly Dolan", group=gr['oar'])
        People.objects.create(name="Judy Cullum", group=gr['oar'])
        People.objects.create(name="Violeta Valenzuela", group=gr['oar'])
        People.objects.create(name="Nick Shope", group=gr['oar'])
        People.objects.create(name="Ted Houtz", group=gr['oar'])
        People.objects.create(name="Todd Blouch", group=gr['oar'])
        People.objects.create(name="Joe Roots", group=gr['oar'])
        People.objects.create(name="Jason Liggett", group=gr['oar'])
        People.objects.create(name="Bill Irvin", group=gr['oar'])
        People.objects.create(name="Dave Mishizen", group=gr['oar'])
        People.objects.create(name="Sharon Kilvington", group=gr['oar'])
        People.objects.create(name="Scott Kinross", group=gr['ods'])
        People.objects.create(name="Charlie Kannair", group=gr['ods'])
        self.stdout.write("Added ods users")

        gr['s'] = Group.objects.create(name="Service")
        gr['cc'] = Group.objects.create(name="Command Center")
        self.stdout.write("Created additional groups")

        pe['mike'] = People.objects.create(name="Michael Hall", group=gr['s'])
        pe['melissa'] = People.objects.create(name="Melissa Lowery", group=gr['cc'])
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
