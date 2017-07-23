import re

from bs4 import BeautifulSoup

from utils.Statics import Statics


class SoupTags:
    PARSER = Statics.PARSER

    @staticmethod
    def _get_soup(text: str, parser=PARSER):
        return BeautifulSoup(text, parser)

    @staticmethod
    def using_h_re_compile(text: str, h_string: str):
        """

        :param text:
        :param h_string:
        :return:
        """
        return SoupTags._get_soup(text).find(
            href=re.compile(''), h=re.compile(h_string))

    @staticmethod
    def using_type_and_id(text: str, type_string: str, id_string: str):
        """

        :param text:
        :param type_string:
        :param id_string:
        :return:
        """
        return SoupTags._get_soup(text).find(type_string, id=id_string)

    @staticmethod
    def using_type_and_class(text: str, type_string: str, class_string: str):
        """

        :param text:
        :param type_string:
        :param class_string:
        :return:
        """
        return SoupTags._get_soup(text).find_all(
            type_string, class_=class_string)

    @staticmethod
    def using_type_and_class_one(
            text: str,
            type_string: str,
            class_string: str):
        """

        :param text:
        :param type_string:
        :param class_string:
        :return:
        """
        return SoupTags._get_soup(text).find(type_string, class_=class_string)
