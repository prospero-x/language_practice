import os
import json

from .output import Output
from copy import deepcopy


class Grader:
	default_phrases = {
		"grade_header_phrase": "Quiz Evaluation",
		"total_points_phrase": "Total Points",
		"completion_time_phrase": "Time to Complete Quiz",
		"correct_answer_phrase": "You gave the correct response",
		"wrong_answer_phrase": "You gave an incorrect response",
		"wrong_answer_correction_phrase": "The correct response was"
	}

	@classmethod
	def set_phrases(cls, language):
		#  Custom grade phrases can be provided. If none are found, defaults are
		#  used.
		try:
			with open("languages/%s/grader_phrases.json" % language, 'r') as f:
				custom_phrases = json.load(f)

			#  Reaching this point without an exception only proves that the file
			#  exists and is in proper json format. We still need to ensure that
			#  all the default fields can be overridden and that they're strings.
			for key in cls.default_phrases.keys():
				#  Try to access the key. If any of these fail, they will trigger
				#  a KeyError and the default phrases will be used.
				str(custom_phrases[key])

			#  No exception. These custom phrases are OK.
			cls.phrases = deepcopy(custom_phrases)
		except Exception:
			#  It's valid for there to be no defined custom phrases. We will simply use
			#  these default ones.
			cls.phrases = cls.default_phrases

	@classmethod
	def print_correct_answer(cls, question):
		correct_answer_phrase = Output.bold_green_str(
			'\n%s: "%s"' % (
				cls.phrases['correct_answer_phrase'],
				question.response
			)
		)
		print(question.message + correct_answer_phrase + "\n\n")

	@classmethod
	def print_incorrect_answer(cls, question):
		wrong_answer_phrase = Output.bold_red_str(
			'\n%s: "%s" ' % (
				cls.phrases['wrong_answer_phrase'],
				question.response
			)
		)

		correction_phrase = (
			'(%s "%s")\n\n' % (
				cls.phrases['wrong_answer_correction_phrase'],
				question.correct_answer
			)
		)

		print(
			question.message + wrong_answer_phrase + correction_phrase
		)

	@classmethod
	def grade_quiz(cls, questions, language, test_start, total_seconds):
		cls.set_phrases(language)
		os.system('clear')
		total_correct = 0

		print(Output.bold_str(cls.phrases['grade_header_phrase']))
		for question in questions:
			answered_correctly = question.Grade()
			if answered_correctly:
				cls.print_correct_answer(question)
				total_correct += 1
			else:
				cls.print_incorrect_answer(question)

		score = "%d/%d" % (total_correct, len(questions))

		minutes = int(total_seconds / 60)
		seconds_remainder = total_seconds % 60
		completion_time = "%dm %0.2fs" % (minutes, seconds_remainder)
		print(
			Output.bold_str(
				"%s: %s" % (cls.phrases['total_points_phrase'], score)
			)
		)
		print(
			Output.bold_str(
				"%s: %s" % (cls.phrases['completion_time_phrase'], completion_time)
			)
		)