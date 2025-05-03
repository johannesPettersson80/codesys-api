class ScriptModuleRepository(object):
    """An instance of an object implementing this interface is injected into the scriptengine scope under the name "modulerepository"."""

    def get_toplevel_instances(self):
        """Gets all Toplevel-Module-Instances of the primary project.

        :rtype: list
        :returns: Returns all Toplevel-Module-Instances of the primary project.

        """
        pass

    def get_all_instances(self):
        """Gets all Module-Instances of the primary project.

        :rtype: list
        :returns: Returns all Module-Instances of the primary project.

        """
        pass

    def get_toplevel_modules(self):
        """Gets all Toplevel-Modules available in the primary project.

        :rtype: list
        :returns: Returns all Toplevel-Modules available in the primary project.

        """
        pass

    def get_all_modules(self):
        """Gets all Modules available in the primary project.

        :rtype: list
        :returns: Returns all Modules available in the primary project.

        """
        pass

    def find_module(self, stQualifiedName):
        """Finds the module with its declaration at the given qualified path (namespace.modulename).

        :type stQualifiedName: str
        :param stQualifiedName: The qualified path of the module description.

        :rtype: ScriptModule
        :returns: The module defined by the module description at the qualified path.

        """
        pass

    def get_compatible_modules(self, slot):
        """Gets all modules which are compatible to a specified slot.

        :type slot: ScriptModuleSlot
        :param slot: The slot for which comaptible modules shall be searched.

        :rtype: list
        :returns: Returns a list of all compatible modules as ScriptModule-Objects.

        """
        pass

    def add_toplevel_instance(self, stInstanceName, scriptMd):
        """Adds a toplevel instance to the module tree.

        :type stInstanceName: str
        :param stInstanceName: The desired name for the toplevel instance.

        :type scriptMd: ScriptModule
        :param scriptMd: The ScriptModule-Object describing the desired module type.

        :rtype: :class:`ScriptObject`
        :returns: Returns the added toplevel instance ScriptObject-Object
            or ``None`` if the operation failed.

        """
        pass

    def add_submodule_instance(self, stInstanceName, scriptMd, scriptSlot, index):
        """Adds a submodule instance to the module tree under the specified slot.

        The slot has to have an ownership of type submodule, otherwise the operation will return ``None``.

        :type stInstanceName: str
        :param stInstanceName: The desired name of the submodule instance.

        :type scriptMd: ScriptModule
        :param scriptMd: The ScriptModule-Object describing the desired module type.

        :type scriptSlot: ScriptModuleSlotInstance
        :param scriptSlot: The ScriptModuleSlot-Object under which the new submodule instance
            shall be created.

        :type index: int
        :param index: The index defining the position of the created submodule instance
            under the slot.

        :rtype: :class:`ScriptObject`
        :returns: Returns the added submodule instance as ScriptObject-Object or ``None`` if the
            operation failed.

        """
        pass

    def add_reference_instance(self, scriptObj, scriptSlot, index):
        """Adds a reference instance to the module tree under the specified slot.

        The slot has to have an ownership of type reference, otherwise the operation will return ``None``.

        :type scriptObj: :class:`ScriptObject`
        :param scriptObj: The ScriptObject-Object of the module instance which shall be reference
            by the created reference instance.

        :type scriptSlot: ScriptModuleSlotInstance
        :param scriptSlot: The ScriptModuleSlot-Object under which the new reference instance
            shall be created.

        :type index: int
        :param index: The index defining the position of the created reference instance
            under the slot. Not relevant if ``scriptSlot`` is a Single-slot.

        :rtype: :class:`ScriptObject`
        :returns: Returns the added reference instance as ScriptObject-Object or ``None`` if the
            operation failed.

        """
        pass

    def set_generator(self, stGenGuid, bEnable):
        """Enables generators in the generator settings.

        :type stGenGuid: str
        :param stGenGuid: The string representation of Guid of the generator,
            which shall be enabled.

        :type bEnable: bool
        :param bEnable: Whether the generator shall be enabled or not.

        :rtype: bool
        :returns: Returns ``True`` if enabling succeeded.

        """
        pass

    def load_wildcard_setting(self, stFileName):
        """Loads a specific XML file into the wildcard options dialog.

        :type stFileName: str
        :param stFileName: The file to be loaded into the wildcard dialogs settings.
            If ``None`` the current filename or last used filename is used.

        :rtype: bool
        :returns: Returns ``True`` if loading succeeded.

        """
        pass

    def create_module_declaration_object(self, stDeclObjectName, stDeclObjectText):
        """Adds a module declaration object to the POU-Pool.

        :type stDeclObjectName: str
        :param stDeclObjectName: The name of the module declaration object.

        :type stDeclObjectText: str
        :param stDeclObjectText: The declaration text in the module declaration object. This text
            can be changed using the module declaration object afterwards.

        :rtype: :class:`ScriptObject`
        :returns: Returns the module declaration object as ScriptObject-Object or ``None`` if
            the operation failed.

        """
        pass

    def generate(self):
        """Generate an IEC-Application from configured module instance tree.

        :rtype: bool
        :returns: Returns ``True`` in case of success.

        """
        pass

    def scan_all_modules(self):
        """Scans all available module declarations.

        :rtype: bool
        :returns: Returns ``True`` in case of no error.

        """
        pass

    def generate_and_login(self):
        """Generates the IEC-Application from the module tree.

        It then uploads this application and logs on.

        :rtype: bool

        """
        pass

    def update_all_module_instances(self):
        """Update all module instances to the current version of the module descriptions."""
        pass


