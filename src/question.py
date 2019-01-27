import os
import sys
from grade import Grade
import json
import pdb

class Question:
	def __init__(self, verb, tense, person, correct_answer):
		self.question = "\n".join([verb, tense, person])
		self.correct_answer = correct_answer
		self.response = ""

	def Ask(self, progress_string):
		os.system('clear')
		print(progress_string)
		self.response = input(self.question + " ")

	def Grade(self):
		if self.response == self.correct_answer:
			Grade.correct_answer(self.question, self.response)
			return 1
		else:
			Grade.incorrect_answer(self.question, self.response, self.correct_answer)
			return 0


	def __str__(self):
		return self.__repr__()

	def __repr__(self): 
		return self.question + "\n"


class QuestionsList(list):

	def __init__(self, language = None):
		pdb.set_trace()
		self.language_dir = language
		self.language_tenses = None
		self.language_subjects = None
		self.verbs = None


	def load_tenses(self):
		with open(self.language_dir + "/tenses.json") as f:
			self.language_tenses = json.load(f)


	def load_subjects(self):
		with open(self.language_dir + "/subjects.json") as f:
			self.language_subjects = json.load(f)


	def load_verbs(self):
		with open(self.language_dir + "/verbs.json") as f:
			self.verbs = json.load(f)


	def Build(self, selector_verb = None, selector_tense = None):
		self.load_tenses()
		self.load_subjects()
		self.load_verbs()


		for verb, tenses in self.verbs.items():
			# If a certain verb was specified at initialization, select only that verb.
			if selector_verb and verb != selector_verb:
				continue

			for tense_code, persons in tenses.items(): 
				# If a certain tense was specified at initialization, select 
				# only that tense
				if selector_tense and self.lanugages_tenses[tense_code] != selector_tense:
					continue

				tense_name = self.language_tenses[tense_code]
				for subject_code, conjugation in persons.items():
					subject = self.language_subjects[subject_code]

					self.append(
						Question(verb, tense_name, subject, conjugation)
					)
