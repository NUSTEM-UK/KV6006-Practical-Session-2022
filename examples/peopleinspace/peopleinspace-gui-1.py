# examples/peopleinspace/peopleinspace-gui-1.py
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
