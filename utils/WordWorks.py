class WordWorks:
    PRE = {
        'begins': {},
        'contains': {
            'space-x': 'spacex',
            "^": '',
            '…': '',
            '–': ' ',
            "—": '',
            '-': ' ',
            '!': ' ',
            "'s": '',
            "'": ' ',
            ".com": ' ',
            "www.": ' ',
            "+": ' ',
            ",": ' ',
            ";": ' ',
            ".": ' ',
            "?": ' ',
            "/": ' ',
            "\\": ' ',
            ":": ' ',
            "#": ' ',
            "&": ' ',
            "(": ' ',
            ")": ' ',
            "@": ' ',
            "[": ' ',
            "...": ' ',
            "]": ' ',
        },
        'ends': {},
        'is': {},
    }
    POST = {
        'begins': {},
        'contains': {
            "'s": '',
            "+": '',
            ",": '',
            "?": '',
            "/": '',
            "\\": '',
            ":": '',
            "#": '',
            "&": '',
            "(": '',
            ")": '',
            "@": '',
            "[": '',
            "...": '',
            "]": '',
        },
        'ends': {},
        'is': {
            'a': '',
            'an': '',
            'and': '',
            'answers': 'answer',
            'at': '',
            'by': '',
            'from': '',
            'for': '',
            'forums': 'forum',
            'have': '',
            'i': '',
            'in': '',
            'is': '',
            'it': '',
            'motors': 'motor',
            'my': '',
            # 'not': '',
            'of': '',
            'on': '',
            'or': '',
            'that': '',
            'the': '',
            'this': '',
            'to': '',
            'vs': 'versus',
            'watching': 'watch',
            'with': '',
        },
    }

    @staticmethod
    def _preclean_word(word: str) -> str:
        return WordWorks._clean_word(word, WordWorks.PRE)

    @staticmethod
    def _clean_word(word: str, clean_dict: dict) -> str:
        begins = clean_dict['begins']
        contains = clean_dict['contains']
        ends = clean_dict['ends']
        iss = clean_dict['is']
        word = word.lower()
        for begin in begins:
            if word.startswith(begin):
                word = f'{begins[begin]}{word[len(begin):]}'
        for end in ends:
            if word.endswith(end):
                word = f'{word[:-len(end)]}{ends[end]}'
        for contain in contains:
            if word.__contains__(contain):
                word = word.replace(contain, contains[contain])
        for _is in iss:
            if word == _is:
                word = iss[_is]
        return word

    @staticmethod
    def _postclean_word(word: str) -> str:
        return WordWorks._clean_word(word, WordWorks.POST)

    @staticmethod
    def _do_result(item, dictionary):
        item = WordWorks._preclean_word(item)
        if item != '' and item != '-':
            item = WordWorks._postclean_word(item)
            if item != '' and item != '-':
                if dictionary.__contains__(item):
                    dictionary[item] += 1
                else:
                    dictionary.update({item: 1})
        return dictionary

    @staticmethod
    def _do_results(dictionary, items):
        for item in items:
            item = WordWorks._preclean_word(item)
            item_split = item.split(' ')
            for word in item_split:
                dictionary = WordWorks._do_result(word, dictionary)
        return dictionary

    @staticmethod
    def do_dict(results):
        dictionary = {}
        for result in results:
            result = WordWorks._preclean_word(result)
            result_split = result.split(' ')
            dictionary = WordWorks._do_results(dictionary, result_split)
        return dictionary
