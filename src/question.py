import os
import json

#  Debug
import pdb

class Question:
	def __init__(self, verb, tense, subject_pronoun, correct_answer):
		self.message = "\n".join([verb, tense, subject_pronoun])
		self.correct_answer = correct_answer
		self.response = ""

	def Ask(self, progress_string):
		os.system('clear')
		print(progress_string)
		self.response = input(self.message + " ")

	def Grade(self):
		return self.response == self.correct_answer

	def __str__(self):
		return self.__repr__()

	def __repr__(self): 
		return self.question + "\n"


class QuestionsList(list):

	def __init__(self, language = None):
		self.language_dir = "languages/"+ language
		self.language_tenses = None
		self.language_subjects = None
		self.verbs = None


	def load_tenses(self):
		with open(self.language_dir + "/tenses.json") as f:
			self.language_tenses = json.load(f)


	def load_subject_pronouns(self):
		with open(self.language_dir + "/subject_pronouns.json") as f:
			self.subject_pronouns = json.load(f)


	def load_verbs(self):
		with open(self.language_dir + "/verbs.json") as f:
			self.verbs = json.load(f)


	def Build(self, selector_verb = None, selector_tense = None):
		self.load_tenses()
		self.load_subject_pronouns()
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
					subject_pronoun = self.subject_pronouns[subject_code]

					self.append(
						Question(verb, tense_name, subject_pronoun, conjugation)
					)
