"""Utility functions and classes for track backends"""

from __future__ import (unicode_literals)
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


class Mapper(object):
    def __init__(self):
        self.edx_to_caliper = {
            "/user_api/v1/account/login_session/": self.session_event_login,
            "/logout": self.session_event_logout,
            "edx.bookmark.added": self.annotation_event,
            "edx.bookmark.accessed": self.annotation_event,
            "edx.bookmark.added": self.annotation_event,
            "edx.bookmark.listed": self.annotation_event,
            "edx.bookmark.removed": self.annotation_event,
        }

    def parse(self, event):
        event_selector = (event["name"] if "name" in event else event["event_type"])
        return self.edx_to_caliper[event_selector](event)

    def session_event_login(self, edx_event):
        caliper_args = dict()
        host = edx_event['host']

        if type(edx_event['event']) == str:
            edx_event["event"] = json.loads(edx_event["event"])

        email = edx_event['event']['POST']['email'][0]

        caliper_args["action"] = caliper.profiles.SessionProfile.Actions['LOGGED_IN']
        caliper_args["actor"] = caliper.entities.Person(
            description="Email: %s" % email,
            entity_id="res://%s/u/email/%s" % (edx_event['host'], email)
        )
        caliper_args["target"] = caliper.entities.DigitalResource(
            entity_id="res://%s/" % host
        )
        caliper_args["generated"] = caliper.entities.Session(
            entity_id="res://%s/" % host,
            actor=caliper_args["actor"]
        )
        caliper_args["eventTime"] = edx_event['time']
        caliper_args["event_object"] = caliper.entities.SoftwareApplication(
            entity_id="res://%s/" % host
        )

        caliper_event = caliper.events.SessionEvent(**caliper_args)
        return caliper_event

    def session_event_logout(self, edx_event):
        caliper_args = dict()
        host = edx_event['host']

        caliper_args["action"] = caliper.profiles.SessionProfile.Actions["LOGGED_OUT"]
        caliper_args["actor"] = caliper.entities.Person(
            entity_id=("http://%s/u/%s" % (edx_event["host"], edx_event["username"]))
        )
        caliper_args["target"] = caliper.entities.Session(
            entity_id="res://%s/" % host,
            actor=caliper_args["actor"]
        )
        caliper_args["eventTime"] = edx_event["time"]
        caliper_args["event_object"] = caliper.entities.SoftwareApplication(
            entity_id="res://%s/" % host
        )

        caliper_event = caliper.events.SessionEvent(**caliper_args)
        return caliper_event

    def annotation_event(self, edx_event):
        annotations_actions = {
            "edx.bookmark.added": caliper.profiles.AnnotationProfile.Actions['BOOKMARKED'],
            "edx.bookmark.accessed": caliper.profiles.AnnotationProfile.Actions['BOOKMARKED'],
            "edx.bookmark.added": caliper.profiles.AnnotationProfile.Actions['BOOKMARKED'],
            "edx.bookmark.listed": caliper.profiles.AnnotationProfile.Actions['BOOKMARKED'],
            "edx.bookmark.removed": caliper.profiles.AnnotationProfile.Actions['BOOKMARKED']
        }
        event_selector = (edx_event["name"] if "name" in edx_event else edx_event["event_type"])

        caliper_args = dict()
        caliper_args["action"] = annotations_actions[event_selector]
        caliper_args["actor"] = caliper.entities.Person(
            entity_id=("http://%s/u/%s" % (edx_event['host'], edx_event['username'])), 
            name=edx_event['username'])
        caliper_args["eventTime"] = edx_event['time']
        caliper_args["event_object"] = caliper.entities.DigitalResource(
            entity_id=unicode(edx_event['referer']))
        caliper_args["generated"] = caliper.entities.Annotation(
            entity_id=unicode(edx_event['referer']),
            description=event_selector,
            name=edx_event['event']['component_usage_id'])

        caliper_event = caliper.events.AnnotationEvent(**caliper_args)
        return caliper_event
