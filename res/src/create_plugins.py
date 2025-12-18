import os



def read_everything(data_folder):
	print('\nreading data folder')
	objs, obj_paths, obj_names = [], [], []
	started = False
	folders = os.listdir(data_folder)
	folders.append('')
	folders.sort()
	for folder in  folders:
		if os.path.isdir(data_folder + folder):
			text_files = os.listdir(data_folder + folder)
			text_files.sort()
			for text_file in text_files:
				if os.path.isfile(data_folder + folder + os.sep + text_file) == False:
					continue
				if len(folder + text_file)  < 80: # just for displaying / max len = 44(currently)
					count = 80 - len(folder + text_file)
					spaces = ''
					for i in range(0, count):
						spaces += ' '
				print('	reading: ' + folder + os.sep + text_file + spaces, end = '\r', flush= True)
				with open(data_folder + folder + os.sep + text_file, 'r') as source_file:
					lines = source_file.readlines()
				index = 0
				for line in lines:
					index += 1
					if line[:1] == '#':
						continue
					elif line == '\n':
						continue
					elif line == '\t\n':
						continue
					elif line == '\t\t\n':
						continue
					elif line[:1] != '\t' or index == len(lines):
						if started == True:
							objs.append(txt.replace('<', '&#60;').replace('>', '&#62;'))
							obj_paths.append(txt2)
							obj_names.append(txt3.replace('\t', ' '))
							started = False
						txt = line
						if folder != '':
							folder_fix = folder + os.sep
						else:
							folder_fix = folder
						txt2 = 'data' + os.sep + folder_fix + text_file
						txt3 = line[:len(line)-1]
						started = True
					else:
						if started == True:
							txt += line
	print('	\n	DONE')
	return objs, obj_paths, obj_names


def remove_asteroids(data_folder, targetfile):
	systemcount = 0
	asteroidcount = 0
	wlines = []
	sourcefile = data_folder + "map systems.txt"
	with open(sourcefile, "r") as sourcefile:
		lines = sourcefile.readlines()
	for line in lines:
		if line[:6] == "system":
			systemcount = systemcount + 1 
			wlines.append("\n")
			wlines.append(line)
		if line[:23] == '	asteroids "small rock"':
			asteroidcount = asteroidcount + 1
			wlines.append('	remove asteroids "small rock"\n')
		if line[:24] == '	asteroids "medium rock"':
			asteroidcount = asteroidcount + 1
			wlines.append('	remove asteroids "medium rock"\n')
		if line[:23] == '	asteroids "large rock"':
			asteroidcount = asteroidcount + 1
			wlines.append('	remove asteroids "large rock"\n')
		if line[:24] == '	asteroids "small metal"':
			asteroidcount = asteroidcount + 1
			wlines.append('	remove asteroids "small metal"\n')
		if line[:25] == '	asteroids "medium metal"':
			asteroidcount = asteroidcount + 1
			wlines.append('	remove asteroids "medium metal"\n')
		if line[:24] == '	asteroids "large metal"':
			asteroidcount = asteroidcount + 1
			wlines.append('	remove asteroids "large metal"\n')
	with open(targetfile, "w") as targetfile:
		targetfile.writelines("# number of systems: " + str(systemcount) + "\n")	
		targetfile.writelines("# number of asteroid entries: " + str(asteroidcount) + "\n")
		for line in wlines:
			targetfile.writelines(line)

def run():
	data_folder = 'tmp/release/data/'
	objs, obj_paths, obj_names = read_everything(data_folder)
	# too.many.asteroids
	try:
		remove_asteroids(data_folder, 'plugins/too.many.asteroids/data/asteroids.txt')
	except:
		print('failed to create too.many.asteroids')
	else:
		print('successfully created too.many.asteroids')


if __name__ == "__main__":
	run()