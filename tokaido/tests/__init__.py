import logging

import transaction

import tokaido
import tokaido.config
import tokaido.models


def setup_db():
    # If setup SQLAlchemy twice, it raise a warning.
    if tokaido.models.Base.metadata.bind:
        return
    tokaido.config.LOG_LEVEL = logging.CRITICAL
    tokaido.config.DATA_SOURCE_NAME = "sqlite:///tokaido_test.sqlite3"
    tokaido.init_database()


def teardown_db():
    _truncate_all_tables()
    tokaido.models.DBSession.close()


def _truncate_all_tables():
    tables = [table.fullname for table in tokaido.models.Base.metadata.sorted_tables]
    with transaction.manager:
        for table in tables:
            # It is not good idea bind value by "format" for SQL. However this time the value
            # can't have "'" and this is only for test. When I found good way, I will rewrite.
            tokaido.models.DBSession.execute(
                "ALTER TABLE {} DISABLE TRIGGER ALL;".format(table))

        for table in tables:
            tokaido.models.DBSession.execute(
                "TRUNCATE {} RESTART IDENTITY CASCADE;".format(table))

        for table in tables:
            tokaido.models.DBSession.execute(
                "ALTER TABLE {} ENABLE TRIGGER ALL;".format(table))

        tokaido.models.mark_changed()
