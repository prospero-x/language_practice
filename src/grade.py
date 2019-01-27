from output_color import OutputColor

class Grade:
	@classmethod
	def correct_answer(cls, question, response):
		print(
			question + "\n"\
			+ OutputColor.BOLD \
			+ OutputColor.GREEN \
			+ "Hai dato la risposta corretta: \"" \
			+ response + "\""\
			+ OutputColor.END_COLOR \
			+ "\n\n"
		)

	@classmethod
	def incorrect_answer(cls, question, response, correct_answer):
		print(
			question + "\n" \
			+ OutputColor.BOLD \
			+ OutputColor.RED \
			+ "Hai risposto in modo errato: \"" \
			+ response + "\" " \
			+ OutputColor.END_COLOR
			+ "(la risposta corretta è stato \"" \
			+ correct_answer \
			+ "\")" \
			+ "\n\n" 
		)

 