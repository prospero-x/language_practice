from __future__ import print_function

from verify_config import load_args_from_config
from quiz import Quiz

#  Debug
import pdb

def gather_languages():
	if not S_ISDIR(mode):
		raise ConfigException(
			"language '%s' must be a directory under 'languages'." 
			% args['language']
		)

if __name__ == '__main__':
	#quiz_args = load_args_from_config()


	quiz = Quiz(
		"this is a test", 
		language = "Italiano",
		verb     = "avere"
	)
	quiz.Run()
