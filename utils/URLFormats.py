from urllib.parse import urlparse, quote


class URLFormats:
    @staticmethod
    def _format(scheme, netloc, path, query):
        if query == '':
            return f'{scheme}://{netloc}{path}'
        else:
            return f'{scheme}://{netloc}{path}?{query}'

    @staticmethod
    def from_parsed(parsed_url) -> str:
        return URLFormats._format(parsed_url.scheme, parsed_url.netloc, parsed_url.path, quote(parsed_url.query, safe='=&'))

    @staticmethod
    def from_string(string: str) -> str:
        return URLFormats.from_parsed(urlparse(string))
