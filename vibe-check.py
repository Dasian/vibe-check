"""
	Relatively rank a group of objects based on vibes
"""
from sort import *
from item import *
from benchmark import *
import PySimpleGUI as sg
import os

def main():
	sg.theme('Dark Grey 12')
	font = 'Courier 64'
	button_font = 'Courier 32'
	# sg.theme_previewer()

	# home screen
	home_layout = [
		[sg.Push(),sg.Text('Vibe Check', font=font, justification='c'), sg.Push()],
		[sg.Push(), sg.Button('New', font=button_font), sg.Push()],
		[sg.Push(), sg.Button('Load', font=button_font), sg.Push()],
		[sg.Push(), sg.Button('Settings', font=button_font), sg.Push()],
		[sg.Push(), sg.Button('Quit', font=button_font), sg.Push()]
	]

	# create new comparison set
	new_layout = [[sg.Text('New Comparison', font=font)], [sg.Button('Home', font=button_font)]]

	# load a previous comparison
	load_layout = [
		[sg.Push(), sg.Text('Load Comparison', font=font), sg.Push()],
		[sg.Button('Home', font=button_font)]
	]

	# settings
	settings_layout = [[sg.Text('Settings', font=font)], [sg.Button('Home', font=button_font)]]

	# comparer window (after new or load)
	comparer_layout = []

	master_layout = [[sg.Column(home_layout, key='-Home-', visible=True), sg.Column(new_layout, visible=False, key='-New-'), sg.Column(load_layout, visible=False, key='-Load-'), sg.Column(settings_layout, visible=False, key='-Settings-')]]

	window = sg.Window('vibes', master_layout, resizable=True)

	curr_layout = '-Home-'
	while True:
		event, values = window.read()
		print((event, values))
		if event == sg.WIN_CLOSED or event == 'Quit':
			break
		if curr_layout == '-Home-':
			new_layout = '-' + event + '-'
			window[f'-Home-'].update(visible=False)
			window[new_layout].update(visible=True)
			curr_layout = new_layout
		if event.startswith('Home'):
			window[curr_layout].update(visible=False)
			window[f'-Home-'].update(visible=True)
			curr_layout = '-Home-'

	window.close()

	# progress meter for choosing?

def tmp():
	# choose how to generate item tree
	# generate items from file system
	inp_path = '/home/dasian/Dasian/vibe-check/test'
	root = generate_fs_tree(inp_path)

	# TODO generate items from spotify/plex

	# get sorting info from user

	# send warnings about running time

	# run
	
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
		for c in children:
			print(c.name)
		inp = input('Name for this group?\n>')
		for c in children:
			c.type = inp
		print()

	return root_item

def benchmark():
	x = 1000
	n = 600
	k = 50		# smaller k, less comparisons for some reason??
	rng = x*n	# range of values for testing

	# test info
	print('num lists per test:', x)
	print('size of list:', n)
	print('num elements to find/partition:', k)
	print()
	sample_args = [x, n, rng]

	# quick_select test
	sort_args = [0, n-1, k]
	print('quick_select')
	verify_partial_set(quick_select, sort_args, sample_args)
	print('verified')
	avg = count_comparisons(quick_select, sort_args, sample_args)
	print('comparison avg:', avg)
	print('time to compute (hours):',round(cmp_to_hours(avg), 4))
	print()

	# quick_sort test
	sort_args = [0, n-1]
	print('quick_sort')
	verify_sort(quick_sort, sort_args, sample_args)
	print('verified')
	avg = count_comparisons(quick_sort, sort_args, sample_args)
	print('comparison avg:', avg)
	print('time to compute (hours):',round(cmp_to_hours(avg), 4))
	print()

	# partial_quick_sort test
	sort_args = [k]
	print('partial_quick_sort')
	verify_partial_sort(partial_quick_sort, sort_args, sample_args)
	print('verified')
	avg = count_comparisons(partial_quick_sort, sort_args, sample_args)
	print('comparison avg:', avg)
	print('time to compute (hours):',round(cmp_to_hours(avg), 4))
	print()

	# partial_insertion_sort test
	sort_args = [k]
	print('partial_insertion_sort')
	verify_partial_set(partial_insertion_sort, sort_args, sample_args)
	print('verified')
	avg = count_comparisons(partial_insertion_sort, sort_args, sample_args)
	print('comparison avg:', avg)
	print('time to compute (hours):',round(cmp_to_hours(avg), 4))
	print()

	# ford-johnson min comparison test

if __name__ == "__main__":
	main()
