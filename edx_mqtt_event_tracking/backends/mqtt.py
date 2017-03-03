"""Event tracker backend that sends events to a message queue."""

from __future__ import absolute_import, unicode_literals
import json
import paho.mqtt.client as mqtt
from edx_mqtt_event_tracking.utils import DateTimeJSONEncoder, Mapper
from urllib import quote

try:
    from track.backends import BaseBackend
except ImportError:
    BaseBackend = object


class MQTTBackend(BaseBackend):
    """
    MQTT Backend for event tracking.
    """

    def __init__(self, host, port, username, password, **kwargs):
        """Event tracker backend that uses MQTT for communication.

        :Parameters:
          - `host`: identifier of the MQTT service, which should have
            been configured using the default python mechanisms.
          - `port`: identifier of the MQTT service
          - `username`: credentials for the MQTT service
          - `password`: credentials for the MQTT service

        """
        super(MQTTBackend, self).__init__(**kwargs)
        self.mqhost = host
        self.mqport = port
        self.mqclient = mqtt.Client()
        self.mqclient.username_pw_set(username, password=password)

    def send(self, event):
        keep_alive = 60
        self.mqclient.connect(self.mqhost, self.mqport, keep_alive)

        try:
            event_topic = (event["name"] if "name" in event else event["event_type"])
        except AttributeError:
            event_str = '{"name": "error",  "exception": "AttributeError", "message": "Event is missing a name"}'
            self.mqclient.publish("error", event_str)
            return

        if event_topic in self.mapper.edx_to_caliper:
            event = self.mapper.parse(event)
            event_str = event.as_json()
        else:
            # Catching any non-caliper events and sending them raw
            try:
                # Event datetime is not serializable by default Python json code - DateTimeJSONEncoder extends it
                event_str = json.dumps(event, cls=DateTimeJSONEncoder)
            except UnicodeDecodeError:
                event_str = '{"name": "error",  "exception": "UnicodeDecodeError"}'
                self.mqclient.publish("error", event_str)
                return

        event_topic = quote(event_topic, "")
        self.mqclient.publish(event_topic, event_str)
        self.mqclient.disconnect()
