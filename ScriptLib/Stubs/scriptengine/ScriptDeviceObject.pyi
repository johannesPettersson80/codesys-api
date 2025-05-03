from enum import Enum
from .dotNETs import *
from .ScriptOnline import *
from .ScriptDeviceParameters import *
from .ScriptDriverInfo import *


class DeviceTrackingMode(Enum):
    """Enumeration that defines how a device is tracked on the network.

    """
    Name = 0
    """Tracked by name (e.g. 'MyPlc')."""

    SystemAddress = 1
    """Tracked by system address (e.g. '[056D]')."""

    IPAddressUdp = 2
    """Tracked by IP using UDP broadcasts."""

    IPAddressTcp = 3
    """Tracked by IP using TCP point-to-point connection."""

    Gateway = 4
    """Device is a Gateway and will not be tracked."""

    Dummy = 5
    """Placeholder device will not be tracked."""

    DNS = 6
    """Tracked by Dns-Address using TCP point-to-point connection."""


class StopResetBehaviour(Enum):
    KeepCurrentValues = 0
    """The outputs keep the last current values."""

    SetToDefault = 1
    """The outputs are set to the default values."""

    ExecuteProgram = 2
    """A user defined program is executed."""


class ConnectorRole(Enum):
    """Describes the role of a connector"""

    Parent = 0
    """The connector allows other devices to be connected to the connectors device."""

    Child = 1
    """The connector allows its device to be connected to another device."""


class AccessRight(Enum):
    """Defines access rights on a parameter."""

    None = 0,
    """The element is not accessible."""

    Read = 1
    """Specifies that the element may be read."""

    Write = 2
    """Specifies that it is allowed to write to the element."""

    ReadWrite = 3
    """Combination of read and write access: The element may be written and read."""


class ChannelType(Enum):
    """Defines the types of a channel."""

    None = 0
    """Not a channel."""

    Input = 1
    """An input channel."""

    Output = 2
    """An output channel."""

    OutputReadOnly = 3
    """A readonly output channel."""


class DiagType(Enum):
    """Describes the function of a parameter in respect to module diagnosis."""

    None = 0,
    """No diagnostic meaning"""

    Diagnosis = 1,
    """Provides the diagnostic message"""

    Acknowledge = 2
    """Acknowledge for current diagnostic message"""


class ScriptDeviceObjectMarker(object):
    """Every ScriptObject instance will be extended with this method."""

    @property
    def is_device(self):
        """Gets a value indicating whether this instance is a device object.

        :rtype: bool

        """
        pass


