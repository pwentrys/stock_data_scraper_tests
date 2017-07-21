from typing import Tuple

from utils.URLFormats import URLFormats


class OutputFormats:
    BEGINS = []
    CONTAINS = ['|', '·', '•', '  ', '<strong>', '</strong>']
    ENDS = ['…', '...', '-']

    @staticmethod
    def entry(string: str) -> str:
        """

        :param string:
        :return:
        """
        string = string.strip()

        for begin in OutputFormats.BEGINS:
            if string.startswith(begin):
                string = string[len(begin):].strip()

        for end in OutputFormats.ENDS:
            if string.endswith(end):
                string = string[:-len(end)].strip()

        for contain in OutputFormats.CONTAINS:
            if string.__contains__(contain):
                string = string.replace(contain, '').strip()

        return string

    @staticmethod
    def title(string: str) -> str:
        """

        :param string:
        :return:
        """
        string = OutputFormats.entry(string)
        return string

    @staticmethod
    def description(string: str) -> str:
        """

        :param string:
        :return:
        """
        string = OutputFormats.entry(string)
        return string

    @staticmethod
    def link(string: str) -> str:
        """

        :param string:
        :return:
        """
        return URLFormats.from_string(string)

    @staticmethod
    def get_result(title: str, desc: str, link: str) -> Tuple[str, str, str]:
        """

        :param title:
        :param desc:
        :param link:
        :return:
        """
        return OutputFormats.title(title), \
               OutputFormats.description(desc), \
               OutputFormats.link(link)
