"""
lz77 encode | decode algorithm
"""


from typing import List


class Lz77:
    """
    Lz77 Compressing method
    """
    def __init__(self,text: str, search_block_len: int, front_block_len: int) -> None:
        self.text=text
        self.search_block_len=search_block_len
        self.front_block_len=front_block_len
        self.coded_message=[]

    def lz77_encode(self) -> List[tuple]:
        """
        Lz77 encoding.
        >>> text1=Lz77("aaaa",0,0)
        >>> text1.lz77_encode()
        [(0, 0, 'a'), (0, 0, 'a'), (0, 0, 'a'), (0, 0, 'a')]
        >>> text1= Lz77("aaaa",1,1)
        >>> text1.lz77_encode()
        [(0, 0, 'a'), (1, 1, 'a'), (1, 1, '')]
        >>> text1=Lz77("abacabacabac",5,5)
        >>> text1.lz77_encode()
        [(0, 0, 'a'), (0, 0, 'b'), (2, 1, 'c'), (4, 5, 'b'), (4, 2, '')]
        >>> text1= Lz77("",5,5)
        >>> text1.lz77_encode()
        []
        >>> text1=Lz77("I love math!!!",5,5)
        >>> text1.lz77_encode()
        [(0, 0, 'I'), (0, 0, ' '), (0, 0, 'l'), (0, 0, 'o'), (0, 0, 'v'), \
(0, 0, 'e'), (5, 1, 'm'), (0, 0, 'a'), (0, 0, 't'), (0, 0, 'h'), (0, 0, '!'), (1, 2, '')]
        """
        front_block_len=self.front_block_len
        search_block_len=self.search_block_len
        text=self.text
        position = 0
        codding = []
        while position < len(text):
            search_block = text[max(0, position - search_block_len) : position]
            front_block = text[position : min(position + front_block_len, len(text))]
            best_match = (0, 0, text[position])
            for i in range(len(search_block) - 1, -1, -1):
                match = 0
                if search_block[i] == front_block[0]:
                    match += 1
                    small_list = search_block[i:]
                    for j in range(1, len(front_block)):
                        if small_list[j % len(small_list)] == front_block[j]:
                            match += 1
                        else:
                            break
                if match > best_match[1]:
                    best_match = (
                        len(search_block) - i,
                        match,
                        "" if position + match > len(text) - 1 else text[position + match],
                    )
            position = position + best_match[1] + 1
            codding.append(best_match)
        self.coded_message=codding
        return codding
    def decodelz77(self) -> str:
        """
        Decodes Lz77 and return text as string
        >>> text1=Lz77("aaa,a",0,0)
        >>> assert(text1.lz77_encode())
        >>> text1.decodelz77()
        'aaa,a'
        >>> text1=Lz77("aaaa",1,1)
        >>> assert(text1.lz77_encode())
        >>> text1.decodelz77()
        'aaaa'
        >>> text1=Lz77("abacabacabac",5,5)
        >>> assert(text1.lz77_encode())
        >>> text1.decodelz77()
        'abacabacabac'
        >>> text1=Lz77("",5,5)
        >>> assert(not text1.lz77_encode())
        >>> text1.decodelz77()
        ''
        >>> text1=Lz77("I love math!!!",5,5)
        >>> assert(text1.lz77_encode())
        >>> text1.decodelz77()
        'I love math!!!'
        """
        codes=self.coded_message
        text = ""
        for code in codes:
            small_list = text[len(text) - code[0] :]
            for k in range(0, code[1]):
                text += small_list[k % code[0]]
            text += code[2]
        return text
    @staticmethod
    def decode_from_str(codes):
        """
        Decoder for deflayte
        """
        text = ""
        codes = codes.split("..")
        codes = [
            (codes[i], codes[i + 1], str(codes[i + 2][1:-1])) for i in range(0, len(codes), 3)
        ]
        for code in codes:
            small_list = text[len(text) - int(code[0]) :]
            for k in range(0, int(code[1])):
                text += small_list[k % int(code[0])]
            text += code[2]
        return text
    def count_compressing(self):
        """
        Count compressing efficiency
        """
        compressed_len = len(self.coded_message)*6
        text_len=len(self.text)
        return 100-((compressed_len / text_len)*100)
