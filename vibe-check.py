"""
	Relatively rank a group of objects based on vibes
"""
import comparer
import random

def main():
	n = 128
	k = 1
	c = comparer.Comparer()	
	
	# generate random list
	arr = []
	while len(arr) < n:
		arr.append(random.randint(0, n))

	# sort test
	print('Best ' + str(k))
	print(c.quick_select(arr, 0, len(arr)-1, k-1))
	
if __name__ == "__main__":
	main()
