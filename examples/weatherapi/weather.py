"""Open Weather Map API demo script.

Documentation for PyOWM:
    https://pyowm.readthedocs.io/en/latest/

Requires:

    pip3 install pyowm
"""

import pyowm
from clientsecrets import owmkey

owm = pyowm.OWM(owmkey)

observation = owm.weather_at_place('Newcastle upon Tyne,GB')
w = observation.get_weather()

print("Got current weather data")
print("-----")

print("Pressure: ", w.get_pressure() )
print("Pressure: ", w.get_pressure()['press'] )
print("Temperature: ", w.get_temperature() )
print("Temperature (Celsius): ", w.get_temperature(unit='celsius')['temp'] )
print("Current weather status: ", w.get_status() )
print("Current weather status: ", w.get_detailed_status() )
print("Recent rain: ", w.get_rain() )
print("Weather icon URL: ", w.get_weather_icon_url() )
print("Sunrise time: ", w.get_sunrise_time('iso') )

print("-----")

