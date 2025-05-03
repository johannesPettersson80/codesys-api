from enum import Enum
from .dotNETs import *
from .ScriptDeviceObject import *
from .ScriptDeviceUserManagement import *
from .ScriptLiveDeviceUserManagement import *
from .ScriptObject import *


def CredentialSourceKind(Enum):
    """The kinds of authentication allowed for the fallback to the default handler."""

    All = -1,
    """ All source kinds are allowed. (This is the default value when 
        no _3S.CoDeSys.Core.Online.ITemporaryLoginCredentialsContext is set.)
    """

    none = 0,
    """No credential source kind allowed."""

    CurrentProjectSession = 1,
    """Tries a device login via the current project login credentials (if logged in)."""

    Interactive = 2,
    """Queries the user interactively for the credentials. Disabling this bit can be
        useful for test scripts or python scripts, when no interactive prompt is wanted.
    """

    InteractivePasswordRenewal = 4
    """Queries the user interactively for a new password. Only works 
        if _3S.CoDeSys.Core.Online.CredentialSourceKind.Interactive is also set.
    """
    pass


class OnlineChangeOption(Enum):
    """Online change options used for multiple download."""

    Never = 0,
    """Online change shall never be performed. In that case a full download is forced."""

    Try = 1,
    """Online change shall be tried. If not possible, a full download shall be performed."""

    Force = 2,
    """Online change shall be forced. If not possible, the action is terminated with no change."""

    Keep = 3
    """Try to login. Do not online update. Do not download. Keep as it is."""
    pass


class ApplicationState(Enum):
    """Execution state of an application."""

    none = 0,
    """No valid application state (eg. not loaded)."""

    run = 1,
    """Application is running."""

    stop = 2,
    """Application is stopped."""

    halt_on_bp = 3,
    """Halted on a breakpoint."""

    debug_step = 4,
    """Executing a single step in the debugger."""

    single_cycle = 5,
    """Executing a single cycle in the debugger."""

    system_application = 255,
    """TOCHECK maybe to delete, a special flag indicating a system application
        (only possible state is stop)
    """

    unknown = 65535
    """Unknown application state. uint.MaxValue, exact value depends on system"""
    pass


class OperatingState(Enum):
    """The global state of an application. Although not defined as such, this enumeration
        is treated like a flags field, so the effective value may be a combination of
        more of these values.
    """

    none = 0,
    """No application loaded."""

    program_loaded = 1,
    """Program code is loaded (ready to execute)"""

    download = 2,
    """A download is in progress."""

    online_change = 4,
    """Performing an online change."""

    store_bootproject = 8,
    """Storing the bootproject."""

    force_active = 16,
    """There are currently forced values for this application."""

    """Application stopped since an exception occurred. A reset is required to restart the application."""
    exception = 32,

    run_after_download = 64,
    """Download code at the end of download is in progress (initialization of the application)"""

    store_bootproject_only = 128,
    """Only the bootproject is stored at download"""

    exit = 256,
    """Application exit is still executed (application is no longer active)"""

    delete = 512,
    """Application is deleted (object is available, but the content is stil deleted)"""

    reset = 1024,
    """Application reset is in progress"""

    retain_mismatch = 2048,
    """Retain mismatch occurred during loading the bootproject (retain data does not match to the application)"""

    bootproject_valid = 4096,
    """Bootproject available (bootproject matched to running application in RAM)"""

    load_bootproject = 8192,
    """Loading bootproject in progress"""

    flow_active = 16384,
    """flow control is active"""

    run_in_flash = 32768,
    """Application is running in flash only"""

    core_dump_loaded = 131072,
    """A Core-Dump for this application is loaded"""

    executionpoints_active = 262144,
    """there are Executionpoints active in the application"""

    core_dump_creating = 524288
    """there are Executionpoints active in the application"""
    pass


class ResetOption(Enum):
    """This enum defines the different kinds of reset (warm, cold, origin)"""

    Warm = 0,
    """Warm reset of the application - keep retain variables."""

    Cold = 1,
    """"Cold" reset - keep persistent variables and applications"""

    Original = 2
    """Reset "original" - erase all variables, applications, etc."""
    pass


class BlockDriverType(Enum):
    """An enumeration to specify the type of Block Driver used on the runtime system"""

    Generic = 0,
    """Any of the regular block drivers without special treatment or unknown"""

    CmpBlkDrvTcp = 1,
    """The Block Driver TCP in the runtime system"""

    CmpBlkDrvCom = 2,
    """The Block Driver COM in the runtime system"""

    CmpBlkDrvUsb = 3,
    """The Block Driver UDP in the runtime system"""

    CmpBlkDrvShm = 4,
    """The Block Driver Shared Memory in the runtime system"""

    CmpBlkDrvUdp = 5,
    """The Block Driver UDP in the runtime system"""

    CmpBlkDrvCanClient = 6,
    """The Block Driver CAN Client in the runtime system"""

    CmpBlkDrvCanServer = 7,
    """The Block Driver CAN Server in the runtime system"""

    CmpBlkDrvDirectCall = 8,
    """The Block Driver Direct Call in the runtime system"""

    CmpBlkDrvDNS = 9
    """The Block Driver DNS in the runtime system"""
    pass


