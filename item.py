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
		self.parent = None
		self.rating = -1
		self.gt = {}	# keeps track the result of self > key, avoids dup cmp

		# for comparing ints in initial benchmarks
		self.value = 0
		self.nc = 0 # num comparisons

	def get_child(self, target):
		""" Returns child object with the target name """
		for c in self.children:
			if c.name == target:
				return c
		return None
	
	# TODO get_children based on depth, name, type
	def get_children(self, depth):
		""" Returns list of children at a given depth """
		children = []
		if self.depth == depth:
			return self.children
		elif self.depth < depth:
			for c in self.children:
				children += c.get_children(depth)
		else:
			return
		return children

	def print_tree(self):
		""" Prints this Item as a tree """
		print(self.depth * '---' + 'type: ' + self.type + ' name: ' + self.name)
		for child in self.children:
			child.print_tree()
		return

	def __str__(self):
		s = 'Item ' + self.name + ' ' + self.type
		return s

	# TODO keep track of unique comparisons 
	def __gt__(self, other):
		if self.type == 'int':
			if other.value not in self.gt.keys():
				self.nc += 1
				self.gt[other.value] = self.value > other.value
				other.gt[self.value] = other.value > self.value
			return self.gt[other.value]
		elif other.name in self.gt.keys():
			return self.gt[other.name]
		else:
			# get user input to decide
			inp = input('1: ' + self.name + ' or 2: ' + other.name+'\n> ')
			if inp == '1':
				self.gt[other.name] = True
				other.gt[self.name] = False
				return True
			elif inp == '2':
				self.gt[other.name] = False
				other.gt[self.name] = True
				return False
			else:
				print('invalid choice')
				return self.__gt__(other)

	def __eq__(self, other):
		if self.type == 'int':
			return self.value == other.value
		else:
			# only equal if name and type? not sure if input needed
			return self.name == other.name and self.type == other.type
