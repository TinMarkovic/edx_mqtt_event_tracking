"""Event tracker backend that sends events to a message queue."""

from __future__ import absolute_import

import json

from django.conf import settings

from edx_mqtt_event_tracking.backends import BaseBackend
from edx_mqtt_event_tracking.utils import DateTimeJSONEncoder

import paho.mqtt.client as mqtt

# TODO: Document and improve.

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
        try:
            event_str = json.dumps(event, cls=DateTimeJSONEncoder)
        except UnicodeDecodeError:
            #application_log.exception(
            #    "UnicodeDecodeError Event_data: %r", event
            #)
            raise

        # TODO: remove trucation of the serialized event, either at a
        # higher level during the emittion of the event, or by
        # providing warnings when the events exceed certain size.
        # - truncation is inherited from the edX implementation
        event_str = event_str[:settings.TRACK_MAX_EVENT]
        keep_alive = 60
        self.mqclient.connect(self.mqhost, self.mqport, keep_alive)
        #self.mqclient.connect("10.0.2.2", 1883, keep_alive)
        self.mqclient.publish("test", event_str)
        self.mqclient.disconnect()
