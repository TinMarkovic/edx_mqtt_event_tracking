"""Event tracker backend that sends events to a message queue."""

from __future__ import absolute_import
import json
from django.conf import settings
from track.backends import BaseBackend
import paho.mqtt.client as mqtt
from edx_mqtt_event_tracking.utils import DateTimeJSONEncoder

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
        event_topic = "test"
        keep_alive = 60
        self.mqclient.connect(self.mqhost, self.mqport, keep_alive)

        try:
            event_str = json.dumps(event, cls=DateTimeJSONEncoder)
        except UnicodeDecodeError:
            # WIP: Will be better handled with different types/topics when we set them down
            event_str = '{"event_type": "error",  "exception": "UnicodeDecodeError"}'
            self.mqclient.publish(event_topic, event_str)
            raise

        event_str = event_str[:settings.TRACK_MAX_EVENT]
        self.mqclient.publish(event_topic, event_str)
        self.mqclient.disconnect()
