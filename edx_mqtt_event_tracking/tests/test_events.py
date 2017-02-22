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
    }
}
