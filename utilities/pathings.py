import os
from pathlib import Path

from utilities.typesext import Types as t


class Pathings:
    @staticmethod
    def pathstr2directories(string: str) -> list:
        """
        Path string to directory list.
        :param string:
        :return:
        """
        return Pathings.path2directories(Path(string))

    @staticmethod
    def _ensure(path):
        """
        Create path if it doesn't exist from path object.
        :param path:
        :return:
        """
        if not path.exists():
            parent = path.parent
            if not parent.exists():
                Pathings._ensure(parent)
            try:
                path.mkdir()
            except Exception as error:
                print(error)

    @staticmethod
    def ensure(path):
        """
        Create path if it doesn't exist from path object or string.
        :param path:
        :return:
        """
        if isinstance(path, t.StringType):
            path = Path(path)

        if os.path.basename(path).__contains__('.'):
            Pathings._ensure(path.parent)
        else:
            Pathings._ensure(path)

    @staticmethod
    def pathstr2exts(string: str) -> dict:
        """
        Path string to file list by extension.
        :param string:
        :return:
        """
        return Pathings.path2exts(Path(string))

    @staticmethod
    def pathstr2files(string: str) -> list:
        """
        Path string to file list.
        :param string:
        :return:
        """
        return Pathings.path2files(Path(string))

    @staticmethod
    def pathstr2contents(string: str) -> list:
        """
        Path string to directory + file list.
        :param string:
        :return:
        """
        return Pathings.path2contents(Path(string))

    @staticmethod
    def path2directories(path) -> list:
        """
        Path object to list of directories.
        :param path:
        :return:
        """
        assert not isinstance(
            path, t.StringType), f'Path was string instead of path obj: {path}'

        results = []
        if path.is_dir():
            results.append(str(path))
            for _path in path.iterdir():
                [results.append(str(item))
                 for item in Pathings.path2directories(_path)]
        return results

    @staticmethod
    def path2exts(path) -> dict:
        """
        Path object to lists of files sorted by extension.
        :param path:
        :return:
        """
        assert not isinstance(
            path, t.StringType), f'Path was string instead of path obj: {path}'

        if not path.exists():
            return {}

        results = {}
        results_list = Pathings.path2files(path)
        for result in results_list:
            base = os.path.basename(result)
            name, ext = os.path.splitext(base)
            if not results.__contains__(ext):
                results[ext] = []
            assert isinstance(
                results[ext],
                t.ListType), f'Result for {ext} is not of type List'
            results[ext].append(name)
        return results

    @staticmethod
    def path2files(path) -> list:
        """
        Path object to list of files.
        :param path:
        :return:
        """
        assert not isinstance(
            path, t.StringType), f'Path was string instead of path obj: {path}'

        results = []
        if path.is_dir():
            for _path in path.iterdir():
                if _path.is_dir():
                    [results.append(str(item))
                     for item in Pathings.path2files(_path)]
                elif _path.is_file():
                    results.append(str(_path))
        elif path.is_file():
            results.append(str(path))
        return results

    @staticmethod
    def path2contents(path) -> list:
        """
        Path object to list of directories and files.
        :param path:
        :return:
        """
        assert not isinstance(
            path, t.StringType), f'Path was string instead of path obj: {path}'

        results = []
        if path.is_dir():
            results.append(str(path))
            for _path in path.iterdir():
                [results.append(str(item))
                 for item in Pathings.path2contents(_path)]
        elif path.is_file():
            results.append(str(path))
        return results
