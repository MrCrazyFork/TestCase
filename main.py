import json
from report_api import ReportAPI
from datetime import date

import dal
import config
import tc_alarm
import tc_logging


def main():

    try:
        # Set report name
        report_name = "input"

        # Set report data
        if not config.IS_TEST_CONFIG:
            report_date = date.today()
        else:
            report_date = "2017-02-01"

        # Init connection to db
        con = dal.SqlServer(config.DWH)

        # Init ReportApi
        report_api = ReportAPI(report_name, report_date)

        # Get data from report api
        report_data = report_api.get_report()

        for rd in report_data:
            # Insert data to report table
            if "Success" in rd.keys():
                t = rd.get("Success")
                con.insert_into_report_table(
                    t.get("user"),
                    t.get("ts"),
                    json.dumps(t.get("context")),
                    t.get("ip")
                )
            # Insert data to error table
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

        tc_logging.logger.info("Finished loading report '{0}' for date '{1}'".format(report_name, report_date))

    except Exception as e:
        tc_logging.logger.exception("Something wrong. Error info: {}".format(e))
        tc_alarm.send_mail("TestCase Failed. Error info: {}".format(e))
        raise e


if __name__ == '__main__':
    main()