class ScriptApplicationComposerObjectMarker(object):
    """Every ScriptObject instance will be extended using this interface."""

    @property
    def is_module_instance_object(self):
        """Gets a bool indicating whether this ScriptObject is a ModuleInstanceObject object.

        :rtype: bool

        """
        pass

    @property
    def is_module_reference_object(self):
        """Gets a bool indicating whether this ScriptObject is a ModuleReference object.

        :rtype: bool

        """
        pass

    @property
    def is_module_declaration_object(self):
        """Gets a bool indicating whether this ScriptObject is a ModuleDeclObject object.

        :rtype: bool

        """
        pass


class ScriptModuleInstanceObject(ScriptApplicationComposerObjectMarker):
    """Functionality for manipulating ModuleInstanceObject-Objects.

    All Objects implementing ModuleInstanceObject will be extended with this methods.

    """

    @property
    def name(self):
        """Gets the Instance-Name of the ModuleInstanceObject-Object.

        :rtype: str

        """
        pass

    @property
    def module(self):
        """Gets the Module this instance is type of.

        :rtype: :class:`ScriptModule`

        """
        pass

    @property
    def parameters(self):
        """Gets the Parameters of the Instance (see ScriptModule).

        :rtype: list

        """
        pass

    @property
    def ios(self):
        """Gets the IOs of the Instance (see ScriptModule).

        :rtype: list

        """
        pass

    @property
    def slots(self):
        """Gets the Slots of the Instance (see ScriptModule).

        :rtype: list

        """
        pass

    @property
    def inst_refs(self):
        """Gets the InstanceReferences of the Instance (see ScriptModule).

        :rtype: list

        """
        pass

    @property
    def toplevel_info(self):
        """Gets the ToplevelInfo of the Instance (see ScriptModule).

        Returns ``None`` if the instance is not toplevel.

        :rtype: :class:`ScriptModuleToplevelInfoInstance`

        """
        pass

    @property
    def parent_instance(self):
        """Gets the parent module instance or ``None`` if this instance is toplevel.

        :rtype: :class:`.ScriptObject`

        """
        pass

    @property
    def parent_slot(self):
        """Gets the slot this module instance is connected to or ``None`` if this instance is toplevel.

        :rtype: :class:`ScriptModuleSlotInstance`

        """
        pass

    @property
    def is_submodule(self):
        """Whether this module instance is a submodule or not.

        :rtype: bool

        """
        pass


class ScriptModuleReferenceObject(ScriptApplicationComposerObjectMarker):
    """Functionality for manipulating ModuleReferenceObjects.

    All Objects implementing ModuleReferenceObject will be extended with this methods.

    """

    @property
    def target(self):
        """Returns the referenced module instance object or ``None`` if the referenced instance does not exit.

        :rtype: :class:`.ScriptObject`

        """
        pass

    @property
    def target_path(self):
        """Returns the (relative) instance path of the referenced object.

        The components of the path are separated by "/" characters,
        the parent path is denoted by the special string "..".

        :rtype: str

        """
        pass


