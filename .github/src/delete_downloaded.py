import os
import shutil


def run():
	if os.path.isdir('.github/tmp/release/data/'):
		print('deleting [release] data')
		shutil.rmtree('.github/tmp/release/data/')
		shutil.rmtree('.github/tmp/release/images/')
		print('DONE')
		print('')
	if os.path.isfile('.github/tmp/release/changelog.txt'):
		print('deleting [release] changelog')
		os.remove('.github/tmp/release/changelog.txt')
		print('DONE')
		print('\n')


if __name__ == "__main__":
	run()