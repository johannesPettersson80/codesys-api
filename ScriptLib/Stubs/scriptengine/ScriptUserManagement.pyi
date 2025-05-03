from enum import Enum
from .dotNETs import *
from .ScriptProject import *
from .ScriptSystem import *


class ObjectPermissionKind(Enum):
    """ This enumeration contains the various possibilites to access an object from the
        viewpoint of the User Management.
    """

    View = 0,
    """The permission to view an object."""

    Modify = 1,
    """The permission to modify an object."""

    Remove = 2,
    """The permission to remove an object."""

    AddRemoveChildren = 3
    """The permission to add or remove a child to or from an object."""


class PermissionState(Enum):
    """The permission state, either "granted", "denied", or "default"."""

    Granted = 0,
    """The corresponding permission is explicitely granted to a certain group."""

    Denied = 1,
    """The corresponding permission is explicitely denied to a certain group."""

    Default = 2
    """The corresponding permission is not explicitely set for a certain group."""


class ScriptUserManagement(object):
    """UserManagement interface."""

    @property
    def project(self):
        """Backlink to the project for this user management.

        :rtype: :class:`ScriptProject`

        """
        pass

    @property
    def users(self):
        """The collection of all defined users for this project.

        :rtype: :class:`ScriptUserList`

        """
        pass

    @property
    def groups(self):
        """The colleciton of all defined groups for this project.

        :rtype: :class:`ScriptGroupList`

        """
        pass

    @property
    def logged_on_user(self):
        """Gets the user which is currently logged in, or None if no user is currently logged in.

        :rtype: :class:`ScriptUser`

        """
        pass

    @property
    def login_time(self):
        """Gets the timestamp since the last successful login, or DateTime.MinValue if no user is currently logged in.

        :rtype: DateTime

        """
        pass

    def login(self, username, password):
        """Log into the project using the specified credentials.

        This is equal to :meth:`ScriptProject.login`.

        :type username: str
        :param username: The username.

        :type password: str
        :param password: The password.

        """
        pass

    def logout(self):
        """Log out from the project (back to the user "nobody").

        This is equal to :meth:`.ScriptProject.logout`.

        """
        pass

    def check_available(self, type):
        """Checks whether permission management for the given PermissionType is available in the given CoDeSys installation.

        :type type: Guid
        :param type: The type.

        :rtype: bool

        """
        pass

    def get_user_management_permission(self):
        """Gets the permission object for the user management.

        :rtype: :class:`ScriptPermission`

        """
        pass

    def get_command_permission(self, commandguid):
        """Gets the permission object for execution of a specific command.

        :type commandguid: Guid or :class:`ScriptCommand`
        :param commandguid: The ScriptCommand or its Guid.

        :rtype: :class:`ScriptCommandPermission`
        :returns: The command permission object.

        """
        pass

    def get_factory_permission(self, factory):
        """Gets the permission object for accessing a specific object factory.

        :type factory: Guid or :class:`ScriptObjectFactory`
        :param factory: The factory or its guid.

        :rtype: :class:`ScriptFactoryPermission`
        :returns: The factory permission object.

        """
        pass

    def get_object_permission(self, obj, kind):
        """Gets a Permission object for that specific script object.

        :type obj: :class:`ScriptObject`
        :param obj: The object we want the permission for.

        :type kind: :class:`ObjectPermissionKind`
        :param kind: The kind of object access permission we want.

        :rtype: :class:`ScriptObjectPermission`
        :returns: The ScriptObject.

        """
        pass

    @property
    def types(self):
        """Gets all available types.

        :rtype: :class:`ScriptPermissionTypes`

        """
        pass