class ScriptModule(object):
    """Interface providing necessary information and functionalities dealing with Modules in Python.

    Equalling the type Module in the application
    composer interface collection.

    """

    @property
    def name(self):
        """Gets the name of the Module.

        :rtype: str

        """
        pass

    @property
    def qualified_name(self):
        """Gets the fully qualified Name (namespace.modulename) of the Module.

        :rtype: str

        """
        pass

    @property
    def parameters(self):
        """Gets all Module-Parameters.

        :rtype: list

        """
        pass

    @property
    def ios(self):
        """Gets all Module-IOs.

        :rtype: list

        """
        pass

    @property
    def slots(self):
        """Gets all Module-Slots.

        :rtype: list

        """
        pass

    @property
    def inst_refs(self):
        """Gets all Module-InstanceReferences.

        :rtype: list

        """
        pass

    @property
    def var_arrays(self):
        """Gets all Module-VarArrays.

        :rtype: list

        """
        pass

    @property
    def toplevel_info(self):
        """Gets the Module-ToplevelInfo.

        Returns ``None`` if module is not toplevel.

        :rtype: :class:`ScriptModuleToplevelInfo`

        """
        pass

    @property
    def meta_data(self):
        """Gets the Module-MetaData.

        Returns ``None`` if module is not toplevel.

        :rtype: :class:`ScriptModuleMetaData`

        """
        pass

    @property
    def proxies(self):
        """Gets all Module-Proxies.

        :rtype: list

        """
        pass

    @property
    def iec_declaration(self):
        """Gets the declaration of the corresponding Module-IEC-FB.

        :rtype: :class:`ScriptModuleIECDecl`

        """
        pass

    @property
    def is_param_page_disabled(self):
        """Whether the Editors Parameters-Page is dissabled or not.

        :rtype: bool

        """
        pass

    @property
    def is_toplevel_page_disabled(self):
        """Whether the Editors Toplevel-Page is dissabled or not.

        :rtype: bool

        """
        pass

    @property
    def device_generator_data(self):
        """Returns the data provided for the device generator.

        :rtype: :class:`ScriptModuleDeviceGeneratorData`

        """
        pass

    @property
    def alarm_generator_data(self):
        """Returns the data provided for the alarm generator.

        :rtype: :class:`ScriptModuleAlarmGeneratorData`

        """
        pass


class ScriptModuleParameter(object):
    """Interface providing necessary information and functionalities for dealing with Module-Parameters in Python."""

    @property
    def name(self):
        """Localized (multi-lingual) name of the Parameter.

        :rtype: str

        """
        pass

    @property
    def description(self):
        """Localized (multi-lingual) description of the Parameter.

        :rtype: str

        """
        pass

    @property
    def id(self):
        """Id of the Parameter. The Id is unique among all Parameters of one module.

        :rtype: str

        """
        pass

    def get_value(self):
        """The current value of the Parameter.

        If no value is set, default or initial values that are actually used are returned.
        If this parameter does not belong to a Module instance an empty string is returned.

        :rtype: str

        """
        pass

    @property
    def type(self):
        """The IEC-Type of the Parameter.

        :rtype: str

        """
        pass

    @property
    def var_path(self):
        """Gets the instance path of the Parameters variable relative to the instance FB of the module.

        :rtype: str

        """
        pass

    @property
    def minimum(self):
        """Gets the minimum value, that is defined for the parameter.

        :rtype: str

        """
        pass

    @property
    def maximum(self):
        """Gets the maximum value, that is defined for the parameter.

        :rtype: str

        """
        pass

    @property
    def group_id(self):
        """The GroupID of the parameter or an empty string if the parameter does not belong to a group.

        :version added: 3.5.13.0

        :rtype: str
        """
        pass

    @property
    def group_name(self):
        """The localized GroupName of the parameter or an empty string if the parameter does not belong to a group.

        :version added: 3.5.13.0

        :rtype: str
        """
        pass


class ScriptModuleParameterInstance(ScriptModuleParameter):
    """Interface providing necessary information and functionalities for dealing with Module-Parameter-Instances in Python."""

    def set_value(self, value):
        """Sets the current value of the Parameter.

        By setting a parameter its standard initial or default values are no longer used.

        :type value: str
        :param value: The value to set for the Parameter.

        """
        pass

    def get_initial_value(self):
        """Gets the initial value of the parameter as string. Never returns ``None``.

        :version added: 3.5.13.0

        :rtype: str
        """
        pass


class ScriptModuleIo(object):
    """Interface providing necessary information and functionallities for dealing with Module-IOs in Python."""

    @property
    def name(self):
        """Localized (multi-lingual) name of the IO.

        :rtype: str

        """
        pass

    @property
    def description(self):
        """Localized (multi-lingual) description of the IO.

        :rtype: str

        """
        pass

    @property
    def id(self):
        """Id of the IO. The Id is unique among all IOs of one module.

        :rtype: str

        """
        pass

    @property
    def is_output(self):
        """Returns whether the IO is output or not.

        :rtype: bool

        """
        pass

    @property
    def is_input(self):
        """Returns whether the IO is input or not.

        :rtype: bool

        """
        pass

    def get_display_name(self):
        """The current representation of the current IO-Channels mapping meant for display.

        If not mapped, a value indicating "missing" is returned.
        If this IO does not belong to an instance an empty string is returned.

        :rtype: str

        """
        pass

    @property
    def type(self):
        """The IEC-Type of the IO-Channel.

        :rtype: str

        """
        pass

    @property
    def var_path(self):
        """Gets the instance path of the IO-Channels variable relative to the instance FB of the module.

        :rtype: str

        """
        pass


