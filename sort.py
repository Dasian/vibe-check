"""
	Implementations of various sorting algorithms

	These will be used to compare two items (see item.py)
	Items don't necessarily have a true ordering, so the
	comparisons can be decided by the user to create a 
	personal ranking
"""

def get_median(arr, left, right):
	""" Returns the median index given left and right index """ 
	# median of 3
	# 3 comparisons, puts the median of the 3 at the returned index
	# change the comparator from > to < if sorting least to most
	mid = (left + right) // 2
	if arr[mid] > arr[left]:
		arr[mid], arr[left] = arr[left], arr[mid]
	if arr[right] > arr[left]:
		arr[right], arr[left] = arr[left], arr[right]
	if arr[right] > arr[mid]:
		arr[right], arr[mid] = arr[mid], arr[right]	
	return mid

# overload this function with all quick_* variations?
def partial_quick_sort(arr, k, true_indices=None, i=1, in_partition=False, quick_select=False, partition_args=[]):
	""" Have the user compare every concept to a pivot, divide set,
		repeat for all sets until completely ordered.
		all unordered sets will be of size <= k.
		
		Every while loop iteration can save and reload the curr state
		of this function's arguments in order to work on large sets
		over a long period of time.

		quicksort: k=1
		quickselect: quickselect boolean
		partial_qs: normal behavior

		O(n + klogk)
		Returns the set of true indices
	"""
	# track the indices that are alread in their final positions
	if true_indices == None:
		true_indices = [0, len(arr)-1]

	# reload save point from partition
	if in_partition:
		pivot_index = partition(*partition_args)	
		true_indices.insert(i, pivot_index)

	# check if all sets are <= k
	# sorts from greatest to smallest
	while i < len(true_indices) and len(true_indices) != len(arr):
		# TODO save true_indices and array progress
		# communicate with save thread?
		# save arr, k, ti, i, ip, pa (this funcs args)
		left = true_indices[i-1]
		right = true_indices[i]
		if right - left > k:
			if left == 0 and right != len(arr)-1:
				right -= 1
			elif right == len(arr)-1 and left != 0:
				left += 1
			elif left != 0 and right != len(arr)-1:
				left += 1
				right -= 1
			pivot_before = get_median(arr, left, right)
			pivot_index	= partition(arr, left, right, pivot_before)
			if pivot_index not in true_indices:
				true_indices.insert(i, pivot_index)
			elif right - left <= 2:
				true_indices.insert(i, pivot_index+1)
		else:
			i += 1
	return true_indices

def partition(arr, left, right, pivot_index):
	""" Partition helper for quick_* funcs
		Returns the "true" index of the selected pivot
		
		true index means that the pivot element is in its
		final sorted position in the list
	"""
	pivot = arr[pivot_index]
	# move pivot to end
	arr[pivot_index], arr[right] = arr[right], arr[pivot_index]
	store = left
	for i in range(left, right):
		if arr[i] > pivot:	# change for largest/smallest value here
			arr[store], arr[i] = arr[i], arr[store]
			store += 1
	arr[right], arr[store] = arr[store], arr[right]
	# true index for the pivot has been determined 
	# TODO save arr, left, right, pi, i, store
	return store

def quick_sort(arr, left, right):
	""" Have the user compare every concept to a pivot, divide set,
		repeat for all sets until completely ordered.
	"""
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

def rank(arr):
	""" Asks the user to rank a list of concepts 
		Returns the ordered list of concepts from best -> worst
	"""
	return arr

def merge_sort(arr):
	""" Have the user rank a list or concepts then mergesort """
	return

def bucket_sort(arr):
	""" Have the user sort each concept into a 'bucket'
		Return the bucket dictionary {'bucket': [c1, c2, ...]}

		Bucket examples: Dislike, Neutral, Like; [0-5]
	"""
	return

def merge_insertion_sort(arr):
	""" has the fewest num of comparisons in theory """
	# https://github.com/TheAlgorithms/Python/blob/master/sorts/merge_insertion_sort.py
	return