class ParamType(Enum):
    """Enumeration defining allowed types for a gateway parameter. The types match the
        equally named .NET types.
    """

    SByte = 17,
    """8 bit signed byte"""

    Byte = 18,
    """Unsigned byte (8 bit)"""

    Int16 = 19,
    """16 bit signed integer"""

    UInt16 = 20,
    """16 bit unsigned integer"""

    Int32 = 21,
    """32 bit signed integer"""

    UInt32 = 22,
    """32 bit unsigned integer"""

    Int64 = 23,
    """64 bit signed integer"""

    UInt64 = 24,
    """64 bit unsigned integer"""

    Char = 25,
    """A single character"""

    Single = 26,
    """Single precission FloatingPoint value"""

    Double = 27,
    """Double precission FloatingPoint value"""

    Boolean = 28,
    """Boolean value (true or false)"""

    StringAnsi = 29,
    """ASCII coded string"""

    StringUnicode = 30
    """Unicode coded string."""
    pass


class AdditionalDirInfo(Enum):
    """Flags to get additional information about a file or directory."""

    None = 0,
    """No information available"""

    PlaceholderDirectory = 1,
    """The directory is defined as a placeholder directory (e.g. $PlcLogic$) on the PLC."""

    RedundantDirectory = 2
    """The directory is a shortcut to another directory (e.g. links to a subdirectory
        in the default path)
    """
    pass


class ScriptOnline(object):
    """Online functionality for the ScriptEngine.

    Some of the commands may temporarily change the active application.

    """

    def create_online_application(self, application=None):
        """Creates an online application.

        To prevent resource leaks, script writers should wrap the usage
        of the online application in a with: block.

        :type application: :class:`ScriptObject`
        :param application: The application object to use. If
            this parameter is omitted, the active application is used.

        :rtype: Before V3.5.0.0 :class:`ScriptOnlineApplication`
        :rtype: :class:`ScriptOnlineDevice`
        :returns: The online application object.

        """
        pass

    @property
    def UNFORCE(self):
        """Special value for unforcing a variable.

        It is returned by
        :meth:`ScriptOnlineApplication.get_prepared_value`
        and can be fed to :meth:`ScriptOnlineApplication.set_prepared_value`. See also
        :meth:`ScriptOnlineApplication.set_unforce_value`.

        :rtype: str

        """
        pass

    @property
    def UNFORCE_RESTORE(self):
        """Special value for unforcing and restoring a variable.

        It is returned by
        :meth:`ScriptOnlineApplication.get_prepared_value`
        and can be fed to :meth:`ScriptOnlineApplication.set_prepared_value`. See also
        :meth:`ScriptOnlineApplication.set_unforce_value`.

        :rtype: str

        """
        pass

    def create_online_device(selfself, device=None):
        """Creates an online device.

        To prevent resource leaks, script writers should wrap the usage
		of the online device in a with: block.

		:type device: ScriptObject
		:param device: The application object to use. If
		    this parameter is omitted, the device of the active application is
            used. (This parameter is optional.)

		:rtype: ScriptOnlineDevice
		:returns: The online application object.

        """
        pass

    def set_default_credentials(self, username, password=None):
        """Sets the default credentials for login to devices.

        This setting is in effect until the end of the current script execution.
        Use None for the username and omit the password to delete the default credentials.

        :version added: 3.5.3.0

        :type username: str
        :param username: The username.

        :type password: str
        :param password: The password.

        """
        pass

    def set_specific_credentials(self, target, username, password=None):
        """Sets the default credentials for login to a specific device.

        This setting is in effect until the end of the current script execution.
        Use None for the username and omit the password to delete the default credentials.

        :version added: 3.5.3.0

        :type target: object
        :param target: The target. You can pass a device object, an online device object,
            an application, or an online application. If you pass an application or online application,
            the setting will take effect for all applications in the corresponding device object.

        :type username: str
        :param username: The username.

        :type password: str
        :param password: The password.

        """
        pass

    def clear_all_credentials(self):
        """Clears all credentials which were set by this script.

        This only clears the cretentials at the level of the script. The online manager
        and other components may cache credentials internally, those caches are currently not
        cleared by this method.

        :version added: 3.5.3.0

        """
        pass

    @property
    def auth_fallback_modes(self):
        """Gets or sets the setting how authentication credentials are acquired when no default credentials are set, and no specific credentials match the target.

        This
        setting is in effect until the end of the current script execution.
        By default, this is set to ``CredentialSourceKind.All``.
        You can modify this value to disable interactive login.

        :version added: 3.5.3.0

        :rtype: CredentialSourceKind

        """
        pass

    @auth_fallback_modes.setter
    def auth_fallback_modes(self, value: CredentialSourceKind):
        pass

    @property
    def gateways(self):
        """Gets all currently known gateways.

        :version added: 3.5.8.0

        :rtype: :class:`ScriptGateways`
        :returns: A python tuple containing the gateways.

        """
        pass

    @property
    def gateway_drivers(self):
        """Gets the gateway drivers.

        :version added: 3.5.8.0

        :rtype: :class:`ScriptGatewayDrivers`
        :returns: A python tuple containing all gateway drivers.

        """
        pass

    def register_trusts_certificate(self, device_object, callback, current_node_name=None):
        """ Register a callback which allows to specify if the certificate of a PLC is trusted for the encrypted communication.

        :version added: 3.5.17.0

        :type device_object: :class:`ScriptObject`
        :param device_object: Device object which provides the node name and Object GUID to get the TLS communication validator.

        :type callback: :meth:`TrustsCertificateCallback`
        :param callback: Callback of the type `TrustsCertificateCallback`.

        :type current_node_name: str
        :param current_node_name: Optional, node name of the PLC if the parameter `device_object` can't provide the node name.

        """
        pass

    def unregister_trusts_certificate(self, device_object, current_node_name=None):
        """ Unregister a previously registered callback which allowed to specify if the certificate of a PLC is trusted for the encrypted communication.
        
        Use the same parameters as from the registration process.

        :version added: 3.5.17.0
                
        :type device_object: :class:`ScriptObject`
        :param device_object: Device object which provides the node name and Object GUID to get the TLS communication validator.

        :type current_node_name: str
        :param current_node_name: Optional, node name of the PLC if the parameter `device_object` can't provide the node name.

        """
        pass

    def unregister_all_trusts_certificate(self):
        """ Unregister all previously registered callbacks which allowed to specify if the certificate of a PLC is trusted for the encrypted communication.

        :version added: 3.5.17.0

        """
        pass


