from .ScriptDeviceObject import *
from .ScriptDeviceParameters import *
from .ScriptDriverInfo import *


class ScriptExplicitConnectorObjectsMarker(object):
    """Decorator for marking an object as explicit connector or not.

    All objects within a project are decorated with this marker since V3.5.4.0.

    :version added: 3.5.4.0

    """

    @property
    def is_explicit_connector(self):
        """Gets a value indicating whether this instance is a device object.

        :rtype: bool
        :returns: ``True`` if this instance is device object; otherwise, ``False``.

        """
        pass


class ScriptExplicitConnectorObject(ScriptExplicitConnectorObjectsMarker, ScriptConnector):
    """Decorator for explicit connector objects.

    All objects within a project which are explicit connector objects are extended with this interface (since V3.5.4.0).

    :version added: 3.5.4.0

    """

    def allowed_interfaces_at(self, index):
        """Get the name of the child interfaces that this device object can accept at the specified insert position.

        :type index: int
        :param index: The child index where a device should be inserted.

        :rtype: list[str]
        :returns: A list of possible interface names or ``None`` if no device can
            be inserted at that position.

        """
        pass

    def insert(self, name: str, index: int, device: DeviceId, module: str = None):
        """Inserts the specified device at the specified index.

        :type name: str
        :param name: Name of the device.

        :type index: int
        :param index: index where to insert the device.

        :type device: :class:`DeviceId`
        :param device: The device id.

        :type module: str
        :param module: The module ID.

        """
        pass

    def insert(self, name: str, index: int, type: int, id: str, version: str, module: str = None):
        """Inserts the specified device at the specified index.

        :type name: str
        :param name: Name of the device.

        :type index: int
        :param index: index where to insert the device.

        :type type: int
        :param type: The device type.

        :type id: str
        :param id: The device identification.

        :type version: str
        :param version: The device version.

        :type module: str
        :param module: The module ID.

        """
        pass

    def add(self, name: str, device: DeviceId, module: str = None):
        """Adds the specified device.

        :type name: str
        :param name: Name of the device.

        :type device: :class:`DeviceId`
        :param device: The device id.

        :type module: str
        :param module: The module ID.

        """
        pass

    def add(self, name: str, type: int, id: str, version: str, module: str = None):
        """Adds the specified device.

        :type name: str
        :param name: Name of the device.

        :type type: int
        :param type: The device type.

        :type id: str
        :param id: The device identification.

        :type version: str
        :param version: The device version.

        :type module: str
        :param module: The module ID.

        """
        pass

    def export_io_mappings_as_csv(self, file_path):
        """Export the io mappings as a CSV file to the specified absolute path.

        :type file_path: str
        :param file_path: The absolute path of the file to export.

        """
        pass

    def import_io_mappings_from_csv(self, file_path):
        """import the io mappings from a CSV file at the specified absolute path.

        :type file_path: str
        :param file_path: The absolute path of the file to import.

        """
        pass

    @property
    def driver_info(self):
        """Get the driver info of the explicit connector.

        :version added: 3.5.15.0

        :rtype: :class:`ScriptDriverInfo`

        """
        pass
