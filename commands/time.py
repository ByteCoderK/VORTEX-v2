import datetime

def current_time():
    current_time = datetime.datetime.now()
    current_time_str = current_time.strftime("%I:%M %p")
    time = "Current time is: " + current_time_str
    return time