class ScriptOnlineApplication(object):
    """Online application object.

    Some of the commands may temporarily change the active application.

    This object keeps an internal connection to the device, so it
    should be disposed when you don't need it any more: Call the Dispose()
    method when you're done with it, or - even better - use the with statement.
    It will be automatically disposed when the script execution ends, but in
    long running scripts, you should dispose it yourself to prevent resource
    leaks, and other side effects of the open connection.

    """

    def login(self, change_option, delete_foreign_apps):
        """Performs the application login.

        If the application was logged in before, it will be logged out and a fresh login will be
        performed.

        :type change_option: :class:`OnlineChangeOption`
        :param change_option: The change option.

        :type delete_foreign_apps: bool
        :param delete_foreign_apps: If set to ``True``, delete foreign applications.

        """
        pass

    def logout(self):
        """Logs this application out. If the application is not logged in, nothing happens."""
        pass

    @property
    def is_logged_in(self):
        """Gets a value indicating whether this :class:`ScriptOnlineApplication` is logged in.

        :rtype: bool
        :returns: ``True`` if is logged in; otherwise, ``False``.

        """
        pass

    def start(self):
        """Starts this application.

        :raises TimeoutException: In case of the operation taking to long.

        """
        pass

    def stop(self):
        """Stops this application.

        :raises TimeoutException: In case of the operation taking to long.

        """
        pass

    @property
    def application_state(self):
        """Gets the application state.

        :rtype: :class:`ApplicationState`

        """
        pass

    @property
    def operation_state(self):
        """Gets the operation status.

        :rtype: :class:`OperatingState`

        """
        pass

    def create_boot_application(self):
        """Creates a boot application for this application on the device.

        If the current application is not online, a file dialog
        asks the user for a path to write the boot file for. You may
        want to use :meth:`.ScriptApplication.create_boot_application`
        instead.

        """
        pass

    def source_download(self):
        """Downloads the source archive to the device."""
        pass

    def write_prepared_values(self):
        """Writes the prepared values.

        :raises ValuesFailedException: If the write of some values fails.

        """
        pass

    def force_prepared_values(self):
        """Forces the prepared values.

        :raises ValuesFailedException: If the force of some values fails.

        """
        pass

    def unforce_all_values(self):
        """Unforces all forced values for the current application.

        :raises ValuesFailedException: If the unforce of some values fails.

        """
        pass

    def get_prepared_value(self, expression):
        """Gets the prepared value for a given expression.

        :type expression: str
        :param expression: The expression

        :rtype: str
        :returns: The prepared value, or ``None`` if nothing is prepared.

        """
        pass

    def read_value(self, expression):
        """Gets the current value for a given expression.

        Monitoring must be enabled.

        :type expression: str
        :param expression: The expression.

        :rtype: str
        :returns: The value.

        """
        pass

    def read_values(self, expressions):
        """Gets the current values for a list of expressions.

        Monitoring must be enabled.

        :type expressions: tuple[str]
        :param expressions: The expressions.

        :rtype: list[str]
        :returns: The values.

        """
        pass

    def get_prepared_expressions(self):
        """Gets all expressions for values currently prepared for this application (including those prepared by other scripts, editors etc).

        :rtype: list[str]
        :returns: The prepared expressions.

        """
        pass

    def get_forced_expressions(self):
        """Gets all expressions for values currently forced for this application (including those prepared by other scripts, editors etc).

        :rtype: list[str]
        :returns: The forced expressions.

        """
        pass

    def set_prepared_value(self, expression, value):
        """Prepares values the specified expression.

        Use None or the empty string to unprepare the value.

        :type expression: str
        :param expression: The expression.

        :type value: str
        :param value: The value.

        """
        pass

    def set_unforce_value(self, expression, restore=False):
        """Prepares the specified forced expression for unforcing.

        :type expression: str
        :param expression: The expression.

        :type restore: bool
        :param restore: If set to ``true``, the value is reset to the value before forcing.

        """
        pass

    @property
    def timeout(self):
        """Gets or sets the timeout for some operations.

        Some operations like start() have to wait for defined application states. If those
        operations take longer than this timeout, a :exc:`TimeoutException` is thrown.
        The default timeout is 60 seconds.

        :rtype: int

        """
        pass

    @timeout.setter
    def timeout(self, value: int):
        pass

    def reset(self, reset_option=ResetOption.Warm, force_kill=False):
        """Resets the online application. This also clears all breakpoints on the application (if any).

        If the application is currently halted on a breakpoint, and
        the device supports to kill a task during the execution cycle
        (:attr:`TargetProperties.TaskKillable`), you can use the
        ``force_kill`` parameter to force the reset
        without running the current cycle to an end. If the device
        does not support :attr:`TargetProperties.TaskKillable`,
        this parameter will be ignored, and the current cycle will always
        be finished.

        :version added: 3.5.0.0

        :type reset_option: ResetOption
        :param reset_option: The reset_option.

        :type force_kill: bool
        :param force_kill: Force the immediate kill of the
            application without finishing of the current cycle.

        """
        pass

    def get_online_device(self):
        """Gets the online device for this application.

        :rtype: :class:`ScriptOnlineDevice`

        """
        pass

    @property
    def application(self):
        """Gets the application object for this online application.

        :rtype: :class:`ScriptObject`

        """
        pass


