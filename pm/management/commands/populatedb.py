from datetime import date

from django.core.management.base import BaseCommand, CommandError
from pm.models import Program, Project, Group, People, Worker, Task, TaskWorker, TaskDependency


class Command(BaseCommand):
    args = '<create_dummy_data>'
    help = 'Populates data in the fresh database'

    def handle(self, *args, **options):
        prg_none = Program.objects.create(name="None", description="Default program for projects.")

        self.stdout.write("Added default project")

        maad = Group.objects.create(name="MAAD")
        oar = Group.objects.create(name="OAR")
        ods = Group.objects.create(name="ODS")

        self.stdout.write("Added ODS groups")

        People.objects.create(name="Anthony Garuccio", group=maad)
        peo_tom = People.objects.create(name="Tom Keane", group=maad)
        People.objects.create(name="Steve Lettieri", group=maad)
        People.objects.create(name="Adam Miller", group=maad)
        People.objects.create(name="Jeff Narus", group=maad)
        People.objects.create(name="Matt Hall", group=maad)
        People.objects.create(name="Glenn Thompson", group=maad)
        People.objects.create(name="Gene May", group=maad)
        peo_ell = People.objects.create(name="Elli Kanal", group=maad)
        People.objects.create(name="Ben Conrad", group=oar)
        People.objects.create(name="Holly Dolan", group=oar)
        People.objects.create(name="Judy Cullum", group=oar)
        People.objects.create(name="Violeta Valenzuela", group=oar)
        People.objects.create(name="Nick Shope", group=oar)
        People.objects.create(name="Ted Houtz", group=oar)
        People.objects.create(name="Todd Blouch", group=oar)
        People.objects.create(name="Joe Roots", group=oar)
        People.objects.create(name="Jason Liggett", group=oar)
        People.objects.create(name="Bill Irvin", group=oar)
        People.objects.create(name="Dave Mishizen", group=oar)
        People.objects.create(name="Sharon Kilvington", group=oar)
        People.objects.create(name="Scott Kinross", group=ods)
        People.objects.create(name="Charlie Kannair", group=ods)

        self.stdout.write("Added ODS users")

        if len(args) > 0:
            s = Group.objects.create(name="Service")
            self.stdout.write("Created service group")

            pe = People.objects.create(name="Michael Hall", group=s)
            self.stdout.write("Created service group person")

            pr = Project.objects.create(
                name="Provider survey reporting",
                requester=pe,
                project_manager=peo_ell,
                description="Set up reporting on IVR provider surveys. Gain access to IVR database, connect to CSR data, provide reporting.",
                start_date=date(2015, 2, 24),
                program=prg_none
            )
            self.stdout.write("Created dummy project")

            t1 = Task.objects.create(
                project=pr,
                name="Create IVR survey table views",
                description="Create views of the IVR tables for reporting by ODS. This contains just IVR data, not agent data.",
                due_date=datetime.date(2015,3,10)
            )
            t2 = Task.objects.create(
                project=pr,
                name="Connect IVR views to Avaya log tables",
                description="Connect the survey data containing customer survey responses to the Avaya log tables containing CSR login IDs.",
                start_date=date(2015, 3, 11),
                due_date=date(2015, 3, 18),
            )
            self.stdout.write("Created dummy tasks")

            w = Worker.objects.create(project=pr, person=peo_tom)
            self.stdout.write("Created dummy worker")

            TaskWorker.objects.create(task=t2, worker=w)
            self.stdout.write("Created dummy taskworker")

            TaskDependency.objects.create(blocking_task=t1, blocked_task=t2)
            self.stdout.write("Created dummy taskdepencency")
