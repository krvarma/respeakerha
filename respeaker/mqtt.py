#!/usr/bin/python

import sys
import paho.mqtt.publish as publish

class Mqtt():
	def __init__(self):
		print("MQTT Start")
	
	def publishcmd(self, topic, message, host="iot.eclipse.org"):
		publish.single(topic, message, hostname=host)