class ScriptOnlineDevice(object):
    """Functionality for manipulating online device objects.

    All device objects for which the online manager returns a IOnlineDevice7 instance are extended with this methods.

    This object keeps an internal connection to the device, so it
    should be disposed when you don't need it any more: Call the Dispose()
    method when you're done with it, or - even better - use the with statement.
    It will be automatically disposed when the script execution ends, but in
    long running scripts, you should dispose it yourself to prevent resource
    leaks, and other side effects of the open connection.

    :version added: 3.5.0.0

    """

    def reset_origin(self):
        """Reset the device to the origin (shipping) state.

        For example, all plc applications, boot
        applications, and retain and persistent variables are deleted.

        """
        pass

    @property
    def device(self):
        """Gets the underlying device object for this online device.

        :rtype: :class:`ScriptObject`

        """
        pass

    def connect(self):
        """Connects this instance. The connection is a shared connection to the device.

        Please note that other actions like reset_origin may implicitly connect to the device.

        :version added: 3.5.2.0

        """
        pass

    def disconnect(self):
        """Disconnects this instance.

        As the connection is shared, the underlying connection may
        actually stay open, for example when an application is still online.

        :version added: 3.5.2.0

        """
        pass

    @property
    def connected(self):
        """Gets a value indicating whether this :class:`ScriptOnlineDevice` is connected.

        :version added: 3.5.2.0

        :rtype: bool

        """
        pass

    @property
    def shared_connected(self):
        """Gets a value indicating whether this ScriptOnlineDevice or anything else has a shared connection to the device.

        :version added: 3.5.2.0

        :rtype: bool
        :returns: ``True`` if connected; otherwise, ``False``.

        """
        pass

    def forced_disconnect(self):
        """Forcibly disconnects all shared connections to the device (connections via online applications, as well as other connections), and resets the current login and session information.

        :version added: 3.5.2.0

        """
        pass

    def current_logged_on_username(self):
        """Gets the name of the user who is currently logged on in the device.

        If ``None`` or an empty string is returned, nobody is logged on.

        :version added: 3.5.2.0

        :rtype: str

        """
        pass

    def create_user_management(self, load_from_project=True):
        """Creates a new user management instance for this device.

        For the devices with runtime V3.5.16.0 or newer you have to use
        :meth:`create_live_user_management` because they only support
        the live user management.

        :version added: 3.5.2.0

        :type load_from_project: bool
        :param load_from_project: By default, the instance is initialized with the
            information stored in the device object in the current project. By setting this
            parameter to false, you can suppress this loading, e. G. if you want to load the user
            management via the :meth:`ScriptDeviceUserManagement.upload` or
            :meth:`ScriptDeviceUserManagement.load` methods.

        :rtype: :class:`ScriptDeviceUserManagement`
        :returns: The created user management instance.

        :raises WrongDeviceUserManagementException: Thrown if the device only supports the live user management.

        """
        pass

    def download_source(self, bCompact=False, additional_items=None):
        """Downloads the source archive to the device.

        For a definition of the additional items, see :class:`ScriptProjectArchiveCategories`.
        If you don't pass any ``additional_items``, :attr:`ScriptProjectArchiveCategories.default`
        is used. To exclude all additional items, explicitly pass ``None``.

        :version added: 3.5.4.0

        :type bCompact: bool
        :param bCompact: If ``True``, the source archive will only contain the PLC and applications
            of the current device. If ``False``, the source archive will contain all PLCs and all
            applications in the project.

        :type additional_items: tuple[:class:`ScriptProjectArchiveCategory]
        :param additional_items: The additional items to include in the project archive.

        """
        pass

    def upload_source(self, archive_path):
        """Uploads the source from the device, and saves it under the specified output path.

        This method will throw various Exceptions on errors.

        :version added: 3.5.4.0

        :type archive_path: str
        :param archive_path: The local path where to save the project archive. (Usually ending
            with the extension .prj).

        """
        pass

    def download_file(self, local_file, remote_file, force_overwrite):
        """Download a file to the PLC.

        :version added: 3.5.9.0

        :type local_file: str
        :param local_file: Path of the local file.

        :type remote_file: str
        :param remote_file: Path of the remote file.

        :type force_overwrite: bool
        :param force_overwrite: Force the overwrite if the remote file already exists.

        """
        pass

    def upload_file(self, remote_file, local_file, force_overwrite):
        """Upload a file from the PLC.

        :version added: 3.5.9.0

        :type remote_file: str
        :param remote_file: Path of the remote file.

        :type local_file: str
        :param local_file: Path of the local file.

        :type force_overwrite: bool
        :param force_overwrite: Force the overwrite if the local file already exists.

        """
        pass

    def rename_file(self, old_name, new_name):
        """Rename a file on the PLC.

        :version added: 3.5.9.0

        :type old_name: str
        :param old_name: Path of the remote file with the old name.

        :type new_name: str
        :param new_name: Path of the remote file with the new name.

        """
        pass

    def delete_file(self, remote_file):
        """Delete a file on the PLC.

        :version added: 3.5.9.0

        :type remote_file: str
        :param remote_file: Path of the remote file.

        """
        pass

    def create_directory(self, remote_directory):
        """Create a directory on the PLC.

        :version added: 3.5.9.0

        :type remote_directory: str
        :param remote_directory: Path of the new directory.

        """
        pass

    def get_file_list_of_directory(self, remote_directory):
        """Read a directory on the PLC.

        :version added: 3.5.9.0

        :type remote_directory: str
        :param remote_directory: Path of the directory.

        :rtype: tuple[:class:`ScriptDirectoryInfo`]
        :returns: Array of info elements which describe the files and directories
            inside the given remote directory.

        """
        pass

    def rename_directory(self, old_name, new_name):
        """Rename a directory on the PLC.

        :version added: 3.5.9.0

        :type old_name: str
        :param old_name: Path of the remote directory with the old name.

        :type new_name: str
        :param new_name: Path of the remote directory with the new name.

        """
        pass

    def delete_directory(self, remote_directory, recursive):
        """Delete a directory on the PLC.

        :version added: 3.5.9.0

        :type remote_directory: str
        :param remote_directory: Path of the remote directory.

        :type recursive: bool
        :param recursive: If ``True``, delete the directory resursively.

        """
        pass

    def activate_license(self, ticket, url=None, license_names=None):
        """Performs a license activation on a remote device.

        The first container returned be the device will be used for activation.

        :version added: 3.5.10.0

        :type ticket: str
        :param ticket: The ticket which contains the licenses.

        :type url: str
        :param url: The license server. If ``None`` the default license server will be used.

        :type license_names: tuple[str]
        :param license_names: The licenses which should be activated. If ``None`` or if no license
            is specified, every kind of license will be activated by default.

        """
        pass

    def change_user_password(self, user, oldPassword, newPassword):
        """Update the passwort of a given user and reset the flag that the user must change the password on next login.

        :version added: 3.5.14.0

        :type user: str
        :param user: The user that shall be authentified.

        :type oldPassword: str
        :param oldPassword: current password of the given user.

        :type newPassword: str
        :param newPassword: new password for the given user.

        """
        pass

    def create_live_user_management(self):
        """ Create a new live user management which is required by PLC runtime V3.5.16.0 or newer.

        You have to create a connection before calling this method otherwise you get an exception.
        With SP16 or newer version of the PLC runtime you can access the user management only when connected.

        :version added: 3.5.16.0

        :raises WrongDeviceUserManagementException: Thrown if the device does not support the live user management.

        :rtype: :class:`ScriptLiveDeviceUserManagement`

        """
        pass

    def set_credentials_for_initial_user(self, username, password, can_change_password=True, must_change_password=False):
        """ Set the username and password for the initial user of the user management if the device requires it or you want one.

        If the device requires an user management you need to specify an initial user otherwise you will get an exception.
        If it is not required and you don't specify an initial user, no user management is created on the device.

        :version added: 3.5.16.0

        :type username: str
        :param username: Username of the initial user.

        :type password: str
        :param password: Password of the initial user

        :type can_change_password: bool
        :param can_change_password: User can change their password.

        :type must_change_password: bool
        :param must_change_password: User must change their password with next login.

        """
        pass


