class DTFormats:
    BDY = '%b %d, %Y'  # Jun 1st, 2017
    YMD = '%Y%m%d'  # 20170601
    YMDDASHED = '%Y-%m-%d'  # 20170601

    @staticmethod
    def dashenate(string: str) -> str:
        if not string.__contains__('-'):
            return f'{string[0:4]}-{string[4:6]}-{string[6:8]}'
        return string
