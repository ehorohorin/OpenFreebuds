import logging

from openfreebuds import event_bus
from openfreebuds.constants.events import EVENT_DEVICE_PROP_CHANGED

log = logging.getLogger("BaseDevice")

class DeviceConfig:
    USE_SOCKET_SLEEP = False
    SAFE_RUN_WRAPPER = None


class BaseDevice:
    def __init__(self):
        self.config = DeviceConfig()
        self.closed = False
        self._prop_storage = {}

    def find_group(self, group):
        if group not in self._prop_storage:
            return {}

        return self._prop_storage[group]

    def find_property(self, group, prop, fallback=None):
        if group not in self._prop_storage:
            return fallback

        if prop not in self._prop_storage[group]:
            return fallback

        return self._prop_storage[group][prop]

    def set_property(self, group, prop, value):
        # Must be overwritten by child class
        self.put_property(group, prop, value)

    def put_group(self, group, value):
        self._prop_storage[group] = value
        # log.debug("Set group of props: " + group)
        event_bus.invoke(EVENT_DEVICE_PROP_CHANGED)

    def put_property(self, group, prop, value):
        if group not in self._prop_storage:
            self._prop_storage[group] = {}

        self._prop_storage[group][prop] = value
        # log.debug("Set prop, group={}, prop={}, value={}".format(group, prop, value))
        event_bus.invoke(EVENT_DEVICE_PROP_CHANGED)

    def list_properties(self):
        return self._prop_storage

    def _send_command(self, ints, read=False):
        raise Exception("Overwrite me!")

    def close(self, lock=False):
        raise Exception("Overwrite me!")

    def connect(self):
        raise Exception("Overwrite me!")
