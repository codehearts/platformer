def ease_in(start_position, end_position, total_time, time_progress, power=2):
    return start_position + (end_position - start_position) * pow(max(time_progress/total_time, 0), power)

def ease_out(start_position, end_position, total_time, time_progress, power=2):
    return start_position + (end_position - start_position) * (1 - pow(1 - min(time_progress/total_time, 1), power))