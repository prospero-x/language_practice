from abc import ABCMeta, abstractmethod


class VerbInterface(metaclass = ABCMeta):

	@abstractmethod
	def get_conjugations(self, verbs):
		'''
		MUST return a dictionary structured as follows:
		{
		    'verb_1': {
	            'tense_1': {
	                'pronoun_1': 'conjudated_verb_1'.
	                ...
	                ...
	            }
		    } 
		}
		'''
		raise NotImplementedError

	@abstractmethod
	def tenses(self):
		'''
		MUST return a set of strings, which will be used to enforce
		agreement rules on tenses specified in verbquiz_conf.yml.

		The tenses in the dictionary returned by get_conjugations must
		be a subset of the set returned by this method.
		'''
		raise NotImplementedError

	@abstractmethod
	def subject_pronouns(self):
		'''
		MUST return a set of strings, which will be used to enforce
		agreement rules on optional pronouns specified in verbquiz_conf.yml.

		The subject pronouns in the dictionary returned by get_conjugations must
		be a subset of the set returned by this method.
		'''
		raise NotImplementedError
