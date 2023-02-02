"""
	Relatively rank a group of objects based on vibes
"""
from sort import *
from item import *
from benchmark import *
import random
import os

def main():
	# TODO generate items from spotify/plex
	inp_path = '/home/dasian/Dasian/vibe-check/test'
	split_inp = inp_path.split('/')
	root_item = Item()
	root_item.name = 'root'
	root_item.type = 'root'
	root_item.depth = 0
	parent = None

	# fill item tree from filesystem
	# Items are folders and files
	# folders have children while files don't
	for root, dirs, files in os.walk(inp_path):
		curr_path = root.split(os.sep)[len(split_inp):]
		
		# find parent
		parent = root_item
		for i in range(0, len(curr_path)):
			parent = parent.get_child(curr_path[i])

		# create children
		children = dirs + files
		depth = len(curr_path) + 1
		# prompt to name this depth type? i.e. albums, shows
		for c in children:
			i = Item()
			i.name = c
			i.depth = depth
			i.parent = parent
			parent.children.append(i)

	# get sorting info from user

	# send warnings about running time

	# run
	

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