class ScriptModuleIoInstance(ScriptModuleIo):
    """Interface providing necessary information and functionallities for dealing with Module-IO-Instances in Python."""

    def set_void_mapping(self):
        """Sets a void mapping, which equals an IO-Channel with no connection."""
        pass

    def set_missing_mapping(self):
        """Sets a missing mapping.

        This indicates that this io channel has no connections (as for void), but remembers the user to set a mapping
        whenever code is generated by the application composer.

        """
        pass

    def set_direct_mapping(self, other):
        """Sets a direct mapping to another IOChannel.

        :type other: ScriptModuleIoInstance
        :param other: The IO-Channel this channel shall be connected to. Note that
            Inputs only can be connected to Outputs and vice versa.

        """
        pass

    def set_io_channel_mapping(self, channel):
        """Sets a channel mapping, which connects this IO to a physical IO-Channel.

        A possible example for a valid string used for this
        type of mapping is "param::Device.EtherCAT_Master.EL9800:1:2000007:dwIn1".

        :type channel: str
        :param channel: String specifying the desired physical IO-Channel in
            the form "param::Device.VisibleParameterPath".

        """
        pass

    def set_expression_mapping(self, expression):
        """Sets a channel mapping to an ST-Expression.

        :type expression: str
        :param expression: String holding the ST-Expression.

        """
        pass


class ScriptModuleSlot(object):
    """Interface providing necessary information and functionallities for dealing with Module-Slots in Python."""

    @property
    def role(self):
        """Localized (multi-lingual) description of the slot role.

        :rtype: str

        """
        pass

    @property
    def id(self):
        """Id of the Slot. The Id is unique among all Slots of a module.

        :rtype: str

        """
        pass

    @property
    def is_submodule_slot(self):
        """Returns whether the Slot is meant to hold submodules or not.

        :rtype: bool

        """
        pass

    @property
    def is_reference_slot(self):
        """Returns whether the Slot is meant to hold references to modules or not.

        :rtype: bool

        """
        pass

    @property
    def is_single(self):
        """Returns whether the Slot is a Single-Slot, which only can hold one instance, or not.

        :rtype: bool

        """
        pass

    @property
    def is_multi(self):
        """Returns whether the Slot is a Multi-Slot, which can hold multiple instances, or not.

        :rtype: bool

        """
        pass

    @property
    def max_connections(self):
        """Gets the number of the maximum of submodules or references, that can be connected to this Slot.

        :rtype: int

        """
        pass

    @property
    def min_connections(self):
        """Gets the number of the minimum of submodules or references, that have to be connected to this Slot.

        :rtype: int

        """
        pass

    @property
    def default_inst_name(self):
        """Gets the default name for module instances, which are connected to this Slot.

        If no default name is defined an empty string is returned.

        :rtype: str

        """
        pass

    @property
    def type(self):
        """Gets the interface type of this Slot.

        Slot is corresponding to the interface, that FBs have to implement, when they shall be connectable to this slot.

        :rtype: str

        """
        pass

    @property
    def var_path(self):
        """The IEC instance path of the slot variable relative to the FB instance of the module.

        :rtype: str

        """
        pass

    @property
    def var_array_size_path(self):
        """Returns instance path.

        For Multi-Slots the instance path of the variable, which holds the number of connected submodules or references,
        relative to the FB instance of the module. For Single-Slots an empty string is returned.

        :rtype: string

        """
        pass

    @property
    def inst_prefix(self):
        """Gets the optional prefix, that is prepended to the name of the FB instance variables of submodules.

        This string can either have a value or is empty,
        what indicates a prefix, or that no prefix is wished. When this string is
        ``None`` no prefix wishes at all are given.

        :rtype: str

        """
        pass

    @property
    def pragmas(self):
        """Returns the compiler-pragmas, that are to be inserted before instances of submodule function blocks.

        :rtype: list

        """
        pass


