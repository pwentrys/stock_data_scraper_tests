# --------------------------------------------------------------------------- #
#                                                                             #
#                           Core Imports                                      #
#                                                                             #
# --------------------------------------------------------------------------- #

from datetime import timedelta

from flask import Flask

from config.configuration import SESSION_LIFETIME, STATIC, TEMPLATES
import base64
from sql import mysql


# --------------------------------------------------------------------------- #
#                                                                             #
#                       Default Configuration                                 #
#                                                                             #
# --------------------------------------------------------------------------- #


class FlaskFactory:
    NAME = __name__
    SPLITS = [' ', '_', '-']

    @staticmethod
    def _run_splits(string: str) -> list:
        """
        Split string if string contains split, else throw string into list.
        :param string:
        :return:
        """
        for split in FlaskFactory.SPLITS:
            if string.__contains__(split):
                return string.split(split)
        return [string]

    @staticmethod
    def _format_item(string: str) -> str:
        """
        Format item, for prettiness.
        :param string:
        :return:
        """
        if len(string) > 1:
            return f'{string[0].upper()}{string[1:].lower()}'
        else:
            return f'{string[0].upper()}'

    @staticmethod
    def _format_items(items: list) -> list:
        """
        Format each item in list.
        :param items:
        :return:
        """
        return [FlaskFactory._format_item(item) for item in items]

    @staticmethod
    def _format_abbrev(string: str) -> str:
        """
        Prettifies abbreviation.
        :param string:
        :return:
        """
        if len(string) < 1:
            return 'Error'

        string_split = FlaskFactory._run_splits(string)

        return ' '.join(string_split)

    @staticmethod
    def _get_secret_key(string: str) -> str:
        """
        Compile secret key using string.
        :param name:
        :return:
        """
        byted = bytes(string, 'utf-8')
        encoded = base64.standard_b64encode(byted)
        stringed = str(encoded)
        formatted = stringed[2:-1]
        return formatted

    @staticmethod
    def _get_session_lifetime() -> timedelta:
        """
        Session lifetime, for cookies.
        :return:
        """
        return timedelta(days=SESSION_LIFETIME)

    @staticmethod
    def create(
            name: str,
            display: str,
            address: str,
            port: int,
            debug: bool,
            threaded: bool) -> Flask:
        """
        Create and return flask app.
        :param name:
        :param address:
        :param port:
        :param debug:
        :param threaded:
        :return:
        """
        app = Flask(
            name.lower(),
            static_url_path='',
            static_folder=STATIC,
            template_folder=TEMPLATES
        )

        app.sql = mysql.Connection()

        display_name = FlaskFactory._format_abbrev(display)
        app.__name__ = display_name
        app.title = display_name
        app.config.from_object(name.lower())

        app.DEBUG = debug
        app.HOST = address
        app.PORT = port
        app.THREADED = threaded

        app.config.update(
            SESSION_COOKIE_DOMAIN=name,
            SESSION_COOKIE_NAME=name,
            DEBUG=debug
        )

        app.secret_key = FlaskFactory._get_secret_key(name)
        app.permanent_session_lifetime = FlaskFactory._get_session_lifetime()

        return app
