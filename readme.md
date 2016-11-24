Event Tracking through MQTT
===========================

A plugin to the edX platform, adding an additional Backend for the Event Tracking mechanisms. Part of the message bus
architecture under Extension Engine projects.

Installation
------------

Installation is modular. Install using pip, from this repository:

```
pip install git+https://github.com/TinMarkovic/edx_mqtt_event_tracking.git
```

After that, depending whether you want to track LMS or Studio, it is required to edit the config files:

```
lms.auth.json
cms.auth.json
# ALTERNATIVELY
edx-platform/cms/envs/common.py
edx-platform/lms/envs/common.py
```

Adding or modifying the following:

```
TRACKING_BACKENDS = {
    'mqtt': {
        'ENGINE': 'edx_mqtt_event_tracking.backends.mqtt.MQTTBackend',
        'OPTIONS': {
            'host': '10.0.2.2',
            'port': '1883'
    }
}
```

You are emitting to the host:port. This was a fitting localhost configuration, yours might differ.

During development on Vagrant, it's suggested that you use the default gateway, easily found with `netstat -rn`.
It will redirect to localhost of the parent computer, and the MQ installed there.