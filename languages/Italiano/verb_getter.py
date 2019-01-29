import json
import os
from cached_property import cached_property

from interface import VerbInterface
from .download import download_conjugations


class VerbGetter(VerbInterface):
	def __init__(self, language):
		#  So the executable running from project root can find the verbstore.
		self.verbstore_path = "languages/%s/verbstore" % language
		self.local_verbs = self._load_verbs_from_local_verbstore()

	def get_conjugations(self, verbs):
		all_conjugations = {}
		for verb in verbs:
			#  First look up the data locally. If it's not there, we need
			#  to download from the web.
			try:
				conjugations = self._get_conjugations_from_local_verbstore(verb)
			except KeyError:
				conjugations = self._download_conjugations_from_web(verb)

			all_conjugations[verb] = conjugations

		return all_conjugations

	def _get_conjugations_from_local_verbstore(self, verb):
		return self.local_verbs[verb]

	def _download_conjugations_from_web(self, verb):
		print("Could not find %s in local verbstore, downloading from web..." % verb)
		conjugations = download_conjugations(verb, self.subject_pronouns)

		#  We always want to update the local verbstore with new verbs.
		self._save_new_conjugations_to_local_verbstore(verb, conjugations)
		return conjugations

	def _load_verbs_from_local_verbstore(self):
		#  The language is used to get the path to the verbstore.
		#  This is assuming that the code will be run from the top-level
		#  directory.
		try:
			with open('%s/verbs.json' % self.verbstore_path, 'r') as f:
				verbs = json.load(f)
			return verbs
		except FileNotFoundError:
			return {}

	def _save_new_conjugations_to_local_verbstore(self, verb, conjugations):
		#  Overwrite the current verbstore, or create one if it doesn't exist.
		#  While this is an expensive operation to perform for each verb, it
		#  should not be a problem since the user will probably not take a
		#  quiz with many verbs.
		try:
			with open("%s/verbs.json" % self.verbstore_path, 'r') as f:
				existing_data = json.load(f)

		except FileNotFoundError:
			existing_data = {}

		finally:
			existing_data[verb] = conjugations
			#  Might need to create a directory
			if not os.path.exists(self.verbstore_path):
				os.makedirs(self.verbstore_path)

			#  Write the data to the json
			with open("%s/verbs.json" % self.verbstore_path, 'w') as f:
				json.dump(existing_data, f)

	@cached_property
	def tenses(self):
		return {
			'Il Presente',
			'L\'Imperfetto',
			'Il Passato Remoto',
			'Il Futuro Semplice',
			'Il Passato Prossimo',
			'Il Trapassato Prossimo',
			'Il Trapassato Remoto',
			'Il Futuro Anteriore',
			'Il Congiuntivo',
			'L\'Imperfetto del Congiuntivo',
			'Il Congiuntivo Passato',
			'Il Trapassato Congiuntivo',
		}

	@cached_property
	def subject_pronouns(self):
		return {"io", "tu", "lui/lei", "noi", "voi", "loro"}