class ScriptModuleSlotInstance(ScriptModuleSlot):
    """Interface providing necessary information and functionalities for dealing with Module-Slot-Instances in Python."""

    @property
    def connected_sub_modules(self):
        """Returns a List of connected ModuleInstanceObject-Objects to this Slot.

        When there are no submodules connected an empty list is returned.

        :rtype: list

        """
        pass

    @property
    def connected_ref_modules(self):
        """Returns a List of connected ModuleReferenceObject-Objects to this Slot.

        When there are no references connected an empty list is returned.

        :rtype: list

        """
        pass


class ScriptModuleInstRef(object):
    """Interface providing necessary information and functionalities for dealing with Module-InstanceReferences in Python."""

    @property
    def description(self):
        """Localized (multi-lingual) description of the InstanceReference role.

        :rtype: str

        """
        pass

    @property
    def is_single(self):
        """Returns whether the InstanceReference can only hold a single instance or not.

        :rtype: bool

        """
        pass

    @property
    def is_multi(self):
        """Returns whether the InstanceReference can hold multiple instances or not.

        :rtype: bool

        """
        pass

    @property
    def max_connections(self):
        """Maximum number of connectable instances.

        :rtype: int

        """
        pass

    @property
    def min_connections(self):
        """Minimal number of connectable instances.

        :rtype: int

        """
        pass

    @property
    def type(self):
        """Gets the interface type of the InstanceReference.

        Only FB instances which implement this interface can be connected to this InstanceReference.

        :rtype: str

        """
        pass

    @property
    def is_interface_type(self):
        """Returns whether the reference type is an interface.

        :rtype: bool

        """
        pass

    @property
    def array_size_var_path(self):
        """Returns instance path.

        Only defined if the InstanceReference is able to hold multiple instances (see "is_multi").
        The IEC instance path of the variable, which holds the number of connected instances, relative to the FB instance.
        of the module.

        :rtype: str

        """
        pass

    def get_connected_instances(self):
        """Return a list of connected instances.

        If there are no instances connected an empty list is returned.

        :rtype: list

        """
        pass


class ScriptModuleInstRefInstance(ScriptModuleInstRef):
    """Interface providing necessary information and functionalities for dealing with Module-InstanceReference-Instances in Python."""

    def set_connected_instances(self, listInstances):
        """Replaces the current list of instances of the InstanceReference instance by the given list of strings describing FB instances.

        :type listInstances: list
        :param listInstances: List of strings describing the new FB instances
            to be connected to this InstanceReference.
            If this is ``None`` or an empty list all InstanceReferences are removed.

        """
        pass


class ScriptModuleVarArray(object):
    """Interface providing information and functionalities for dealing with Module-VarArrays."""

    @property
    def id(self):
        """Id of the VarArray. The Id is unique among the VarArrays of a module.

        :rtype: str

        """
        pass

    @property
    def type(self):
        """The IEC-Type of the array elements.

        :rtype: str

        """
        pass

    @property
    def var_path(self):
        """The IEC instance path of the array variable, relative to the module FB instance.

        :rtype: str

        """
        pass

    @property
    def array_size_var_path(self):
        """The IEC instance path of the variable, which holds the size of the array, relative to the module FB instance.

        :rtype: str

        """
        pass

    @property
    def instance_name(self):
        """The optional instance name of the array variable.

        :rtype: str

        """
        pass

    @property
    def pragmas(self):
        """Returns the compiler-pragmas that are to be inserted before the created array variables.

        :rtype: list

        """
        pass


class ScriptModuleMetaData(object):
    """Interface providing necessary information and functionalities for dealing with Module-MetaData in Python."""

    @property
    def description(self):
        """Localized (multi-lingual) description of the module.

        :rtype: str

        """
        pass

    @property
    def category(self):
        """The hierarchic category of the module. The components are separated by '|'.

        :rtype: str

        """
        pass

    @property
    def inst_prefix(self):
        """An optional, default instance prefix that is prepended to the name of the FB-instance variables of submodules and to the names of VarArray variables.

        "" is a possible value. If no prefix is given, 'inst_prefix' is ``None``.

        :rtype: str

        """
        pass

    @property
    def default_inst_name(self):
        """Returns the default name for instances of this module type.

        :rtype: str

        """
        pass


class ScriptModuleAlarmGeneratorData(object):
    """Interface providing necessary information and functionalities for dealing with the Alarm-Generator in Python."""

    @property
    def set_alarms(self):
        """Returns a list of all alarms generated for a module.

        :rtype: list

        """
        pass


