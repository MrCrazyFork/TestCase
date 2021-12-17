from json_checker import Checker
from json_checker.core.exceptions import DictCheckerError

import gzip
import json
import shutil
import urllib.request
from typing import List
from datetime import date
import os

import config


class ReportAPI:
    def __init__(self, report_name: str, dt: date) -> None:
        self._report_name = report_name
        self._dt = dt

        self._url = config.URL

        self._full_report_name = "{0}-{1}".format(self._report_name, str(self._dt))
        print(self._full_report_name)
        self._url_file = self._url + self._full_report_name + ".json.gz"
        self._result_path = os.path.join(config.SOURCE_FOLDER, self._full_report_name + ".csv")

        self._checker = Checker(config.REPORTS.get(self._report_name))

    def _get_file(self):
        try:
            # Open connection
            with urllib.request.urlopen(self._url_file) as f:
                # Open file
                with gzip.open(f, 'rb') as f_in:
                    # Write to result path
                    with open(self._result_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
        except Exception as e:
            raise e

    def _parse_json(self, json_string: str) -> dict:
        # Trying to validate
        try:
            # Validate structure
            json_line = json.loads(json_string)
            # Validate data
            result = self._checker.validate(json_line)
            # Write results
            res = {"Success": result}

        # Json structure and data validation
        except (ValueError, DictCheckerError) as je:
            fail = {
                "line": json_string.replace("\n", ""),
                "error": str(je).replace("'", "\"")
            }
            # Write error
            res = {"Failure": fail}
        except Exception as e:
            # If there is other error, then raise
            raise e

        return res

    def get_report(self) -> List[dict]:
        # Download file
        self._get_file()

        res = []

        # Parse json
        with open(self._result_path, 'r') as f:
            for line in f:
                res.append(self._parse_json(line))

        return res

