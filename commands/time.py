import datetime
import pytz
def current_time():
    tz = pytz.timezone("Asia/Kolkata")  # Valid timezone from pytz
    now = datetime.datetime.now(tz)
    current_time_str = now.strftime("%I:%M %p")
    return "Current time is: " + current_time_str

print(current_time())