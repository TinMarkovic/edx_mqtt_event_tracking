import os
from setuptools import setup
from setuptools import find_packages

README = open(os.path.join(os.path.dirname(__file__), 'readme.md')).read()
REQUIREMENTS = [line.strip() for line in
                open("requirements.txt").readlines()]

setup(name='edx-mqtt-event-tracking',
      version='0.1',
      description='Event tracking through mqtt in edX',
      long_description=README,
      install_requires=REQUIREMENTS,
      url='https://github.com/TinMarkovic/edx_mqtt_event_tracking',
      author='ExtensionEngine',
      author_email='tmarkovic@extensionengine.com',
      license='',
      packages=find_packages())
