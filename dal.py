from datetime import datetime

import pymssql

import config


class SqlServer:

    def __init__(self, connection_config: dict) -> None:
        self._host = connection_config.get("host")
        self._db = connection_config.get("database")
        self._port = connection_config.get("port")
        self._user = connection_config.get("user")
        self._password = connection_config.get("password")

    def _dml_query(self, query) -> None:
        if not config.IS_TEST_CONFIG:
            try:
                with pymssql.connect(
                        host=self._host,
                        database=self._db,
                        port=self._port,
                        user=self._user,
                        password=self._password,
                        autocommit=True
                ) as conn:
                    with conn.cursor() as cur:
                        cur.execute(query)
            except Exception as e:
                raise e
        else:
            # Simulate insert
            print(query)

    def _truncate_report_table(self):
        q = "truncate table schema.report_table"

        self._dml_query(q)

    # Not multipurpose due to testcase
    def insert_into_report_table(
            self,
            v_id: int,
            v_ts: float,
            v_context: str,
            v_ip: str
    ) -> None:
        # There is no info in test case if this is historical table or one time use
        # So we pretend that it's one time use table and truncate it every time
        self._truncate_report_table()

        q = """
                insert into schema.report_input 
                (
                        id
                    ,   ts
                    ,   context
                    ,   ip
                )
                values
                (
                        {0}
                    ,   {1}
                    ,   '{2}'
                    ,   '{3}'
                )
            """.format(v_id, v_ts, v_context, v_ip)

        self._dml_query(q)

    def insert_into_error_table(
            self,
            v_api_report: str,
            v_api_date: str,
            v_row_text: str,
            v_error_text: str

    ) -> None:
        # We won't truncate this table to see historical errors
        q = """
                insert into schema.data_error 
                (
                        api_report
                    ,   api_date
                    ,   row_text
                    ,   error_text
                    ,   ins_ts
                )
                values
                (
                        '{0}'
                    ,   '{1}'
                    ,   '{2}'
                    ,   '{3}'
                    ,   '{4}'
                )
            """.format(
            v_api_report,
            v_api_date,
            v_row_text,
            v_error_text,
            datetime.now()
        )

        self._dml_query(q)
