from .ScriptDeviceUserManagement import *
from .ScriptOnline import *


class ScriptLiveDeviceUserManagement(object):
    """ This object represents the live user management on a given device.

    :version added: 3.5.16.0

    """

    @property
    def online_device(self):
        """ Gets the online device this user management is using.

        :rtype: :class:`ScriptOnlineDevice`

        """
        pass

    @property
    def users(self):
        """ Gets the users on the device.

        :rtype: :class:`ScriptLiveDeviceUserList`

        """
        pass

    @property
    def groups(self):
        """ Gets the groups on the device.

        :rtype: :class:`ScriptLiveDeviceGroupList`

        """
        pass

    def upload(self):
        """ Uploads the user and group information from the device.

        """
        pass

    def backup(self, directory, password):
        """ Backups the user management from the device.

        Don't change the name of the backup file because the device uses a fixed file name.
        Use different directories to store different backups.

        :type directory: str
        :param directory: Directory where the backup file shall be stored.

        :type password: str
        :param password: Password which should be used to protected the backup file.

        :rtype: str
        :returns: Full path of the backup file.

        """
        pass

    def restore(self, path, password):
        """ Restores the user management to the device.

        .. note::
            After the restore of the user management it is possible to get an authentication exception
            during the next operation on the online device because the current login session is no longer valid.
            In this case you catch the exception, reconnect the online device and repeat the operation.

            For example::

                online_device = online.create_online_device(device_obj)
                user_mgmt = online_device.create_live_user_management()
                user_mgmt.restore(file, password)
                try:
                    user_mgmt.upload()
                except:
                    online_device.disconnect()
                    online_device.connect()
                    user_mgmt.upload()

        :type path: str
        :param path: Path of the backup file.

        :type password: str
        :param password: Password which was used to protect the backup file.

        """
        pass

    def add_user(self, name, password, can_change_password=True, must_change_password=False):
        """ Adds a new user with the specified name.

        :type name: str
        :param name: The name of the new user.

        :type password: str
        :param password: Password for the new user.

        :type can_change_password: bool
        :param can_change_password: User can change their password.

        :type must_change_password: bool
        :param must_change_password: User must change their password with next login.

        """
        pass

    def remove_user(self, name):
        """ Removes the user with the specified name.

        :type name: str
        :param name: The name of the existing user.

        """
        pass

    def set_user_password(self, name, password):
        """ Sets the password for this user.

        :type name: str
        :param name: The name of the user.

        :type password: str
        :param password: The password to set.

        """
        pass

    def set_user_flags(self, name, flags):
        """ Sets flags for the user.

        :type name: str
        :param name: The name of the user.

        :type flags: :class:`DeviceUserManagementFlags`
        :param flags: The flags to set.

        """
        pass

    def add_group(self, name, group_members, user_members):
        """ Adds a new group with the specified name.

        :type name: str
        :param name: The name of the new group.

        :type group_members: list[str]
        :param group_members: The group members of the new group.

        :type user_members: list[str]
        :param user_members: The user members of the new group.

        """
        pass

    def remove_group(self, name):
        """ Removes the group with the specified name.

        :type name: str
        :param name: The name of the existing group.

        """
        pass

    def set_members_of_group(self, name, group_members, user_members):
        """ Sets the members of groups and users which shall be in the group.

        :type name: str
        :param name: The name of the group.

        :type group_members: list[str]
        :param group_members: Group names which should be member for the group.

        :type user_members: list[str]
        :param user_members: User names which should be member for the group.

        """
        pass


class ScriptLiveDeviceUserList(list):
    """ Represents a list of script device users.

    :version added: 3.5.16.0

    """

    @property
    def flags(self):
        """ Gets flags concerning the entire user list.

        :rtype: :class:`DeviceUserManagementFlags`

        """
        pass

    def __getitem__(self, index):
        """ Gets the user at the specified index or with the specfied name.

        :type index: int
        :param index: The zero-based index.

        :rtype: :class:`ScriptLiveDeviceUser`
        :returns: The user at the specified index.

        """
        pass

    def __getitem__(self, name):
        """ Gets the user at the specified index or with the specfied name.

        :type name: str
        :param name: The name of the user.

        :rtype: :class:`ScriptLiveDeviceUser`
        :returns: The user with the specified name or `None` if such a user does not exist.

        """
        pass

    def __len__(self):
        """ Gets the number of users in this list.

        :rtype: int

        """
        pass


class ScriptLiveDeviceGroupList(list):
    """ A list of groups on the device.

    :version added: 3.5.16.0

    """

    @property
    def flags(self):
        """ Gets flags concerning the entire group list.

        :rtype: :class:`DeviceUserManagementFlags`

        """
        pass

    def __getitem__(self, index):
        """ Gets the group at the specified index or with the specfied name.

        :type index: int
        :param index: The zero-based index.

        :rtype: :class:`ScriptLiveDeviceGroup`
        :returns: The group at the specified index.

        """
        pass

    def __getitem__(self, name):
        """ Gets the group at the specified index or with the specfied name.

        :type name: str
        :param name: The name of the group.

        :rtype: :class:`ScriptLiveDeviceGroup`
        :returns: The group with the specified name or `None` if such a group does not exist.

        """
        pass

    def __len__(self):
        """ Gets the number of groups in this list.

        :rtype: int
        
        """
        pass


class ScriptLiveDeviceUser(object):
    """ An user on the device.

    :version added: 3.5.16.0

    """

    @property
    def flags(self):
        """ Gets flags concerning this particular user.

        :rtype: :class:`DeviceUserManagementFlags`

        """
        pass

    @property
    def name(self):
        """ Gets the name of the user.

        :rtype: str

        """
        pass


class ScriptLiveDeviceGroup(object):
    """ A group of users, which have common rights on the device.

    :version added: 3.5.16.0

    """

    @property
    def flags(self):
        """ Gets flags concerning this particular group.

        :rtype: :class:`DeviceUserManagementFlags`

        """
        pass

    @property
    def name(self):
        """ Gets the name of the group.

        :rtype: str

        """
        pass

    @property
    def user_members(self):
        """ Gets the user names which are member of this group.

        :rtype: tuple[str]

        """
        pass

    @property
    def group_members(self):
        """ Gets the group names which are member of this group.

        :rtype: tuple[str]

        """
        pass

    def check_cyclic_membership(self, new_group_member):
        """ Checks whether adding the specified group member would cause a cyclic membership dependency.

        :type new_group_member: str
        :param new_group_member: The name of the new group membership to check.

        :rtype: bool
        :returns: `True` if adding the specified group member would cause a cycle, `False` otherwise.

        """
        pass
