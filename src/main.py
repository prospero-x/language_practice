from input_validation import verify_args

import verbquiz


CONF_FILE = 'verbquiz_conf.yml'


def format_questions_args(quiz_args, mask):
	mask = set(mask)
	questions_args = {}
	for k in quiz_args.keys():
		if k in mask:
			questions_args[k + "_mask"] = set(quiz_args[k].copy()) or None
	return questions_args


if __name__ == '__main__':
	#  Load quiz arguments.
	quiz_args = verbquiz.get_inputs_from_config(CONF_FILE)
	verify_args(quiz_args)

	#  Initilize the quiz object
	language = quiz_args['language']
	quiz = verbquiz.Quiz(language)

	#  Build the question based on the quiz arguments
	questions_args = format_questions_args(
		quiz_args, ('verbs', 'tenses', 'pronouns')
	)
	quiz.questions.Build(**questions_args)

	#  Run the quiz.
	quiz.Run()
