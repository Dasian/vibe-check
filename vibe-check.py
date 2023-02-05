"""
	Relatively rank a group of objects based on vibes
"""
from sort import *
from item import *
from benchmark import *
from settings import *
import PySimpleGUI as sg
import threading as th

def main():
	# gui needs threads, console doesn't
	gui()

def algo_worker(sort_func, sort_args):
	# run algo, communication now in item cmp methods
	sort_func(*sort_args)
	# finished, send output to gui?
	# send two none's to signal lmao
	gui_read_queue.put(None)
	gui_read_queue.put(None)
	vals = [[x.name] for x in sort_args[0]]
	print(vals)
	gui_read_queue.put(vals)
	# or send curr state after every comparison
	return

def gui():
	sg.theme('Dark Grey 12')
	font = 'Courier 64'
	button_font = 'Courier 32'
	# sg.theme_previewer()

	# home screen
	home_layout = [
		[sg.Push(),sg.Text('Vibe Check', font=font, justification='c'), sg.Push()],
		[sg.VPush()],
		[sg.Push(), sg.Button('New', font=button_font), sg.Push()],
		[sg.Push(), sg.Button('Load', font=button_font), sg.Push()],
		[sg.Push(), sg.Button('Settings', font=button_font), sg.Push()],
		[sg.Push(), sg.Button('Quit', font=button_font), sg.Push()]
	]

	# create new comparison set
	# TODO finish
	# show tree?
	# currently just continue to go to comparer screen
	new_layout = [
		[sg.Push(), sg.Text('New Comparison', font=font), sg.Push()], 
		[sg.Button('File Import'), sg.Button('Spotify Login'), sg.Button('Plex Login')],
		[sg.Push(), sg.Input(key='-Folder-', font=button_font), sg.FolderBrowse(font=button_font), sg.Push()],
		[sg.Push(), sg.Button('Continue', font=button_font), sg.Push()],
		[sg.Push(), sg.Button('Home', font=button_font), sg.Push()]
	]

	# load a previous comparison
	load_layout = [
		[sg.Push(), sg.Text('Load Comparison', font=font), sg.Push()],
		[sg.Button('Home', font=button_font)]
	]

	# settings
	settings_layout = [[sg.Text('Settings', font=font)], [sg.Button('Home', font=button_font)]]

	# comparer window (after new or load)
	# use clickable tables to display ranking (cookbook)
	# progress meter for choosing?
	opt1_layout = [
		[sg.Push(), sg.Text('Opt 1', font=font, key='-Opt1-'), sg.Push()],
		[sg.Push(), sg.Button('A', font=button_font), sg.Push()]
	]
	opt2_layout = [
		[sg.Push(), sg.Text('Opt 2', font=font, key='-Opt2-'), sg.Push()],
		[sg.Push(), sg.Button('B', font=button_font), sg.Push()]
	]
	comparer_layout = [
		[sg.Push(), sg.Text('Vibe Checker', font=font), sg.Push()],
		[sg.Column(opt1_layout), sg.Push(), sg.Text('vs', font=font), sg.Push(), sg.Column(opt2_layout)],
		[sg.Push(), sg.Button('Home', font=button_font), sg.Push()]
	]

	results_layout = [
		[sg.Push(), sg.Text('Results', font=font), sg.Push()],
		[sg.Push(), sg.Button('Home', font=button_font), sg.Push()],
		[sg.Push(), sg.Table([['Ranking']], auto_size_columns=True, key='-Results Table-', font='Courier 16', justification='left'), sg.Push()]
	]

	# switches window layout
	master_layout = [
		[sg.Column(home_layout, key='-Home-', visible=True), 
		sg.Column(new_layout, visible=False, key='-New-'), 
		sg.Column(load_layout, visible=False, key='-Load-'), 
		sg.Column(settings_layout, visible=False, key='-Settings-'),
		sg.Column(comparer_layout, visible=False, key='-Comparer-'),
		sg.Column(results_layout, visible=False, key='-Results-')
		]
	]

	window = sg.Window('vibes', master_layout, resizable=True, finalize=True)

	curr_layout = '-Home-'
	valid_choices = ['A', 'B']
	sort_func = None
	root_item = None
	algo_thread = None
	done_sorting = False
	# Event loop runs while gui window is open
	while True:
		event, values = window.read()
		print((event, values))
		print()

		if event == sg.WIN_CLOSED or event == 'Quit':
			# maybe a save prompt?
			if algo_thread != None:
				algo_thread.join()
			break

		# home menu navigation
		elif curr_layout == '-Home-':
			new_layout = '-' + event + '-'
			window[f'-Home-'].update(visible=False)
			window[new_layout].update(visible=True)
			curr_layout = new_layout

		# return home
		elif event.startswith('Home'):
			window[curr_layout].update(visible=False)
			window[f'-Home-'].update(visible=True)
			curr_layout = '-Home-'

		# create new comparison list
		elif curr_layout == '-New-' and event == 'Continue':
			# change window layout
			window[curr_layout].update(visible=False)
			window[f'-Comparer-'].update(visible=True)
			curr_layout = '-Comparer-'
			# fill Item tree
			root_item = generate_fs_tree(values['Browse'])

			# TEMP BEHAVIOR, run quicksort
			arr = root_item.get_children(3)
			sort_algo = quick_sort
			sort_args = [arr, 0, len(arr)-1]
			algo_args = [sort_algo, sort_args]
			algo_thread = th.Thread(target=algo_worker, args=algo_args, daemon=True)
			algo_thread.start()	
			# wait for next options to update window
			opt1 = gui_read_queue.get()
			opt2 = gui_read_queue.get()
			window['-Opt1-'].update(opt1)
			window['-Opt2-'].update(opt2)

		# get algo info somewhere?

		# comparison choice
		elif curr_layout == '-Comparer-' and event in valid_choices and not done_sorting:
			# send choice to algo thread
			gui_write_queue.put(event)
			# wait for next option to be ready
			opt1 = gui_read_queue.get()
			opt2 = gui_read_queue.get()
			if opt1 != None and opt2 != None:
				window['-Opt1-'].update(opt1)
				window['-Opt2-'].update(opt2)
			else:
				# sorting is finished
				done_sorting = True
				results = gui_read_queue.get()
				curr_layout = '-Results-'
				window['-Comparer-'].update(visible=False)
				window[curr_layout].update(visible=True)
				window['-Results Table-'].update(results)

	window.close()

if __name__ == "__main__":
	main()
