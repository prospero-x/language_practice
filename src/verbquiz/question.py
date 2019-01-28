import json


def load_mapping(dirname):
	if dirname is None:
		return None

	with open(dirname) as f:
		mapping = json.load(f)
	return mapping


class Question:
	def __init__(self, verb, tense, pronoun, correct_answer):
		self.verb = verb
		self.tense = tense
		self.pronoun = pronoun
		self.message = " - ".join([verb, tense, pronoun])
		self.correct_answer = correct_answer
		self.response = ""

	def Ask(self, progress_string):
		print(progress_string)
		self.response = input(self.message + " ")

	def Grade(self):
		return self.response == self.correct_answer

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return self.message + "\n"


class QuestionsList(list):

	def __init__(self, language = None):
		self.language_dir = "languages/" + language

	def Build(self, verbs_mask=None, tenses_mask=None, pronouns_mask=None):
		tense_names = load_mapping(self.language_dir + "/tenses.json")
		pronoun_names = load_mapping(
			self.language_dir + "/subject_pronouns.json"
		)
		verbs = load_mapping(self.language_dir + "/verbs.json")

		for v, tenses in verbs.items():
			# If a certain verb was specified at initialization, select only
			# that verb.
			if verbs_mask and v not in verbs_mask:
				continue

			for tense_code, persons in tenses.items():
				# If a certain tense was specified at initialization, select
				# only that tense
				tense_name = tense_names[tense_code]
				if tenses_mask and tense_name not in tenses_mask:
					continue

				tense_name = tense_names[tense_code]
				for pronoun_code, conjugation in persons.items():
					#  If a certain pronoun was specified at initialization,
					#  select only that pronoun
					pronoun_name = pronoun_names[pronoun_code]
					if pronouns_mask and pronoun_name not in pronouns_mask:
						continue

					self.append(
						Question(v, tense_name, pronoun_name, conjugation)
					)

	def append(self, other):
		if not isinstance(other, Question):
			raise TypeError(
				"attempting to append object of type %s to QuestionsList"
				% type(other)
			)

		super(QuestionsList, self).append(other)

	def extend(self, iterable):
		for other in iterable:
			if not isinstance(other, Question):
				raise TypeError(
					"attempting to extend list containing object of type %s "
					% type(other) + "to QuestionsList"
				)

		super(QuestionsList, self).extend(iterable)

	def insert(self, other):
		if not isinstance(other, Question):
			raise TypeError(
				"attempting to insert object of type %s into QuestionsList"
				% type(other)
			)

		super(QuestionsList, self).append(other)

	def __repr__(self):
		s = ""
		for n, q in enumerate(self):
			s += "%d: %s" % (n + 1, q)
		return s

	def __str__(self):
		return self.__repr__()