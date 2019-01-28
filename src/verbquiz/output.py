
class _OutputColor:
	BOLD = "\033[1m"
	RED = "\033[91m"
	GREEN = "\033[92m"
	END_COLOR = '\033[0m'


class Output:
	@staticmethod
	def bold_str(s):
		return _OutputColor.BOLD + s + _OutputColor.END_COLOR

	@staticmethod
	def green_str(s):
		return _OutputColor.GREEN + s + _OutputColor.END_COLOR

	@staticmethod
	def bold_green_str(s):
		start = _OutputColor.BOLD + _OutputColor.GREEN
		end = _OutputColor.END_COLOR
		return start + s + end

	@staticmethod
	def red_str(s):
		return _OutputColor.RED + s + _OutputColor.END_COLOR

	@staticmethod
	def bold_red_str(s):
		start = _OutputColor.BOLD + _OutputColor.RED
		end = _OutputColor.END_COLOR
		return start + s + end