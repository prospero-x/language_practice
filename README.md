## Running
 1. You'll need to install pew if you don't have it yet: 
```bash
pip install pew
```

2. Create a new virtual environment and install the required packages:
```bash
pew new custom_env_name
pip install -r requirements.txt
```

3. Specify options in verbquiz_conf.yml (see next section)
4. Run
```bash
./verbquiz
```
## verbquiz_conf.yml

This file includes both required and optional values to pass to the quiz before running.
Required: 
1. **language**  (must be a directory under "*languages/*")
2. **verbs** (must be a list)
3. **tenses** (must be a list)

Optional:
1. **pronouns** (subset of all pronouns, acts as a mask)
2. **max_questions** (limits the number of questions in verbquiz)

## Quiz Structure

This is a verb quiz.  The fundamental building blocks are:
1. verbs
2. tenses
3. pronouns

That is to say, each for a given language, any verb can be conjugated into a certain
tense, and further inflected to agree with different subject pronouns. For each question in the quiz, you will be given a verb in language X (specified in verbquiz_conf.yml) in the infinitive form, along with a tense and a subject pronoun. Your task will be to conjugate and inflect the verb correctly.

## Adding a new language

To add a new language named X, create a new directory under *languages/* called 
X. You **must** implement an interface called "VerbGetter" which inherits from *src/interface.VerbInterface*, and save it in fily *languages/X/verb_getter.py*. The base class for this interface is shown below:

```python
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

		The subject pronouns in the dictionary returned by get_conjugations
		must be a subset of the set returned by this method.
		'''
		raise NotImplementedError
```

In general, it is up to you how to implement this interface. For example, the implementation
in Italiano/ reads the conjugations from a web service as www.italian-verbs.com.

An optional file in *languages/X/* is _grader_phrases.json_, in which you can specify phrases that the quiz will display to you when grading the results of the quiz. Note that the keys **must** be identical to the ones shown here. If any are missing, the program will fall back on the default English phrases.

```json
{
	"grade_header_phrase": <your_custom_phrases_here>,
	"total_points_phrase": <your_custom_phrases_here>,
	"completion_time_phrase": "<your_custom_phrases_here>,
	"correct_answer_phrase": <your_custom_phrases_here>,
	"wrong_answer_phrase": <your_custom_phrases_here>,
	"wrong_answer_correction_phrase": <your_custom_phrases_here>
}
```

## Development
run this command from the project root directory:
```bash
export PYTHONPATH=$PYTHONPATH:$PWD/src
```

This will allow you to call the following:
```python
from interface import VerbInterface
```
in any of your source files under *languages/*.