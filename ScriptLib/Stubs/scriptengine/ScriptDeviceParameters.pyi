from .ScriptDeviceObject import *
from .ScriptExplicitConnectorObjects import *


class ScriptDeviceConnectorSet(list):
    """The readonly list of connectors for a specific device object."""

    def get_device_object(self):
        """Gets the device object associated with this connector set.

        :rtype: :class:`ScriptDeviceObject`

        """
        pass

    def by_id(self, id):
        """Gets the specific connector by its id.

        :type id: int
        :param id: The id.

        :rtype: :class:`ScriptDeviceConnector`
        :returns: The connector

        """
        pass

    def __contains__(self, id: int):
        """Determines whether the list contains an element with the specified id.

        :type id: int
        :param id: The id.

        :rtype: bool
        :returns: ``True`` if the list contains an element with the specified id, otherwise ``False``.

        """
        pass

    def __contains__(self, visible_name):
        """Determines whether the list contains this element or an element with the specified id or name.

        :type visible_name: str
        :param visible_name: The visible name.

        :rtype: bool
        :returns: ``True`` if the list contains an element with the specified name, otherwise ``False``.

        """
        pass

    def __contains__(self, element: ScriptDeviceConnector):
        """Determines whether the list contains this element or an element with the specified id or name.

        :type element: :class:`ScriptDeviceConnector`
        :param element: The element.

        :rtype: bool
        :returns: ``True`` if the list contains the specified element, otherwise ``False``.

        """
        pass

    def __getitem__(self, visible_name):
        """Gets the :class:`ScriptDeviceConnector` with the specified ``visible_name``.

        :type visible_name: str

        :rtype: :class:`ScriptDeviceConnector`

        """
        pass


class ScriptConnector(object):
    """A connector.

    This is implemented by the :class:`ScriptDeviceConnector` instances returned by the :class:`ScriptDeviceConnectorSet`
    as well as by :class:`ScriptExplicitConnectorObject`.

    """

    @property
    def module_type(self):
        """Id of the connector. This id is used by the driver on the runtime system.

        The Id's of matching parent and child connectors are different. Therefore in order
        to find a matching device for a given parent connector use the ``ConnectorType``
        Property instead.

        :rtype: int

        """
        pass

    @property
    def interface(self):
        """The unique typename of a connector, eg. "Common.PCI".

        A parent connector may be connected to a child connector, if this connector
        type matches.

        :rtype: str

        """
        pass

    @property
    def interface_name(self):
        """Get an internationalized version of the interface name for presentation purposes.

        :rtype: str

        """
        pass

    @property
    def connector_id(self):
        """The unique connector id.

        :rtype: int

        """
        pass

    @property
    def host_path(self):
        """Get the id of the next connector towards the host.

        ``-1``, if the attached device is the controlling host.

        :rtype: int

        """
        pass

    @property
    def connector_role(self):
        """Get whether this connector is a parent or child connector.

        :rtype: ConnectorRole

        """
        pass

    @property
    def is_explicit(self):
        """Get whether a separate node should be shown in the user interface for this connector.

        :rtype: bool

        """
        pass

    @property
    def host_parameters(self):
        """Get the host parameter set of this connector.

        The returned list is read-only which means you can't add, insert or remove
        parameters or clear it. The list of available parameters is defined
        in the device description.

        :rtype: :class:`ScriptDeviceParameterSet`

        """
        pass

    def get_device_object(self):
        """Get an instance of the device object this connector belongs to.

        :rtype: :class:`ScriptDeviceObject`
        :returns: The device object.

        """
        pass

    @property
    def additional_interfaces(self):
        """Gets the additional interfaces of the connector.

        This may be useful to find out which child connector of the current parent
        connector is actually valid.

        :version added: 3.5.6.0

        :rtype: list
        :returns: A python tuple containing strings declaring the additional interfaces.

        """
        pass


class ScriptDeviceConnector(ScriptConnector):
    """A device connector as contained in the :class:`ScriptDeviceConnectorSet`."""

    @property
    def parent(self):
        """Gets the :class:`ScriptDeviceConnectorSet` defining this connector.

        :rtype: :class:`ScriptDeviceConnectorSet`

        """
        pass

    @property
    def io_always_mapping(self):
        """Gets a value indicating whether this ScriptDeviceConnector is always mapping the I/Os belonging to this connector, even if they're not used in the IEC code.

        By default, I/Os which are not used in the IEC code are not updated
        in the I/O task. For debugging and other purposes, this behaviour can be overridden
        with this property.

        :version added: 3.5.8.0

        :rtype: bool

        """
        pass

    @io_always_mapping.setter
    def io_always_mapping(self, value: bool):
        pass

    @property
    def driver_info(self):
        """Get the driver info of the device connector.

        :version added: 3.5.15.0

        :rtype: :class:`ScriptDriverInfo`

        """
        pass


