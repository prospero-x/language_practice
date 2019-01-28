from __future__ import print_function

import yaml
import sys

try:
	#  Unix
	import tty
	import termios
except ImportError:
	#  Windows
	import msvcrt


def get_inputs_from_config(conf_file):
	try:
		with open(conf_file, 'r') as fstream:
			args = yaml.load(fstream)
		return args

	except yaml.YAMLError as e:
		print("Yaml error: %s" % e)

	except FileNotFoundError as e:
		print(e)


#  _Getch is credited to Danny Yoo, who posted a general solution
#  to ActiveState on Friday, June 21, 2002
#  http://code.activestate.com/recipes/134892/
class Getch:
	'''
	Gets a single character from standard input.  Does not echo to the
	screen.
	'''
	def __init__(self):
		if "msvcrt" in sys.modules:
			self.impl = _GetchWindows()
		else:
			self.impl = _GetchUnix()

	def __call__(self):
		return self.impl()


class _GetchUnix:

	def __call__(self):
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch


class _GetchWindows:

	def __call__(self):
		return msvcrt.getch()
