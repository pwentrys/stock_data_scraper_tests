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
        return SoupTags._get_soup(text).find(href=re.compile(""), h=re.compile(h_string))

    @staticmethod
    def using_type_and_id(text: str, type_string: str, id_string: str):
        return SoupTags._get_soup(text).find(type_string, id=id_string)

    @staticmethod
    def using_type_and_class(text: str, type_string: str, class_string: str):
        return SoupTags._get_soup(text).find_all(type_string, class_=class_string)

    @staticmethod
    def using_type_and_class_one(text: str, type_string: str, class_string: str):
        return SoupTags._get_soup(text).find(type_string, class_=class_string)

    # staticmethod
    # def li__b_algo(tag):
    #     return tag.name == 'li' and tag.has_attr('class') and tag.get('class') == ['b_algo']

    # staticmethod
    # def a_link_title(tag):
    #     return tag.name == 'a' and tag.has_attr('h') and tag.parent.name == 'h2'

    # staticmethod
    # def a_link_desc(tag):
    #     return tag.name == 'p'

    # staticmethod
    # def a_link_news_dt(tag):
    # return tag.name == 'span' and tag.has_attr('class') and tag.get('class') ==
        #  ['news_dt'] and tag.parent.name == 'div' and tag.parent.parent.name == 'div'
