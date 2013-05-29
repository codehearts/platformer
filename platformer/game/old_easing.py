# TODO Port these over to classes and delete this file
# duration - in seconds
def ease_in(start, end, duration, time_delta, ease_power=2):
	return start + (end - start) * pow(max(time_delta/duration, 0), ease_power)

def ease_out(start, end, duration, time_delta, ease_power=2):
	return start + (end - start) * (1 - pow(1 - min(time_delta/float(duration), 1), ease_power))