class ScriptModuleSetAlarm(object):
    """Interface providing necessary information for a alarm, which is generated by the alarm generator."""

    @property
    def alarm_id(self):
        """Returns the internal id of the module alarm.

        :rtype: str

        """
        pass

    @property
    def module_call_flags(self):
        """Returns the type of module calls for alarming.

        :rtype: int

        """
        pass

    @property
    def message(self):
        """Returns the message of the module alarm.

        :rtype: str

        """
        pass

    @property
    def alarm_class(self):
        """Returns the alarm class of the module alarm.

        :rtype: str

        """
        pass

    @property
    def latch_var_1(self):
        """Returns the latch variable 1 of the module alarm.

        :rtype: str

        """
        pass

    @property
    def latch_var_2(self):
        """Returns the latch variable 2 of the module alarm.

        :rtype: str

        """
        pass

    @property
    def deactivation(self):
        """Returns the deactivation variable of the module alarm.

        :rtype: str

        """
        pass

    @property
    def pending_time(self):
        """Returns the pending time of the module alarm.

        :rtype: str

        """
        pass

    @property
    def higher_prio_alarm_id(self):
        """Returns the id of the higher priority alarm of the current module alarm.

        :rtype: str

        """
        pass

    @property
    def expression(self):
        """Returns the expression being alarm watched.

        :rtype: str

        """
        pass

    @property
    def comparer(self):
        """Returns the type of comparison for UpperLimit, LowerLimit and Equality alarms.

        :rtype: str

        """
        pass

    @property
    def limit_expression_1(self):
        """Returns the limiting expression for UpperLimit and LowerLimit alarms, the equality expression for Equality alarms, the lower area expression for InsideRange and OutsideRange alarms.

        :rtype: str

        """
        pass

    @property
    def limit_expression_2(self):
        """Returns the higher area expression for InsideRange and OutsideRange alarms.

        :rtype: str

        """
        pass

    @property
    def inclide_limit_1(self):
        """Returns whether the lower area expression (limit_expression_1) is includes in the defined area.

        :rtype: bool

        """
        pass

    @property
    def inclide_limit_2(self):
        """Returns whether the higher area expression (limit_expression_2) is includes in the defined area.

        :rtype: bool

        """
        pass

    @property
    def inside_range(self):
        """Returns whether a InsideRange or OutsideRange alarm is used.

        :rtype: bool

        """
        pass

    @property
    def hysteresis(self):
        """Returns the alarm hysteresis for UpperLimit, LowerLimit, Equality, InsideRange and OutsideRange expressions.

        :rtype: double

        """
        pass

    @property
    def latch_vars(self):
        """Returns all latch variables of the module alarm.

        :rtype: Dictionary(int, string)

        """
        pass


class ScriptModuleDeviceGeneratorData(object):
    """Interface providing necessary information and functionalities for dealing with Module-DeviceGenerator-Data in Python."""

    @property
    def generated_devices(self):
        """Returns a list of objects corresponding to the generated devices of the module.

        :rtype: list

        """
        pass

    @property
    def generated_ios(self):
        """Returns a list of objects corresponding to the generated ios of the module.

        :rtype: list

        """
        pass

    @property
    def generated_inst_refs(self):
        """Returns a list of objects corresponding to the generated instance references of the module.

        :rtype: list

        """
        pass

    @property
    def generated_device_parameters(self):
        """Returns a list of objects corresponding to the gerenrated device parameters of the module.

        :rtype: list

        """
        pass


class ScriptModuleGeneratedDevice(object):
    """Interface providing necessary information and functionalitties for dealing with Module-DeviceGenerator-Generated-Devices in Python."""

    @property
    def device_id(self):
        """Returns the internal identification of the (generated) device.

        :rtype: str

        """
        pass

    @property
    def parent_device_id(self):
        """Returns the internal identification of the parent (generated) device if available.

        :rtype: str

        """
        pass

    @property
    def device_type(self):
        """Returns the Device-Identification-Type of the generated device if available.

        :rtype: str

        """
        pass

    @property
    def device_identification_id(self):
        """Returns the Device-Identification-Id of the generated device if available.

        :rtype: str

        """
        pass

    @property
    def device_version(self):
        """Returns the Device-Identification-Version of the generated device if available.

        :rtype: str

        """
        pass

    @property
    def device_module_id(self):
        """Returns the Device-Identification-Module-Id of the generated device if available.

        :rtype: str

        """
        pass

    @property
    def wildcard_type(self):
        """Returns the Wildcard-Device-Type of the generated device if available.

        :rtype: str

        """
        pass

    @property
    def wildcard_description(self):
        """Return the Wildcard-Description of the generated device if available.

        :rtype: str

        """
        pass

    @property
    def flexible_wildcard_maximum(self):
        """Returns the maximum number of flexible Wildcard-Devices if available.

        :rtype: str

        """
        pass


