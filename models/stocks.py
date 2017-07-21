from models.stock import Stock


class Stocks:
    def __init__(self, data):
        self.data = data
        self.stocks = self._update()

    def _update(self):
        out = []
        if len(self.data) < 2:
            return out

        for line in self.data:
            line_split = line.split(',')
            day = int(line_split[0])
            display = line_split[1]
            symbol = line_split[2]
            pages = line_split[3]
            out.append(
                Stock(
                    display,
                    symbol,
                    day,
                    pages
                )
            )
        return out
