"""Event tracker backend that sends events to a message queue."""

from __future__ import absolute_import
import json
from django.conf import settings
from track.backends import BaseBackend
import paho.mqtt.client as mqtt
from edx_mqtt_event_tracking.utils import DateTimeJSONEncoder, Mapper
from urllib import quote
import logging # remove later
import traceback # remove later

class MQTTBackend(BaseBackend):
    """
    MQTT Backend for event tracking.
    """

    def __init__(self, host, port, **kwargs):
        """Event tracker backend that uses MQTT for communication.

        :Parameters:
          - `host`: identifier of the MQTT service, which should have
            been configured using the default python mechanisms.
          - `port`: identifier of the MQTT service, which should have
            been configured using the default python mechanisms.

        """
        super(MQTTBackend, self).__init__(**kwargs)
        self.mqhost = host
        self.mqport = port
        self.mqclient = mqtt.Client()

    def send(self, event):
        keep_alive = 60
        self.mqclient.connect(self.mqhost, self.mqport, keep_alive)

        try:
            event_topic = (event["name"] if "name" in event else event["event_type"])
        except AttributeError:
            event_str = '{"name": "error",  "exception": "AttributeError", "message": "Event is missing a name"}'
            self.mqclient.publish("error", event_str)
            return

        event["event"] = json.loads(event["event"])

        mapper = Mapper()
        if event_topic in mapper.edx_to_caliper:
            try:
                event = mapper.parse(event).as_dict()
            except Exception:
                event_str = '{"name": "error",  "exception": "Exception", "message": "' + traceback.format_exc() + '"}'
                self.mqclient.publish("error", event_str)
                return

        event_topic = quote(event_topic, "")

        try:
            event_str = json.dumps(event, cls=DateTimeJSONEncoder)
        except UnicodeDecodeError:
            # WIP: Will be better handled with different types/topics when we set them down
            event_str = '{"name": "error",  "exception": "UnicodeDecodeError"}'
            self.mqclient.publish("error", event_str)
            return

        event_str = event_str[:settings.TRACK_MAX_EVENT]
        self.mqclient.publish(event_topic, event_str)
        self.mqclient.disconnect()