class ValuesFailedException(Exception):
    """This exception is thrown by :meth:`ScriptOnlineApplication.write_prepared_values` and :meth:`ScriptOnlineApplication.force_prepared_values`."""

    def ValuesFailedException(self, failed_expressions):
        """Initializes a new instance of the :class:`ValuesFailedException` class.

        :type failed_expressions: list[str]
        :param failed_expressions: The failed expressions.

        :rtype: :class:`ValuesFailedException`

        """
        pass

    @property
    def failed_expressions(self):
        """Gets the list of the failedexpressions.

        :rtype: list[str]

        """
        pass


class ScriptGateway(object):
    """Script engine representation of a configured gateway for runtime connections.

    :version added: 3.5.8.0

    """

    @property
    def name(self):
        """Gets the name of the gateway.

        For backwards compatibility reasons, the gateway names are not
        guaranteed to be unique - several gateways with the same name may exist.

        :rtype: str

        """
        pass

    @property
    def guid(self):
        """Gets the unique identifier of the gateway.

        :version added: 3.5.8.0

        :rtype: Guid

        """
        pass

    @property
    def gateway_driver(self):
        """Gets the gateway protcol driver used for this gateway.

        :version added: 3.5.8.0

        :rtype: :class:`ScriptGatewayDriver`

        """
        pass

    @property
    def config_params(self):
        """Gets a python dictionary with a copy of the current configuration of the gateway, using the :attr:`ScriptGatewayParameterDescription.id` as keys and the parameter values as values.

        :version added: 3.5.8.0

        :rtype: object

        """
        pass

    def find_address_by_ip(self, ip_or_name: str, port: int = 11740):
        """Finds an CODESYS address by scanning the network by IP or Hostname.

        Currently, only IPv4 addresses are supported. This method blocks until either the device
        responded or the timeout for network scans is reached. Any exceptions coming form the
        communication layer will be thrown (e.g. if the Gateway is not running).

        :version added: 3.5.8.0

        :type ip_or_name: str
        :param ip_or_name: The IP address.

        :type port: ushort
        :param port: The port.

        :raises TimeoutException: Thrown in case no device replies.
        :raises Exception: Any other exception forwarded from the communication layer.

        :rtype: string
        :returns: The CODESYS address.

        """
        pass

    def find_address_by_ip(self, address: IPAddress, port: int = 11740):
        """Finds an CODESYS address by scanning the network by IP or Hostname.

        Currently, only IPv4 addresses are supported. This method blocks until either the device
        responded or the timeout for network scans is reached. Any exceptions coming form the
        communication layer will be thrown (e.g. if the Gateway is not running).

        :version added: 3.5.8.0

        :type address: IPAddress
        :param address: The IP address.

        :type port: ushort
        :param port: The port.

        :raises TimeoutException: Thrown in case no device replies.
        :raises Exception: Any other exception forwarded from the communication layer.

        :rtype: string
        :returns: The CODESYS address.

        """
        pass

    def perform_network_scan(self):
        """Performs a network scan on this gateway.

        This method will block at least for the duration of the
        network scan timeout period.

        :version added: 3.5.8.0

        :raises Exception: Any exceptions occurring durint the network scan.

        :rtype: tuple[:class:`ScriptScanTargetDescription`]
        :returns: The list of devices which were found.

        """
        pass

    def get_cached_network_scan_result(self):
        """Gets the cached result of the last network scan on this gateway.

        :rtype: tuple[:class:`ScriptScanTargetDescription`]
        :returns: The list of devices which were found.

        """
        pass


