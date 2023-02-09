"""
	Gui window layouts
"""
import PySimpleGUI as sg

font = 'Courier 64'
button_font = 'Courier 32'
save_dir = 'saves/'
sg.theme('Dark Grey 12')

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
]]
