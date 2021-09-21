import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

REPO_URL = 'http://github.com/otto-torino/django-admin-export-action'

setup(
    name='django-admin-export-action',
    version='0.2.4',
    packages=['admin_export_action'],
    include_package_data=True,
    license='MIT License',
    description='Export action for django admin',
    long_description=README,
    long_description_content_type='text/markdown',
    url=REPO_URL,
    author='abidibo',
    author_email='abidibo@gmail.com',
    install_requires=[
        'openpyxl',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development',
    ],
    project_urls={
        'Documentation': REPO_URL + '/blob/master/README.md',
        'Source': REPO_URL,
        'Tracker': REPO_URL + '/issues',
    },
)
