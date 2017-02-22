from django.test import TestCase
from edx_mqtt_event_tracking.backends.mqtt import MQTTBackend
from edx_mqtt_event_tracking.tests.test_events import mock_edx_events


class MQTTBackendTestCase(TestCase):
    def setUp(self):
        self.events = mock_edx_events
        self.backend = MQTTBackend("mock_host", "mock_port")
        self.backend.mqclient = MockClient()

    def test_all_events_firing(self):
        for event in self.events:
            self.backend.send(self.events[event])


class MockClient(object):
    def connect(self, host, port, keep_alive):
        pass

    def publish(self, topic, content):
        pass

    def disconnect(self):
        pass
