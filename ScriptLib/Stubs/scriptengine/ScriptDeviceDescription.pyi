from .ScriptDeviceObject import DeviceId


class ScriptDeviceCollection(list):
    """A collection of :class:`ScriptDeviceDescription` objects."""

    @property
    def __len__(self):
        """Gets the length (number of device descriptions).

        :rtype: int
        :returns: The number of device descriptions.

        """
        pass

    @property
    def vendors(self):
        """Gets the list of all vendors in the collection.

        :rtype: tuple[int]

        """
        pass

    def get_devices_of_vendor(self, vendor):
        """Get all devices in the list which match the specified vendor.

        :type vendor: str
        :param vendor: Vendor name.

        :rtype: ScriptDeviceCollection
        :returns: A collection of devices from one vendor.

        """
        pass


class ScriptDeviceDescription(object):
    """Description of a device."""

    @property
    def device_id(self):
        """Get the identification object of the device.

        :rtype: :class:`DeviceID`
        :returns: DeviceID

        """
        pass

    @property
    def device_info(self):
        """Get information about the device.

        :rtype: :class:`ScriptDeviceInfo`
        :returns: DeviceInfo

        """
        pass

    @property
    def connectors(self):
        """Gets the connectors.

        :rtype: :class:`ScriptDeviceConnectorSet`
        :returns: DeviceConnectorSet

        """
        pass

    @property
    def name(self):
        """Internationalized name of the device.

        :rtype: str

        """
        pass

    @property
    def description(self):
        """Internationalized description of the device.

        :rtype: str

        """
        pass

    @property
    def vendor(self):
        """Internationalized vendor of the device vendor.

        :rtype: str

        """
        pass

    @property
    def categories(self):
        """Gets a list of categories this device belongs to.

        :rtype: tuple[int]

        """
        pass

    @property
    def families(self):
        """Gets a list of vendor-specific families this device belongs to.

        Each string has got the format ``VendorId:FamilyId``.

        :rtype: tuple[str]

        """
        pass

    @property
    def custom(self):
        r"""Get vendor specific information for the device.

        This property may contain all kinds of information not defined by the specification,
        structured as an XML-Fragment with root node "Custom".

        Example::
            `&lt;Custom&gt;&lt;MaxTemp&gt;30&lt;/MaxTemp&gt;&lt;/Custom&gt;`\\

        :rtype: str

        """
        pass

    @property
    def order_number(self):
        """Vendor specific order number for this device.

        :rtype: str

        """
        pass

    @property
    def default_instance_name(self):
        """The default intance name for this device.

        :version added: 3.5.11.0

        :rtype: str

        """
        pass


class ScriptVendorDescription(object):
    """Vendor description."""

    @property
    def vendor_id(self):
        """Id of the vendor.

        :rtype: int

        """
        pass

    @property
    def version(self):
        """Version.

        :rtype: str

        """
        pass

    @property
    def vendor_info(self):
        """Vendor information.

        :rtype: :class:`ScriptVendorInfo`

        """
        pass

    @property
    def families(self):
        """Get all families of the vendor.

        :rtype: tuple[ScriptDeviceFamily]

        """
        pass

    def get_family(self, family_id):
        """Get the family with the specified family Id.

        :type family_id: int
        :param family_id: Family Id.

        :rtype: :class:`ScriptDeviceFamily`
        :returns: Device family object or ``None`` if there is no matching family.

        """
        pass


class ScriptVendorInfo(object):
    """Vendor information."""

    @property
    def name(self):
        """Vendor name.

        :rtype: str

        """
        pass

    @property
    def addresses(self):
        """Address of the vendor.

        :rtype: tuple[str]

        """
        pass

    @property
    def phones(self):
        """Phone number(s).

        :rtype: tuple[str]

        """
        pass

    @property
    def faxes(self):
        """Fax number(s).

        :rtype: tuple[str]

        """
        pass

    @property
    def mail_addresses(self):
        """eMail address(es).

        :rtype: tuple[str]

        """
        pass

    @property
    def web_addresses(self):
        """Web address(es).

        :rtype: tuple[str]

        """
        pass


class ScriptDeviceFamily(object):
    """Family Id."""

    @property
    def family_id(self):
        """Family Id.

        :rtype: int

        """
        pass

    @property
    def parent_family(self):
        """Parent family.

        :rtype: str

        """
        pass

    @property
    def name(self):
        """Family name.

        :rtype: str

        """
        pass

    @property
    def description(self):
        """Description of the family.

        :rtype: str

        """
        pass

    @property
    def sub_families(self):
        """Sub families of the family.

        :rtype: tuple[ScriptDeviceFamily]

        """
        pass
