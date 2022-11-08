import requests
from guizero import App, Text

# Give ourselves an application window to put things in
app = App(title="People iiiiin Spaaaaaace!", height=350)

# Get the data and parse it as JSON
r = requests.get('http://api.open-notify.org/astros.json')
data = r.json()

# Write text into the GUI window
message0 = Text(app, " ", height=2) # Spacer to push things down.
message1 = Text(app, "Number of people in space: ", size=24)
message2 = Text(app, data['number'], size=48, color='red')
people_string = ""
for person in data['people']:
    people_string += person['name']
    people_string += "\r" # Add a new line
message3 = Text(app, people_string, size=14, color='blue')

# Now show the window
app.display()
