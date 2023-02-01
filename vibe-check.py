"""
	Relatively rank a group of objects based on vibes
"""
from sort import *
from item import *
from benchmark import *
import random

def main():
	x = 1000
	n = 600
	k = 5		# smaller k, less comparisons for some reason??
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
