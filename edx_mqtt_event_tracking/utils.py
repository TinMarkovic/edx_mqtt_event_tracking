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
            "edx.special_exam.proctored.attempt.started": self.assessment_event,
            "edx.special_exam.practice.attempt.started": self.assessment_event,
            "edx.special_exam.timed.attempt.started": self.assessment_event,
            "edx.special_exam.practice.attempt.submitted": self.assessment_event,
            "edx.special_exam.timed.attempt.submitted": self.assessment_event,
            "edx.special_exam.proctored.attempt.submitted": self.assessment_event,
            "edx.special_exam.proctored.attempt.created": self.assessment_event,
            "edx.special_exam.practice.attempt.created": self.assessment_event,
            "edx.special_exam.timed.attempt.created": self.assessment_event,
            "edx.special_exam.proctored.attempt.ready_to_submit": self.assessment_event,
            "edx.special_exam.practice.attempt.ready_to_submit": self.assessment_event,
            "edx.special_exam.timed.attempt.ready_to_submit": self.assessment_event
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

    def assessment_event(self, edx_event):
        assessment_actions = {
            "created": caliper.profiles.AssessmentProfile.Actions["STARTED"],
            "started": caliper.profiles.AssessmentProfile.Actions["RESTARTED"],
            "ready_to_submit": caliper.profiles.AssessmentProfile.Actions["PAUSED"],
            "submitted": caliper.profiles.AssessmentProfile.Actions["SUBMITTED"],
        }
        caliper_args = dict()
        caliper_args["action"] = assessment_actions[edx_event["event"]["attempt_status"]]
        caliper_args["actor"] = caliper.entities.Person(
            entity_id=("http://" + edx_event["host"] + "/u/" + edx_event["username"]),
            name=edx_event["username"])
        caliper_args["event_object"] = caliper.entities.Assessment(
            entity_id=edx_event["referer"],
            dateCreated=edx_event["event"]["attempt_started_at"],
            name=edx_event["event"]["exam_name"]
        )
        caliper_args["eventTime"] = edx_event['time']
        if not edx_event["event"]["exam_is_proctored"]:  # timed
            pass
        elif edx_event["event"]["exam_is_practice_exam"]:
            pass
        else:
            pass
        caliper_event = caliper.events.AssessmentEvent(**caliper_args)
        return caliper_event
