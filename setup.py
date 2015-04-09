import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

setup(
    name='django-projManager',
    version='0.2.2',
    packages=find_packages(),
    install_requires=['django >= 1.7', 'django-crispy-forms', 'django-jsonview'],
    include_package_data=True,
    license='BSD License',  # example license
    description='A Django app for project management.',
    long_description=README,
    author='Eliezer Kanal',
    author_email='eykanal@erikdev.com',
    url='',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
