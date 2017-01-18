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
            "textbook.pdf.search.executed": self.reading_event,
            "textbook.pdf.search.navigatednext": self.reading_event,
            "edx.course.student_notes.searched": self.reading_event,
            "book": self.reading_event,
            "edx.googlecomponent.calendar.displayed": self.reading_event,
            "edx.googlecomponent.document.displayed": self.reading_event,
            "oppia.exploration.loaded": self.reading_event,
            "microsoft.office.mix.loaded": self.reading_event,
            "microsoft.office.mix.slide.loaded": self.reading_event,
            "edx.course.student_notes.notes_page_viewed": self.reading_event,
            "edx.course.student_notes.viewed": self.reading_event
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

    def reading_event(self, edx_event):
        reading_actions = {
            "textbook.pdf.search.executed": caliper.profiles.ReadingProfile.Actions['SEARCHED'],
            "textbook.pdf.search.navigatednext": caliper.profiles.ReadingProfile.Actions['SEARCHED'],
            "edx.course.student_notes.searched": caliper.profiles.ReadingProfile.Actions['SEARCHED'],
            "book": caliper.profiles.ReadingProfile.Actions['VIEWED'],
            "edx.googlecomponent.calendar.displayed": caliper.profiles.ReadingProfile.Actions['VIEWED'],
            "edx.googlecomponent.document.displayed": caliper.profiles.ReadingProfile.Actions['VIEWED'],
            "oppia.exploration.loaded": caliper.profiles.ReadingProfile.Actions['VIEWED'],
            "microsoft.office.mix.loaded": caliper.profiles.ReadingProfile.Actions['VIEWED'],
            "microsoft.office.mix.slide.loaded": caliper.profiles.ReadingProfile.Actions['VIEWED'],
            "edx.course.student_notes.notes_page_viewed": caliper.profiles.ReadingProfile.Actions['VIEWED'],
            "edx.course.student_notes.viewed": caliper.profiles.ReadingProfile.Actions['VIEWED']
        }
        event_selector = (edx_event["name"] if "name" in edx_event else edx_event["event_type"])

        caliper_args = dict()
        caliper_args["action"] = reading_actions[event_selector]
        caliper_args["actor"] = caliper.entities.Person(
            entity_id=("http://" + edx_event['host'] + "/u/" + edx_event['username']), 
            dateModified=edx_event['time'],
            name=edx_event['username'])
        caliper_args["eventTime"] = edx_event['time']
        caliper_args["event_object"] = caliper.entities.DigitalResource(
            entity_id=("res://" + edx_event['host'] + "/"), 
            dateModified=edx_event['time'])
        caliper_args["target"] = caliper.entities.Frame(
            entity_id=("res://" + edx_event['host'] + "/"), 
            keywords=([edx_event['event']['query']] if edx_event['event'].get('query') else []),
            dateModified=edx_event['time'])

        caliper_event = caliper.events.ReadingEvent(**caliper_args)
        return caliper_event
