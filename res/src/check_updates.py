import requests
import json
from datetime import datetime, timedelta
import time
import os
import zipfile
import shutil



def decide_update(vpath, vapi, vchangelog):
	print('  checking the online changelog/data folder')
	# check for folder
	if not os.path.isdir('tmp/'):
		os.mkdir('tmp/')
	if not os.path.isdir(vpath):
		os.mkdir(vpath)
	# get last modified changelog
	request = requests.get(vapi, allow_redirects=True, timeout=30)
	data = request.json()
	lastmodifiedO = datetime.strptime(data[0]['commit']['committer']['date'],'%Y-%m-%dT%H:%M:%SZ')
	if vpath == 'tmp/continuous/': # request last modified data folder instead
		newrequest = requests.get('https://api.github.com/repos/endless-sky/endless-sky/commits?path=data&page=1&per_page=1', allow_redirects=True, timeout=30) 
		data = newrequest.json()
		lastmodifiedO = datetime.strptime(data[0]['commit']['committer']['date'],'%Y-%m-%dT%H:%M:%SZ')
	# get version number
	request = requests.get(vchangelog)
	with open(vpath + 'changelog.txt', 'wb') as changelog:
		changelog.write(request.content) # downloading the changelog
	with open(vpath + 'changelog.txt', 'r') as sourcefile:
		onlineversion = sourcefile.readline().replace('Version ', '').replace('\n', '') # result example: 0.10.10
	# check for local data
	if not os.path.isfile(vpath + 'check.txt'):
		# create a new check.txt
		print('  no local data found, creating it now')
		with open(vpath + 'check.txt', 'w') as target:
			target.writelines('version=' + onlineversion + '\n')
			target.writelines('lastUpdate=' + str(lastmodifiedO)+ '\n')
		return True, onlineversion, lastmodifiedO
	# local data is there
	else:
		print('  found local data, comparing now')
		with open(vpath + 'check.txt', 'r') as source:
			localversion = source.readline().replace('version=', '').replace('\n', '')
			uDate = datetime.strptime(source.readline().replace('lastUpdate=', '').replace('\n', ''),'%Y-%m-%d %H:%M:%S')
		if uDate != lastmodifiedO:
			print('  online and local data is different')
			with open(vpath + 'check.txt', 'w') as target:
				target.writelines('version=' + onlineversion + '\n')
				target.writelines('lastUpdate=' + str(lastmodifiedO)+ '\n')
			return True, onlineversion, lastmodifiedO
		else:
			print('  online and local data is the same')
			return False, onlineversion, lastmodifiedO
	

def download(version, vpath, vzip):
	# downloading zip
	if vpath == 'tmp/release/':
		vzip = vzip.replace('0.10.10', version)
	print('  downloading now')
	request = requests.get(vzip, allow_redirects=True, timeout=30)
	with open(vpath + version + '.zip', 'wb') as zipped: # creating zip file
		zipped.write(request.content)
	print('    download complete')


def unpack(version, vpath, lastmodifiedO):
	# modifying index.html
	print('  unpacking zip')
	archive = zipfile.ZipFile(vpath + version + '.zip')
	os.remove(vpath + version + '.zip')
	print('    unpacking done')


def run():
	# checking for Release update
	print('[release version]')
	vRpath = 'tmp/release/'
	vRapi = 'https://api.github.com/repos/endless-sky/endless-sky/commits?path=changelog&page=1&per_page=1'
	vRchangelog = 'https://github.com/endless-sky/endless-sky/raw/refs/heads/master/changelog'
	vRzip = 'https://github.com/endless-sky/endless-sky/releases/download/v0.10.10/EndlessSky-win64-v0.10.10.zip' # 0.10.10 will be replaced with current version	
	update, version, lastmodifiedO = decide_update(vRpath, vRapi, vRchangelog)
	if update == True:
		download(version, vRpath, vRzip)
		unpack(version, vRpath, lastmodifiedO)
		print('  DONE')
	else:
		print('  ABORTING')
	#print('')
	# checking for Android update
	#print('[android version]')
	#vApath = 'tmp/android/'
	#vAapi = 'https://api.github.com/repos/thewierdnut/endless-mobile/commits?path=changelog&page=1&per_page=1'
	#vAchangelog = 'https://github.com/thewierdnut/endless-mobile/raw/refs/heads/android/changelog'
	#vAzip = 'https://github.com/thewierdnut/endless-mobile/archive/refs/heads/android.zip'	
	#update, version, lastmodifiedO = decide_update(vApath, vAapi, vAchangelog)
	#if update == True:
	#	download(version, vApath, vAzip)
	#	unpack(version, vApath, lastmodifiedO)
	#	print('  DONE')
	#else:
	#	print('  ABORTING')
	#print('')
	# checking for Continous update
	#print('[continuous version]')
	#vCpath = 'tmp/continuous/'
	#vCapi = 'https://api.github.com/repos/endless-sky/endless-sky/commits?path=changelog&page=1&per_page=1'
	#vCchangelog = 'https://github.com/endless-sky/endless-sky/raw/refs/heads/master/changelog'
	#vCzip = 'https://github.com/endless-sky/endless-sky/archive/refs/heads/master.zip'
	#update, version, lastmodifiedO = decide_update(vCpath, vCapi, vCchangelog)
	#if update == True:
	#	download(version, vCpath, vCzip)
	#	unpack(version, vCpath, lastmodifiedO)
	#	print('  DONE')
	#else:
	#	print('  ABORTING')
	#print('')


if __name__ == "__main__":
	run()
