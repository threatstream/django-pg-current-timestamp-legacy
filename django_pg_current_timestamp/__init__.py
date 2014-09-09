# -*- coding: utf-8 -*-

"""Adds django compatibility with / capability to use `CURRENT_TIMESTAMP` on DateTimeField objects."""

import logging

from django.utils import timezone

from psycopg2.extensions import ISQLQuote


__version__ = '0.2.1'
__author__ = 'Jay Taylor [@jtaylor]'


logger = logging.getLogger(__name__)


class CurrentTimestamp(object):

    def __str__(self):
        return 'CURRENT_TIMESTAMP'

    def as_sql(self, qn, val):
        return self.__str__(), {}

    def __conform__(self, proto):
        """Does the given protocol conform to what Psycopg2 expects?"""
        if proto == ISQLQuote:
            return self
        else:
            raise Exception('Error implementing psycopg2 protocol. Is psycopg2 installed?')

    def getquoted(self):
        """Returns a properly quoted string for use in PostgreSQL/PostGIS."""
        # Psycopg will figure out whether to use E'\\000' or '\000'.
        return self.__str__()

    @classmethod
    def patch(cls, field):
        orig_pre_save = field.pre_save
        orig_prep_db = field.get_db_prep_value
        orig_prep_lookup = field.get_prep_lookup
        orig_db_prep_lookup = field.get_db_prep_lookup

        def pre_save(self, model_instance, add):
            """
            Pre-save `CURRENT_TIMESTAMP` injector.
            NB: The returned value is what will go into the database, and the `timezone.now()` value will be set on the model instance.
            """
            if self.auto_now or (self.auto_now_add and add):
                value = CurrentTimestamp()
                setattr(model_instance, self.attname, timezone.now()) # Attach an approximate TS to the object.
                return value
            else:
                return orig_pre_save(self, model_instance, add)

        def prep_db_value(self, value, connection, prepared=False):
            result = value if isinstance(value, cls) else orig_prep_db(self, value, connection, prepared)
            #logger.debug('prep_db_value :: name={} type(result)={} result={}'.format(self.name, type(result), result))
            return result

        def prep_lookup(self, lookup_type, value):
            result = value if isinstance(value, cls) else orig_prep_lookup(self, lookup_type, value)
            #logger.debug('prep_lookup :: name={} type(result)={} result={}'.format(self.name, type(result), result))
            return result

        def prep_db_lookup(self, lookup_type, value, connection, prepared=True):
            result = value if isinstance(value, cls) else orig_db_prep_lookup(self, lookup_type, value, connection=connection, prepared=True)
            #logger.debug('prep_db_lookup :: name={} type(result)={} result={}'.format(self.name, type(result), result))
            return result

        field.pre_save = pre_save
        field.get_db_prep_value = prep_db_value
        field.get_prep_lookup = prep_lookup
        field.get_db_prep_lookup = prep_db_lookup


def init():
    """Activation for automatic support of DateTimeField fields with `auto_now` and/or `auto_now_add` columns."""
    from django.db.models import DateTimeField
    logger.info('django_pg_current_timestamp :: Monkey-patching django.db.models.DateTimeField to enable automatic `CURRENT_TIMESTAMP` support for DateTimeField')
    CurrentTimestamp.patch(DateTimeField)

