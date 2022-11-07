"""Demo Pimoroni Scroll pHAT.
"""

import time
import scrollphathd
from scrollphathd.fonts import font5x5, font5x7

BRIGHTNESS = 0.4 # The ScrollpHAT is insanely bright
scrollphathd.rotate(degrees=0) # If it's upside-down set this to 180

message = " The time is: "
# But the 5x5 font can only show uppercase characters, so:
message = message.upper()

while True:
    targetTime = time.time() + 5 # Set a time three second in the future

    scrollphathd.clear()
    scrollphathd.write_string(message, font=font5x5, brightness=BRIGHTNESS)
    # Now display the message, scrolling, until 5 seconds is up
    while (time.time() < targetTime):
        scrollphathd.show()
        scrollphathd.scroll()
        time.sleep(0.075) # Adjust to change scrolling speed

    # Get the current time, formatted HH:MM
    timeString = time.strftime("%H:%M")
    # Clear the display
    scrollphathd.clear()
    # Display the time
    scrollphathd.write_string(timeString, font=font5x5, brightness=BRIGHTNESS)
    # Update the display
    scrollphathd.show()
    # Wait three seconds...
    time.sleep(3)
    # ...and around we go again.

