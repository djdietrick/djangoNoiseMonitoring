This is a Noise Monitoring Project that is built off of a Django framework running on a Raspberry Pi.
The system also uses Arduinos equipped with microphones and radio transceivers that are used as nodes
in the system to record sound level readings at regular intervals and transmit those to a receiver
Arduino that will then pass the information to the RPi via USB.

The components of this repository include:

myapp - Django app that can be added onto existing Django project.  To install, go into settings.py and include myapp and rest_framework under installed apps.

controller.py - This is the python script that accepts data from the Arduino, creates new Django models for each reading, and emails the admin if the sound level exceeds a certain threshold.

Arduino - Code for Arduino nodes (receiver and transmitter).  Transmitter includes code for recording sound levels and converting to dB, although the conversion equation is not exactly correct.
To use RF24 library, install library from: https://github.com/maniacbug/RF24


More detailed documentation to come...