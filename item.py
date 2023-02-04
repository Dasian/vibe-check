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
from settings import *
import os

class Item():
	def __init__(self):
		self.type = ''	# name for concepts at the same depth (album)
		self.name = ''	# name for this object (To Pimp a Butterfly)
		# 0 is the root "largest" concept
		# children are "smaller" concepts
		self.depth = 0	# what level of the tree are you
		self.children = []
		self.parent = None
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
		global is_gui
		print('is_gui', is_gui)
		if self.type == 'int':
			if other.value not in self.gt.keys():
				self.nc += 1
				self.gt[other.value] = self.value > other.value
				other.gt[self.value] = other.value > self.value
			return self.gt[other.value]
		elif other.name in self.gt.keys():
			return self.gt[other.name]
		elif self.name == other.name:
			return False
		elif is_gui:
			# get user input from gui
			# send options to gui
			gui_read_queue.put(self.name)
			gui_read_queue.put(other.name)	
			# needs to wait?
			# get user choice
			choice = gui_write_queue.get()
			if choice == 'A':
				print(self.name +' was chosen')
				print()
				self.gt[other.name] = True
				other.gt[self.name] = False
				return True
			elif choice == 'B':
				print(other.name +' was chosen')
				print()
				self.gt[other.name] = False
				other.gt[self.name] = True
				return False
		else:
			# get user input from console
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

def generate_fs_tree(inp_path):
	""" Generates an item tree where the root is the
		user input path and the children are folders
		and files
		
		Returns the root of the tree
	"""
	split_inp = inp_path.split('/')
	root_item = Item()
	root_item.name = 'root'
	root_item.type = 'root'
	root_item.depth = 0
	max_depth = 0
	parent = None

	# fill item tree from filesystem
	for root, dirs, files in os.walk(inp_path):
		curr_path = root.split(os.sep)[len(split_inp):]
		
		# find parent
		parent = root_item
		for i in range(0, len(curr_path)):
			parent = parent.get_child(curr_path[i])

		# create children
		children = dirs + files
		depth = len(curr_path) + 1
		if depth > max_depth:
			max_depth = depth
		for c in children:
			i = Item()
			i.is_gui = True
			i.name = c
			i.depth = depth
			i.parent = parent
			parent.children.append(i)

	# group files at a depth
	for i in range(max_depth):
		children = root_item.get_children(i)
		for c in children:
			print(c.name)
		# inp = input('Name for this group?\n>')
		# for c in children:
			# c.type = inp
		print()

	return root_item
