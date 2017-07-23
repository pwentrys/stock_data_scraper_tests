import pathlib
import pyodbc
from os import listdir, path

from utilities.dictionary import Dictionary as d
from config.configuration import SQL


class Connection:
    def __init__(self):
        """
        Object for db connection.
        :return:
        """
        self.schema = SQL['DATABASE']
        self.drivers = pyodbc.drivers()
        self.connected = False
        self.connection = self.connect()
        self.cursor = self.connection.cursor()
        self.ensure_tables()

    def get_tables_list(self):
        """
        Get list of all tables in schema.
        :return:
        """
        show_tables_res = self.execute('SHOW TABLES;')
        show_tables = []
        for show_table in show_tables_res:
            show_tables.append(show_table[0])
        return show_tables

    def ensure_tables(self):
        """
        Ensure all tables in defines exist.
        :return:
        """
        path_real = path.realpath(__file__)
        path_dir = path.dirname(path_real)
        tables_dir = pathlib.Path(f'{path_dir}\\tables')
        if not tables_dir.exists():
            pathlib.Path.mkdir(tables_dir)
            if not tables_dir.exists():
                print(tables_dir)
                return

        show_tables = self.get_tables_list()
        table_files = listdir(str(tables_dir))
        for table_file in table_files:
            table_file_name = table_file.split(d.period)[0]

            if not show_tables.__contains__(table_file_name):
                table_file_path = f'{tables_dir}\\{table_file}'
                if pathlib.Path(table_file_path).exists():
                    sql_text = pathlib.Path(table_file_path).read_text()
                    if not sql_text[len(sql_text) - 1] == ';':
                        sql_text = f'{sql_text};'
                    self.execute(sql_text)
                    self.commit()
                show_tables.append(table_file_name)

        show_tables = self.get_tables_list()
        for table_sql in show_tables:
            sql_path = f'{tables_dir}\\{table_sql}.sql'
            res = self.execute(f'SHOW CREATE TABLE {table_sql};')
            res_str = d.empty
            for line in res:
                res_str = line[1]

            if not pathlib.Path(sql_path).exists():
                self.write_text(sql_path, res_str)

    def write_text(self, str_path: str, text: str):
        """
        Write text to file at path.
        :param str_path:
        :param text:
        :return:
        """
        pathlib.Path(str_path).write_text(text)

    def truncate(self, schema: str, table: str):
        """
        Wipes all data in table.
        :param schema:
        :param table:
        :return:
        """
        try:
            if not self.connected:
                return

            self.execute(f'TRUNCATE `{schema}`.`{table}`;')
            self.commit()
        except Exception as error:
            print(error)

    def commit(self):
        """
        Apply outstanding transactions.
        :return:
        """
        self.connection.commit()

    def connect(self):
        """
        Connect to server.
        Actual connect string: DRIVER={0};SERVER={1};DATABASE={2};UID={3};PWD={4};
        :return:
        """
        try:
            if self.connected:
                print(f'Already Connected.')
                return False

            string_odbc = f'DRIVER={self.drivers[3] if len(self.drivers) > 2 else self.drivers[1]};' \
                          f'SERVER={SQL["ADDRESS"]};' \
                          f'DATABASE={SQL["DATABASE"]};' \
                          f'UID={SQL["USERNAME"]};' \
                          f'PWD={SQL["PASSWORD"]};'
            self.connection = pyodbc.connect(string_odbc)
            self.connection.setdecoding(pyodbc.SQL_CHAR, encoding=d.utf_8)
            self.connection.setencoding(encoding=d.utf_8)
            self.connected = True
            return self.connection
        except Exception as error:
            print(f'CONNECTION ERROR\n{error}')
            self.connected = False
            return error

    def execute(self, query: str) -> list:
        """
        Get attempts connection to server.
        If successful -> run query and return result.
        If error -> return error.
        Close connection to server.
        :param query:
        :return:
        """
        try:
            if not self.connected:
                return "ERROR"

            result = self.cursor.execute(query).fetchall()
            return result
        except Exception as error:
            print(query)
            print(error)
            return []

    @staticmethod
    def interpret_error(error):
        # TODO Interpret Errors
        """
        Translate error to human-readable fashion, and / or use for reconnection logic.
        https: // docs.microsoft.com / en - us / sql / odbc / reference / syntax / sqldriverconnect - function
        :param error:
        :return:
        """
        return error

    def disconnect(self):
        """
        Disconnect from serv.
        :return:
        """
        try:
            if not self.connected:
                return

            self.connected = False
            self.connection.close()
        except Exception as error:
            print(error)
