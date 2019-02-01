from __future__ import print_function

from .directory import DirectoryStatus, validate_directory

CONF_FILE = "quiz_conf.yml"

DEFAULT_MAX_QUESTIONS = 50


class ConfigException(ValueError):
	def __init__(self, error_message):
		config_message = (
			".\nPlease check %s to make sure you have the correct options."
			% CONF_FILE
		)
		super(ConfigException, self).__init__(error_message + config_message)


def verify_language(args):
	#  Verify language was passed
	if 'language' not in args:
		raise ConfigException("'language' must be specified.")

	#  Verify language value is a directory in 'languages'
	language = args['language']
	result = validate_directory('languages/%s' % language)

	if result == DirectoryStatus.NOT_FOUND:
		raise ConfigException(
			"language '%s' does not exist under directory 'languages'"
			% language
		)

	elif result == DirectoryStatus.NOT_A_DIRECTORY:
		raise ConfigException(
			"language '%s' must be a directory under 'languages'."
			% language

		)
	return language


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
	return num_verbs


def warn_quiz_length(num_verbs, num_tenses, num_pronouns, max_q = None):
	global DEFAULT_MAX_QUESTIONS

	#  If the user defined a value for max_questions, no need to warn
	#  here because the quiz will be MAX_QUESTIONS long.
	if max_q:
		return

	num_questions = num_verbs * num_tenses * num_pronouns
	if num_questions > DEFAULT_MAX_QUESTIONS:
		print(
			"\n\n!!! WARNING !!!\n\nYou have specified {num_verbs} verbs"
			" and {num_tenses} tenses. With {num_pronouns} pronouns, this"
			"  will cause the quiz to be {num_questions} questinos long."
			" Are you sure you wish to continue?\n\nPress"
			" any key to continue, or Ctrl + C to exit.".format(
				num_verbs = num_verbs,
				num_tenses = num_tenses,
				num_pronouns = num_pronouns,
				num_questions = num_questions
			)
		)

		#  Wait for either "Enter" or SIGINT from user.
		input()


def verify_tenses(args, allowed_tenses):
	#  Tenses is a required argument
	if 'tenses' not in args:
		raise ConfigException("'tenses' must be specified")

	#  Tenses must be iterable.
	tenses = args['tenses']
	try:
		list(tenses)
	except (TypeError, AttributeError):
		raise ConfigException("'tenses' must be a list")

	return len(tenses)


def verify_pronouns(args, allowed_pronouns):
	if 'pronouns' not in args:
		return len(allowed_pronouns)

	try:
		pronouns = set(args['pronouns'])
	except (TypeError, AttributeError):
		raise ConfigException("'pronouns' must be a list")

	notallowed = pronouns - allowed_pronouns
	if len(notallowed) > 0:
		raise ConfigException(
			"'pronouns' was defined with unrecognized values: %s"
			% ", ".join(notallowed)
		)

	return len(pronouns)


def verify_max_questions(args):
	if 'max_questions' not in args:
		return None

	max_questions = args['max_questions']
	try:
		int(max_questions)
	except ValueError:
		raise ConfigException(
			"'max_questions' was defined with an invalid integer: `%s`"
			% max_questions
		)

	return max_questions


