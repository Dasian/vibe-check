"""
	One conceptual structure that is also a
	node in a tree, an element that can be ranked.
	For example: a song, album, artist, genre

	A genre has a list of artists as its children (overlapping)
	Artist has a list of albums as its children
	An album has a list of songs as its children

	Node of a tree, also a tree itself.
	One comparison object

	Two concepts don't need to be of the same type to be compared.
	I think TPAB is better than Macklemore.
"""

class Item():
	def __init__(self):
		self.type = ''	# name for concepts at the same depth (album)
		self.name = ''	# name for this object (To Pimp a Butterfly)
		# 0 is the root "largest" concept
		# children are "smaller" concepts
		self.depth = 0	# what level of the tree are you
		self.children = []
		self.rating = -1

	# TODO implement object comparisons
	