class ScriptScanTargetDescription(object):
    """Description of a scan target found during a device scan.

    :version added: 3.5.8.0

    """

    @property
    def device_name(self):
        """Gets the name of the device.

        Example: "PLCFeeder". If no name
        has been explicitly assigned to the device, it is derived from the
        corresponding router address, e.g. "@127.5".

        :rtype: str

        """
        pass

    @property
    def type_name(self):
        """Gets a string indicating the device type.

         Example: "Beckhoff CX1000-100" or "BRC Motion Logic Controller".

        :rtype: str

        """
        pass

    @property
    def vendor_name(self):
        """Gets a string indicating the device vendor.

        Example: "Beckhoff" or "BRC"

        :rtype: str

        """
        pass

    @property
    def device_id(self):
        """Gets the ID of the type to be matched with the installed device types (target descriptions).

        :rtype: :class:`DeviceID`

        """
        pass

    @property
    def address(self):
        """Gets the router address for this device.

        A hierarchical addressing
        scheme is used. Example: "123.5". Each component of the router
        address corresponds to an array element of the return value.

        :rtype: str

        """
        pass

    @property
    def parent_address(self):
        """Get the router address of the parent node of this device.

        Usually this will be the device address without the last address component.
        Is ``None`` if the parentAddress is unknown.

        :rtype: str

        """
        pass

    @property
    def locked_in_cache(self):
        """If set to true, the devicedescription will stay in the gateways device cache, even during rebuild.

        So this is not a property of the device itself but a property
        of the device description object and may be changed by plugins.

        :rtype: bool

        """
        pass

    @property
    def block_driver(self):
        """Property to access the type of block driver used for this target.

        :rtype: :class:`BlockDriverType`

        """
        pass

    @property
    def block_driver_address(self):
        """Property to store and retrieve the driver-specific address for this target.

        :rtype: str

        """
        pass


