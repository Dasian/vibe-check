"""
	Implementations of various relative comparison algorithms.

	These will be used to compare two concepts. Since concepts
	are abstract ideas, there isn't necessarily a true ordering
	like there are with real numbers.
"""
import math

class Comparer():
	def __init__(self):
		self.rankings = []	# not sure yet, an ordered ranking of concepts?
		self.nc = 0

	def rank(self, arr):
		""" Asks the user to rank a list of concepts 
			Returns the ordered list of concepts from best -> worst
		"""

		return arr

	def merge_sort(self, arr):
		""" Have the user rank a list or concepts then mergesort """
		return

	def quick_sort(self, arr, rank_size):
		""" Have the user compare every concept to a pivot, divide set,
			repeat for all sets until completely ordered.
			rank_size is the max list size the user needs to order
		"""
		# TODO implement
		# might want to restrict to small n or at least have some type
		# of estimated time function to warn the user
		return

	def quick_select(self, arr, left, right, k):
		"""	Return the best k+1 elements in a set (unsorted)
			(currently set to the largest elements')

			128 elements with perfect median and best k=1 takes 254
			comparisons or avg case 2(n-k)

			num_medians with perfect median is floor(log(n-k-1))?
		"""
		# one element in list	
		if left == right:	
			print('num_comparisons', self.nc)
			return arr[0:k+1]
		# "median" selection or middle of list
		pivot_index = math.floor((left + right)/2)
		pivot_index = self.partition(arr, left, right, pivot_index)
		# pivot is in final sorted position
		if k == pivot_index:
			print('num_comparisons', self.nc)
			# first k, best or worst?
			return arr[0:k+1]
		elif k < pivot_index:
			return self.quick_select(arr, left, pivot_index-1, k)
		else:
			return self.quick_select(arr, pivot_index+1, right, k)

	def partition(self, arr, left, right, pivot_index):
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
			self.nc += 1
			if arr[i] > pivot:	# change for largest/smallest value here
				arr[store], arr[i] = arr[i], arr[store]
				store += 1
		arr[right], arr[store] = arr[store], arr[right]
		# true index for the pivot has been determined 
		# TODO
		# cache results (if not being done already)
		# and give the user some statistics on their progress
		return store

	def bucket_sort(self, arr):
		""" Have the user sort each concept into a 'bucket'
			Return the bucket dictionary {'bucket': [c1, c2, ...]}

			Bucket examples: Dislike, Neutral, Like; [0-5]
		"""
		return