class ScriptDeviceObject(ScriptDeviceObjectMarker):
    """Functionality for manipulating device objects.

    All device objects implementing DeviceObject will be extended with this methods.

    """

    def get_device_identification(self):
        """Gets the device identification.

        :rtype: :class:`DeviceId`

        """
        pass

    def enable(self):
        """Marks this device as enabled during download."""
        pass

    def disable(self):
        """Marks this device as disabled during download."""
        pass

    def is_enabled(self):
        """Determines whether this instance is enabled during download.

        :rtype: bool
        :returns: ``True`` if this instance is enabled during download; otherwise, ``False``.

        """
        pass

    def update(self, device: DeviceId, module: str = None):
        """Updates the specified device.

        :type device: :class:`DeviceId`
        :param device: The device Id.

        :type module: str
        :param module: The module ID. (This parameter is optional.)

        """
        pass

    def update(self, type: int, id: str, version: str, module: str = None):
        """Updates the specified device.

        :type type: int
        :param type: The device type.

        :type id: str
        :param id: The device identification.

        :type version: str
        :param version: The device version.

        :type module: str
        :param module: The module ID. (This parameter is optional.)

        """
        pass

    def plug(self, name: str, device: DeviceId, module: str = None):
        """Plugs the specified device.

        :type name: str
        :param name: Name of the device.

        :type device: :class:`DeviceId`
        :param device: The device Id.

        :type module: str
        :param module: The module ID. (This parameter is optional.)

        """
        pass

    def plug(self, name: str, type: int, id: str, version: str, module: str = None):
        """Plugs the specified device.

        :type name: str
        :param name: Name of the device.

        :type type: int
        :param type: The device type.

        :type id: str
        :param id: The device identification.

        :type version: str
        :param version: The device version.

        :type module: str
        :param module: The module ID. (This parameter is optional.)

        """
        pass

    def add(self, name: str, device: DeviceId, module: str = None):
        """Adds the specified device.

        :type name: str
        :param name: Name of the device.

        :type device: :class:`DeviceId`
        :param device: The device Id.

        :type module: str
        :param module: The module ID. (This parameter is optional.)

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
        :param module: The module ID. (This parameter is optional.)

        """
        pass

    def insert(self, name: str, index: int, device: DeviceId, module: str = None):
        """Inserts the specified device at the specified index.

        :type name: str
        :param name: Name of the device.

        :type index: int
        :param index: Index where to insert the device.

        :type device: :class:`DeviceId`
        :param device: The device Id.

        :type module: str
        :param module: The module ID. (This parameter is optional.)

        """
        pass

    def insert(self, name: str, index: int, type: int, id: str, version: str, module: str = None):
        """Inserts the specified device at the specified index.

        :type name: str
        :param name: Name of the device.

        :type index: int
        :param index: Index where to insert the device.

        :type type: int
        :param type: The device type.

        :type id: str
        :param id: The device identification.

        :type version: str
        :param version: The device version.

        :type module: str
        :param module: The module ID. (This parameter is optional.)

        """
        pass

    def unplug(self):
        """Unplugs the specified device."""
        pass

    def get_simulation_mode(self):
        """Gets the simulation mode.

        :returns: ``True`` if simulation is enabled.

        """
        pass

    def set_simulation_mode(self, simulation):
        """Sets the simulation mode.

        :type simulation: bool
        :param simulation: if set to ``True``, simulation is enabled.

        """
        pass

    def get_gateway(self):
        """Gets the gateway.

        See also: :attr:`ScriptDeviceObject.get_device_communication_settings`

        :rtype: Guid
        :returns: The guid of the gateway.

        """
        pass

    def get_address(self):
        """Gets the address of the device.

        See also: :attr:`ScriptDeviceObject.get_device_communication_settings`

        :rtype: str
        :returns: The device address in the bus independent CODESYS format.

        """
        pass

    def set_gateway_and_address(self, gateway: Guid, address: str):
        """Sets the gateway and address.

        If you pass the empty gateway and an empty address, the gateway address will be
        cleared. You can use :meth:`ScriptGateway.find_address_by_ip` to search the
        CODESYS address when you know the ip address or hostname.

        :type gateway: Guid
        :param gateway: The gateway (Guid).

        :type address: str
        :param address: The address in the bus independent CODESYS format.

        """
        pass

    def set_gateway_and_address(self, gateway: str, address: str):
        """Sets the gateway and address.

        If you pass the empty gateway and an empty address, the gateway address will be
        cleared. You can use :meth:`ScriptGateway.find_address_by_ip` to search the
        CODESYS address when you know the ip address or hostname.

        :type gateway: str
        :param gateway: The gateway Guid (string representation),
            or (since V3.5.8.0) the name of the gateway, if unique.

        :type address: str
        :param address: The address in the bus independent CODESYS format.

        """
        pass

    def set_gateway_and_address(self, gateway: ScriptGateway, address: str):
        """Sets the gateway and address.

        If you pass the empty gateway and an empty address, the gateway address will be
        cleared. You can use :meth:`ScriptGateway.find_address_by_ip` to search the
        CODESYS address when you know the ip address or hostname.

        :type gateway: :class:`ScriptGateway`
        :param gateway: The gateway.

        :type address: str
        :param address: The address in the bus independent CODESYS format.

        """
        pass

    def get_module_identification(self):
        """Returns the unique identification of a module.

        A module is a special type of device, that is only available within the
        context of a certain device. The module is identified by the same values
        as each owning device, with an additional module id, to distinguish it from
        other modules of the same device.

        Examples for modules are device local io modules and similar nodes.

        :version added: 3.4.4.0

        :rtype: str
        :returns: The module identification, or an empty string if this module
            has no module identification.

        """
        pass

    def allow_interfaces_at(self, index):
        """Get the name of the child interfaces that this device object can accept at the specified insert position.

        :version added: 3.5.4.0

        :type index: int
        :param index: The child index where a device should be inserted.

        :rtype: list[str]
        :returns: A list of possible interface names or ``None`` if no device can
            be inserted at that position.

        """
        pass

    @property
    def device_parameters(self):
        """Gets the set of device parameters.

        Since V3.5.8.0, this actually is a :class:`ScriptMappableDeviceParameterSet`.

        :version added: 3.5.4.0

        :rtype: :class:`ScriptDeviceParameterSet`

        """
        pass

    @property
    def connectors(self):
        """Gets the connectors.

        :rtype: :class:`ScriptDeviceConnectorSet`

        """
        pass

    def set_gateway_and_device_name(self, gateway: ScriptGateway, device_name: str):
        """Sets the gateway and device name for communication.

        If you pass the empty guid and an empty address, the gateway address will be
        cleared. The device will be tracked by its device name - when trying to go online, a quick
        online scan will be made and the first device with the given name will be selected.

        :version added: 3.5.8.0

        :type gateway: :class:`ScriptGateway`
        :param gateway: The gateway.

        :type device_name: str
        :param device_name: The device name.

        """
        pass

    def set_gateway_and_device_name(self, gateway: Guid, device_name: str):
        """Sets the gateway and device name for communication.

        If you pass the empty guid and an empty address, the gateway address will be
        cleared. The device will be tracked by its device name - when trying to go online, a quick
        online scan will be made and the first device with the given name will be selected.

        :version added: 3.5.8.0

        :type gateway: Guid
        :param gateway: The gateway Guid.

        :type device_name: str
        :param device_name: The device name.

        """
        pass

    def set_gateway_and_device_name(self, gateway: str, device_name: str):
        """Sets the gateway and device name for communication.

        If you pass the empty guid and an empty address, the gateway address will be
        cleared. The device will be tracked by its device name - when trying to go online, a quick
        online scan will be made and the first device with the given name will be selected.

        :version added: 3.5.8.0

        :type gateway: str
        :param gateway: The gateway Guid(as string) or its name.

        :type device_name: str
        :param device_name: The device name.

        """
        pass

    def set_gateway_and_ip_address(self, gateway: ScriptGateway, ip_address: str, port: int = 11740):
        """Sets the gateway and IP address for communication.

        :version added: 3.5.8.0

        :type gateway::class:`ScriptGateway`
        :param gateway: The gateway.

        :type ip_address: str
        :param ip_address: The IP Address as a string. If ``port`` is omitted, the port can be
            passed here separated by a colon (e.G. "``127.0.0.1:11739``").

        :type port: ushort
        :param port: The port. Omit to use the default port 11740.

        :raises InvalidOperaionException: If ``gateway`` is passed as a string and several
            gateways have the same name.

        """
        pass

    def set_gateway_and_ip_address(self, gateway: ScriptGateway, ip_address: IPAddress, port: int = 11740):
        """Sets the gateway and IP address for communication.

        :version added: 3.5.8.0

        :type gateway: :class:`ScriptGateway`
        :param gateway: The gateway.

        :type ip_address: IPAddress
        :param ip_address: The IP Address as a string.

        :type port: ushort
        :param port: The port. Omit to use the default port 11740.

        :raises InvalidOperaionException: If ``gateway`` is passed as a string and several
            gateways have the same name.

        """
        pass

    def set_gateway_and_ip_address(self, gateway: Guid, ip_address: str, port: int = 11740):
        """Sets the gateway and IP address for communication.

        :version added: 3.5.8.0

        :type gateway: Guid
        :param gateway: The gateway's Guid.

        :type ip_address: str
        :param ip_address: The IP Adress as a string. If ``port`` is omitted, the port can be
            passed here separated by a colon (e.G. "``127.0.0.1:11739``").

        :type port: ushort
        :param port: The port. Omit to use the default port 11740.

        :raises InvalidOperaionException: If ``gateway`` is passed as a string and several
            gateways have the same name.

        """
        pass

    def set_gateway_and_ip_address(self, gateway: Guid, ip_address: IPAddress, port: int = 11740):
        """Sets the gateway and IP address for communication.

        :version added: 3.5.8.0

        :type gateway: Guid, str or :class:`ScriptGateway`
        :param gateway: The gateway's' Guid.

        :type ip_address: IPAddress
        :param ip_address: The IP Address.

        :type port: ushort
        :param port: The port. Omit to use the default port 11740.

        :raises InvalidOperaionException: If ``gateway`` is passed as a string and several
            gateways have the same name.

        """
        pass

    def set_gateway_and_ip_address(self, gateway: str, ip_address: str, port: int = 11740):
        """Sets the gateway and IP address for communication.

        :version added: 3.5.8.0

        :type gateway: str
        :param gateway: The gateway guid (as string) or name.

        :type ip_address: str
        :param ip_address: The IP Address as a string. If ``port`` is omitted, the port can be
            passed here separated by a colon (e.G. "``127.0.0.1:11739``").

        :type port: ushort
        :param port: The port. Omit to use the default port 11740.

        :raises InvalidOperaionException: If ``gateway`` is passed as a string and several
            gateways have the same name.

        """
        pass

    def set_gateway_and_ip_address(self, gateway: str, ip_address: IPAddress, port: int = 11740):
        """Sets the gateway and IP address for communication.

        :version added: 3.5.8.0

        :type gateway: str
        :param gateway: The gateway guid (as string) or name.

        :type ip_address: IPAddress
        :param ip_address: The IP Address.

        :type port: ushort
        :param port: The port. Omit to use the default port 11740.

        :raises InvalidOperaionException: If ``gateway`` is passed as a string and several
            gateways have the same name.

        """
        pass

    def get_device_communication_settings(self):
        """Gets the communication settings of the device.

        :rtype: :class:`ScriptCommunicationSettings`

        """
        pass

    def export_io_mappings_as_csv(self, file_path):
        """Export the io mappings as a CSV file to the specified absolute path.

        :version added: 3.5.8.0

        :type file_path: str
        :param file_path: The absolute path of the file to export.

        """
        pass

    def import_io_mappings_from_csv(self, file_path):
        """Imports the io mappings from a CSV file at the specified absolute path.

        :version added: 3.5.8.0

        :type file_path: str
        :param file_path: The absolute path of the file to import.

        """
        pass

    @property
    def driver_info(self):
        """Get the driver info of the device.

        :version added: 3.5.9.0

        :rtype: :class:`ScriptDriverInfo`

        """
        pass

    @property
    def allow_symbolic_var_access_in_sync_with_iec_cycle(self):
        """Property used by the symbol configuration to determine if symbolic variable access is allowed to be synchronized with the IEC cycle.

        The default is False and should be kept for most use cases. Setting this
        to ``True`` may increase the jitter for all applications running on the device because the
        task accessing the variables may block other tasks. The device object has to
        support :class:`DeviceObject` (3.5.10.0) to access the value.

        :version added: 3.5.10.0

        :rtype: bool

        """
        pass

    @allow_symbolic_var_access_in_sync_with_iec_cycle.setter
    def allow_symbolic_var_access_in_sync_with_iec_cycle(self, value):
        pass


