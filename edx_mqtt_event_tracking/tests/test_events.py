mock_edx_events = {
    "login": {
        "username": "",
        "event_type": "/user_api/v1/account/login_session/",
        "ip": "13.13.13.13",
        "agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36",
        "host": "precise64",
        "referer": "http://www.example.com/login",
        "accept_language": "en-GB,en;q=0.8,en-US;q=0.6,hr;q=0.4",
        "event": "{\"POST\": {\"password\": \"********\", \"email\": [\"dinosaurs@sharklasers.com\"], \"remember\": [\"false\"]}, \"GET\": {}}",
        "event_source": "server",
        "context": {
            "user_id": "",
            "org_id": "",
            "course_id": "",
            "path": "/user_api/v1/account/login_session/"
        },
        "time": "1939-09-01T12:00:46.059027+00:00",
        "page": ""
    },

    "logout": {
        "username": "dinosaurs",
        "event_type": "/logout",
        "ip": "13.13.13.13",
        "agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36",
        "host": "precise64",
        "referer": "",
        "accept_language": "en-GB,en;q=0.8,en-US;q=0.6,hr;q=0.4",
        "event": "{\"POST\": {}, \"GET\": {}}",
        "event_source": "server",
        "context": {
            "user_id": 5,
            "org_id": "",
            "course_id": "",
            "path": "/logout"
        },
        "time": "1939-09-01T12:00:50.737221+00:00",
        "page": ""
    },

    "book": {
        "username": "dinosaurs",
        "event_source": "browser",
        "name": "book",
        "accept_language": "en-US,en;q=0.8",
        "time": "2017-02-28T15:26:55.578170+00:00",
        "agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
        "page": "http://0.0.0.0:8000/courses/course-v1:edX+DemoX+Demo_Course/pdfbook/0/?viewer=true&file=/asset-v1:edX+DemoX+Demo_Course+type@asset+block/pdf.pdf#zoom=page-fit&disableRange=true",
        "host": "precise64",
        "session": "a2187119f607d46001cd757c45133451",
        "referer": "http://0.0.0.0:8000/courses/course-v1:edX+DemoX+Demo_Course/pdfbook/0/?viewer=true&file=/asset-v1:edX+DemoX+Demo_Course+type@asset+block/pdf.pdf",
        "context": {
            "user_id": 5,
            "org_id": "edX",
            "course_id": "course-v1:edX+DemoX+Demo_Course",
            "path": "/event",
            },
        "ip": "13.13.13.13",
        "event": "{'chapter': '/asset-v1:edX+DemoX+Demo_Course+type@asset+block/pdf.pdf', 'old': 1, 'type': 'gotopage', 'name': 'textbook.pdf.page.loaded', 'new': 1}",
        "event_type": "book",
    }
}