class ScriptPermissionTypes(list):
    """This object represents all available permission types."""

    @property
    def usermanagement(self):
        """The permission type guid for user management, or Guid.Empty if not available in this installation.

        :rtype: Guid

        """
        pass

    @property
    def objectaccess(self):
        """The permission type guid for object access rights, or Guid.Empty if not available in this installation.

        :rtype: Guid

        """
        pass

    @property
    def objectfactory(self):
        """The permission type guid for object factory rights (object creation), or Guid.Empty if not available in this installation.

        :rtype: Guid

        """
        pass

    @property
    def commandexecution(self):
        """The permission type guid for execution of commands, or Guid.Empty if not available in this installation.

        :rtype: Guid

        """
        pass


class ScriptUserList(list):
    """Represents the list of all users known to the current project."""

    @property
    def user_management(self):
        """Back-Link to the project's user management.

        :rtype: :class:`ScriptUserManagement`

        """
        pass

    @property
    def project(self):
        """Backlink to the project for this user management.

        :rtype: :class:`ScriptProject`

        """
        pass

    def create(self, name):
        """Creates a new user with the specified name.

        :type name: str
        :param name: The name.

        :rtype: :class:`ScriptUser`

        """
        pass

    def __getitem__(self, id_or_name):
        """Gets the :class:`ScriptUser` with the specified id or name.

        :type id_or_name: Guid or str

        :rtype: :class:`ScriptUser`

        """
        pass


class ScriptUserOrGroup(object):
    """This interface contains the common members of :class:`ScriptUser` and :class:`ScriptGroup`."""

    @property
    def project(self):
        """Backlink to the project for this user management.

        :rtype: :class:`ScriptProject`

        """
        pass

    @property
    def user_management(self):
        """Back-Link to the project's user management.

        :rtype: :class:`ScriptUserManagement`

        """
        pass

    @property
    def is_user(self):
        """Gets a value indicating whether this ScriptUserOrGroup is an user.

        :rtype: bool

        """
        pass

    @property
    def is_group(self):
        """Gets a value indicating whether this ScriptUserOrGroup is a group.

        :rtype: bool

        """
        pass

    @property
    def id(self):
        """Gets the ID of this user or group.

        :rtype: Guid

        """
        pass

    @property
    def name(self):
        """Gets the login name of this user or group.

        :rtype: str

        """
        pass

    @property
    def description(self):
        """Gets or sets the description for this user or group. This is informative only.

        :rtype: str

        """
        pass

    @description.setter
    def description(self, value: str):
        pass

    def add_to(self, parent):
        """Adds this user or group to the specified parent group.

        :type parent: :class:`ScriptGroup`
        :param parent: The parent.

        """
        pass

    def remove_from(self, parent):
        """Removes this user or group from the specified parent group.

        :type parent: :class:`ScriptGroup`
        :param parent: The parent.

        """
        pass


class ScriptUser(ScriptUserOrGroup):
    """Instances of this interface represent a single user within the user management.

    A user is uniquely identified by its ID (not by its name), although its name must also be unique
    within a user list.

    """

    @property
    def userlist(self):
        """Backreference to the user list.

        :rtype: :class:`ScriptUserList`

        """
        pass

    @property
    def fullname(self):
        """Gets or sets the full name of this user. This is informative only.

        :rtype: str

        """
        pass

    @fullname.setter
    def fullname(self, value: str):
        pass

    @property
    def active(self):
        """Gets or sets a boolean which indicates whether this user is currently active.

        Inactive users cannot login to the user management.

        :rtype: bool

        """
        pass

    @active.setter
    def active(self, value: bool):
        pass

    def check_password(self, password):
        """Checks the password for an user.

        :type password: str
        :param password: The password.

        :rtype: bool
        :returns: ``True`` if the password is correct.

        """
        pass

    def change_password(self, old_password, new_password):
        """Changes the password for the user.

        :type old_password: str
        :param old_password: The old password.

        :type new_password: str
        :param new_password: The new password.

        """
        pass

    def remove(self):
        """Removes the user with the specified ID from this list.

        :raises UserNotExistingException: If the user does not exist
            (e. G. because it was removed before).

        :raises CannotRemoveLastMemberFromOwnerGroupException: If the user is the last member of
            the owner group.

        """
        pass

    def rename(self, newname):
        """Renames the user.

        :type newname: str
        :param newname: The new name.

        """
        pass

    @property
    def groups(self):
        """Gets a python tuple with the groups this user is member of.

        :rtype: tuple[ScriptGroup]

        """
        pass


