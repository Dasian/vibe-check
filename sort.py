"""
	Implementations of various sorting algorithms

	These will be used to compare two items (see item.py)
	Items don't necessarily have a true ordering, so the
	comparisons can be decided by the user to create a 
	personal ranking
"""
import settings
import copy

def get_median(arr, left, right, num_cmp=-1):
	""" Returns the median index given left and right index """ 
	# median of 3
	# change the comparator from > to < if sorting least to most
	global save_state
	mid = (left + right) // 2
	save_state.update({'in_median': True})
	save_state.update({'median_args': [left, right]})

	# num_cmp prevents entering a comparison
	# conditional if it has already been checked
	if num_cmp < 0 and arr[mid] > arr[left]:
		arr[mid], arr[left] = arr[left], arr[mid]
		median_args = [left, right, 0]
		save_state.update({'median_args': median_args})
	if num_cmp < 0 and settings.new_choice and not settings.is_benchmark:
		save_state.update({'arr': arr})
		save = copy.deepcopy(save_state)
		settings.save_queue.put(save)

	if num_cmp < 1 and arr[right] > arr[left]:
		arr[right], arr[left] = arr[left], arr[right]
		median_args = [left, right, 1]
		save_state.update({'median_args': median_args})
	if num_cmp < 1 and settings.new_choice and not settings.is_benchmark:
		save_state.update({'arr': arr})
		save = copy.deepcopy(save_state)
		settings.save_queue.put(save)

	if num_cmp < 2 and arr[right] > arr[mid]:
		arr[right], arr[mid] = arr[mid], arr[right]	
		median_args = [left, right, 2]
		save_state.update({'median_args': median_args})
	if num_cmp < 2 and settings.new_choice and not settings.is_benchmark:
		save_state.update({'arr': arr})
		save = copy.deepcopy(save_state)
		settings.save_queue.put(save)

	return mid

def partial_quick_sort(arr, k, quick_select=False, true_indices=None, i=1, in_partition=False, in_median=False,  partition_args=[], median_args=[]):
	"""	
		Loadable partial_quicksort/quick_select function

		O(n + klogk)
		Returns a list of indices that are in their final position
	"""
	global save_state
	save_state = {'arr': arr, 'k': k, 'true_indices': true_indices, 'i': i, 'in_partition': in_partition, 'in_median': in_median,'quick_select': quick_select, 'partition_args': partition_args, 'median_args': median_args}

	# TODO maybe just pass the dict and unpack here??

	# track the indices that are alread in their final positions
	if true_indices == None:
		true_indices = [0, len(arr)-1]

	# reload save point from partition
	elif in_partition:
		pivot_index = partition(*partition_args)
		left = partition_args[1]
		right = partition_args[2]

		# saved i is incorrect, update here
		while true_indices[i] < pivot_index:
			i += 1

		# edge case magic for insertion
		if pivot_index not in true_indices:
			true_indices.insert(i, pivot_index)
		elif right - left <= 2:
			true_indices.insert(i, pivot_index+1)

	# quick_select
	# get k elements instead of kth index
	if quick_select:
		k -= 1
	while quick_select and i < len(true_indices):
		left = true_indices[i-1]
		right = true_indices[i]
		if left == k or right == k:
			save_state.update({'arr': arr})
			save = copy.deepcopy(save_state)
			settings.save_queue.put(save)
			return true_indices
		if right < k:
			i += 1
		elif left > k:
			i -= 1
		else:
			custom_partition(arr, left, right, true_indices, i, in_median, median_args)
			if in_median:
				in_median = False

	# partial_quicksort
	# check if all sets are <= k
	# sorts from greatest to smallest
	while not quick_select and i < len(true_indices) and len(true_indices) != len(arr):
		left = true_indices[i-1]
		right = true_indices[i]
		if right - left > k:
			custom_partition(arr, left, right, true_indices, i, in_median, median_args)
			if in_median:
				in_median = False
		else:
			i += 1
	return true_indices

