from input_validation import (
	verify_language,
	verify_verbs,
	verify_tenses,
	verify_pronouns,
	verify_max_questions,
	warn_quiz_length
)
from importlib import import_module
import verbquiz

CONF_FILE = 'verbquiz_conf.yml'


def import_verb_getter(language):
	verb_getter_module = import_module('languages.%s.verb_getter' % language)
	verb_getter = verb_getter_module.VerbGetter(language)
	return verb_getter


if __name__ == '__main__':
	#  Load quiz arguments.
	quiz_args = verbquiz.get_inputs_from_config(CONF_FILE)

	#  Initilize the quiz object
	language = verify_language(quiz_args)
	max_questions = verify_max_questions(quiz_args)
	quiz = verbquiz.Quiz(language, max_questions)

	#  Verify verbs before getting them
	num_verbs = verify_verbs(quiz_args)
	verb_getter = import_verb_getter(language)
	verbs = verb_getter.get_conjugations(quiz_args['verbs'])

	#  Verify the rest of the arguments
	num_tenses = verify_tenses(quiz_args, verb_getter.tenses)
	num_pronouns = verify_pronouns(quiz_args, verb_getter.subject_pronouns)
	warn_quiz_length(num_verbs, num_tenses, num_pronouns, max_questions)

	#  Pull in the rest of the parameters now that they have been verified
	tenses = quiz_args['tenses']
	pronouns = quiz_args.get('pronouns')  # OK if these are not defined

	#  Build the questions based on the user-specified inputs
	quiz.questions.Build(verbs, tenses, pronouns)

	#  Run the quiz.
	quiz.Run()
