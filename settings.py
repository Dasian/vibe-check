""" 
	Keeps track of global vars and settings
"""
from queue import Queue

global is_gui
global gui_read_queue
global gui_write_queue

is_gui = True
# inter thread communication
gui_read_queue = Queue()
gui_write_queue = Queue()
