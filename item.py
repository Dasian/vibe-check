"""
	An element that can be compared and ranked by the user.

	For example: song, album, artist, genre

	Two items don't need to be of the same type to be compared.
	I think TPAB (album) is better than Macklemore (artist).
"""
import settings
import os

class Item():
	def __init__(self):
		self.type = ''	# name for a group of items (album)
		self.name = ''	# name for this item (To Pimp a Butterfly)
		self.depth = 0
		self.children = []
		self.parent = None
		self.gt = {}	# keeps track the result of self > key, avoids dup cmp

		# for comparing ints in initial benchmarks
		self.value = 0
		self.nc = 0 	# num unique comparisons

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

	def __gt__(self, other):
		if self.type == 'int':
			if other.value not in self.gt.keys():
				settings.new_choice = True
				self.nc += 1
				self.gt[other.value] = self.value > other.value
				other.gt[self.value] = other.value > self.value
			else:
				settings.new_choice = False
			return self.gt[other.value]
		elif other.name in self.gt.keys():
			settings.new_choice = False
			return self.gt[other.name]
		elif self.name == other.name:
			settings.new_choice = False
			return False
		elif settings.is_gui:
			# get user input from gui
			settings.new_choice = True
			# send options to gui
			settings.gui_read_queue.put(self.name)
			settings.gui_read_queue.put(other.name)	
			# get user choice
			choice = settings.gui_write_queue.get()
			if choice == 'A':
				self.gt[other.name] = True
				other.gt[self.name] = False
				return True
			elif choice == 'B':
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
			i.name = c
			i.depth = depth
			i.parent = parent
			parent.children.append(i)

	# group files at a depth
	for i in range(max_depth):
		children = root_item.get_children(i)
		# inp = input('Name for this group?\n>')
		# for c in children:
			# c.type = inp

	return root_item
