"""Output current UK electricity supply generation mix.

Simple example of parsing a JSON API source. See
'example.json' for what the response looks like.

Uses the requests library, which automatically parses JSON data.

Based on example code from NationalGrid:
https://carbon-intensity.github.io/api-definitions/?python#generation
"""

import requests

# r = requests.get('https://api.carbonintensity.org.uk/generation')
r = requests.get('https://api.carbonintensity.org.uk/generation')

# Parse the JSON response
mix = r.json()

# Now step through the fuels list; see example.json for the structure we're walking through.
for fuel in mix['data']['generationmix']:
    fueltype = fuel['fuel']
    percentage = fuel['perc']
    # Need to cast perc to string to concatenate it for printing:
    print(fueltype + ": " + str(percentage))
