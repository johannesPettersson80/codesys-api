from .dotNETs import *
from .ScriptDeviceDescription import *
from .ScriptDeviceObject import *


class ScriptDeviceRepository(object):
    """Device respository."""

    @property
    def sources(self):
        """Get the repository sources of the device repository.

        :rtype: :class:`ScriptRepositorySourceList`

        """
        pass

    def create_device_identification(self, type, id, version):
        """Factory method for a :class:`DeviceId` object.

        :type type: int
        :param type: The device type.

        :type id: str
        :param id: The device id.

        :type version: str

        :rtype: str
        :returns: A new :class:`DeviceId` object with the provided values.

        """
        pass

    def create_module_identification(self, type, id, version, module_id):
        """Factory method for a :class:`ModuleId` object.

        :type type: int
        :param type: The device type.

        :type id: str
        :param id: The device id.

        :type version: str

        :type module_id: str
        :param module_id: The module id.

        :rtype: str
        :returns: A new :class:`.ModuleId` object with the provided values.

        """
        pass

    def import_device(self, stream: Stream, source: ScriptRepositorySource, source_path: str,
                      save_device_cache: bool = True):
        """Import a device description file into a repository.

        .. warning:: The original C# function that is called with this method contains 3 overloads.
            It is strongly advised to pass *all* arguments with their respective keywords.
            ``stream``, ``path``, and ``source_path`` are not actually optional, they just aren't
            required in every overload. Pass them if your overload needs them!

        :type stream: Stream
        :param stream: The System.IO.Stream that contains the device description. This must be a
            valid device description file. Other types of device descriptions must be imported by
            special plug-ins.

        :type source: :class:`ScriptRepositorySource`
        :param source: The repository source where the device should be stored. This parameter may
            be ``None``, in which case the default repository source is used.
            The repository source must be one of the sources defined in :attr:`sources`.

        :type source_path: str
        :param source_path: Sourcepath for the import. Relative file references inside the device
            description are resolved relative to this source path. May be empty, if the device
            description contains only absolute file references.

        :type save_device_cache: bool
        :param save_device_cache: If ``True``,
            after removing the device the device cache is also written.
            If ``False``,
            the device cache is not written. If many devices are removed, this is much faster.

        :rtype: :class:`DeviceId`
        :returns: The ID of the imported device description.

        """
        pass

    def import_device(self, path: str, source: ScriptRepositorySource, save_device_cache: bool = True):
        """Import a device description file into a repository.

        .. warning:: The original C# function that is called with this method contains 3 overloads.
            It is strongly advised to pass *all* arguments with their respective keywords.
            ``stream``, ``path``, and ``source_path`` are not actually optional, they just aren't
            required in every overload. Pass them if your overload needs them!

        Import a device description file into a repository.

        :type path: str
        :param path: The file that contains the device description. This must be a valid device
            description file. Other types of device descriptions must be imported by special
            plug-ins.

        :type source: :class:`ScriptRepositorySource`
        :param source: The repository source where the device should be stored. This parameter may
            be ``None``, in which case the default repository source is used.
            The repository source must be one of the sources defined in :attr:`sources`.

        :type save_device_cache: bool
        :param save_device_cache: If ``True``,
            after removing the device the device cache is also written.
            If ``False``,
            the device cache is not written. If many devices are removed, this is much faster.

        :rtype: :class:`DeviceId`
        :returns: The ID of the imported device description.

        """
        pass

    def import_device(self, path: str, source: ScriptRepositorySource, converter_factory_guid: Guid,
                      save_device_cache: bool = True):
        """Import a device description file into a repository.

        .. warning:: The original C# function that is called with this method contains 3 overloads.
            It is strongly advised to pass *all* arguments with their respective keywords.
            ``stream``, ``path``, and ``source_path`` are not actually optional, they just aren't
            required in every overload. Pass them if your overload needs them!

        Convert a foreign device description file and import the result into a repository.

        .. csv-table:: List of known converter factories:
            :widths: auto

            {C633F245-876F-45E8-AAB4-3FBD994C08B8}, "Use as default because all available converters are tried"
            {3992C588-7BDB-4A7C-908D-F444808D8CD2}, "XML files of EtherCAT"
            {6066AEF4-F19A-41ac-A249-721BDAE32D40}, "GSDML files of Profinet IO"
            {CDDE0374-9EFD-401e-93C8-F19443FB60ED}, "XML files of Sercos3"
            {1ce4a9c1-37d3-496c-9e80-cd99ad3807ee}, "EDS files of CANbus"

        :type path: str
        :param path: The file that contains the device description. This must be a valid device
            description file. Other types of device descriptions must be imported by special
            plug-ins.

        :type source: :class:`ScriptRepositorySource`
        :param source: The repository source where the device should be stored. This parameter may
            be ``None``, in which case the default repository source is used.
            The repository source must be one of the sources defined in :attr:`sources`.

        :type converter_factory_guid: str
        :param converter_factory_guid: The guid of the converter to import a foreign device
            description. For example CANopen EDS files.

        :type save_device_cache: bool
        :param save_device_cache: If ``True``,
            after removing the device the device cache is also written.
            If ``False``,
            the device cache is not written. If many devices are removed, this is much faster.

        :rtype: :class:`DeviceId`
        :returns: The ID of the imported device description.

        """
        pass

    def import_vendor_description(self, stream: Stream, source: ScriptRepositorySource, source_path: str):
        """Import a device description file into a repository.

        .. warning:: The original C# function that is called with this method contains 2 overloads.
            It is strongly advised to pass *all* arguments with their respective keywords.
            ``stream``, ``path``, and ``source_path`` are not actually optional, they just aren't
            required in every overload. Pass them if your overload needs them!

        :type stream: System.IO.Stream
        :param stream: The stream that contains the vendor description. This must be a valid vendor
            description file. Other types of vendor descriptions must be imported by special
            plug-ins.

        :type source: :class:`ScriptRepositorySource`
        :param source: The repository source where the device should be stored. This parameter may
            be ``None``, in which case the default repository source is used.
            The repository source must be one of the sources defined in :attr:`sources`.

        :type source_path: str
        :param source_path: Sourcepath for the import. Relative file references inside the vendor
            description are resolved relative to this source path. May be empty, if the vendor
            description contains only absolute file references.

        :rtype: :class:`ScriptVendorDescription`
        :returns: The imported vendor description.

        """
        pass

    def import_vendor_description(self, path: str, source: ScriptRepositorySource):
        """Import a device description file into a repository.

        .. warning:: The original C# function that is called with this method contains 2 overloads.
            It is strongly advised to pass *all* arguments with their respective keywords.
            ``stream``, ``path``, and ``source_path`` are not actually optional, they just aren't
            required in every overload. Pass them if your overload needs them!

        **import_vendor_description(path, source) (2/2)**

        :type path: str
        :param path: The file that contains the vendor description. This must be a valid vendor
            description file.

        :type source: :class:`ScriptRepositorySource`
        :param source: The repository source where the device should be stored. This parameter may
            be ``None``, in which case the default repository source is used.
            The repository source must be one of the sources defined in :attr:`sources`.

        :rtype: :class:`ScriptVendorDescription`
        :returns: The imported vendor description.

        """
        pass

    def remove_device(self, device_id, source, save_device_cache=True):
        """Remove a device from the specified repository source.

        :type device_id: :class:`DeviceId`
        :param device_id: Defines the device to remove.

        :type source: :class:`ScriptRepositorySource`
        :param source: Remove the device from this repository source.
            If ``None`` the device is removed from the default repository source.

        :type save_device_cache: bool
        :param save_device_cache: If ``True``,
            after removing the device the device cache is also written.
            If ``False``,
            the device cache is not written. If many devices are removed, this is much faster.

        """
        pass

    def remove_vendor_description(self, vendor_id, source):
        """Remove a vendor description from the specified repository source.

        :type vendor_id: int
        :param vendor_id: The vendor id.

        :type source: :class:`ScriptRepositorySource`
        :param source: Remove the device from this repository source.
            If ``None`` the device is removed from the default repository source.

        """
        pass

    def save_device_cache(self):
        """Saves the current devices in the device cache. Could be used to force it after adding or removing many devices."""
        pass

    def rebuild_device_cache(self):
        """Rebuild the device cache.

        The device cache is deleted, initialized and saved.

        """
        pass

    def get_device_category(self, category_id: int):
        """This overload is called when ``category_id`` is of type *int*.

        Get the device category with the specified device category ID.

        :type category_id: int
        :param category_id: The device category ID of the device category implementation.
            This value corresponds to the ``DeviceDescription/DeviceInfo/Category`` tags of the
            device description file.

        :rtype: :class:`ScriptDeviceCategory`
        :returns: The requested device category, or ``None`` if the device category does not exist.

        """
        pass

    def get_device_category(self, category: Guid):
        """This overload is called when ``category_id`` is of type *int*.

        Get the device category with the specified type GUID.

        :type category_id: Guid
        :param category_id: The type GUID of the device category implementation.

        :rtype: :class:`ScriptDeviceCategory`
        :returns: The requested device category, or ``None`` if the device category does not exist.

        """
        pass

    def get_device_family(self, family):
        """Device family.

        :type family: str
        :param family: ``VendorID:FamilyID``.

        :rtype: :class:`ScriptDeviceFamily`

        """
        pass

    def get_all_devices(self):
        """Get a collection containing all devices in the repository.

        .. warning:: The original C# function that is called with this method contains 5 overloads.
            It is strongly advised to pass *all* arguments with their respective keywords.

        Devices which are installed in more than one repository source are returned only once.

        :rtype: :class:`ScriptDeviceCollection`
        :returns: A device collection containing the current result of the query.

        """
        pass

    def get_all_devices(self, device_id: DeviceId):
        """Get a collection containing all devices in the repository.

        .. warning:: The original C# function that is called with this method contains 5 overloads.
            It is strongly advised to pass *all* arguments with their respective keywords.

        Get a collection containing all devices in the repository, including local modules of
        ``device_id``

        :type device_id: :class:`DeviceId`
        :param device_id: The id of the device that provides the context for the local modules.

        :rtype: :class:`ScriptDeviceCollection`
        :returns: A device collection containing the current result of the query.

        """
        pass

    def get_all_devices(self, source: ScriptRepositorySource):
        """Get a collection containing all devices in the repository.

        .. warning:: The original C# function that is called with this method contains 5 overloads.
            It is strongly advised to pass *all* arguments with their respective keywords.

        Get a collection containing all devices in the specified repository source.

        :type source: :class:`ScriptRepositorySource`
        :param source: The repository source to enumerate.

        :rtype: :class:`ScriptDeviceCollection`
        :returns: A device collection containing the current result of the query.

        """
        pass

    def get_all_devices(self, device_id: DeviceId, source: ScriptRepositorySource):
        """Get a collection containing all devices in the repository.

        .. warning:: The original C# function that is called with this method contains 5 overloads.
            It is strongly advised to pass *all* arguments with their respective keywords.

        Get a collection containing all devices in the specified repository source.

        :type device_id: :class:`DeviceId`
        :param device_id: The id of the device that provides the context for the local modules.

        :type source: :class:`ScriptRepositorySource`
        :param source: The repository source to enumerate.

        :rtype: :class:`ScriptDeviceCollection`
        :returns: A device collection containing the current result of the query.

        """
        pass

    def get_all_devices(self, name: str, source: ScriptRepositorySource):
        """Get a collection containing all devices in the repository.

        .. warning:: The original C# function that is called with this method contains 5 overloads.
            It is strongly advised to pass *all* arguments with their respective keywords.

        Get all device which contain the specified name.

        :type name: str
        :param name: Text which the name of the device has to contain.

        :type source: :class:`ScriptRepositorySource`
        :param source: If not ``None``, only this repository source will be searched.

        :rtype: tuple
        :returns: A device tuple containing the current result of the query.

        """
        pass

    def get_device(self, device_id):
        """Get the device description with the specified device identification.

        :type device_id: :class:`DeviceId`
        :param device_id: Device identification.

        :rtype: :class:`ScriptDeviceDescription`
        :returns: The requested device description, or ``None`` if the device description does not exist.
        """
        pass

    def get_all_vendor_descriptions(self):
        """Get a collection of all vendor descriptions in the repository.

        .. warning:: The original C# function that is called with this method contains 2 overloads.
            It is strongly advised to pass *all* arguments with their respective keywords.

        :rtype: tuple[ScriptVendorDescription]
        :returns: A collection of vendor descriptions.

        """
        pass

    def get_all_vendor_descriptions(self, source: ScriptRepositorySource):
        """Get a collection of all vendor descriptions in the repository.

        .. warning:: The original C# function that is called with this method contains 2 overloads.
            It is strongly advised to pass *all* arguments with their respective keywords.

        Get the vendor description with the specified vendor Id.

        :type source: :class:`ScriptRepositorySource`
        :param source: Repository source.

        :rtype: tuple[ScriptVendorDescription]
        :returns: A collection of vendor descriptions containing the current result of the query.

        """
        pass

    def get_vendor_description(self, vendor_id):
        """Get the vendor description with the specified vendor Id.

        :type vendor_id: int
        :param vendor_id: Vendor Id.

        :rtype: :class:`ScriptVendorDescription`
        :returns: The requested vendor description,
            or ``None`` if the vendor description does not exist.

        """
        pass