class ScriptModuleGeneratedIO(object):
    """Interface providing necessary information and functionalities for dealing with Module-DeviceGenerator-Generated-IOs in Python."""

    @property
    def io_id(self):
        """Returns the internal id of the Generated-IO.

        :rtype: str

        """
        pass

    @property
    def parent_id(self):
        """Returns the parent (generated) device id of the Generated-IO.

        :rtype: str

        """
        pass

    @property
    def connected_parameter_id(self):
        """Returns the Device-Parameter-ID of the connected Generated-IO if available.

        :rtype: str

        """
        pass

    @property
    def connected_connector_id(self):
        """Returns the Device-Connector-ID of the connected Generated-IO if available.

        :rtype: str

        """
        pass

    @property
    def connected_element_path(self):
        """Returns the Device-Element-Path of the connected Generated-IO if available.

        :rtype: str

        """
        pass

    @property
    def demanded_description(self):
        """Returns the description of the demanded Generated-IO if available.

        :rtype: str

        """
        pass

    @property
    def demanded_properties(self):
        """Returns the demanded properties of the demanded Generated-IO if available.

        :rtype: list

        """
        pass


class ScriptModuleGeneratedInstRef(object):
    """Interface providing necessary information and functionalitties for dealing with Module-DeviceGenerator-Generated-InstRefs in Python."""

    @property
    def inst_ref_id(self):
        """Returns the internal id of the demanded Generated-InstRef if available.

        :rtype: str

        """
        pass

    @property
    def parent_id(self):
        """Returns the demanded id of the Instance reference.

        :rtype: str

        """
        pass

    @property
    def demanded_description(self):
        """Returns the description of the demanded Generated-InstRef if available.

        :rtype: str

        """
        pass

    @property
    def demanded_properties(self):
        """Returns the demanded properties of the demanded Generated-InstRef if available.

        :rtype: list

        """
        pass


class ScriptModuleGeneratedDeviceParameter(object):
    """Interface providing necessary information and functionalities for dealing with Module-DeviceGenerator-Generated-Device-Parameters in Python."""

    @property
    def target_id(self):
        """Returns the (generated) device id for which a parameter is set/added.

        :rtype: str

        """
        pass

    @property
    def internal_id(self):
        """Returns the internal id of the Generated-Device-Parameter.

        :rtype: str

        """
        pass

    @property
    def connected_parameter_id(self):
        """connected_parameter_id.

        :rtype: str

        """
        pass

    @property
    def connected_connector_id(self):
        """Returns the Device-Connector-ID of the Generated-Device-Parameter if available.

        :rtype: str

        """
        pass

    @property
    def connected_element_path(self):
        """Returns the Device-Element-Path of the Generated-Device-Parameter if available.

        :rtype: str

        """
        pass

    @property
    def add_parameter_name(self):
        """Returns the parameter name of the added Generated-Device-Parameter.

        :rtype: str

        """
        pass

    @property
    def add_parameter_type(self):
        """Returns the parameter type of the added Generated-Device-Parameter.

        :rtype: str

        """
        pass

    @property
    def set_parameter_value(self):
        """Returns the parameter value of the set Generated-Device-Parameter.

        :rtype: str

        """
        pass


class ScriptModuleToplevelInfo(object):
    """Interface providing all neccessary information and functionalities for dealing with Module-ToplevelInfo."""

    def get_home(self):
        """Gets the home location of a toplevel module where the composer generates the applications.

        It has the form "Device.AppName" or holds the special string "POU Pool".

        :rtype: string

        """
        pass

    @property
    def gvl_name(self):
        """Gets the name of the global variable list where the module instances will be declared.

        :rtype: str

        """
        pass

    def get_standard_task_high(self):
        """Returns the standard task info for the high priority task, or `None`` if this task was not enabled.

        :rtype: :class:`ScriptModuleStdTaskInfo`

        """
        pass

    def get_standard_task_medium(self):
        """Returns the standard task info for the medium priority task, or ``None`` if this task was not enabled.

        :rtype: :class:`ScriptModuleStdTaskInfo`

        """
        pass

    def get_standard_task_low(self):
        """Returns the standard task info for the low priority task, or ``None`` if this task was not enabled.

        :rtype: :class:`ScriptModuleStdTaskInfo`

        """
        pass

    @property
    def custom_tasks(self):
        """Returns all defined custom tasks.

        :rtype: str

        """
        pass

    @property
    def pragmas(self):
        """Returns the compiler pragmas that are to be inserted before instances of the module function block.

        :rtype: list

        """
        pass