class ScriptProjectDeviceExtension(object):
    """Functionality to add top-level devices (e. G. SPS) to projects.

    ScriptProject instances are amended with these objects.

    :version added: 3.4.3.0

    """

    def add(self, name: str, device: DeviceId, module: str = None):
        """Adds the specified device.

        :type name: str
        :param name: Name of the device.

        :type device: :class:`DeviceId`
        :param device: The device Id.

        :type module: str
        :param module: The module ID. (This parameter is optional.)

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
        :param module: The module ID. (This parameter is optional.)

        """
        pass


class DeviceId(object):
    """Represents a Device ID.

    An implementation class of this interface is injected under the
    name "DeviceID" into the python scope, so python code can create
    device IDs without the need to subclass that interface. The
    constructor signature is: DeviceID(int iType, string stId, string
    stVersion)

    """

    @property
    def type(self):
        """Type of the device.

        :rtype: int

        """
        pass

    @property
    def id(self):
        """Id of the device.

        The format for this id is specified for each type.
        The id is unique within the class of devices of one type.

        :rtype: str

        """
        pass

    @property
    def version(self):
        """The version of the device.

        The format for the version string is specified for each type.

        :rtype: str

        """
        pass


class ModuleId(DeviceId):
    """Unique identification for a module.

    A module is a special type of device, that is only available within the
    context of a certain device. The module is identified by the same values
    as each owning device, with an additional module id, to distinguish it from
    other modules of the same device.

    Examples for modules are device local io modules and similar nodes.

    """

    @property
    def module_id(self):
        """Id of the module.

        The format for this id is specified for each type.
        The id is unique within the class of devices of one type.

        :rtype: str

        """
        pass