class ScriptRepositorySourceList(list):
    """A collection of :class:`ScriptRepositorySource` objects."""

    def __getitem__(self, index):
        """Get the :class:`ScriptRepositorySource` at the specified position or with the specified name.

        If there is no repository source at the specified position ``None`` is returned.

        :type index: int

        :rtype: :class:`ScriptRepositorySource`

        """
        pass

    def __getitem__(self, name):
        """Get the :class:`ScriptRepositorySource` at the specified position or with the specified name.

        If there is no repository source with the specified name ``None`` is returned.

        :type name: str

        :rtype: :class:`ScriptRepositorySource`

        """
        pass

    def add(self, name, location_url):
        """Add a new repository source with the specified name.

        :type name: str
        :param name: Name for the new source.

        :type location_url: str

        :rtype: :class:`ScriptRepositorySource`
        :returns: The added repository source.

        """
        pass

    def remove(self, source):
        """Remove an existing repository source.

        Internal sources cannot be removed.

        :type source: :class:`ScriptRepositorySource`
        :param source: The repository source to remove.

        """
        pass

    def move(self, source, index):
        """Move an existing repository source to the specified location in the collection.

        :type source: :class:`ScriptRepositorySource`
        :param source: Existing repository source.

        :type index: int
        :param index: New index of the repository source.

        """
        pass

    def __len__(self):
        """Gets the length (number of sources).

        :rtype: int

        """
        pass