class ScriptGateways(list):
    """A collection of gateways currently configured in CODESYS.

    :version added: 3.5.8.0

    """

    def __getitem__(self, guid: Guid):
        """Gets the :class:`ScriptGateway` with the specified unique identifier.

        :type guid: Guid
        :param guid: The guid.

        :raises InvalidOperationException: If several gateways have the same name.
        :raises KeyNotFoundException: No gateway with the name or guid exists.
        :raises ArgumentNullException: ``name_or_guid`` is ``None``

        :rtype: :class:`ScriptGateway`
        :returns: The script gateway.

        """
        pass

    def __getitem__(self, name_or_guid: str):
        """Gets the :class:`ScriptGateway` with the specified unique identifier.

        :type name_or_guid: str
        :param name_or_guid: The name or the guid as string.

        :raises InvalidOperationException: If several gateways have the same name.
        :raises KeyNotFoundException: No gateway with the name or guid exists.
        :raises ArgumentNullException: ``name_or_guid`` is ``None``

        :rtype: :class:`ScriptGateway`
        :returns: The script gateway.

        """
        pass

    def find_with_name(self, name):
        """Finds all gateways with the name.

        :type name: str
        :param name: The name.

        :rtype: list[:class:`ScriptGateway`]
        :returns: A (possibly empty) sequence of all gateways with the name.

        """
        pass

    def remove_gateway(self, gateway: ScriptGateway):
        """Removes the specified gateway.

        If the specified one is the default one, the next one (if any) will be the new default.

        :type gateway: :class:`ScriptGateway`
        :param guid: The gateway to remove.

        """
        pass

    def remove_gateway(self, guid: Guid):
        """Removes the specified gateway.

        If the specified one is the default one, the next one (if any) will be the new default.

        :type guid: Guid
        :param gateway: The guid of the gateway to remove.

        """
        pass

    def add_new_gateway(self, name, parameters, driver=None, gateway_guid=None):
        """Creates and adds a new gateway.

        The keys of the ``parameters`` dictionary need to be integers corresponding to the
        :attr:`ScriptGatewayParameterDescription.id`, the
        :class:`ScriptGatewayParameterDescription` itself, or strings corresponding to the
        :attr:`ScriptGatewayParameterDescription.name` of the parameter (if the names are unique).
        The values will be converted using the :meth:`convert_gateway_parameter` method.

        :type name: str
        :param name: The name.

        :type parameters: dict[int or str or ScriptGatewayParameterDescription, object]
        :param parameters: The gateway parameters (as a python dictionary).

        :type driver: :class:`ScriptGatewayDriver`
        :param driver: The driver - if you don't pass a driver,
            the default TCP/IP driver will be used.

        :type gateway_guid: Guid or None
        :param gateway_guid: The gateway guid - if ``None`` is passed, a new one will be generated.

        :rtype: :class:`ScriptGateway`

        """
        pass

    def convert_gateway_parameter(self, parameter, paramType):
        """Converts an object to the specified gateway parameter type.

        :type parameter: object
        :param parameter: The parameter.

        :type paramType: :class:`ParamType`
        :param paramType: Type of the parameter.

        :rtype: obj
        :returns: The object converted to the specified :class:`ParamType`.

        """
        pass


class ScriptGatewayDrivers(list):
    """Represents a list of script gateway drivers.

    :version added: 3.5.8.0

    """

    def __getitem__(self, guid):
        """Gets the :class:`ScriptGatewayDriver` with the specified name or guid.

        :type guid: Guid
        :param guid: The guid.

        :raises InvalidOperationException: If several gateway drivers have the same name.
        :raises KeyNotFoundException: No gateway driver with the name or guid exists.
        :raises ArgumentNullException: ``name_or_guid`` is ``None``

        :rtype: :class:`ScriptGatewayDriver`

        """
        pass

    def __getitem__(self, name_or_guid):
        """Gets the :class:`ScriptGatewayDriver` with the specified name or guid.

        :type name_or_guid: str
        :param name_or_guid: The name or guid (as string).

        :raises InvalidOperationException: If several gateway drivers have the same name.
        :raises KeyNotFoundException: No gateway driver with the name or guid exists.
        :raises ArgumentNullException: ``name_or_guid`` is ``None``

        :rtype: :class:`ScriptGatewayDriver`

        """
        pass

    def find_with_name(self, name):
        """Finds all gateway drivers with the name.

        :type name: str
        :param name: The name.

        :rtype: list of :class:`ScriptGatewayDriver`
        :returns: A (possibly empty) sequence of all gateway drivers with the name.

        """
        pass

    @property
    def default_driver(self):
        """Gets the default gateway driver (currently bound to TCP/IP on standard CODESYS and most derivates).

        :rtype: :class:`ScriptGatewayDriver`

        """
        pass


