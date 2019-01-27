import os

class HistoricalResults:
	COLUMN_DELIMITER = "\t"


	def read_in_prev_results(self, records_file):
		full_results = {}

		# Best times for each score are indicated by an asterisk in the time_string
		# If we find a value higher than the record, that's the new record.
		if os.path.isfile(records_file):
			with open(records_file, 'r') as f:
				for line in f.readlines():
					
					quiz_name, t_stamp, score, time_str = line.strip().split("\t")

					if quiz_name not in full_results:
						full_results[quiz_name] = {}
					if score not in full_results[quiz_name]:
						full_results[quiz_name][score] = []
					full_results[quiz_name][score].append([t_stamp, time_str])

		return full_results

	def update_results(self, results, timestamp, completion_time, score):
		full_results = {}

		congrats_str = "Congratulazione!\n" \
			+ "Questo è stato " \
			+ "un nuovo miglior tempo (%s) " %  completion_time \
			+ "per questo risultato (%s)." % score \

		c_time = float(completion_time)
		prev_record_found = False
		old_record = "(N/A)"

		

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