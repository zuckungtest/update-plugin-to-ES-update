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
	# unpacking
	for file in archive.namelist():
		# if release
		if vpath == 'tmp/release/':
			if file.startswith('data/') or file.startswith('images/'):
				archive.extract(file, vpath)
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
	download(version, vRpath, vRzip)
	unpack(version, vRpath, lastmodifiedO)
	print('  DONE')


if __name__ == "__main__":
	run()
