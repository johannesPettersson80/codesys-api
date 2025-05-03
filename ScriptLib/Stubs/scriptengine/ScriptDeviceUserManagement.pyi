from enum import Enum
from .dotNETs import *
from .ScriptOnline import *


class DeviceUserManagementFlags(Enum):
    """Flags for the entire _3S.CoDeSys.Core.Online.IDeviceUserList, the entire _3S.CoDeSys.Core.Online.IDeviceGroupList,
    a single _3S.CoDeSys.Core.Online.IDeviceUser, or a single _3S.CoDeSys.Core.Online.IDeviceGroup.

    """

    Edit = 1,
    """If set, the particular _3S.CoDeSys.Core.Online.IDeviceUser or _3S.CoDeSys.Core.Online.IDeviceGroup
        can be edited.
    """

    AddMember = 2,
    """If set, users or groups can be added to the particular _3S.CoDeSys.Core.Online.IDeviceGroup."""

    RemoveMember = 4,
    """If set, users or groups can be removed from the particular _3S.CoDeSys.Core.Online.IDeviceGroup."""

    Create = 8,
    """If set, new users can be created in the particular _3S.CoDeSys.Core.Online.IDeviceUserList,
        or new groups can be created in the particular _3S.CoDeSys.Core.Online.IDeviceGroupList.
    """

    Delete = 16,
    """If set, existing users can be deleted from the particular _3S.CoDeSys.Core.Online.IDeviceUserList,
        or existing groups can be deleted from the particular _3S.CoDeSys.Core.Online.IDeviceGroupList
    """

    RemoveAllMembers = 32,
    """If set, all existing users can be removed from the particular _3S.CoDeSys.Core.Online.IDeviceUserList.
        If not set, at least one user must be available in this group.
    """

    EditRights = 64,
    """If set, permissions for the particular _3S.CoDeSys.Core.Online.IDeviceGroup can
        be changed
    """

    Owner = 128,
    """If set, the particular _3S.CoDeSys.Core.Online.IDeviceGroup is the owner group"""

    NameEditable = 256,
    """If set, the name of the particular _3S.CoDeSys.Core.Online.IDeviceUser or _3S.CoDeSys.Core.Online.IDeviceGroup
        is editable.
    """

    PasswordUpToDate = 4096,
    """If this flag is not set, a new password needs to be set by the user at the next login."""

    PasswordEditable = 8192,
    """If this flag is set, the user can change his own password."""

    All = 4294967167
    """All flags together except flag Owner."""


class ScriptDeviceUserManagement(object):
    """This object represents the user management on a given device."""

    @property
    def online_device(self):
        """Gets the online device this user management was created from.

        :rtype: :class:`ScriptOnlineDevice`

        """
        pass

    @property
    def users(self):
        """Gets the users on the device.

        Modifications of this list will take place
        offline and come into effect by downloading the user management to the device.

        :rtype: :class:`ScriptDeviceUserList`

        """
        pass

    @property
    def groups(self):
        """Gets the groups on the device.

        Modifications of this list will take place
        offline and come into effect by downloading the user management to the device.

        :rtype: :class:`ScriptDeviceGroupList`

        """
        pass

    def reload_from_program(self):
        """Reloads the user management contents from the device object in the project."""
        pass

    def store_to_project(self):
        """Writes the current contents of the user management back to the device object in the project.

        You should always use this method to persist your changes into the project. If you
        don't call this method, the project will contain an outdated state.

        """
        pass

    def upload(self):
        """Uploads the user and group information from the device."""
        pass

    def download(self):
        """Downloads the user and group information to the device."""
        pass

    def load(self, xml_or_file_name: str):
        """Loads the contents of the given XML element into this user management object.

        :type xml_or_file_name: str
        :param xml_or_file_name: The XML document to read. If this is a valid file name of
		    an existing file, its contents will be read. If it directly contains a valid XML
		    document, it will be parsed directly.

        """
        pass

    def load(self, element: XmlElement):
        """Loads the contents of the given XML element into this user management object.

        :type element: XmlElement
        :param element: The element.

        """
        pass

    def save(self):
        """Saves the contents of this user management object as XML into a string.

        :rtype: str
        :returns: A string containing the XML representation of this user management.

        """
        pass

    def save(self, file_name):
        """Saves the contents of this user management object as XML into a file.

        :type file_name: str
        :param file_name: The file name.

        """
        pass

    def save(self, writer=None):
        """Saves the contents of this user management object as XML into an ``System.Xml.XmlWriter``.

        :type writer: XmlWriter
        :param writer: The writer.

        """
        pass


