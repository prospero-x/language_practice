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

	def Build(self, verbs, tenses_mask, pronouns_mask=None):
		for v, all_tenses in verbs.items():
			for tense, inflections in all_tenses.items():
				if tense not in tenses_mask:
					continue

				for subject_pronoun, conjugation in inflections.items():
					#  If a certain pronoun was specified at initialization,
					#  select only that pronoun
					if pronouns_mask and subject_pronoun not in pronouns_mask:
						continue

					self.append(
						Question(v, tense, subject_pronoun, conjugation)
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