"""
Haffman encode | decode algorithm
"""


class HuffmanCode:
    """
    Huffman code encode and decoder.
    """

    def __init__(self, data: str):
        """
        Initialize the data.
        """
        self.data = data
        self.probabilities = []
        self.code = ""
        self.code_dict = {}

    def calculate_frequency(self) -> list:
        """
        Helper method to calculate frequency of the characters.
        >>> text = HuffmanCode("aaaaabbbbbffffhhhrro")
        >>> sorted(text.calculate_frequency())
        [[0.05, '', 'o'], [0.1, '', 'r'], [0.15, '', 'h'], [0.2, '', 'f'], [0.25, '', 'a'], [0.25, '', 'b']]
        >>> text = HuffmanCode("aaaaaaaaa")
        >>> sorted(text.calculate_frequency())
        [[1.0, '', 'a']]
        """
        characters = set()
        for i in self.data:
            characters.add(i)
        result = []
        for ch in characters:
            self.probabilities.append([ch, (self.data.count(ch))/len(self.data)])
            result.append([(self.data.count(ch))/len(self.data), '', ch])
        return result

    def encode_start(self, list_l):
        """
        Main method to encode the string to Huffman code.
        Returns list of lists, where the first element of each sublist is probability of the letter
        and the second is it`s code.
        >>> text = HuffmanCode("aaaaabbbb")
        >>> prb = text.calculate_frequency() 
        >>> text.encode_start(prb)
        [[0.4444444444444444, '0', 'b'], [0.5555555555555556, '1', 'a']]
        >>> text = HuffmanCode("a")
        >>> prb = text.calculate_frequency() 
        >>> text.encode_start(prb)
        [[1.0, '1', 'a']]
        >>> text = HuffmanCode("")
        >>> prb = text.calculate_frequency() 
        >>> text.encode_start(prb)
        []
        """
        if len(list_l)==0:
            return []
        if len(list_l)==1:
            list_l[0][1]="1"
            return list_l
        if len(list_l) > 2:
            list_l = sorted(list_l, key=lambda x: x[0], reverse=True)
            last_1 = list_l[-1]
            last_2 = list_l[-2]
            summary = [last_1[0] + last_2[0], "", "", last_1[-1] + last_2[-1]]
            list_l = list_l[:-2] + [summary]
            list_l = self.encode_start(list_l)
            list_l = sorted(list_l, key=lambda x: x[0])
            for i in list_l:
                try:
                    if i[-1] == last_1[-1] + last_2[-1]:
                        last_1[1] = i[1] + "0"
                        last_2[1] = i[1] + "1"
                        list_l.remove(i)
                        list_l.append(last_1)
                        list_l.append(last_2)
                        break
                except IndexError:
                    continue
            self.code_dict = list_l
            return list_l
        #If lenght of the list is 2 than we can assign codes:
        else:
            list_l = sorted(list_l, key=lambda x: x[0])
            list_l[0][1] = "0"
            list_l[1][1] = "1"
            return list_l

    def encode(self):
        """
        Returns the code string.
        """
        buf = self.data
        for i in self.code_dict:
            buf = (buf).replace(i[2], i[1])
        self.code = buf
        return self.code

    def decode(self):
        """
        Decoding the Huffman code.
        """
        result = ''
        dicti = dict()
        for j in self.code_dict:
            dicti[j[1]] = j[2]
        now = ''
        for i in self.code:
            now += i
            if now in dicti:
                result += dicti[now]
                now = ''
        result = result.replace('¡', '0')
        result = result.replace('#', '1')
        return result
