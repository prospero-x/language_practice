from question import QuestionsList
from random import randint
import os
from grade import Grade
import pdb
import time
import pytz
from datetime import datetime
import argparse
from output_color import OutputColor


def get_current_time(timezone):
	fmt = "%Y-%m-%d %H:%M:%S %Z"
	dt_now = datetime.now()
	return pytz.timezone(timezone).localize(dt_now).strftime(fmt)

class Quiz:

	def __init__(
		self, 
		name, 
		language = None, 
		verb = None, 
		tense = None, 
		timezone = "UTC",
		save_history = False):
		#  Scoop up variables
		self.name = name
		self.language = language
		self.verb = verb
		self.tense = tense
		self.timezone = timezone
		self.save_history = save_history

		# Build the questions list
		self.questions = QuestionsList(language = language)
		self.questions.Build(selector_verb = verb, selector_tense = tense)

		# Prepare for runs
		self.run_buffer = QuestionsList()
		self.times_run = 0

		self.records_file = os.getcwd() + "/historical_results.txt"

	def print_not_initialized_error_message(self):
		if self.verb:
			indicator_word = "_verb"
			indicator_value = self.verb

		else:
			indicator_word = "_tense"
			indicator_value = self.tense
		print(
			  "Quiz has not been initialized with any questions" \
			+ "for _language:`%s` " % self.language \
			+ "and %s:`%s`. \n" % (indicator_word, indicator_value) \
			+ "Nothng to do..."
		)

	def _run(self):
		question_num = 0 

		# Start the quiz.
		start = end = None
		while self.questions:

			# Increment the progress label.
			question_num += 1
			progress_string = "(%d/%d)" % (question_num, total_questions)

			# Get the next question at random
			question_index = randint(0, len(self.questions) - 1)

			# # Remove it from the list. this ensures no question gets asked twice.
			question = self.questions.pop(question_index)


			# Ask the question
			start = start if start else time.time()
			question.Ask(progress_string)
			end = time.time()
			
			self.run_buffer.append(question)

		self.times_run += 1
		self.questions = self.run_buffer.copy()
		self.run_buffer = QuestionsList()

		completion_time = "%.2f" % ( end - start )
		return start, completion_time
		

	def Run(self):

		total_questions = len(self.questions)
		if total_questions == 0:
			self.print_not_initialized_error_message()
			return

		test_start, completion_time = self._run()
		self.Grade(test_start, completion_time)



	def Grade(self, timestamp, completion_time):
		os.system('clear')
		total_correct = 0

		print(OutputColor.BOLD + "La Valutazione del Quiz" + OutputColor.END_COLOR)
		for question in self.questions:
			total_correct += question.Grade()

		score = "%d/%d" % (total_correct, len(self.questions))
		print(
			OutputColor.BOLD \
			+ "Il Punteggio Cumulativo: %s\n" % score \
			+ "Il tuo tempo per completare è stato: %ss" % completion_time \
			+ OutputColor.END_COLOR
		)
	
		if self.save_results_to_history:
			new_results = self.update_results(timestamp, completion_time, score)
			self.flush_results_to_file(new_results)

	def read_in_prev_results():
		return

	def update_results(self, timestamp, completion_time, score):
		full_results = {}

		congrats_str = "Congratulazione!\n" \
			+ "Questo è stato " \
			+ "un nuovo miglior tempo (%s) " %  completion_time \
			+ "per questo risultato (%s)." % score \

		c_time = float(completion_time)
		prev_record_found = False
		old_record = "(N/A)"

		#  Best times for each score are indicated by an asterisk in the time_string
		# If we find a value higher than the record, that's the new record.
		if os.path.isfile(self.records_file):
			with open(self.records_file, 'r') as f:
				for line in f.readlines():
					
					quiz_name, t_stamp, prev_score, prev_time_str = line.strip().split("\t")
					new_time_str = prev_time_str #  In most cases, the stamp remains unchanged.

					prev_time = float(prev_time_str.replace("*", ""))

					
					if quiz_name == self.name and score == prev_score:

						# If we find an older record and the new record is better, remove the 
						# "*" from the old record. 
						if "*" in prev_time_str and c_time < prev_time:
							new_time_str = "%.2f" % prev_time
							old_record = prev_time_str.replace("*", "")

						# If we find an older record which beats this record, update this record
						elif c_time > prev_time:
							prev_record_found = True


					if quiz_name not in full_results:
						full_results[quiz_name] = {}
					if score not in full_results[quiz_name]:
						full_results[quiz_name][score] = []
					full_results[quiz_name][score].append([t_stamp, new_time_str])

		if not prev_record_found:
			record_tag = "*"
			print ( OutputColor.GREEN + congrats_str + "\n(Il miglior precedente: %s)" % old_record + OutputColor.END_COLOR)
		else:
			record_tag = ""

		if self.name not in full_results:
			full_results[self.name] = {}
		if score not in full_results[self.name]:
			full_results[self.name][score] = []
		full_results[self.name][score].append((timestamp, completion_time + record_tag))
		return full_results


	def flush_results_to_file(self, full_results):
		with open(self.records_file, "w") as f:
			for name in sorted(full_results.keys()):
				pdb.set_trace()
				name = full_results[timestamp]['name']
				score = full_results[timestamp]["score"]
				completion_time = full_results[timestamp]["time"]

				# Save the results to the file
				f.write("\t".join([name, timestamp, score, completion_time+"\n"]))



def configure_args():
	parser = argparse.ArgumentParser(description='Process some integers.')
	quiz_types = parser.add_mutually_exclusive_group(required = True)
	quiz_types.add_argument(
		'--verb', 
		help='option for single-verb vertical quiz'
	  )

	quiz_types.add_argument(
		'--tense',
		help = 'option for single-tense horizontal quiz'
	)

	parser.add_argument(
		'--language',
		help='the language of the quiz you want to take.'
	)

	return parser

def collect_args(parser):
	return parser.parse_args()

def verify_args(args):
	if args.verb and not isinstance(args.verb, str):
		raise TypeError("Verb argument must be a string.")
	elif args.tense and not isinstance(args.tense, str):
		raise TypeError("Tense argument must be a string.")

	if not args.language:
		raise ValueError("argument --language is required")

	if not isinstance(args.language, str):
		raise TypeError("Language argument must be a string.")


def main():
	parser = configure_args()
	args = collect_args(parser)
	verify_args(args)
 
	quiz_name = "%s %s Quiz" % (
		"Horizontal" if args.tense else "Vertical",
		args.tense if args.tense else args.verb
	)

	quiz = Quiz(
		quiz_name, 
		language = args.language,
		verb     = args.verb,
		tense    = args.tense,
		timezone = "America/Chicago"
	)
	quiz.Run()

if __name__ == '__main__':
	main()