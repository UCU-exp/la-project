"""
Deflate encode | decode algorithm
"""


class Deflate:
	"""
	Performs the Delfate algorithm
	>>> defl=Deflate("test")
	>>> defl.encode()
	'110110100001101101011001101101001010111010100'
	>>> assert defl.decode()=="test"
	"""

	def __init__(self, data):
		"""
		Initial method
		"""
		self.data = data
		self.special_0 = "⌇"
		self.special_1 = "˚"
		self.haffman = object

	def encode(self) -> str:
		"""
		Encoding the string by combination LZ77 and Huffman algorithms.
		"""
		lz77 = Lz77(self.data, 100, 100)
		code = lz77.lz77_encode()
		code_str = (
			str(code)
			.replace(", ", "..")
			.replace(")..(", "..")
			.replace("0", self.special_0)
			.replace("1", self.special_1)
		)[2:][:-2]
		haffman = HuffmanCode(code_str)
		self.haffman = haffman
		prob = haffman.calculate_frequency()
		haffman.encode_start(prob)
		haffman.encode()
		return self.haffman.code

	def decode(self) -> str:
		"""
		Decode deflayte
		"""
		lz_str = str(
			self.haffman.decode()
			.replace(self.special_0, "0")
			.replace(self.special_1, "1")
		)
		return Lz77.decode_from_str(lz_str)

	def compare_compression(self) -> float:
		"""
		Compare compression of Deflate algorithm.
		"""
		return 100-(len(self.haffman.code)/(len(self.data))*8)
