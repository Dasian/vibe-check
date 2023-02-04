"""
	Collection of methods to verify the accuracy 
	and count the number of comparisons of different
	sorting implementations
"""
from item import *
import random

def generate_sample(x, n, rng):
	""" Generates a list of x lists. Each list of x has n elements.
		Every element is in the range of 0 to rng. Any list should
 		not have repeated elements.
 	"""
	sample = []
	for i in range(x):
		arr = []
		vals = []
		while len(arr) < n:
			i = Item()
			i.type = 'int'
			value = random.randint(0, rng)
			while value in vals:
				value = random.randint(0, rng)
			i.value = value
			arr.append(i)
			vals.append(value)
		sample.append(arr)
	return sample

def cmp_to_hours(num):
	""" Converts number of comparisons to time in hours """
	secs_per_cmp = 8
	return num * secs_per_cmp / 3600

def count_comparisons(sort_func, sort_args, sample_args):
	""" Returns the average number of comparisons used
		in the passed sorting function
	"""
	sample = generate_sample(*sample_args)
	comparisons = []
	for arr in sample:
		sort_func(arr, *sort_args)
		comparisons.append(sum(x.nc for x in arr))
		for x in arr:
			x.nc = 0
	return sum(comparisons)/len(comparisons)

def verify_sort(sort_func, sort_arg, sample_arg):
	sample = generate_sample(*sample_arg)
	for arr in sample:
		sort_func(arr, *sort_arg)
		if not is_sorted(arr):
			raise('invalid sort')

def verify_partial_sort(sort_func, sort_arg, sample_arg):
	sample = generate_sample(*sample_arg)
	for arr in sample:
		pivots = sort_func(arr, *sort_arg)
		if not is_partially_sorted(arr, sort_arg[0], pivots):
			raise('invalid partial sort')

def verify_partial_set(sort_func, sort_arg, sample_arg):
	k = -1
	if len(sort_arg) > 1:
		k = sort_arg[2]
	elif len(sort_arg) == 1:
		k = sort_arg[0]
	else:
		raise('unknown partial set function')
	# determine if one set is in the top k
	sample = generate_sample(*sample_arg)
	for arr in sample:
		set1 = sort_func(arr, *sort_arg)
		min1 = min(set1)
		arr.sort(reverse=True)
		# it should be the kth largest element
		if not arr.index(min1) == k-1:
			set1_vals = [x.value for x in set1]
			min1_val = min1.value
			vals = [x.value for x in arr]
			print('set1', len(set1), set1_vals)
			print('min1', min1_val)
			print('k', k)
			print('arr.index(min1)', arr.index(min1))
			print('vals', vals)
			raise('invalid partial set')

def is_sorted(arr):
	""" Determines if an array is sorted from asc to desc """
	if len(arr) <= 1 or arr[0].type != 'int':
		return True
	for i in range(1, len(arr)-1):
		# sorted from highest to lowest
		if not arr[i] < arr[i-1]:
			return False
	return True

def is_partially_sorted(arr, k, pivots):
	""" Determines if an array is partially sorted from asc
		to desc
		
		A set is partially sorted if it's divided into
		subsets of at most length k and every element
		in one subset is larger than every element in
		the next adjacent subset. A fully sorted set
		has these properties with a subset of 1.
	"""
	# every subset length should be <= k
	for i in range(1, len(pivots)-1):
		if pivots[i] - pivots[i-1] > k:
			return False

	# all elements in the first subset should be
	# greater than all elements in the next subset
	for i in range(2, len(pivots)-1):
		set1 = arr[pivots[i-2]:pivots[i-1]]
		set2 = arr[pivots[i-1]:pivots[i]]
		if not min(set1) > max(set2):
			return False

	return True

def benchmark():
	""" Benchmark the performance of every implemented sorting algo """
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
