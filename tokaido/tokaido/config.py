import logging
import os
import sys

import owattr


LOG_LEVEL = logging.NOTSET
DATA_SOURCE_NAME = "sqlite:///tokaido.sqlite3"


owattr.from_dict(sys.modules[__name__], dict(os.environ))
