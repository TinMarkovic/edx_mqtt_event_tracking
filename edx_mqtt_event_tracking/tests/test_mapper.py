from __future__ import (unicode_literals)

from django.test import TestCase
from edx_mqtt_event_tracking.utils import Mapper
from edx_mqtt_event_tracking.tests.test_events import mock_edx_events
import caliper


class MapperTestCase(TestCase):
    def setUp(self):
        self.events = mock_edx_events
        self.mapper = Mapper()

    def test_login_event(self):
        event = self.events["login"]
        event = self.mapper.parse(event)
        self.assertIsInstance(event, caliper.events.SessionEvent)
        self.assertEqual(event.action, caliper.profiles.SessionProfile.Actions['LOGGED_IN'])

    def test_logout_event(self):
        event = self.events["logout"]
        event = self.mapper.parse(event)
        self.assertIsInstance(event, caliper.events.SessionEvent)
        self.assertEqual(event.action, caliper.profiles.SessionProfile.Actions['LOGGED_OUT'])
