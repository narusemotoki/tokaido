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
    tokaido.models.Base.metadata.drop_all()
    tokaido.models.DBSession.close()