class ScriptDeviceParameterSet(list):
    """A device parameter set.

    The list is read-only which means you can't add, insert or remove
    parameters or clear it. The list of available parameters is defined
    in the device description.

    """

    @property
    def parent(self):
        """Gets the parent.

        This is either a :class:`ScriptDeviceObject`, a :class:`ScriptConnector`,
        or a :class:`ScriptExplicitConnectorObject`.

        :rtype: obj

        """
        pass

    def get_device_object(self):
        """Gets the device object or explicit connector object defining this parameter set.

        :rtype: :class:`ScriptDeviceObject`

        """
        pass

    def __getitem__(self, name):
        """Gets the :class:`ScriptDeviceParameter` with the specified name.

        :type name: str

        :rtype: :class:`ScriptDeviceParameter`

        """
        pass

    def __contains__(self, id: int):
        """Determines wether it contains the specified ScriptDeviceParameter or one with the specified id or name.

        :type id: int
        :param id: The id.

        :rtype: bool
        :returns: ``True`` if the set contains a parameter with the given properties,
            otherwise false.

        """
        pass

    def __contains__(self, name):
        """Determines wether it contains the specified ScriptDeviceParameter or one with the specified id or name.

        :type name: str
        :param name: The name.

        :rtype: bool
        :returns: ``True`` if the set contains a parameter with the given properties,
            otherwise false.

        """
        pass

    def __contains__(self, parameter: ScriptDeviceParameter):
        """Determines wether it contains the specified ScriptDeviceParameter or one with the specified id or name.

        :type parameter: :class:`ScriptDeviceParameter`
        :param parameter: The parameter.

        :rtype: bool
        :returns: ``True`` if the set contains a parameter with the given properties,
            otherwise false.

        """
        pass

    def by_id(self, id: int):
        """Gets the :class:`ScriptDeviceParameter` with the specified id.

        :type id: int

        :rtype: :class:`ScriptDeviceParameter`

        """
        pass


class ScriptMappableDeviceParameterSet(ScriptDeviceParameterSet):
    """Extension interface for the :class:`ScriptDeviceParameterSet` returned by :meth:`ScriptDeviceObject.device_parameters`."""

    @property
    def io_always_mapping(self):
        """Gets a value indicating whether this ScriptMappableDeviceParameterSet is always mapping the I/Os belonging to device parameter set (not part of any connectors), even if they're not used in the IEC code.

        By default, I/Os which are not used in the IEC code are not updated in the I/O
        task. For debugging and other purposes, this behaviour can be overridden with this
        property.

        :rtype: bool

        """
        pass

    @io_always_mapping.setter
    def io_always_mapping(self, value: bool):
        pass