def custom_partition(arr, left, right, true_indices, i, in_median, median_args):
	""" Helper partitioner for partial_quicksort """
	# don't compare indices that are already in place
	if left == 0 and right != len(arr)-1:
		right -= 1
	elif right == len(arr)-1 and left != 0:
		left += 1
	elif left != 0 and right != len(arr)-1:
		left += 1
		right -= 1

	# partition subset around pivot
	if in_median:
		pivot_index = get_median(*median_args)
	else:
		pivot_index = get_median(arr, left, right)
	save_state.update({'in_median': False})	
	pivot_index = partition(arr, left, right, pivot_index)
	save_state.update({'in_partition': False})	

	# fixes some edge cases and prevents inf loops
	# what edge cases you may ask
	# I also ask
	if pivot_index not in true_indices:
		true_indices.insert(i, pivot_index)
	elif right - left <= 2:
		true_indices.insert(i, pivot_index+1)

	# update sorting progress
	save_state.update({'true_indices': true_indices, 'i': i, 'arr': arr})

def partition(arr, left, right, pivot_index, i=None, store=None):
	""" Partition helper for quick_* funcs
		Returns the "true" index of the selected pivot
		
		true index means that the pivot element is in its
		final sorted position in the list
	"""
	global save_state
	save_state.update({'in_partition': True})

	if store == None and i == None:
		# set local vars if not loading from a save
		i = left
		store = left
		pivot = arr[pivot_index]
		# move pivot to end
		arr[pivot_index], arr[right] = arr[right], arr[pivot_index]
	else:
		# pivot was already set at the end
		pivot = arr[right]

	# bread and butter bb
	while i < right:
		if arr[i] > pivot:	# change for largest/smallest value here
			arr[store], arr[i] = arr[i], arr[store]
			store += 1
			i += 1
			partition_args = [left, right, pivot_index, i, store]
			save_state.update({'arr': arr, 'partition_args': partition_args})
		else:
			i += 1

		# only save state if the user makes a new decision
		if settings.new_choice and not settings.is_benchmark:
			# deepcopy dict change error here
			# more likely when n is big
			# but it still finishes?
			save = copy.deepcopy(save_state)
			settings.save_queue.put(save)

	# place pivot in final position
	arr[right], arr[store] = arr[store], arr[right]
	return store

def quick_sort(arr, left, right):
	""" Have the user compare every concept to a pivot, divide set,
		repeat for all sets until completely ordered.
	"""
	global save_state
	save_state = {}
	# might want to restrict to small n or at least have some type
	# of estimated time function to warn the user
	if left < right:
		pivot_index = get_median(arr, left, right)
		pivot_index = partition(arr, left, right, pivot_index)
		quick_sort(arr, left, pivot_index-1)	# sort left
		quick_sort(arr, pivot_index+1, right)	# sort right

def quick_select(arr, left, right, k):
	"""	Return the best k elements in a set (unsorted)
		(currently set to the largest elements')
		Basically O(n)
	"""
	global save_state
	save_state = {}
	if left == right:	
		return arr[0:k]
	pivot_index = get_median(arr, left, right) 
	pivot_index = partition(arr, left, right, pivot_index)
	# pivot is in final sorted position
	if k == pivot_index:
		return arr[0:k]
	elif k < pivot_index:
		return quick_select(arr, left, pivot_index-1, k)
	else:
		return quick_select(arr, pivot_index+1, right, k)

def partial_insertion_sort(arr, k):
	""" Finds the top k elements in an array
		Essentially insertion sort but inserts a new
		element to the sorted portion using binary search
	"""
	global save_state
	save_state = {}
	# TODO replace top with an in place implementation?
	i = 0
	top = []	# top k elements, sorted from best to worst
	while i < len(arr):
		if len(top) < k:
			index = binary_search(top, arr[i], 0, len(top)-1)
			top.insert(index, arr[i])
		elif arr[i] > top[-1] or arr[i] > top[0]:
			index = binary_search(top, arr[i], 0, len(top)-1)
			top.insert(index, arr[i])
			top.pop(0)
		i += 1	
	return top

def binary_search(arr, val, start, end):
	""" Finds a value's index in a sorted array with binary search
		Helper for binary insertion sort to find insertion index
		in the sorted portion
	""" 
	if start == end:
		if arr[start] > val:
			return start
		else:
			return start+1
	if start > end:
		return start
	mid = (start+end)//2
	if arr[mid] < val:
		return binary_search(arr, val, mid+1, end)
	elif arr[mid] > val:
		return binary_search(arr, val, start, mid-1)
	else:
		return mid

def merge_insertion_sort(arr):
	""" has the fewest num of comparisons in theory """
	# https://github.com/TheAlgorithms/Python/blob/master/sorts/merge_insertion_sort.py
	return
