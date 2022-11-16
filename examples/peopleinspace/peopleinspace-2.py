"""Query the 'People in Space' API and display via GUIZero.

Based on code from Raspberry Pi project:
https://projects.raspberrypi.org/en/projects/people-in-space-indicator

Note that the data source is updated manually!
http://open-notify.org/Open-Notify-API/People-In-Space/
"""

import requests
from guizero import App, Text

app = App(title="People iiiin Spaaaaaace!", height=150)

# Get data and parse it as JSON
r = requests.get('http://api.open-notify.org/astros.json')
data = r.json()

# Write some text to the GUI window
message0 = Text(app, " ", height=2) # spacer to push other text down the window a little
message1 = Text(app, "Number of people in space: ", size=24)
message2 = Text(app, data['number'], size=48, color='red')

# Now show the window, containing the messages
app.display()