class ScriptGroupList(list):
    """Represents the list of all known groups in this project."""

    @property
    def user_management(self):
        """Back-Link to the project's user management.

        :rtype: :class:`ScriptUserManagement`

        """
        pass

    @property
    def project(self):
        """Backlink to the project for this user management.

        :rtype: :class:`ScriptProject`

        """
        pass

    def create(self, name):
        """Creates a new group with the specified name.

        :type name: str
        :param name: The name.

        :rtype: :class:`ScriptGroup`
        :returns: The newly created group.

        """
        pass

    def __getitem__(self, id_or_name):
        """Gets the :class:`ScriptGroup` with the specified id or name.

        :type id_or_name: Guid or str

        :rtype: :class:`ScriptUser`
        :returns: The ScriptGroup, or ``None`` if such a group does not exist.

        """
        pass

    @property
    def owner_group(self):
        """Owner group.

        :rtype: :class:`ScriptGroup`

        """
        pass

    @property
    def everyone_group(self):
        """
        Everyone group.

        :rtype: :class:`ScriptGroup`

        """
        pass


class ScriptGroup(ScriptUserOrGroup):
    """Instances of this interface represent a single group within the user management.

    A group is uniquely identified by its ID (not by its name), although its name must also be unique
    within a group list.

    """

    @property
    def grouplist(self):
        """Backlink to the grouplist.

        :rtype: :class:`ScriptGroupList`

        """
        pass

    def add_member(self, member):
        """Adds a member to this group. This might be either a user or another group.

        If such a user or group does not exist, (e. G. because it was deleted in the meantime),
        a UserNotExistingException, GroupNotExistingException, or
        UserOrGroupNotExistingException is thrown. If the user or group is already a member of
        this group, a UserIsAlreadyMemberOfGroupException or
        GroupIsAlreadyMemberOfGroupException is thrown.

        :type member: :class:`ScriptUserOrGroup`
        :param member: The user or group.

        :raises GroupCycleException: If this addition would cause a membership cycle.

        """
        pass

    def remove_member(self, member):
        """Removes a member from this group.

        :type member: :class:`ScriptUserOrGroup`
        :param member: The member.

        """
        pass

    def has_member(self, member):
        """Checks whether the specified user or group is a member of this group.

        :type member: :class:`ScriptUserOrGroup`
        :param member: The member.

        :rtype: bool
        :returns: ``True`` if the specified user or group is member of this group,
            otherwise ``False``.

        """
        pass

    def get_user_members(self, recursive):
        """Returns a python tuple of all users which are member of this group, or which are members of group members of this group.

        :type recursive: bool
        :param recursive: if set to ``True``, includes users which are members of group members
            of this group.

        :rtype: list
        :returns: A python tuple of :class:`ScriptUser` objects.

        """
        pass

    def get_group_members(self):
        """Gets a python tuple of all groups which are member of this group.

        :rtype: list

        """
        pass

    @property
    def is_everyone_group(self):
        """Gets a boolean value indicating whether this group is the "everyone" group.

        :rtype: bool

        """
        pass

    @property
    def is_owner_group(self):
        """Gets a boolean value indicating whether this group is the "owner" group.

        :rtype: bool

        """
        pass

    def rename(self, newname):
        """Renames the group.

        :type newname: str
        :param newname: The new name.

        """
        pass

    def remove(self):
        """Removes this group from the containing grouplist."""
        pass


