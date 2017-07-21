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
        if not self.current.is_file():
            self.current.write_text('', encoding=Statics.UTF8)

        return self.current.read_text(encoding=Statics.UTF8)

    def _move_current_to_previous(self):
        self.previous.write_text(self._current_text(), encoding=Statics.UTF8)
        # self.current.write_text(Statics.EMPTY)

    def append_current(self, items: list):
        """

        :param items:
        """
        text = self._current_text()
        if len(text) < 1:
            split = []
        else:
            split = text.splitlines()

        split.extend(items)  # for item in items:
        if len(split) > 0:
            split = set(split)
            split = sorted(split, key=lambda x: int(x.split('|')[0]))
            self.current.write_text('\n'.join(split), encoding=Statics.UTF8)
        items.clear()
