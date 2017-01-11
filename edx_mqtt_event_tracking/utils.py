"""Utility functions and classes for track backends"""

from datetime import datetime, date
import json
import caliper

from pytz import UTC


class DateTimeJSONEncoder(json.JSONEncoder):
    """JSON encoder aware of datetime.datetime and datetime.date objects"""

    def default(self, obj):  # pylint: disable=method-hidden
        """
        Serialize datetime and date objects of iso format.

        datatime objects are converted to UTC.
        """

        if isinstance(obj, datetime):
            if obj.tzinfo is None:
                # Localize to UTC naive datetime objects
                obj = UTC.localize(obj)
            else:
                # Convert to UTC datetime objects from other timezones
                obj = obj.astimezone(UTC)
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()

        return super(DateTimeJSONEncoder, self).default(obj)


class CaliperParser(object):
    def __init__(self, event):
        self.event = event
        self.parsed_event = {}
        self.event_name = (self.event["name"] if "name" in self.event else self.event["event_type"])

    def parse(self):
        caliper_event_name = edx_to_caliper["events"][self.event_name]
        for f in event_properties[caliper_event_name]:
            getattr(self, '_parse_%s' % f)()
        return edx_to_caliper["event_class"][caliper_event_name](**self.parsed_event)

    def _parse_actor(self):
        # mock
        self.parsed_event['actor'] = caliper.entities.Person(entity_id="res://" + self.event['host'] +
                                                                       "/username/" + self.event['username'])

    def _parse_action(self):
        # mock
        self.parsed_event["action"] = edx_to_caliper["actions"][self.event_name]

    def _parse_edApp(self):
        # mock
        self.parsed_event['edApp'] = caliper.entities.SoftwareApplication(entity_id="res://" + self.event['host'] + "/")

    def _parse_group(self):
        # mock
        self.parsed_event['group'] = caliper.entities.Organization(entity_id="res://" + self.event['host'] +
                                                                             "/org/" + self.event['context']['org_id'])

    def _parse_event_object(self):
        # mock
        self.parsed_event['event_object'] = caliper.entities.DigitalResource(entity_id="res://" + self.event['host'] +
                                                                                       "/something")

    def _parse_navigatedFrom(self):
        self.parsed_event['navigatedFrom'] = caliper.entities.DigitalResource(entity_id=self.event["event"]["current_url"])

    def _parse_target(self):
        self.parsed_event['target'] = caliper.entities.DigitalResource(entity_id=self.event["event"]["target_url"])

    def _parse_eventTime(self):
        # mock
        self.parsed_event['eventTime'] = self.event['time']

    def _parse_endedAtTime(self):
        # mock
        self.parsed_event['endedAtTime'] = self.event['time']


# TODO: Move away
event_properties = {
    "Navigation": ("actor", "event_object", "navigatedFrom", "target", "eventTime"),
    "Session": ("action", "actor", "event_object", "target", "eventTime")
}

edx_to_caliper = {
    "events": {
        "/user_api/v1/account/login_session/": "Session",
        "/logout": "Session"
    },
    "event_class": {
        "Navigation": caliper.events.NavigationEvent,
        "Session": caliper.events.SessionEvent
    },
    "actions": {
        "/user_api/v1/account/login_session/": caliper.profiles.SessionProfile.Actions['LOGGED_IN'],
        "/logout": caliper.profiles.SessionProfile.Actions['LOGGED_OUT']
    }
}