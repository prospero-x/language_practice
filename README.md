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

This file includes both required and optional values to pass to the quiz before running. Required: 
1. language (one of the directories under languages/)

Optional:
1. verbs
2. tenses
3. pronouns
4. max_questions

For each of the optional parameters in (verbs, tenses, pronouns), a list of values may be passed which will select a subset of verbs, tenses, and pronouns (respectively) from languages/LANGUAGE/verbs.json. If no values are provided, then all values in verbs.json will be used for questions in the quiz. 

If max_questions is defined, the quiz will choose a subset of MAX_QUESTIONS to ask on the quiz. Otherwise, all one question for each possible combination of verbs, tenses, and pronouns will be asked.
## Quiz Structure

This is a verb quiz.  The fundamental building blocks are:
1. verbs
2. tenses
3. pronouns

That is to say, each for a given language, any verb can be conjugated into a certain
tense, and further inflected to agree with different subject pronouns. For each question in the quiz, you will be given a verb in language X (specified in verbquiz_conf.yml) in the infinitive form, along with a tense and a subject pronoun. Your task will be to conjugate and inflect the verb correctly. Correct answeres are in languages/X/verbs.json.

## Adding a new language

To add a new language for the quiz, create a new directory under languages/ called 
LANGUAGE_NAME. The three required files under languages/LANGUAGE_NAME/ are _verbs.json_, _tenses.json_, and _subject_pronouns.json_. Examples below are given for languages/Italiano/:

1. _verbs.json_: 
```json
{
	"avere": {
		"a": {
			"1": "ho",
			"2": "hai",
			"3": "ha",
			"4": "abbiamo",
			"5": "avete",
			"6": "hanno"
		},
		"b": {
		    ...
		    ...
		}
	}
}
```

2. _tenses.json_:
```json
 {
	"a": "Il Presento",
    ...
    ...
}
```


3. _subject_pronouns.json_:
```json
{
	"1": "io",
	...
	...
}
```

Note that they keys in _tenses.json_ and _subject_pronouns.json_ **must** match the keys in verbs.json. I.e., if you have key "a" for tense one in _verbs.json_ "a" must be a defined key in tenses.json, and the same for _subject_pronouns.json_

A fourth optional file is _grader_phrases.json_, in which you can specify phrases that the quiz will display to you when grading the results of the quiz. Note that the keys **must** be identical to the ones shown here. If any are missing, the program will fall back on the default English phrases.

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