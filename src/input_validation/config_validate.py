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


def verify_language(args):
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


def verify_verbs(args):
	#  Verbs is a required argument
	if 'verbs' not in args:
		raise ConfigException("'verbs' must be specified.")

	#  Verbs must be iterable
	try:
		list(args['verbs'])
	except (TypeError, AttributeError):
		raise ConfigException("'verbs' must be a list.")

	num_verbs = len(args['verbs'])
	if num_verbs > 10:
		print(
			"\n\n!!! WARNING !!!\n\nYou have specified {num_verbs} verbs."
			" This could cause the quiz to be more than {num_questions} "
			"questions long. Are you sure you wish to continue?\n\nPress "
			"Enter to continue, or Ctrl + C to exit.".format(
				num_verbs = num_verbs,
				num_questions = num_verbs * 6
			)
		)

		#  Wait for either "Enter" or SIGINT from user.
		input()


def verify_tenses(args, allowed_tenses):
	#  Tenses is a required argument
	if 'tenses' not in args:
		raise ConfigException("'tenses' must be specified")

	#  Tenses must be iterable.
	try:
		list(args['tenses'])
	except (TypeError, AttributeError):
		raise ConfigException("'tenses' must be a list")


def verify_pronouns(args, allowed_pronouns):
	if 'pronouns' not in args:
		return

	try:
		pronouns = set(args['pronouns'])
	except (TypeError, AttributeError):
		raise ConfigException("'pronouns' must be a list")

	notallowed = pronouns - allowed_pronouns
	if len(notallowed) > 0:
		raise ConfigException(
			"'pronouns' was defined with unrecognized values: %s" % ", ".join(notallowed)
		)
