# KV6006 Practical Session - 4 - Putting it all together

At this point you have:

- Retrieved data from API endpoints, structured as JSON.
- Subscribed to sensor data feeds over MQTT, setting up a callback function to parse and handle new data when it arrives.
- Sent commands (formatted as JSON) over MQTT, to control a physical output device.
- You've also drawn graphs and built a simple GUI.

Broadly, you have inputs and outputs, and several fragments of Python which might help you glue those together.

## Your challenge

The sensor device is happily spewing data into the aether. It seems a shame not to do something with it. So:

> **Pick some inputs, and hook them up to some outputs.**

You might turn your servo into a pointer on a scale, indicating some received value. Or use the colour of your LED to indicate the state of something.

### Sensors

For reference, here's a diagram of the Pico sensor device with all the wires in the right places:

![Alt text](images/Pico_sensors_wiring.png)

The JSON output looks something like:

```json
{
  "sensors": [
      { "name": "temperature", "value": 26.10811 },
      { "name": "magnet", "value": 1 },
      { "name": "dial", "value": 45931 },
      { "name": "force", "value": 688 },
      { "name": "blue", "value": 1 },
      { "name": "yellow", "value": 1 },
      { "name": "pink", "value": 1 },
      { "name": "green", "value": 1 }
  ]
}
```

As with the Mbed boards, `temperature` is taken from an on-chip sensor, so it's pretty hopeless as a room thermometer.

### Things that might be useful

Cardboard, scissors, tape and pens are available.

**Range**. You may need to investigate the min/max range the sensors might output. How could you do that?

**Converting scales**. You'll very likely need to convert a number that lies between two limits into the corresponding number that lies between two different limits. For example, scaling hue angle from 0..360 to 0..255. This Python function might help:

```python
def rescale(x, in_min, in_max, out_min, out_max):
    """Rescale a value from one range to another."""
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
```

To scale a value `input` which lies between `0..360` to the corresponding value which lies between `0..255`:

```python
output = rescale(input, 0, 360, 0, 255)
```

Make sure both ranges are positive, and non-zero.

**guiZero**. GUI toolkits can be fiddly, and to be honest I'd recommend sticking with physical device output over MQTT. But if you really want to explore:

* [guiZero docs](https://lawsie.github.io/guizero/). (note the menu along the top.)
* [A more extensive app example](https://github.com/NUSTEM-UK/vet/blob/main/vet.py), with some work-arounds for nasty timing collisions between MQTT stuff and GUI toolkit stuff. See lines 350 onwards, mostly.

### Things to discuss

- How does your program store state? Does it need to?
- You're working on a Raspberry Pi, which is orders of magnitude more powerful than the Pico W and ESP8266 devices. Do you need all that power to achieve what you're doing?
- The sensor device is a spiky mess of wires, but where might you encounter similar sorts of sensors 'in the real world'?
