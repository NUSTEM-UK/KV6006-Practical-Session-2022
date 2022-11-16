"""Scrape Met Office website for pollen data.

Uses PyQuery to parse web page:

    pip3 install pyquery

On a Pi, may need:

    sudo apt install libxslt-dev

(packaging error for pyquery on some Debian releases)

(note that there's no pollen data for half of the year)
"""

from pyquery import PyQuery as pq

# Get the web page
data = pq(url="https://www.metoffice.gov.uk/weather/warnings-and-advice/seasonal-advice/pollen-forecast")

# ...now select the bit we want by drilling down through the HTML structure
pollen = data("#ne table tbody tr td div span")
# ...and output the HTML representation of whatever we're left with
print(pollen.html())

# That should output 'L' or 'M' or 'H', etc.