class ScriptDataElement(object):
    """A data element of an online parameter.

    Notice that instances of this interface usually also implement at least one of the
    related interfaces :class:`ScriptCompoundDataElement`, :class:`ScriptValueDataElement`,
    :class:`ScriptDeviceParameter`, :class:`ScriptCompoundDataElement`,
    :class:`ScriptEnumerationDataElement`, :class:`ScriptRangeDataElement`, which contain
    additional useful members, e. G. :attr:`ScriptValueDataElement.value`. Which interface
    applies can be determined via the properties :attr:`has_sub_elements`, :attr:`is_range_type`,
    :attr:`is_enumeration`, :attr:`is_union` and :attr:`parameter`.

    """

    @property
    def parent(self):
        """Gets the parent.

        This property returns either the parent :class:`ScriptDataElement` (which may be the
        :class:`ScriptDeviceParameter`), or the :class:`ScriptDeviceParameterSet` if the current
        element is the device parameter.

        :rtype: obj

        """
        pass

    @property
    def parameter(self):
        """Gets the parameter defining this data element.

        This will return the same instance if called on the :class:`ScriptDeviceParameter`.

        :rtype: :class:`ScriptDeviceParameter`

        """
        pass

    @property
    def identifier(self):
        """Unique identifier of this data element within it's parent element.

        :rtype: str

        """
        pass

    @property
    def visible_name(self):
        """Internationalized name of the data element (this is the name used in the user interface).

        :rtype: str

        """
        pass

    @property
    def description(self):
        """Internationalized  description of the data element.

        :rtype: str

        """
        pass

    @property
    def unit(self):
        """Internationalized unit of the data element. To be used by the presentation layer.

        :rtype: str

        """
        pass

    @property
    def bit_size(self):
        """Get the size of this parameters value in bits.

        :rtype: int

        """
        pass

    @property
    def user_comment(self):
        """Get or set a specified user comment.

        :rtype: str

        """
        pass

    @user_comment.setter
    def user_comment(self, value: str):
        pass

    @property
    def has_sub_elements(self):
        """Get information whether this element is a compound type.

        True for structs, arrays, bitfields, ... - in this case,
        the element implements :class:`ScriptCompoundDataElement`. If this is False, the
        element implements ScriptPrimitiveTypeDataElement. The properties :attr:`is_enumeration`
        and :attr:`has_sub_elements` are mutually exclusive, only one of them can be true at the
        same time.

        :rtype: bool

        """
        pass

    @property
    def is_range_type(self):
        """True, if the elements value must be within a certain range.

        If this is true, the element implements the :class:`ScriptRangeDataElement` interface.

        :rtype: bool

        """
        pass

    @property
    def is_enumeration(self):
        """True if this element is defined as an enumeration. It then also implements :class:`ScriptEnumerationDataElement`.

        The properties :attr:`is_enumeration` and :attr:`has_sub_elements`
        are mutually exclusive, only one of them can be true at the same time.

        :rtype: bool

        """
        pass

    @property
    def is_union(self):
        """Gets a value indicating whether this :class:`ScriptDataElement` is an union.

        :rtype: bool

        """
        pass

    @property
    def can_access_online(self):
        """Gets a value indicating whether this :class:`ScriptDataElement` can be read online.

        If this is true, the element additionally implements :class:`ScriptValueDataElement`.

        :rtype: bool

        """
        pass

    @property
    def is_mappable_io(self):
        """Gets a value indicating whether this :class:`ScriptDataElement` is a mappable input or output.

        :version added: 3.5.8.0

        :rtype: bool
        :returns: ``True`` if is a mappable input or output; otherwise, ``False``.

        """
        pass

    @property
    def io_mapping(self):
        """Gets the io mapping of this data element.

        :version added: 3.5.8.0

        :rtype: :class:`ScriptIoMapping`
        :returns: The mapping, or ``None`` if no mapping exists (e. G. the data element
            is a device parameter and not an input or output).

        """
        pass


class ScriptCompoundDataElement(list):
    """Data element representing compound values which cannot be read or written, but they have subelements which can be modified (if they're not ScriptCompoundDataElements themselves).

    Implementations of this interface also implement :class:`ScriptDataElement` and
    sometimes also :class:`ScriptDeviceParameter`.

    """

    def __getitem__(self, identifier):
        """Return the element with the specified identifier.

        :type identifier: str
        :param identifier: :attr:`DataElement.Identifier` of the requested DataElement

        :raises ArgumentException: Thrown if ``Identifier`` is ``None`` or no element with that
            identifier exists in the collection.

        :rtype: :class:`ScriptDataElement`

        """
        pass

    def __contains__(self, identifier: str):
        """Return ``True`` if a ScriptDataElement with this identifier exists in the collection.

        :type identifier: str
        :param identifier: :attr:`ScriptDataElement.Identifier` of the requested DataElement

        :rtype: bool
        :returns: ``True`` if the element exists.

        """
        pass

    def __contains__(self, sub_element: ScriptDataElement):
        """Return ``True`` if a ScriptDataElement with this identifier exists in the collection.

        :type sub_element: str or :class:`ScriptDataElement`
        :param sub_element: :attr:`DataElement.Identifier`
            of the requested DataElement

        :rtype: bool
        :returns: ``True`` if the element exists.

        """
        pass


