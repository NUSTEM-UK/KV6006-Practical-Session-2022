# KV6006 2022 - IOT Practical

## Introduction

In this session, you'll write some short scripts which will pull data from a range of sources (web APIs and sensor devices), manipulate the data, then display or output it in some way. Some of the examples are trivial or silly, but they're designed to illustrate the basic concepts of data manipulation. Crucially, they're intended to present the idea that networked systems can be thought of as *small pieces, loosely joined*. If the network is reliable and data is structured in a consistent way, sources can publish data without too much regard for how it's being consumed. Similarly, data sinks (output destinations) can be combined in novel and unexpected ways.

Since neither source nor sink knows how it's being employed, it's also possible to build systems which are relatively resilient to partial network outages, sensor failures, or other issues which might afflict a long-running aggregate system.

## Terminology

We're going to use three main pieces of jargon:

* **API** means 'Application Program Interface.' An informal definition would be: a documented specification which describes how somebody else's program can interface with yours. Developers might query for data from your API, or pass data to your software through it. As long as your code behaves as you've documented, the other developer doesn't need to know anything about your implementation details. Good API design is a science (or possibly art form) in itself.
* **JSON** is a common data interchange format, often used for IOT applications. Data is structured in key/value pairs.
* **MQTT** is a simple message-passing protocol, which relies on a central server (or 'broker') to handle data. Programs can register themselves with a broker an *publish* message through it, or *subscribe* to messages from it. Each message has two components: the *topic* (which you can think of as a channel), and the *payload* (the actual data).

## Platform

We're going to use Raspberry Pis, which are simple desktop computers running a version of the Linux operating system. We'll be writing code in Python, using the Thonny editor. In principle you could use any desktop or laptop computer and pretty much any language, but getting all the libraries installed can be a bit of a faff.

If you've not used Python before it can be a bit of a jolt, but you'll pick it up as you go along. The main things to remember are:

1. Indentation is significant. Where you've used curly braces `{...}` in other languages to denote blocks of code, in Python you indent by four spaces. Make sure your editor is set to convert a tab character to four spaces, if you mix them up Python will complain.
2. You have to define classes and functions before you can use them. It's not like C where you (for example) declare a function, use it, then define it somewhere else entirely - in Python the `def` has to appear above the first use of the function.

### Microcontrollers

We'll be communicating with networked microcontroller devices. Some are ESP8266 or ESP32 devices, running the Arduino (C++) platform, while others are Raspberry Pi Pico boards running MicroPython.

Microcontrollers typically lack an operating system as such, and store their program in flash memory. Apply power, and they'll immediately start running whatever code they were last flashed with. Even cheap hobbyist devices are astonishingly robust: we've had boards which have sat on a shelf for years between uses, without issue, and others which have run continuously for several years.

Networked microcontrollers can cost under $5. They're often limited in processing power and RAM, but less so than you might imagine.
