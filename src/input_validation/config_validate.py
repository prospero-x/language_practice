from __future__ import print_function

from .directory import DirectoryStatus, validate_directory

CONF_FILE = "quiz_conf.yml"


class ConfigException(ValueError):
	def __init__(self, error_message):
		config_message = (
			" Please check %s to make sure you have the correct options."
			% CONF_FILE
		)
		super(ConfigException, self).__init__(error_message + config_message)


def verify_args(args):
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
		raise ConfigException("'language' must be specified.")

	#  Verify language value is a directory in 'languages'
	result = validate_directory('languages/%s' % args['language'])

	if result == DirectoryStatus.NOT_FOUND:
		raise ConfigException(
			"language '%s' does not exist under directory 'languages'"
			% args['language']
		)

	elif result == DirectoryStatus.NOT_A_DIRECTORY:
		raise ConfigException(
			"language '%s' must be a directory under 'languages'."
			% args['language']

		)