class ScriptPermission(object):
    """Interface for permission objects."""

    @property
    def type(self):
        """Gets the type.

        :rtype: Guid

        """
        pass

    def check_permission(self, silent_or_group):
        """This overload is used when ``silent_or_group`` is of type *bool*.

        Checks whether the currently logged in user has a specific permission or not.

        :type silent: bool
        :param silent: If of type bool:
            If ``False``, when the permission is not granted, the ``RequestAuthorization`` event
            is triggered which typically prompts a new login interactively and the permission is
            checked again with the new login. If ``True``, nothing will be prompted.

        :rtype: bool
        :returns: True if the user is allowed.


        This overload is used when ``silent_or_group`` is of type *ScriptGroup*.

        :type group: :class:`ScriptGroup`
        :param group: The group.

        :rtype: bool
        :returns: True if the permission is allowed.

        """
        pass

    def get_permission_state(self, group, resolve_effective=True, resolve_inherited=False):
        """Gets the the state of a specific permission.

        You can use :attr:`.System.commands` to search for a command guid.

        :type group: :class:`ScriptGroup`
        :param group: The group.

        :type resolve_effective: bool
        :param resolve_effective: If ``True``, when the permission is not explicitely
            granted or denied, it will be resolved (e.g. by asking the parent object, and finally
            deferring to a default value). This value overrides ``resolve_inherited``.

        :type resolve_inherited: bool
        :param resolve_inherited: If set to ``True``, for hierarchical properties
            (currently only the object access properties), the parent objects are resolved for
            inherited properties. If set to false, only the properties directly set at the object
            are resolved. If ``resolve_effective`` is ``True``, the parents are
            always resolved and this parameter is ignored.

        :rtype: :class:`PermissionState`
        :returns: If ``resolve_effective`` is ``True``, :attr:`PermissionState.Granted` or
            :attr:`PermissionState.Denied`. If ``resolve_effective`` is ``False``,
            :attr:`PermissionState.Default` might be returned additionally.

        """
        pass

    def set_permission_state(self, group, state):
        """Sets the permissions for a specific command.

        :type group: :class:`ScriptGroup`
        :param group: The group.

        :type state: :class:`PermissionState`
        :param state: The state.

        """
        pass

    def check_set_permission_state(self, group, state, silent=True):
        """Checks whether our group is allowed to set a specific permission.

        :type group: :class:`ScriptGroup`
        :param group: The group.

        :type state: :class:`PermissionState`
        :param state: The state.

        :type silent: bool
        :param silent: If ``False``, when the permission is not granted, the
            ``RequestAuthorization`` event is triggered which typically prompts a new login
            interactively and the permission is checked again with the new login.
            If ``True``, nothing will be prompted.

        :rtype: bool
        :returns: ``True`` if the user is allowed.

        """
        pass


class ScriptObjectPermission(ScriptPermission):
    """ObjectAccess Permissions come with additional information about which object to access, and the specific kind of object access."""

    def check_permission_extended(self):
        """Checks the effective permission the current user has for the given object.

        This considers permission inheritance along the object tree etc. This method may prompt the user for a new
        login.

        :rtype: Exception
        :returns: An Exception object describing why the user currently does not have access for
            the given object, and None if the user has access.

        """
        pass

    @property
    def target_object(self):
        """Target object.

        :rtype: :class:`ScriptObject`

        """
        pass

    @property
    def access_kind(self):
        """Access kind.

        :rtype: :class:`ObjectPermissionKind`

        """
        pass


class ScriptCommandPermission(ScriptPermission):
    """Permissions for commands come with the command guid."""

    @property
    def command_guid(self):
        """Gets the command guid.

        :rtype: Guid

        """
        pass


class ScriptFactoryPermission(ScriptPermission):
    """Permissions for factories come with a guid describing the object factory."""

    @property
    def factory_guid(self):
        """Gets the factory guid.

        :rtype: Guid

        """
        pass
