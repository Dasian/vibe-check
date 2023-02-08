"""
	Relatively rank a group of objects based on vibes
"""
from sort import *
from item import *
from benchmark import *
import settings
import PySimpleGUI as sg
import threading as th
import pickle
import os

def main():
	gui()
	# benchmark()
	# load_test()

def algo_worker(sort_func, sort_args):
	# run algo, communication now in item cmp methods
	sort_func(*sort_args)
	# finished, send output to gui?
	# send two none's to signal lmao
	settings.gui_read_queue.put(None)
	settings.gui_read_queue.put(None)
	vals = [[x.name] for x in sort_args[0]]
	print(vals)
	settings.gui_read_queue.put(vals)
	# or send curr state after every comparison
	return

def gui():
	sg.theme('Dark Grey 12')
	font = 'Courier 64'
	button_font = 'Courier 32'
	save_dir = 'saves/'
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

	# create new comparison list
	# show tree?
	new_layout = [
		[sg.Push(), sg.Text('New Comparison', font=font), sg.Push()], 
		[sg.Push(), sg.Button('File Import', font=button_font), sg.Button('Spotify Login', font=button_font), sg.Button('Plex Login', font=button_font), sg.Push()],
		[sg.Push(), sg.Input(key='-Folder-', font=button_font), sg.FolderBrowse(font=button_font), sg.Push()],
		[sg.Push(), sg.Button('Continue', font=button_font), sg.Push()],
		[sg.Push(), sg.Button('Home', font=button_font), sg.Push()]
	]

	# load a save
	load_layout = [
		[sg.Push(), sg.Text('Load', font=font), sg.Push()],
		[sg.Push(), sg.Input(key='-Load Path-', font=button_font), sg.FileBrowse(font=button_font, initial_folder=save_dir), sg.Push()],
 		[sg.Push(), sg.Button('Continue', key='-Load Save-', font=button_font), sg.Push()],
		[sg.Push(), sg.Button('Home', font=button_font), sg.Push()]
	]

	# settings
	settings_layout = [[sg.Text('Settings', font=font)], [sg.Button('Home', font=button_font)]]

	# comparer window (after new or load)
	# use clickable tables to display ranking (cookbook)
	# progress meter for choosing?
	# save as and save button types?
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
		[sg.Push(), sg.Button('Home', font=button_font), sg.Save(font=button_font), sg.Push()]
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
	hist_len = 1
	history = [None for x in range(hist_len)]
	# Event loop runs while gui window is open
	while True:
		event, values = window.read()
		print((event, values))
		print()

		# home menu navigation
		if curr_layout == '-Home-' and event != 'Quit':
			new_layout = '-' + event + '-'
			window[f'-Home-'].update(visible=False)
			window[new_layout].update(visible=True)
			curr_layout = new_layout

		if event == sg.WIN_CLOSED or event == 'Quit':
			# maybe a save prompt?
			break

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
			sort_algo = partial_quick_sort
			sort_args = [arr, 1]
			algo_args = [sort_algo, sort_args]
			algo_thread = th.Thread(target=algo_worker, args=algo_args, daemon=True)
			algo_thread.start()	
			# wait for next options to update window
			opt1 = settings.gui_read_queue.get()
			opt2 = settings.gui_read_queue.get()
			window['-Opt1-'].update(opt1)
			window['-Opt2-'].update(opt2)

		# TODO get sorts args from user

		# comparison choice
		elif curr_layout == '-Comparer-' and event in valid_choices and not done_sorting:
			# send choice to algo thread
			settings.gui_write_queue.put(event)
			# wait for next option to be ready
			opt1 = settings.gui_read_queue.get()
			opt2 = settings.gui_read_queue.get()
			if opt1 != None and opt2 != None:
				# display next options
				window['-Opt1-'].update(opt1)
				window['-Opt2-'].update(opt2)
				# save sort progress
				history[0] = settings.save_queue.get()
				print('new save received')
				print(history[0])
			else:
				# sorting is finished
				done_sorting = True
				results = settings.gui_read_queue.get()
				curr_layout = '-Results-'
				window['-Comparer-'].update(visible=False)
				window[curr_layout].update(visible=True)
				window['-Results Table-'].update(results)

		# TODO implement history

		# TODO prevent popup if already set
		elif event.startswith('Save') and history[0] != None:
			fname = sg.popup_get_file('hey there', initial_folder=save_dir, save_as=True)
			if fname != None:
				print('Saving...')
				print('history[0]:', history[0])
				f = open(fname, 'wb')
				pickle.dump(history[0], f)
				f.close()

		# TODO load from file
		elif curr_layout == '-Load-' and event == '-Load Save-':
			if values['-Load Path-'] == '':
				continue
			f = open(values['-Load Path-'], 'rb')
			save = pickle.load(f)
			f.close()
			print('Loading...')
			print(save)

			# TODO terminate thread if it exists
			algo_thread = load_save(save)
			algo_thread.start()
	
			# wait for next options to update window
			window[curr_layout].update(visible=False)
			window[f'-Comparer-'].update(visible=True)
			curr_layout = '-Comparer-'
			opt1 = settings.gui_read_queue.get()
			opt2 = settings.gui_read_queue.get()
			window['-Opt1-'].update(opt1)
			window['-Opt2-'].update(opt2)

	window.close()

def load_save(save):
	""" 
		Loads a save from unpickled save file 
		Returns a thread obj to be started
	"""
	# unpack data
	k = save['k']
	arr = save['arr']
	true_indices = save['true_indices']
	i = save['i']
	in_partition = save['in_partition']
	in_median = save['in_median']
	quick_select = save['quick_select']
	partition_args = save['partition_args']
	median_args = save['median_args']
	median_args.insert(0, arr)
	partition_args.insert(0, arr)

	# load thread
	sort_algo = partial_quick_sort
	sort_args = [arr, k, true_indices, i, in_partition, in_median, quick_select, partition_args, median_args]
	algo_args = [sort_algo, sort_args]
	algo_thread = th.Thread(target=algo_worker, args=algo_args, daemon=True)
	return algo_thread	

if __name__ == "__main__":
	main()
