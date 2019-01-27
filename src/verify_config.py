from __future__ import print_function

import yaml
import os
from stat import S_ISDIR

CONF_FILE = "quiz_conf.yml"

class ConfigException(ValueError):
	def __init__(self, error_message):
		config_message = (
			" Please check %s to make sure you have the correct options."
			% CONF_FILE
		)
		super(ConfigException, self).__init__(error_message + config_message)

def verify_args(args, mutex_args):
	'''
	In addition to verifying presence and type of arguments in
	CONF_FILE, this function also performs up-front checks that it is 
	safe to call Quiz.Run(), such as verifying that the value for 'language' 
	is a directory under languages.


	param args: all args gathered in CONF_FILE
	param mutex_args: subset of mutually exclusive args, exactly one of which 
	                  must be in args.
	'''

	#  Verify language was passed
	if 'language' not in args:
		raise ConfigException(
			"'language' must be specified."
		)

	#  Verify language value is a director in 'languages'
	try:
		mode = os.stat('languages/%s' % args['language']).st_mode
		if not S_ISDIR(mode):
			raise ConfigException(
				"language '%s' must be a directory under 'languages'." 
				% args['language']
		
			)
	except FileNotFoundError:
		raise ConfigException(
			"language '%s' does not exist under directory 'languages'"
			% args['language']
		)


	#  Mutually exclusive args: EXACTLY one must be passed
	mutex_args_provided = list( filter (lambda m: m in args, mutex_args) )         
	if not mex_args_provided:
		raise ConfigException(
			"At least one of ['%s'] must be specified." 
			% "', '".join(mutex_args)
		)
	elif len( mex_args_provided ) > 1:
		raise ConfigException(
			"No more than one out of ['%s'] can be defined."
			% "', '".join(mutex_args)
		)



def load_args_from_config(conf_file, mutex_args):
	try:
		with open(conf_file, 'r') as fstream:
			args = yaml.load(fstream)

		verify_args(args, mutex_args)
		return args

	except yaml.YAMLError as e:
		print("Yaml error: %s", e)

	except FileNotFoundError as e:
		print(e)