class ScriptRepositorySource(object):
    """Repository source."""

    @property
    def name(self):
        """Get or set the name of the repository source.

        :rtype: str

        """
        pass

    @name.setter
    def name(self, value: str):
        pass

    @property
    def location_url(self):
        """Get or set the location URL.

        :rtype: str

        """
        pass

    @location_url.setter
    def location_url(self, value: str):
        pass

    @property
    def is_internal(self):
        """Return whether the repository source is internal.

        If true, then this repository source is an implicit source
        (like the project internal repository or the installation specific
        repository). Therefore its properties like name and location are
        readonly and may not be changed.

        :rtype: bool

        """
        pass


class ScriptDeviceCategory(object):
    """Category of devices.

    Devices can be grouped into categories by means of the
    ``DeviceDescription/Device/DeviceInfo/Category`` tags of the device description
    file. One can implement a corresponding class of this interface to display these types in a
    user-friendly way.

    """

    @property
    def category_id(self):
        """Id of the category.

        :rtype: int

        """
        pass

    @property
    def parent_category(self):
        """The type GUID of the parent device category implementation, or ``Guid.Empty``, if this device implementation is top-level.

        :rtype: Guid

        """
        pass

    @property
    def name(self):
        """Gets a user-friendly display name for this device category.

        This string should be localized.

        :rtype: str

        """
        pass

    @property
    def description(self):
        """Gets a user-friendly description for this device category.

        This string should be localized.

        :rtype: str

        """
        pass
