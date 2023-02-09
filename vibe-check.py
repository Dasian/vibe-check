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

def sort_worker(sort_func, sort_args):
	"""
		Used to run a sort function in a thread
	"""
	sort_func(*sort_args)

	# send two Nones to signal completion
	settings.gui_read_queue.put(None)
	settings.gui_read_queue.put(None)
	vals = [[x.name] for x in sort_args[0]]

	# send sorted values to gui
	settings.gui_read_queue.put(vals)

def gui():
	sg.theme('Dark Grey 12')
	font = 'Courier 64'
	button_font = 'Courier 32'
	save_dir = 'saves/'

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
	# TODO improve list creation
	# show tree?
	new_layout = [
		[sg.Push(), sg.Text('New Comparison', font=font), sg.Push()], 
		[sg.Push(), sg.Button('File Import', font=button_font), sg.Button('Spotify Login', font=button_font), sg.Button('Plex Login', font=button_font), sg.Push()],
		[sg.Push(), sg.Input(key='-Folder-', font=button_font), sg.FolderBrowse(font=button_font), sg.Push()],
		[sg.Push(), sg.Button('Continue', font=button_font), sg.Push()],
		[sg.Push(), sg.Button('Home', font=button_font), sg.Push()]
	]

	# sort choice layout
	sort_layout = [
		[sg.Push(), sg.Text('Sort Choice', font=font), sg.Push()],
		[sg.Push(), sg.Radio('Top x', group_id='sort_group', default=True, key='-Quick Select-', font=button_font), sg.Radio('Partial Sort', group_id='sort_group', key='-Partial Sort-', font=button_font), sg.Radio('Full Sort', group_id='sort_group', key='-Quick Sort-', font=button_font), sg.Push()],
		[sg.Push(), sg.Text('X:', font=button_font), sg.Input(key='-k-', font=button_font, size=(5,1)), sg.Push()],
		[sg.Push(), sg.Button('Home',font=button_font), sg.Button('Help', key='-Sort Help-',font=button_font), sg.Button('Continue',font=button_font), sg.Push()]
	]

	# load a save
	load_layout = [
		[sg.Push(), sg.Text('Load', font=font), sg.Push()],
		[sg.Push(), sg.Input(key='-Load Path-', font=button_font), sg.FileBrowse(font=button_font, initial_folder=save_dir), sg.Push()],
 		[sg.Push(), sg.Button('Continue', key='-Load Save-', font=button_font), sg.Push()],
		[sg.Push(), sg.Button('Home', font=button_font), sg.Push()]
	]

	# TODO settings
	settings_layout = [[sg.Text('Settings', font=font)], [sg.Button('Home', font=button_font)]]

	# comparer window
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
		[sg.Push(), sg.Button('Home', font=button_font), sg.Save(key='-Save-', font=button_font), sg.Push()]
	]

	# show comparison results
	results_layout = [
		[sg.Push(), sg.Text('Results', font=font), sg.Push()],
		[sg.Push(), sg.Table([['Ranking']], auto_size_columns=False, key='-Results Table-', font='Courier 16', justification='left', def_col_width=20), sg.Push()],
		[sg.Push(), sg.Button('Save', key='-Save Result-', font=button_font), sg.Push()],
		[sg.Push(), sg.Button('Home', font=button_font), sg.Push()],
	]

	# switches window layout
	master_layout = [
		[sg.Column(home_layout, key='-Home-', visible=True), 
		sg.Column(new_layout, visible=False, key='-New-'), 
		sg.Column(sort_layout, visible=False, key='-Sort-'),
		sg.Column(load_layout, visible=False, key='-Load-'), 
		sg.Column(settings_layout, visible=False, key='-Settings-'),
		sg.Column(comparer_layout, visible=False, key='-Comparer-'),
		sg.Column(results_layout, visible=False, key='-Results-')
		]
	]

	# so many variables!
	curr_layout = '-Home-'
	valid_choices = ['A', 'B']
	sort_func = None
	root_item = None
	sort_thread = None
	done_sorting = False
	# TODO create save dir if it doesn't exist
	# save_dir = 'saves/'
	hist_len = 1
	history = [None for x in range(hist_len)]
	window = sg.Window('vibes', master_layout, resizable=True, finalize=True)

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

		# exit
		if event == sg.WIN_CLOSED or event == 'Quit':
			# maybe a save prompt?
			break

		# return home
		elif event.startswith('Home'):
			window[curr_layout].update(visible=False)
			window[f'-Home-'].update(visible=True)
			curr_layout = '-Home-'

		# load sort from file
		elif curr_layout == '-Load-' and event == '-Load Save-':
			if values['-Load Path-'] == '':
				continue
			f = open(values['-Load Path-'], 'rb')
			save = pickle.load(f)
			f.close()

			# TODO terminate thread if it exists
			sort_thread = load_save(save)
			sort_thread.start()
	
			# wait for next options to update window
			window[curr_layout].update(visible=False)
			window[f'-Comparer-'].update(visible=True)
			curr_layout = '-Comparer-'
			opt1 = settings.gui_read_queue.get()
			opt2 = settings.gui_read_queue.get()
			window['-Opt1-'].update(opt1)
			window['-Opt2-'].update(opt2)

		# create new comparison list
		elif curr_layout == '-New-' and event.startswith('Continue'):
			# change window to sort choice
			window[curr_layout].update(visible=False)
			curr_layout = '-Sort-'
			window[curr_layout].update(visible=True)

			# TODO better list creation
			# fill Item tree
			root_item = generate_fs_tree(values['Browse'])

		# sort help
		elif curr_layout == '-Sort-' and event == '-Sort Help-':
			# display sort_help_layout as a popup
			help_text = 'Top x will find your favorite x elements (unordered)\nPartial Sort will sort the list in groups of x\nFull Sort will completely sort your list'
			sg.popup_ok(help_text)

		# TODO sort choice
		elif curr_layout == '-Sort-' and event.startswith('Continue'):
			# TODO get better way to generate list
			# get sort choice
			sort_algo = partial_quick_sort
			sort_args = []
			arr = root_item.get_children(3)
			try:
				k = int(values['-k-'])
			except:
				# maybe a popup here
				# doesn't let you run full sort without setting x
				continue
			if values['-Quick Select-']:
				# TODO not implemented in a savable way
				sort_args = [arr]
			elif values['-Partial Sort-']:
				sort_args = [arr, k]
			elif values['-Quick Sort-']:
				sort_args = [arr, 1]

			# run sort in a new thread
			thread_args = [sort_algo, sort_args]
			sort_thread = th.Thread(target=sort_worker, args=thread_args, daemon=True)
			sort_thread.start()	

			# change to comparison window
			window[curr_layout].update(visible=False)
			window[f'-Comparer-'].update(visible=True)
			curr_layout = '-Comparer-'
			# update window with first comparison
			opt1 = settings.gui_read_queue.get()
			opt2 = settings.gui_read_queue.get()
			window['-Opt1-'].update(opt1)
			window['-Opt2-'].update(opt2)

		# comparison choice
		elif curr_layout == '-Comparer-' and event in valid_choices and not done_sorting:
			# send choice to sort thread
			settings.gui_write_queue.put(event)

			# get next comparison
			opt1 = settings.gui_read_queue.get()
			opt2 = settings.gui_read_queue.get()
			if opt1 != None and opt2 != None:
				window['-Opt1-'].update(opt1)
				window['-Opt2-'].update(opt2)
				# save sort progress
				history[0] = settings.save_queue.get()
			else:
				# sorting is finished
				# display results
				done_sorting = True
				results = settings.gui_read_queue.get()
				curr_layout = '-Results-'
				window['-Comparer-'].update(visible=False)
				window[curr_layout].update(visible=True)
				window['-Results Table-'].update(results)

		# TODO implement sorting history

		# TODO prevent popup if already set
		# save sorting progress
		elif event == '-Save-' and history[0] != None and curr_layout == '-Comparer-':
			fname = sg.popup_get_file('Save current sorting progress', initial_folder=save_dir, save_as=True)
			if fname != None:
				f = open(fname, 'wb')
				pickle.dump(history[0], f)
				f.close()

		# save results
		elif event == '-Save Result-' and curr_layout == '-Results-':
			fname = sg.popup_get_file('Save results to a txt file', initial_folder=save_dir, save_as=True)
			if fname != None:
				table = window['-Results Table-'].Values
				results = [arr[0] + '\n' for arr in table]
				f = open(fname, 'w')
				f.writelines(results)
				f.close()
				
	window.close()

def load_save(save):
	""" 
		Loads a save from an unpickled save file 
		Returns a sort thread obj to be started
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
	thread_args = [sort_algo, sort_args]
	sort_thread = th.Thread(target=sort_worker, args=thread_args, daemon=True)
	return sort_thread	

if __name__ == "__main__":
	main()
