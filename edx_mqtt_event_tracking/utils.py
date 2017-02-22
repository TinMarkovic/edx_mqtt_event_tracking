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
            "/logout": self.session_event_logout
        }

    def parse(self, event):
        event_selector = (event["name"] if "name" in event else event["event_type"])
        return self.edx_to_caliper[event_selector](event)

    def session_event_login(self, edx_event):
        raise NotImplementedError
        # return caliper_event

    def session_event_logout(self, edx_event):
        raise NotImplementedError
        # return caliper_event

    def annotation_event(self, edx_event):
        annotations_actions = {
            #"edx.bookmark.accessed": caliper.profiles.AnnotationProfile.Actions['SEARCHED'],
            "edx.bookmark.added": caliper.profiles.AnnotationProfile.Actions['BOOKMARKED'],
            #"edx.bookmark.listed": caliper.profiles.AnnotationProfile.Actions['SEARCHED'],
            #"edx.bookmark.removed": caliper.profiles.AnnotationProfile.Actions['SEARCHED'],

            "edx.course.student_notes.added": caliper.profiles.AnnotationProfile.Actions['SEARCHED'],
            "edx.course.student_notes.deleted": caliper.profiles.AnnotationProfile.Actions['SEARCHED'],
            "edx.course.student_notes.edited": caliper.profiles.AnnotationProfile.Actions['SEARCHED'],
            "edx.course.student_notes.notes_page_viewed": caliper.profiles.AnnotationProfile.Actions['SEARCHED'],
            "edx.course.student_notes.searched": caliper.profiles.AnnotationProfile.Actions['SEARCHED'],
            "edx.course.student_notes.used_unit_link": caliper.profiles.AnnotationProfile.Actions['SEARCHED'],
            "edx.course.student_notes.viewed": caliper.profiles.AnnotationProfile.Actions['SEARCHED']
        }
        event_selector = (edx_event["name"] if "name" in edx_event else edx_event["event_type"])

        caliper_args = dict()
        caliper_args["action"] = annotations_actions[event_selector]
        caliper_args["actor"] = caliper.entities.Person(
            entity_id=("http://%s/u/%s" % (edx_event['host'], edx_event['username'])), 
            dateModified=edx_event['time'],
            name=edx_event['username'])
        caliper_args["eventTime"] = edx_event['time']
        caliper_args["event_object"] = caliper.entities.DigitalResource(
            entity_id=edx_event['referer'], 
            dateModified=edx_event['time'])
        caliper_args["target"] = caliper.entities.Annotation(
            entity_id=edx_event['referer'], 
            keywords=([edx_event['event']['query']] if edx_event['event'].get('query') else []),
            dateModified=edx_event['time'])

        caliper_event = caliper.events.AssessmentEvent(**caliper_args)
        return caliper_event
