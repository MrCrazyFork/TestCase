import json

import config
from report_api import ReportAPI
from datetime import date
import dal


def main():

    con = dal.SqlServer(config.DWH)

    if not config.IS_TEST_CONFIG:
        report_date = date.today()
    else:
        report_date = "2017-02-01"

    report_name = "input"

    report_api = ReportAPI(report_name, report_date)
    report_data = report_api.get_report()

    for rd in report_data:
        if "Success" in rd.keys():
            t = rd.get("Success")
            con.insert_into_report_table(
                t.get("user"),
                t.get("ts"),
                json.dumps(t.get("context")),
                t.get("ip")
            )
        elif "Failure" in rd.keys():
            t = rd.get("Failure")
            con.insert_into_error_table(
                report_name,
                report_date,
                t.get("line"),
                t.get("error")
            )
        else:
            raise ValueError("There is wrong state in report_data")


if __name__ == '__main__':
    main()
