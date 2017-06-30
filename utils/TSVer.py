from utils.Statics import Statics


class TSVer:
    """

    """

    def __init__(self, symbol: str):
        self.symbol = symbol
        self.current, self.previous = Statics.get_tsv_path(symbol)
        self._move_current_to_previous()

    def update_symbol(self, symbol: str):
        """

        :param symbol:
        """
        if self.symbol != symbol:
            self.symbol = symbol
            self.current, self.previous = Statics.get_tsv_path(self.symbol)

    def _current_text(self):
        if self.current.is_file():
            return self.current.read_text(encoding=Statics.UTF8)
        else:
            return Statics.EMPTY

    def _move_current_to_previous(self):
        self.previous.write_text(self._current_text(), encoding=Statics.UTF8)
        self.current.write_text(Statics.EMPTY)

    def append_current(self, items: list):
        """

        :param items:
        """
        text = self._current_text()
        split = text.splitlines()
        split.extend(items)  # for item in items:
        self.current.write_text('\n'.join(set(split)), encoding=Statics.UTF8)
        items.clear()