class ScriptValueDataElement(ScriptDataElement):
    """Data element representing values of basic member elements which can be read and written."""

    @property
    def default_value(self):
        """Get the default value for this data element.

        If the string is empty, then no explicit defaultvalue has been set.

        :rtype: str

        """
        pass

    @property
    def value(self):
        """Set/get the value for this element as a string representation.

        Invalid values are accepted, but cause the error flag to be set.

        :raises InvalidOperationException: Thrown if this element is a
            compound type (struct, array, ...) - in other words,
            when :attr:`ScriptDataElement.has_sub_elements` is True - in that case,
            you need to set the values of the sub elements.

        :rtype: str

        """
        pass

    @value.setter
    def value(self, value: str):
        pass

    @property
    def base_type(self):
        """Gets the base type of this data element, or None if the type is a compound type.

        :rtype: str

        """
        pass

    def read_online_value(self, nTimeOut=1000):
        """Get the online value with the specified timeout.

        You need to check :attr:`ScriptDataElement.can_access_online` before using this property.

        :type nTimeOut: int
        :param nTimeOut: The timeout.

        :rtype: str
        :returns: The read value.

        """
        pass

    def write_online_value(self, value):
        """Writes the specified value to the device.

        You need to check :attr:`ScriptDataElement.can_access_online`
        before using this property.

        :type value: str
        :param value: The value.

        """
        pass


class ScriptRangeDataElement(ScriptValueDataElement):
    """Data element representing values with a limited range."""

    @property
    def min_value(self):
        """Get the minimal value for this element as a string representation.

        :raises InvalidOperationException: Thrown if this element is not a range type element
            (equivalent to ``IsRangeType == False``).

        :rtype: str

        """
        pass

    @property
    def max_value(self):
        """Get the maximum value for this element as a string representation.

        :raises InvalidOperationException: Thrown if this element is not a range type element
            (equivalent to ``IsRangeType == False``).

        :rtype: str

        """
        pass


class ScriptEnumerationDataElement(ScriptValueDataElement):
    """Data element representing enumeration values."""

    @property
    def enum_value(self):
        """Set/get the current value for this element as an enumeration value.

        :raises InvalidOperationException: Thrown if this element is not a valid
            enumeration element.

        :rtype: :class:`ScriptEnumerationValue`

        """
        pass

    @enum_value.setter
    def enum_value(self, value: ScriptEnumerationValue):
        pass

    @property
    def allowed_values(self):
        """Set/get the current value for this element as an enumeration value.

        Invalid values are accepted, but cause the error flag to be set.

        :raises InvalidOperationException: Thrown if this element is not a valid
            enumeration element.

        :rtype: list[ScriptEnumerationValue]

        """
        pass

    @property
    def value_index(self):
        """Gets or sets the index of the current value within the :attr:`allowed_values` array.

        :rtype: int
        :returns: ``-1`` if the current value is not a valid enumeration value.

        """
        pass

    @value_index.setter
    def value_index(self, value: int):
        pass

    def read_online_enum_value(self, nTimeout=1000):
        """Get_online_enum_values the specified n timeout.

        You need to check :attr:`ScriptDataElement.can_access_online`
        before using this property.

        :type nTimeout: int
        :param nTimeout: The timeout in milliseconds.

        :rtype: :class:`ScriptEnumerationValue`
        :returns: Teh enumeration value.

        """
        pass

    def write_online_value(self, value):
        """Writes the specified value to the device.

        You need to check :attr:`ScriptDataElement.can_access_online`
        before using this property.

        :type value: :class:`ScriptEnumerationValue`
        :param value: The value.

        """
        pass


class ScriptEnumerationValue(object):
    """Defines one element of an enumeration."""

    @property
    def parent(self):
        """Gets the defining :class:`ScriptEnumerationDataElement`.

        :rtype: :class:`ScriptEnumerationDataElement`

        """
        pass

    @property
    def identifier(self):
        """Unique identifier of this enumeration value within its enumeration element.

        This is the value to use with the :attr:`ScriptValueDataElement.value` property.

        :rtype: str

        """
        pass

    @property
    def visible_name(self):
        """Internationalized name of the enumeration value. To be used by the presentation layer.

        :rtype: str

        """
        pass

    @property
    def description(self):
        """Internationalized description of the enumeration value. To be used by the presentation layer.

        :rtype: str

        """
        pass

    @property
    def value(self):
        """Gets the value.

        :rtype: str

        """
        pass

    @property
    def index(self):
        """Gets the index of this value within the :attr:`ScriptEnumerationDataElement.allowed_values` list.

        :rtype: str

        """
        pass


