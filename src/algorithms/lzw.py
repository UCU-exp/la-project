"""
LZW encode | decode algoithm
"""


class Lzw:
    """
    Class to perform LZW encoding and decoding.
    >>> text = Lzw('abacabadabacacacd')
    >>> text.encode()
    [0, 1, 0, 2, 4, 0, 3, 8, 7, 12, 3]
    >>> 'abacabadabacacacd' == text.decode([0, 1, 0, 2, 4, 0, 3, 8, 7, 12, 3])
    True
    """
    def __init__(self, data):
        '''
        Initialize the data.
        '''
        self.data = data

    def encode(self):
        """
        The main method to encode LZW code.
        Returns list with code.
        >>> text = Lzw('aaabbbbcccc')
        >>> text.encode()
        [0, 3, 1, 5, 1, 2, 8, 2]
        """
        code = []
        symbols = []
        for ch in self.data:
            if ch not in symbols:
                symbols.append(ch)
        read = ''
        for symbol in self.data:
            with_next = read + symbol
            if with_next in symbols:
                read = with_next
            else:
                code.append(symbols.index(read))
                symbols.append(with_next)
                read = symbol
        if read in symbols:
            code.append(symbols.index(read))
        return code

    def decode(self, code: list):
        """
        The LZW decoding.
        """
        result = []
        symbols = []
        for ch in self.data:
            if ch not in symbols:
                symbols.append(ch)
        previous = ''
        for i in code:
            if i < len(symbols):
                if len(result) != 0:
                    previous = result[-1]
                    symbols.append(previous + (symbols[i])[0])
                result.append(symbols[i])
            if i == len(symbols):
                if len(result) != 0:
                    previous = result[-1]
                    symbols.append(previous + previous[0])
                result.append(previous + previous[0])
            elif i > len(symbols):
                if len(result) != 0:
                    previous = result[-1]
                new_str = previous + (symbols[i])[0]
                symbols.append(new_str)
                result.append(new_str)
        return ''.join(result)