class ScriptDeviceUserList(list):
    """Represents a list of script device users."""

    @property
    def flags(self):
        """Gets flags concerning the entire user list.

        :rtype: DeviceUserManagementFlags

        """
        pass

    def __len__(self):
        """Gets the number of users in this list.

        :rtype: int

        """
        pass

    def __getitem__(self, index: int):
        """Gets the user at the specified index or with the specified name.

        :type index: int
        :param index: The zero-based index.

        :rtype: :class:`ScriptDeviceUser`
        :returns: The user at the specified index or ``None`` if such a user does not exist.

        """
        pass

    def __getitem__(self, name: str):
        """Gets the user at the specified index or with the specified name.

        :type name: str
        :param name: The user name.

        :rtype: :class:`ScriptDeviceUser`
        :returns: The user  with the specified name, or ``None`` if such a user does not exist.

        """
        pass

    def add(self, name):
        """Adds a new user with the specified name.

        :type name: str
        :param name: The name of the new user.

        :raises ArgumentException: A user with the specified name already exists.
        :raises NotSupportedException: Adding new users is not supported. Check :attr:`flags` for
            the :attr:`DeviceUserManagementFlags.Create` flag in advance.

        :rtype: :class:`ScriptDeviceUser`
        :returns: The newly created user.

        """
        pass

    def remove(self, name):
        """Removes the user with the specified name.

        :type name: str
        :param name: The name of the existing user.

        :raises NotSupportedException:
            * Deleting existing users is not supported. Check
              :attr:`ScriptDeviceUser.flags` for the :attr:`DeviceUserManagementFlags.Delete` flag
              in advance.
            * Removing a member from a group in which the specified user is a member of is not
              supported.
              Check :attr:`ScriptDeviceGroup.flags` of all affected groups for the
              :attr:`DeviceUserManagementFlags.RemoveMember` flag in advance.

        :rtype: bool
        :returns: ``True`` if the user existed and was removed, otherwise ``False``

        """
        pass

    def clear(self):
        """Removes all users.

        :raises NotSupportedException: Deleting existing users is not supported. Check
            :attr:`ScriptDeviceUser.flags` for the :attr:`DeviceUserManagementFlags.Delete` flag in
            advance.
            --OR--
            Removing a member from a group in which the specified user is a member of is not
            supported.
            Check :attr:`ScriptDeviceGroup.flags` of all affected groups for the
            :attr:`DeviceUserManagementFlags.RemoveMember` flag in advance.

        """
        pass


class ScriptDeviceGroupList(list):
    """A list of groups on the device."""

    @property
    def flags(self):
        """Gets flags concerning the entire group list.

        :rtype: :class:`DeviceUserManagementFlags`

        """
        pass

    def __len__(self):
        """Gets the number of groups in this list.

        :rtype: int

        """
        pass

    def __getitem__(self, index):
        """Gets the group at the specified index or with the specified name.

        :type index: int
        :param index: The zero-based index or the group name.

        :rtype: :class:`ScriptDeviceGroup`
        :returns: The group at the specified index.
            or ``None`` if such a group does not exist.

        """
        pass

    def __getitem__(self, name):
        """Gets the group at the specified index or with the specified name.

        :type name: str
        :param name: The group name.

        :rtype: :class:`ScriptDeviceGroup`
        :returns: The group with the specified name,
            or ``None`` if such a group does not exist.

        """
        pass

    def add(self, name):
        """Adds a new group with the specified name.

        :type name: str
        :param name: The name of the group.

        :rtype: :class:`ScriptDeviceGroup`
        :returns: The newly created group, or ``None`` if a group with the specified name already
            exists.

        """
        pass

    def remove(self, name):
        """Removes the group with the specified name.

        :type name: str
        :param name: The name of the existing group.


        :rtype: bool
        :returns: ``True`` if the group existed and was removed, otherwise ``False``

        """
        pass

    def clear(self):
        """Removes all groups."""
        pass


class ScriptDeviceUser(object):
    """An user on this device."""

    @property
    def flags(self):
        """Gets flags concerning this particular user.

        :rtype: :class:`DeviceUserManagementFlags`

        """
        pass

    @property
    def name(self):
        """Gets or sets the name of the user.

        :raises NotSupportedException: Editing this user is not supported. Check :attr:`flags` for
            the :attr:`DeviceUserManagementFlags.Edit` flag in advance.

        :raises ArgumentException: A user with the specified name already exists.

        :rtype: str

        """
        pass

    @name.setter
    def name(self, value: str):
        pass

    def set_password(self, password):
        """Sets the password for this user.

        :type password: str
        :param password: The password to set.

        """
        pass

    @property
    def password_hash(self):
        """Gets or sets the encrypted password for this user.

        :raises NotSupportedException: Editing this user is not supported. Check :attr:`flags` for
            the :attr:`DeviceUserManagementFlags.Edit` flag in advance.

        :rtype: str

        """
        pass

    @password_hash.setter
    def password_hash(self, value: str):
        pass

    def set_user_flags(self, flags):
        """Sets flags for the user.

        :type flags: DeviceUserManagementFlags
        :param flags: The flags to set.
        """
        pass


class ScriptDeviceGroup(object):
    """A group of users, which have common rights on the device."""

    @property
    def flags(self):
        """Gets flags concerning this particular group.

        :rtype: :class:`DeviceUserManagementFlags`

        """
        pass

    @property
    def name(self):
        """Gets or sets the name of the group.

        :raises NotSupportedException: Editing this user is not supported. Check :attr:`flags` for
            the :attr:`DeviceUserManagementFlags.Edit` flag in advance.

        :raises ArgumentException: A group with the specified name already exists.

        :rtype: str

        """
        pass

    @name.setter
    def name(self, value: str):
        pass

    @property
    def user_members(self):
        """Gets the list of all user names which are members of this group.

        This list can be modifed in-place to add or remove users
        from this group.

        :rtype: list[string]

        """
        pass

    @property
    def group_members(self):
        """Gets the list of all group names which are members of this group.

        This list can be modifed in-place to add or remove groups
        from this group.

        :rtype: list[str]

        """
        pass

    def check_cyclic_membership(self, new_group_member):
        """Checks whether adding the specified group member would cause a cyclic membership dependency.

        :type new_group_member: str
        :param new_group_member: The name of the new group membership to check.

        :rtype: bool
        :returns: ``True`` if adding the specified group member would cause a cycle,
            otherwise ``False``.

        """
        pass
