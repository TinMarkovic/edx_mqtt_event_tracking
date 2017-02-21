import django, sys
from django.conf import settings
from django.test.runner import DiscoverRunner

settings.configure(DEBUG=True,
                   DATABASES={
                        'default': {
                            'ENGINE': 'django.db.backends.sqlite3',
                        }
                    },
                   ROOT_URLCONF='edx_mqtt_event_tracking.tests.urls',
                   INSTALLED_APPS=('django.contrib.auth',
                                   'django.contrib.contenttypes',
                                   'django.contrib.sessions',
                                   'django.contrib.admin',
                                   'edx_mqtt_event_tracking'))

django.setup()
test_runner = DiscoverRunner(verbosity=1)

failures = test_runner.run_tests(['edx_mqtt_event_tracking'])
if failures:
    sys.exit(failures)
