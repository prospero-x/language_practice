import os
import json

from output_color import OutputColor
from copy import deepcopy

#  Debug
import pdb

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
				#  Try to access the key. If any of these fail, they will trigger an KeyError
				#  and the default phrases will be used.
				phrase = str(custom_phrases[key])


			#  No exception. These custom phrases are OK.
			cls.phrases = deepcopy(custom_phrases)
		except Exception:
			#  It's valid for there to be no defined custom phrases. We will simply use 
			#  these default ones. 
			cls.phrases = cls.default_phrases


	@classmethod
	def print_correct_answer(cls, question):
		print(
			question.message + "\n"\
			+ OutputColor.BOLD \
			+ OutputColor.GREEN \
			+ "%s: \"" % cls.phrases['correct_answer_phrase']\
			+ question.response + "\""\
			+ OutputColor.END_COLOR \
			+ "\n\n"
		)

	@classmethod
	def print_incorrect_answer(cls, question):
		print(
			question.message + "\n" \
			+ OutputColor.BOLD \
			+ OutputColor.RED \
			+ "%s: \"" % cls.phrases['wrong_answer_phrase']\
			+ question.response + "\" " \
			+ OutputColor.END_COLOR
			+ "(%s \"" % cls.phrases['wrong_answer_correction_phrase'] \
			+ question.correct_answer \
			+ "\")" \
			+ "\n\n" 
		)

	@classmethod
	def grade_quiz(cls, questions, language, test_start, completion_time):
		cls.set_phrases(language)
		os.system('clear')
		total_correct = 0

		print(OutputColor.BOLD + cls.phrases['grade_header_phrase'] + OutputColor.END_COLOR)
		for question in questions:
			answered_correctly = question.Grade()
			if answered_correctly:
				cls.print_correct_answer(question)
				total_correct += 1
			else:
				cls.print_incorrect_answer(question)

		score = "%d/%d" % (total_correct, len(questions))
		print(
			OutputColor.BOLD \
			+ "%s: %s\n" % (cls.phrases['total_points_phrase'], score) \
			+ "%s: %ss" % (cls.phrases['completion_time_phrase'], completion_time) \
			+ OutputColor.END_COLOR
		)