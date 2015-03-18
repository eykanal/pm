=====
ProjManager
=====

ProjManager is a project management application for management of projects for small groups. It allows users to define groups and users, as well as projects and tasks. The dashboard view allows for a quick birds-eye view of all current projects, while detail pages for both projects and people show more specifics about each project and person, respectively.

Quick start
-----

1. Add 'pm' ot your INSTALLED_APPS settings like this::

    INSTALLED_APPS = (
        ...
        'pm',
    )

2. Include the pm URLconf in your project urls.py like this::

	url(r'^pm/', include('pm.urls', namespace='pm')),

3. Run `python manage.py migrate` to create the pm models.

4. Start the development server and visit http://127.0.0.1:8000/admin/ to create users, groups, and projects (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/pm/ to view the projects application.