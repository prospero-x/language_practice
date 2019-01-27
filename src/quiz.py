#  Generic
import os
from random import randint
import time
from datetime import datetime

#  Project
from grader import Grader
from question import QuestionsList
from output_color import OutputColor

#  Debug 
import pdb

class Quiz:

	def __init__( self, name, language, verb = None, tense = None):
		self.name = name
		self.language = language
		self.verb = verb
		self.tense = tense

		#  Build the questions list
		self.questions = QuestionsList(language = language)
		self.questions.Build(selector_verb = verb, selector_tense = tense)
		if len(self.questions) == 0:
			self._print_quiz_not_initialized_error_message()
			return

		#  Prepare for runs
		self.times_run = 0

	def _print_quiz_not_initialized_error_message(self):
		if self.verb:
			indicator_word = "_verb"
			indicator_value = self.verb

		else:
			indicator_word = "_tense"
			indicator_value = self.tense
		print(
			  "Quiz has not been initialized with any questions" \
			+ "for _language:`%s` " % self.language \
			+ "and %s:`%s`. \n" % (indicator_word, indicator_value) \
			+ "Nothng to do..."
		)

	def _run(self):
		question_num = 0
		total_questions = len(self.questions)

		#  Each time a question is asked, it is removed from self.questions
		#  and placed onto the run_buffer. After all questions are asked, the
		#  questions are copied back.
		run_buffer = []

		#  Start the quiz.
		start = end = None
		while self.questions:

			#  Increment the progress label.
			question_num += 1
			progress_string = "(%d/%d)" % (question_num, total_questions)

			#  Get the next question at random
			question_index = randint(0, len(self.questions) - 1)

			#  Remove it from the list. this ensures no question gets asked twice.
			question = self.questions.pop(question_index)

			#  Ask the question
			start = start if start else time.time()
			question.Ask(progress_string)
			end = time.time()
			
			run_buffer.append(question)

		self.times_run += 1
		self.questions = run_buffer.copy()
		
		completion_time = "%.2f" % ( end - start )
		return start, completion_time
		

	def Run(self):
		test_start, completion_time = self._run()
		Grader.grade_quiz(self.questions, self.language, test_start, completion_time)



	