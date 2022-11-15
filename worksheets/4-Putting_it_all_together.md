# KV6006 Practical Session - 4. Putting it all together

At this point you have:

- Retrieving data from API endpoints, structured as JSON
- Subscribing to sensor data feeds over MQTT, and setting up a callback function to parse and handle new data when it arrives.
- Sending commands (formatted as JSON) over MQTT, to control a physical output device.
- Also: drawing graphs and building a simple GUI.

Broadly, you have inputs and outputs, and several fragments of Python which might help you glue those together. So... let's do that.

> Pick an input, and hook it up to an output.

You might turn your servo into a pointer on a scale, indicating some received value. Or use the colour of your LED to indicate the state of something.

Cardboard, scissors, tape and pens are available.

## Things that might be useful

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