class ScriptCommunicationSettings(object):
    """Provides access to the communication settings of the device."""

    @property
    def gateway_guid(self):
        """The guid of the gateway.

        :rtype: Guid

        """
        pass

    @property
    def device_address(self):
        """The address of the device.

        :rtype: str

        """
        pass

    @property
    def prompt_at_login(self):
        """Whether there's a prompt at login.

        :rtype: bool

        """
        pass

    @property
    def secure_online_mode(self):
        """Gets a boolean value indicating whether secure online mode is activated for the corresponding devices.

        If set, user interfaces should prompt the user before an
        operation is executed which changes the state of the controller.

        :rtype: bool

        """
        pass

    @property
    def device_name(self):
        """Gets the name of the device as entered on the communication settings page.

        :rtype: str

        """
        pass

    @property
    def monitoring_interval_msec(self):
        """The interval for status and variable monitoring measured in milliseconds.

        Default = 200ms, Minimum = 10ms, Maximum = 1000ms, Increment 10ms.
        Invalid values will be ignored

        :rtype: int

        """
        pass

    @property
    def monitoring_interval(self):
        """The interval for status and variable monitoring measured in milliseconds.

        Default = 200ms, Minimum = 10ms, Maximum = 1000ms, Increment 10ms.
        Invalid values will be ignored

        :rtype: TimeSpan

        """
        pass

    @property
    def TrackingMode(self):
        """Property to get the mode used to track a device on the network - whether the device is tracked via CODESYS address, ip address or name.

        :rtype: DeviceTrackingMode

        """
        pass

    @property
    def scanned_device_name(self):
        """The name of the physical device (E.g. "MyPlc"), as seen in the network scan.

        :rtype: str

        """
        pass

    @property
    def scanned_ip_address_and_port(self):
        """Device IP Address and Port if block driver TCP is used for connection.

        Format: "192.168.101.109:11740", as seen in the network scan.

        This may return the emtpy string if it's not available. Even if some
        network scan members are set, this does not guarantee that all of them are set.

        :rtype: str

        """
        pass

    @property
    def scanned_target_id(self):
        """Target ID.

        Format: "1234 ABCD" (=hexadecimal), same as in device description, as seen in the network scan.

        This may return the emtpy string if it's not available. Even if some
        network scan members are set, this does not guarantee that all of them are set.

        :rtype: str

        """
        pass

    @property
    def scanned_target_name(self):
        """The name of the target (E.g. "CODESYS PLC Win NT"), as seen in the network scan.

        This may return the emtpy string if it's not available. Even if some
        network scan members are set, this does not guarantee that all of them are set.

        :rtype: str

        """
        pass

    @property
    def scanned_target_type(self):
        """Target Type (Format: "4096" (=decimal), same as in device description), as seen in the network scan.

        This may return the emtpy string if it's not available. Even if some
        network scan members are set, this does not guarantee that all of them are set.

        :rtype: str

        """
        pass

    @property
    def scanned_target_vendor(self):
        """The vendor of the target, as seen in the network scan.

        This may return the emtpy string if it's not available. Even if some
        network scan members are set, this does not guarantee that all of them are set.

        :rtype: str

        """
        pass

    @property
    def scanned_target_version(self):
        """The version of the target, as seen in the network scan.

        This may return the emtpy string if it's not available. Even if some
        network scan members are set, this does not guarantee that all of them are set.

        :rtype: str

        """
        pass

    @property
    def is_communication_encrypted(self):
        """Get or set if encrypted communication should be used with the device.
        
        :version added: 3.5.16.10

        :rtype: bool

        """
        pass

    @is_communication_encrypted.setter
    def is_communication_encrypted(self, value):
        pass