class ScriptGatewayDriver(object):
    """Script engine representation of a gateway driver.

    :version added: 3.5.8.0

    """

    @property
    def guid(self):
        """A Guid that uniquely identifies the driver type.

        Each implementation for a gateway driver is identified by a Guid.

        :rtype: Guid

        """
        pass

    @property
    def name(self):
        """Get the user-readable name of this gateway driver.

        :rtype: str

        """
        pass

    @property
    def gateway_parameters(self):
        """Gets the gateway parameter descriptions - those are used when a new gateway with this driver is created.

        :rtype: ScriptGatewayParameterDescriptions
        :returns: A collection containing the gateway parameters.

        """
        pass


class ScriptGatewayParameterDescriptions(list):
    """A collection of script gateway parameters.

    :version added: 3.5.8.0

    """

    def __getitem__(self, id):
        """Gets the :class:`ScriptGatewayParameterDescription` with the specified id.

        :type id: int
        :param id: The id.

        :raises InvalidOperationException: If several parameters have the same name.
        :raises KeyNotFoundException: No parameter with this name or id exists.
        :raises ArgumentNullException: ``id_or_name`` is ``None``

        :rtype: :class:`ScriptGatewayParameterDescription`
        :returns: The parameter description with the given id.

        """
        pass

    def __getitem__(self, name):
        """Gets the :class:`ScriptGatewayParameterDescription` with the specified id.

        :type name: str
        :param name: The name.

        :raises InvalidOperationException: If several parameters have the same name.
        :raises KeyNotFoundException: No parameter with this name or id exists.
        :raises ArgumentNullException: ``id_or_name`` is ``None``

        :rtype: :class:`ScriptGatewayParameterDescription`
        :returns: The parameter description with the given id.

        """
        pass


class ScriptGatewayParameterDescription(object):
    """Description of parameters for a gateway driver - those are used when a new gateway with this driver is created.

    :version added: 3.5.8.0

    """

    @property
    def id(self):
        """The id of the parameter.

        The id is unique for any particular gateway driver.

        :rtype: long

        """
        pass

    @property
    def name(self):
        """Human readable string, giving the name of the parameter.

        :rtype: str

        """
        pass

    @property
    def description(self):
        """Human readable string describing the parameter.

        :rtype: str

        """
        pass

    @property
    def parameter_type(self):
        """The type of the parameter value.

        The types here have finer granularity than the types
         available in python. However, users don't need to cast to the
         corresponding .NET types, this will be done by the script engine
         as long as the generic type kind is matching - e. G. a python
         integer is ok for all integer param types, or a single-character
         python string is ok for ``ParamType.Char``.

        :rtype: :class:`ParamType`

        """
        pass

    @property
    def default_value(self):
        """Default value of the parameter. May be ``None``.

        :rtype: object

        """
        pass

    def validate(self, value):
        """Check whether the provided object is a valid value for this parameter.

        You can use the :meth:`ScriptGateways.convert_gateway_parameter` method
        to convert the parameter to the corresponding type.

        :type value: object
        :param value: The value to check.

        :raises Exception: If the object is not valid.

        """
        pass


class ScriptDirectoryInfo(object):
    """Describes contents of a remote directory on the PLC.

    :version added: 3.5.9.0

    """

    @property
    def name(self):
        """Gets the name of the file/directory.

        :rtype: str

        """
        pass

    @property
    def creation_time(self):
        """Get the creation time of the file/directory.

        :rtype: DateTime

        """
        pass

    @property
    def last_access_time(self):
        """Get the last access time of the file/directory.

        :rtype: DateTime

        """
        pass

    @property
    def last_modification_time(self):
        """Get the last modification time of the file/directory.

        :rtype: DateTime

        """
        pass

    @property
    def is_directory(self):
        """Whether it is a directory.

        :rtype: bool

        """
        pass

    @property
    def is_file(self):
        """Whether it is a file.

        :rtype: bool

        """
        pass

    @property
    def size(self):
        """Get the file size in bytes.

        :rtype: int

        """
        pass

    @property
    def additional_dir_info(self):
        """Get the additional information of the file/directory.

        :rtype: :class:`AdditionalDirInfo`

        """
        pass


def TrustsCertificateCallback(certificate, chain, node_name):
    """This callback allows to specify if the certificate of a PLC should be trusted for the encrypted communcation.

    :version added: 3.5.17.0

    :type certificate: X509Certificate2
    :param certificate: Certificate of the PLC.

    :type chain: X509Chain
    :param chain: Chain of trust.

    :type node_name: str
    :param node_name: Name of the PLC.

    :rtype: bool
    :returns: `True`, if you trust the certificate.
    """
    pass
