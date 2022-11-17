"""Query the 'People in Space' API.

Based on code from Raspberry Pi project:
https://projects.raspberrypi.org/en/projects/people-in-space-indicator

Note that the data source is updated manually!
http://open-notify.org/Open-Notify-API/People-In-Space/
"""

import requests

r = requests.get('http://api.open-notify.org/astros.json')

# Parse the response as JSON - example data in example.json
data = r.json()

print("Total people in space: ", data['number'])
