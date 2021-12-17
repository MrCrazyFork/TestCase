import os

IS_TEST_CONFIG = 1

# General
_cur_dir = os.getcwd()

TOOL_FOLDER = _cur_dir if IS_TEST_CONFIG else os.path.join("C:\\", "path", "to", "application", "TestCase")
SOURCE_FOLDER = os.path.join(TOOL_FOLDER, "source")
LOG_NAME = "log.log"

# Connection
URL = "https://snap.datastream.center/techquest/"

DWH = {
    "host": "host",
    "port": "port",
    "database": "db",
    "user": "user",
    "password": "psw",
}

# Reports schema for validation
REPORTS = {
    "input": {
        "user": int,
        "ts": float,
        "context": {
            "hard": int,
            "soft": int,
            "level": int,
        },
        "ip": str
    }
}