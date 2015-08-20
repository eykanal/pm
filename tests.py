from django.test import TestCase

from datetime import date
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from pm.models import Program, Project, Group, People, Worker, Task, TaskWorker, TaskDependency
from pm.forms import ProjectForm, TaskForm


class PmTestCase(TestCase):
    def setUp(self):
        prg = {}
        pr = {}
        pe = {}
        gr = {}
        t = {}
        w = {}

        User.objects.create_superuser("admin", "admin@example.com", "admin")
        self.client.login(username='admin', password='admin')

        prg['none'] = Program.objects.get(name="None")

        gr['maad'] = Group.objects.create(name="MAAD", internal=True)
        gr['oar'] = Group.objects.create(name="OAR", internal=True)
        gr['ods'] = Group.objects.create(name="ODS", internal=True)

        n = User.objects.create_user("lid0001", first_name="Anthony", last_name="Garuccio")
        People.objects.create(name=n, group=gr['maad'])
        n = User.objects.create_user("lid0002", first_name="Tom", last_name="Keane")
        pe['tom'] = People.objects.create(name=n, group=gr['maad'])
        n = User.objects.create_user("lid0003", first_name="Steve", last_name="Lettieri")
        People.objects.create(name=n, group=gr['maad'])
        n = User.objects.create_user("lid0004", first_name="Adam", last_name="Miller")
        People.objects.create(name=n, group=gr['maad'])
        n = User.objects.create_user("lid0005", first_name="Jeff", last_name="Narus")
        pe['jeff'] = People.objects.create(name=n, group=gr['maad'])
        n = User.objects.create_user("lid0006", first_name="Glenn", last_name="Thompson")
        pe['glenn'] = People.objects.create(name=n, group=gr['maad'])
        n = User.objects.create_user("lid0007", first_name="Elli", last_name="Kanal")
        pe['elli'] = People.objects.create(name=n, group=gr['maad'])
        n = User.objects.create_user("lid0008", first_name="Gene", last_name="May")
        People.objects.create(name=n, group=gr['maad'])
        n = User.objects.create_user("lid0009", first_name="Ben", last_name="Conrad")
        People.objects.create(name=n, group=gr['oar'])
        n = User.objects.create_user("lid0010", first_name="Holly", last_name="Dolan")
        People.objects.create(name=n, group=gr['oar'])
        n = User.objects.create_user("lid0011", first_name="Judy", last_name="Cullum")
        People.objects.create(name=n, group=gr['oar'])
        n = User.objects.create_user("lid0012", first_name="Violeta", last_name="Valenzuela")
        People.objects.create(name=n, group=gr['oar'])
        n = User.objects.create_user("lid0013", first_name="Nick", last_name="Shope")
        People.objects.create(name=n, group=gr['oar'])
        n = User.objects.create_user("lid0014", first_name="Ted", last_name="Houtz")
        People.objects.create(name=n, group=gr['oar'])
        n = User.objects.create_user("lid0015", first_name="Joe", last_name="Roots")
        People.objects.create(name=n, group=gr['oar'])
        n = User.objects.create_user("lid0016", first_name="Jason", last_name="Liggett")
        People.objects.create(name=n, group=gr['oar'])
        n = User.objects.create_user("lid0017", first_name="Dave", last_name="Mishizen")
        People.objects.create(name=n, group=gr['oar'])
        n = User.objects.create_user("lid0018", first_name="Sharon", last_name="Kilvington")
        People.objects.create(name=n, group=gr['oar'])
        n = User.objects.create_user("lid0019", first_name="Scott", last_name="Kinross")
        People.objects.create(name=n, group=gr['ods'])
        n = User.objects.create_user("lid0020", first_name="Charlie", last_name="Kannair")
        People.objects.create(name=n, group=gr['ods'])
        n = User.objects.create_user("lid0021", first_name="Matt", last_name="Hall")
        People.objects.create(name=n, group=gr['maad'])
        n = User.objects.create_user("lid0022", first_name="Todd", last_name="Blouch")
        People.objects.create(name=n, group=gr['oar'])
        n = User.objects.create_user("lid0023", first_name="Bill", last_name="Irvin")
        People.objects.create(name=n, group=gr['oar'])

        gr['s'] = Group.objects.create(name="Service")
        gr['cc'] = Group.objects.create(name="Command Center")

        n = User.objects.create_user("michael_hall", first_name="Michael", last_name="Hall")
        pe['mike'] = People.objects.create(name=n, group=gr['s'])
        n = User.objects.create_user("melissa_lowery", first_name="Melissa", last_name="Lowery")
        pe['melissa'] = People.objects.create(name=n, group=gr['cc'])

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

        w['psr_tom'] = Worker.objects.create(project=pr['psr'], person=pe['tom'])
        w['pg_jeff'] = Worker.objects.create(project=pr['pg'], person=pe['jeff'])
        w['pg_glenn'] = Worker.objects.create(project=pr['pg'], person=pe['glenn'])
        w['qa_glenn'] = Worker.objects.create(project=pr['qa'], person=pe['glenn'])

        TaskWorker.objects.create(task=t[1], worker=w['psr_tom'])
        TaskWorker.objects.create(task=t[2], worker=w['pg_jeff'])
        TaskWorker.objects.create(task=t[3], worker=w['pg_jeff'])
        TaskWorker.objects.create(task=t[3], worker=w['pg_glenn'])
        TaskWorker.objects.create(task=t[4], worker=w['pg_glenn'])
        TaskWorker.objects.create(task=t[5], worker=w['pg_glenn'])

        TaskDependency.objects.create(blocking_task=t[0], blocked_task=t[1])

    def test_index(self):
        response = self.client.get(reverse('pm:index'))
        self.assertEqual(response.status_code, 200)

    def test_project_page(self):
        response = self.client.get(reverse('pm:project-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_people_page(self):
        response = self.client.get(reverse('pm:person-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_new_project_form(self):
        # test full submit
        data1 = {
            'name': 'test',
            'requester': People.objects.values_list('pk', flat=True).get(name__username='melissa_lowery'),
            'project_manager': People.objects.values_list('pk', flat=True).get(name__username='lid0007'),  # Kanal
            'description': 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.',
            'start_date': date.today(),
            'due_date': date.today(),
            'date_complete': date.today(),
            'sharepoint_ticket': 'http://www.example.com/',
            'priority': Project.STANDARD,
            'status': Project.ACTIVE,
            'program': Program.objects.values_list('pk', flat=True).get(name="None"),
            'workers': tuple(People.objects.values_list('pk', flat=True).filter(Q(name__username="lid0004") | Q(name__username="lid0008"))),
        }
        p1 = ProjectForm(data1)
        self.assertTrue(p1.is_valid())

        # test only required fields
        data2 = {
            'name': 'test',
            'requester': People.objects.values_list('pk', flat=True).get(name__username='melissa_lowery'),
            'project_manager': People.objects.values_list('pk', flat=True).get(name__username='lid0007'),  # Kanal
            'description': 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.',
            'start_date': date.today(),
            'priority': Project.STANDARD,
            'status': Project.ACTIVE,
            'program': Program.objects.values_list('pk', flat=True).get(name="None"),
            'workers': tuple(People.objects.values_list('pk', flat=True).filter(Q(name__username="lid0004") | Q(name__username="lid0008"))),
        }
        p2 = ProjectForm(data2)
        self.assertTrue(p2.is_valid())

    def test_new_task_form(self):
        # test full submit
        data1 = {
            'project': Project.objects.values_list('pk', flat=True).get(pk=1),
            'name': 'test',
            'description': 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.',
            'start_date': date.today(),
            'due_date': date.today(),
            'date_complete': date.today(),
            'status': Task.ACTIVE,
            'worker': (2,),  # Tom's ID, still not sure how it wants me to pass it in
        }
        t1 = TaskForm(data1, project_id=1)
        self.assertTrue(t1.is_valid())

        # test only required fields
        data2 = {
            'project': Project.objects.values_list('pk', flat=True).get(pk=1),
            'name': 'test',
            'start_date': date.today(),
            'status': Task.ACTIVE,
            'worker': (2,),  # Tom's ID, same as above
        }
        t2 = TaskForm(data2, project_id=1)
        self.assertTrue(t2.is_valid())