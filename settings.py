""" 
	Keeps track of global vars and settings
"""
from queue import Queue

is_gui = True
is_benchmark = False

# interthread communication
gui_read_queue = Queue()
gui_write_queue = Queue()
save_queue = Queue()

# set when the user makes a new decision
# used to determine when to save state
new_choice = False