class ScriptModuleToplevelInfoInstance(ScriptModuleToplevelInfo):
    """Interface providing all neccessary information and functionalities for dealing with Module-ToplevelInfo-Instances."""

    def set_home(self, stHome):
        """Sets the home location of a toplevel module.

        :type stHome: str
        :param stHome: String describing the home location in
            the form "Device.AppName" or by the special string "POU Pool".

        """
        pass

    def set_standard_task_high(self, stTaskName):
        """Sets the Name of the standard high priority task.

        :type stTastName: str
        :param stTastName: The desired task name.

        """
        pass

    def set_standard_task_medium(self, stTaskName):
        """Sets the Name of the standard medium priority task.

        :type stTastName: str
        :param stTastName: The desired task name.

        """
        pass

    def set_standard_task_low(self, stTaskName):
        """Sets the Name of the standard low priority task.

        :type stTastName: str
        :param stTastName: The desired task name.

        """
        pass


class ScriptModuleStdTaskInfo(object):
    """Interface providing all necessary information and functionallities for dealing with a StandardTaskInfo."""

    @property
    def name(self):
        """The name of the task.

        :rtype: str

        """
        pass

    @property
    def description(self):
        """Localized (multi-lingual) description of the task.

        :rtype: str

        """
        pass

    @property
    def is_update_ios(self):
        """Whether module IOs that are directly mapped (i.e. not mapped to physical IOs) are read and written in this task or not.

        :rtype: str

        """
        pass

    @property
    def is_create_if_missing(self):
        """Whether the task is created, if it did not exist yet, or not.

        :rtype: str

        """
        pass

    @property
    def is_readonly(self):
        """Whether the name can be changed by the user or not.

        :rtype: str

        """
        pass


class ScriptModuleCustomTaskInfo(object):
    """Interface providing all necessary information and functionalities for dealing with a CustomTaskInfo."""

    @property
    def method_name(self):
        """The name of the method that will be called from this task.

        :rtype: str

        """
        pass

    @property
    def priority(self):
        """The priority of the task (0 (lowest) to 31 (highest)).

        :rtype: int

        """
        pass

    @property
    def interval(self):
        """The task interval in milliseconds.

        :rtype: int

        """
        pass

    @property
    def is_shared(self):
        """Whether several custom tasks may share one method or not.

        :rtype: bool

        """
        pass

    @property
    def is_update_ios(self):
        """Whether module IOs that are directly mapped (i.e. not to physical IOs) are read an written in this task or not.

        :rtype: bool

        """
        pass


class ScriptModuleProxy(object):
    """Interface providing necessary information and functionallities for dealing with Module-Proxies in Python."""

    @property
    def id(self):
        """The Id of the proxy. The Id is unique among all proxies of a module.

        :rtype: str

        """
        pass

    @property
    def iec_declaration(self):
        """Gets the FB declaration of this proxy (i.o.w. the Proxy-FB).

        :rtype: :class:`ScriptModuleIECDecl`

        """
        pass


class ScriptModuleIECDecl(object):
    """Interface providing necessary information and functionallities for dealing with module-bound Declarations in Python."""

    @property
    def name(self):
        """Gets the name of the declaration object.

        :rtype: str

        """
        pass

    @property
    def is_fb(self):
        """Whether this declaration is an FB or not.

        :rtype: bool

        """
        pass

    @property
    def is_interface(self):
        """Whether this declaration is an interface or not.

        :rtype: bool

        """
        pass

    @property
    def is_struct(self):
        """Whether this declaration is a struct or not.

        :rtype: bool

        """
        pass

    @property
    def is_method(self):
        """Whether this declaration is a method or not.

        :rtype: bool

        """
        pass

    @property
    def is_union(self):
        """Whether this declaration is an union or not.

        :rtype: bool

        """
        pass

    @property
    def is_other(self):
        """Whether this declaration is of an other type or not.

        :rtype: bool

        """
        pass


class ScriptModuleDeclaration(ScriptApplicationComposerObjectMarker):
    """Interface providing necessary information and functionalities dealing with Modules Declarations in Python.

    This interface is equalling the type ModuleDeclObject in the application composer interface collection.

    """

    @property
    def decltext(self):
        """Set or Gets the declaration text of the corresponding ModuleDeclObject.

        :rtype: str

        """
        pass

    @decltext.setter
    def decltext(self, value):
        pass
