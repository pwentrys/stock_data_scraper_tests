class Transformers:
    @staticmethod
    def list2string(string_list: list, separator='\n') -> str:
        """
        Turn list of objects into one string object.
        :param separator:
        :param string_list:
        :return:
        """
        if len(string_list) > 0:
            return ''.join([f'{item}{separator}' for item in string_list])[
                   :-len(separator)]
        return ''
