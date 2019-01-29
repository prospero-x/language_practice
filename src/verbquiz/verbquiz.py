#  Generic
import os
from random import randint
import time
from cached_property import cached_property

#  Project
from .grader import Grader
from .question import QuestionsList
from .inputs import Getch


class Quiz:

	def __init__(self, language, max_questions = None):
		self.language = language
		self.max_questions = int(max_questions) if max_questions else None

		#  Initialize the questions list
		self.questions = QuestionsList(language = language)

		#  Prepare for runs
		self.times_run = 0

	def _run(self):
		question_num = 0
		total_questions = (
			min(self.max_questions, len(self.questions))
			if self.max_questions
			else len(self.questions)
		)

		#  Each time a question is asked, it is removed from self.questions
		#  and placed in questions_asked. After all questions are asked, the
		#  questions are copied back.
		questions_asked = []

		#  Start the quiz.
		start = end = None
		for _ in range(total_questions):

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

			questions_asked.append(question)

		self.questions.extend(questions_asked)

		total_seconds = (end - start)
		self.times_run += 1
		return start, total_seconds, questions_asked

	def Run(self):
		#  No questions, nothing to do..
		if len(self.questions) == 0:
			print(
				"Quiz has not been initialized with any questions. "
				"Nothing to do..."
			)
			return

		#  Print quiz introduction
		os.system('clear')
		print(self.get_description)
		print("Press any key to begin.")
		listener = Getch()
		listener()
		os.system('clear')

		#  Ask the questions
		test_start, total_seconds, questions_asked = self._run()

		#  Score the result
		Grader.grade_quiz(questions_asked, self.language, test_start, total_seconds)

	@cached_property
	def get_description(self):
		descr = "language: " + self.language + "\n"
		verbs = set()
		tenses = set()
		pronouns = set()
		for question in self.questions:
			verbs.add(question.verb)
			tenses.add(question.tense)
			pronouns.add(question.pronoun)

		descr += "verbs(%d): " % len(verbs) + " - ".join(verbs) + "\n"
		descr += "tenses(%d): " % len(tenses) + " - ".join(tenses) + "\n"
		descr += "pronouns:(%d): " % len(pronouns) + " - ".join(pronouns) + "\n"
		descr += "total questions: %d" % len(self.questions) + "\n"

		if self.max_questions:
			descr += "max questions: %d" % self.max_questions
		return descr
