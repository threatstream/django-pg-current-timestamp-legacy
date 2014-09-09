# -*- coding: utf-8 -*-

import unittest
import logging

from django.conf import settings
try:
    from django.utils.functional import empty
except ImportError:
    empty = None


logger = logging.getLogger(__name__)


def setup_test_environment():
    # reset settings
    settings._wrapped = empty

    apps = [
        'django_pg_current_timestamp',
        'django_pg_current_timestamp.tests',
        'django_pg_current_timestamp.test_app',
    ]

    settings_dict = {
        'DATABASES': {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'django_pg_current_timestamp',
            },
        },
        'MIDDLEWARE_CLASSES': [],
        'INSTALLED_APPS': apps,
        'SITE_ID': 1,
        'DEFAULT_INDEX_TABLESPACE': '',
    }

    # set up settings for running tests for all apps
    settings.configure(**settings_dict)
    try:
        from django import setup
        setup()  # Needed for Django>=1.7
    except ImportError:
        pass


class TestCase(unittest.TestCase):
    """Initializes the db with models from `test_app`, see http://stackoverflow.com/a/10657706/293064."""
    initiated = False

    @classmethod
    def setUpClass(cls, *args, **kwargs):
        if not TestCase.initiated:
            TestCase.create_models_from_app('django_pg_current_timestamp.test_app')
            TestCase.initiated = True
        super(TestCase, cls).setUpClass(*args, **kwargs)

    @classmethod
    def create_models_from_app(cls, app_name):
        """
        Manually create Models (used only for testing) from the specified string app name.
        Models are loaded from the module '<app_name>.models'
        """
        from django.db import connection, DatabaseError
        from django.db.models.loading import load_app
        from django.test.simple import DjangoTestSuiteRunner

        app = load_app(app_name)
        from django.core.management import sql
        from django.core.management.color import no_style
        sql = sql.sql_create(app, no_style(), connection)
        cursor = connection.cursor()
        for statement in sql:
            try:
                cursor.execute(statement)
            except DatabaseError, excn:
                logger.debug(excn.message)

    def testIt(self):
        from django.test.simple import DjangoTestSuiteRunner
        runner = DjangoTestSuiteRunner(verbosity=1, interactive=False, failfast=False)
        return runner.run_tests(['django_pg_current_timestamp'])


def runtests():
    setup_test_environment()
    unittest.main()


if __name__ == '__main__':
    runtests()