class ScriptDeviceParameter(ScriptDataElement):
    """A device parameter."""

    @property
    def id(self):
        """Each parameter has a unique id within it's parameter list. This is also returned as the identifier in the underlying DataElement.

        :rtype: int

        """
        pass

    @property
    def name(self):
        """Internationalized name of the data element. To be used by the presentation layer.

        :rtype: str

        """
        pass

    @property
    def offline_access_rights(self):
        """Get the allowed access to this parameter in offline mode.

        :rtype: AccessRight

        """
        pass

    @property
    def online_access_rights(self):
        """Get the allowed access to this parameter in online mode.

        :rtype: AccessRight

        """
        pass

    @property
    def downloaded_with_ioconfig(self):
        """Get whether this parameter will be downloaded with the IO-Config.

        :rtype: bool

        """
        pass

    @property
    def channel_type(self):
        """If this parameter represents an IO channel, returns whether it is an input or an output channel. Otherwise this property returns ChannelType.None.

        :rtype: ChannelType

        """
        pass

    @property
    def diagnostic_type(self):
        """Get or set the diagnostic type of this parameter.

        :rtype: DiagType

        """
        pass

    @property
    def type_string(self):
        """Returns a string which fully describes the type.

        :rtype: str

        """
        pass

    @property
    def section(self):
        """Gets the section of the parameter.

        The sections are purely informative and help to structure the device parameters in user interfaces.

        :rtype: str

        """
        pass

    @property
    def iec_type(self):
        """Gets the iec type of this parameter, or ``None`` if none is defined.

        :rtype: str

        """
        pass

    @property
    def param_type(self):
        """get information about the original paramtype (e.g. "std:uint" or "localtypes:struct").

        Usually, this is the best method to describe the type of an parameter - however, in old
        projects, this value might not be accurate or even empty.

        :rtype: str

        """
        pass

    def get_device_object(self):
        """Gets the device object associated with this parameter.

        :rtype: :class:`ScriptDeviceObject`

        """
        pass

    @property
    def disable_mapping(self):
        """Get whether this parameter will be in the task mapping list for the io drivers.

        :version added: 3.5.12.20

        :rtype: bool

        """
        pass


class ScriptIoVariableMapping(object):
    """Represents a single variable mapping."""

    @property
    def Id(self):
        """Gets the identifier.

        :rtype: int

        """
        pass

    @property
    def variable(self):
        """Gets or sets the variable for the mapping.

        The string must be a valid IEC variable expression. If it's an unqualified
        expression, a new variable with the given name will be created. Qualified expressions
        define a mapping to an existing variable.

        :rtype: str

        """
        pass

    @variable.setter
    def variable(self, value: str):
        pass

    @property
    def default_variable(self):
        """Gets the default variable, if defined in the device description.

        The default variable, if existing, is defined in the device description.

        :rtype: str

        """
        pass

    @property
    def mapping_creates_variable(self):
        """Gets a value indicating whether this :class:`ScriptIoVariableMapping` creates a new variable.

        This is the opposite of :attr:`maps_to_existing_variable`.

        :rtype: bool
        :returns: ``True`` if it creates a new variable; otherwise, ``False``.

        """
        pass

    @property
    def maps_to_existing_variable(self):
        """Gets a value indicating whether this :class:`ScriptIoVariableMapping` maps to an existing variable.

        This is the opposite of :attr:`mapping_creates_variable`.

        :rtype: bool
        :returns: ``True`` if it maps to an existing variable; otherwise, ``False``.

        """
        pass


class ScriptIoMapping(ScriptIoVariableMapping):
    """Describing the I/O Mapping options. This object also represents the first actual mapping for the variable.

    Currently the device IO mapping editor UI allows only a single mapping to be
    configured, so we'll implicitly handle this mapping similar to what the device IO mapping
    editor does. When an output variable (or a member thereof) is a struct, either the struct
    itself or its components may be mapped, but not both, as the semantics of the colliding
    mappings is not clear.

    """

    @property
    def automatic_iec_address(self):
        """Gets or sets a value indicating whether this :class:`ScriptIoMapping` has automatically assigned IEC addresses.

        :rtype: bool
        :returns: ``True`` if the IEC addresses are automatically assigned; otherwise, ``False``.

        """
        pass

    @automatic_iec_address.setter
    def automatic_iec_address(self, value: bool):
        pass

    @property
    def manual_iec_address(self):
        """Gets or sets the manually assigned IEC address.

        Setting this to ``None`` will set :attr:`automatic_iec_address` to ``True``,
        setting this to an address will set :attr:`automatic_iec_address` to ``False``.

        :rtype: str
        :returns: The manually assigned IEC address, or the automatically assigned address if
            the IEC address is automatically assigned.

        """
        pass

    @manual_iec_address.setter
    def manual_iec_address(self, value: str):
        pass
