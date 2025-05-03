from enum import Enum
from .ScriptProject import *


class PromptOverwriteResult(Enum):
    """Enum that enumerates the possible results for the overwrite handling."""

    Yes = 0
    """The user selected "Yes", which means that the file or item should be overwritten."""
    No = 1
    """The user selected "No", which means that the file or item should not be overwritten."""
    Cancel = 2
    """The user selected "Cancel", which means that the project archive extraction should be terminated."""


class VersionUpdateFlags(Enum):
    """
    Flags for the _3S.CoDeSys.VersionCompatibilityManager.IVersionCompatibilityManager2.SetVersionUpdateFlags(_3S.CoDeSys.VersionCompatibilityManager.VersionUpdateFlags)
    method.
    """

    Regular = 0,
    """
        The _3S.CoDeSys.VersionCompatibilityManager.IVersionCompatibilityManager checks
        for updates when opening a project and displays a related dialog for the user
        to manually update the versions.
    """

    NoUpdates = 1,
    """
        The _3S.CoDeSys.VersionCompatibilityManager.IVersionCompatibilityManager will
        not check for updates when the next project will be opened. Therefore, there
        will be no dialog.
    """

    SilentMode = 2,
    """
        Determines if a dialog for user interaction is shown or not. If this flag is
        set, there will be no dialog.
    
        Remarks:
        This flag is often combined with one of the Update… flags.
    """

    UpdateAllCustomProviders = 4,
    """
        The _3S.CoDeSys.VersionCompatibilityManager.IVersionCompatibilityManager will
        automatically update all items to the newest available version when the next
        project will be opened. To avoid a dialog, combine this flag with the _3S.CoDeSys.VersionCompatibilityManager.VersionUpdateFlags.SilentMode
        flag.
    """

    UpdateLibraries = 8,
    """
        The _3S.CoDeSys.VersionCompatibilityManager.IVersionCompatibilityManager will
        automatically update all libraries to the newest available version when the next
        project will be opened. To avoid a dialog, combine this flag with the _3S.CoDeSys.VersionCompatibilityManager.VersionUpdateFlags.SilentMode
        flag.
    """

    UpdateCompiler = 16,
    """
        The _3S.CoDeSys.VersionCompatibilityManager.IVersionCompatibilityManager will
        automatically update the compiler version to the newest available version when
        the next project will be opened. To avoid a dialog, combine this flag with the
        _3S.CoDeSys.VersionCompatibilityManager.VersionUpdateFlags.SilentMode flag.
    """

    UpdateVisualisation = 32,
    """
        The _3S.CoDeSys.VersionCompatibilityManager.IVersionCompatibilityManager will
        automatically update the visualisation profile to the newest available version
        when the next project will be opened. To avoid a dialog, combine this flag with
        the _3S.CoDeSys.VersionCompatibilityManager.VersionUpdateFlags.SilentMode flag.
    """

    UpdateDevices = 64,
    """
        The _3S.CoDeSys.VersionCompatibilityManager.IVersionCompatibilityManager will
        automatically update the device profile to the newest available version when
        the next project will be opened. To avoid a dialog, combine this flag with the
        _3S.CoDeSys.VersionCompatibilityManager.VersionUpdateFlags.SilentMode flag.
    """

    UpdateVisualisationStyles = 128,
    """
        The _3S.CoDeSys.VersionCompatibilityManager.IVersionCompatibilityManager will
        automatically update the used visualization styles to the newest available versions
        when the next project will be opened. To avoid a dialog, combine this flag with
        the _3S.CoDeSys.VersionCompatibilityManager.VersionUpdateFlags.SilentMode flag.
    """

    UpdateUnresolvedUnboundPlaceholders = 256,
    """
        The _3S.CoDeSys.VersionCompatibilityManager.IVersionCompatibilityManager will
        automatically redirect the unresolved unbound placeholders to the newest available
        versions when the next project will be opened. To avoid a dialog, combine this
        flag with the _3S.CoDeSys.VersionCompatibilityManager.VersionUpdateFlags.SilentMode
        flag.
    """

    UpdateAll = 65532
    """
        The _3S.CoDeSys.VersionCompatibilityManager.IVersionCompatibilityManager will
        automatically update all items to the newest available version when the next
        project will be opened. To avoid a dialog, combine this flag with the _3S.CoDeSys.VersionCompatibilityManager.VersionUpdateFlags.SilentMode
        flag.
    
        Remarks:
        Please note that this enum value sets all bits in the range of 2 to 15 to "1".
    """


class ScriptProjects(object):
    """The ScriptDriverProjects uses this interface to provide project handling functionality for the python scripts."""

    def create(self, path, primary=True):
        """Creates a new project.

        :version added:
        :type path: str
        :param path: The location where the project content is to be stored.

        :type primary: bool or None
        :param primary: if set to ``True`` the project will be the new primary
            project. See :attr:`ScriptProject.primary` for more information.

        :rtype: :class:`ScriptProject`
        :returns: The created ScriptProject instance.

        """
        pass

    def open(self, path, password=None, primary=True, encryption_password=None, session_user=None,
             session_password=None, update_flags=VersionUpdateFlags.NoUpdates,
             allow_readonly=False):
        r"""Opens the specified project.

        .. warning::
            If a password is given, SystemInstances.ObjectManager must
            implement IObjectManager9, or a InvalidOperationException will
            be thrown (even if the project is not actually password
            protected).

        If the password is omitted, ``None`` or empty string,
        opening a password protected archive will prompt the user for a
        password.

        For the ``update_flags`` parameter, the :attr:`VersionUpdateFlags.SilentMode`
        is usually combined with one or more of the ``Update...`` flags defined in the
        :class:`VersionUpdateFlags` enum. If you only pass some ``Update...`` flags without the
        :attr:`VersionUpdateFlags.SilentMode` flag, they will be used as initial values when the
        update dialog pops up. To silently update everything, you can pass the combination
        :attr:`VersionUpdateFlags.SilentMode`\ \|\ :attr:`VersionUpdateFlags.UpdateAll`\ .

        :type path: str
        :param path: The path of the project file to open.

        :type password: str
        :param password: The password for the project encryption.

        :type primary: bool
        :param primary: if set to ``True``, open as primary
            project. See :attr:`ScriptProject.primary` for more information.

        :type encryption_password: str
        :param encryption_password: Version added: 3.5.5.0
            The project encryption password.

        :type session_user: str
        :param session_user: Version added: 3.5.5.0
            The project session user (project usermanagement).

        :type session_password: str
        :param session_password: Version added: 3.5.5.0
            The project session password (project usermanagement).

        :type update_flags: :class:`VersionUpdateFlags`
        :param update_flags: Version added: 3.5.8.0
            The flags telling whether some aspects (libraries, compiler version) ought to be
            updated when the project is loaded. The default is to silently update nothing.

        :type session_password: bool
        :param session_password: Version added: 3.5.8.0
            If set to ``True``, allow the project to be opened as read-only.

        :rtype: :class:`ScriptProject`
        :returns: The opened project.

        """
        pass

    def open_archive(self, archivefile, projectpath, overwrite=False, password=None,
                     encryption_password=None, session_user=None, session_password=None,
                     update_flags="VersionUpdateFlags.NoUpdates",
                     prompt_absolute_path=None):
        r"""Opens a project archive.

        The parameter ``projectpath`` will be evaluated using the following algorithm:

            1.  If it's the path of an existing file, and ``overwrite`` is true,
                it will be overwritten.
            #.  If it's the path to an existing file, and ``overwrite`` is false,
                an :exc:`IOException` will be thrown.
            #.  If this points to an existing directory, the project will be extracted with its
                original name into that directory.
            #.  If the path does not exist, but ends with a "/" or "\", the directory (and all
                non-existing parent directories) will be created, then the project will be extracted
                with its original name into that directory.
            #.  If the path does not exist, but the parent directory exists, the given path (directory
                and file name) will be used.
            #.  Otherwise, if the path ends with ".project" or ".library", the project will be
                extracted using the given path, creating all necessary parent directories.

            #.  In all other cases, a :exc:`DirectoryNotFoundException` will be thrown.

        This method will return ``None`` when the archive extraction was cancelled due
        to an error, overwriting of files or cancel request for absolute path handling.
        If a password is given, SystemInstances.ObjectManager must implement IObjectManager9,
        or a MissingMethodException will be thrown (even if the project
        is not actually password protected). If the password is
        omitted, ``None`` or empty string, opening a password protected
        archive will prompt the user for a password.

        For the ``update_flags`` parameter, the :attr:`VersionUpdateFlags.SilentMode`
        is usually combined with one or more of the ``Update...`` flags defined in the
        :class:`VersionUpdateFlags` enum. If you only pass some ``Update...`` flags without the
        :attr:`VersionUpdateFlags.SilentMode` flag, they will be used as initial values when the
        update dialog pops up. To silently update everything, you can pass the combination
        :attr:`VersionUpdateFlags.SilentMode`\ \|\ :attr:`VersionUpdateFlags.UpdateAll`\ .

        :type archivefile: str
        :param archivefile: The path of the project archive.

        :type projectpath: str
        :param projectpath: The path for the extracted project.

        :type overwrite: bool
        :param overwrite: if set to ``true``, overwrite existing objects and project files

        :type password: str
        :param password: The password.

        :type encryption_password: str
        :param encryption_password: Version added: 3.5.5.0
            The project encryption password.

        :type session_user: str
        :param session_user: Version added: 3.5.5.0
            The project session user (project usermanagement).

        :type session_password: str
        :param session_password: Version added: 3.5.5.0
            The project session password (project usermanagement).

        :type update_flags: :class:`VersionUpdateFlags`
        :param update_flags: Version added: 3.5.8.0
            The flags telling whether some aspects (libraries, compiler version) ought to be
            updated when the project is loaded. The default is to silently update nothing.

        :type prompt_absolute_path: `PromptAbsolutePath`
        :param prompt_absolute_path: Version added: 3.5.16.0
            The callback which allows to decide if an project archive item with an absolute
            path should be extracted relatively to the project file or not at all.
            Or if the operation should be canceled. The default is to cancel the operation.

        :rtype: :class:`ScriptProject`
        :returns: The opened project or null if it was canceled.

        """
        pass

    def get_by_path(self, path):
        """Gets a Project by the absolute path where the project is physically stored.

        :type path: str
        :param path: The path to the project.

        :rtype: :class:`ScriptProject`
        :returns: The project instance

        """
        pass

    @property
    def primary(self):
        """Gets the primary project, or None if no primary project currently exists.

        The primary project is the one the user usually works with.
        See :attr:`ScriptProject.primary` for more information.

        :version added:

        :rtype: :class:`ScriptProject`

        """
        pass

    @property
    def all(self):
        """Gets a (possibly empty) List of all currently opened projects.

        :rtype: list[ScriptProject]

        """
        pass

    def convert(self, path, output_path=None, converter=None, primary=True):
        """Converts the specified project.

        Currently, password and device conversion prompts cannot be caught by the script.

            .. list-table:: Some converter guids are:
                :widths: auto
                :header-rows: 1

                * - Guid
                  - Description
                * - {E3BC006A-5E3E-4f8f-AEE7-27FD1E0F2A3F}
                  - CoDeSys for Automation Alliance project files (bevore V3.0, \*.pro)
                * - {941937BF-9A12-4174-814E-63D1523C94CC}
                  - CoDeSys for Automation Alliance library files (before V3.0, \*.lib)

        :version added: 3.5.0.0

        :type path: str
        :param path: The path of the project to convert.

        :type output_path: str
        :param output_path: The output path. This parameter is optional, if it is omitted,
            the output path will be auto-generated from the project path by changing the file
            extension.

        :type converter: str
        :param converter: The GUID of the CoDeSys converter factory as string object. This
            parameter is optional, if omitted, the script engine will try to guess using the
            extension of the file name.

        :type primary: bool
        :param primary: If set to ``True``, open as primary project.
            See :attr:`ScriptProject.primary` for more information.

        :rtype: :class:`ScriptProject`
        :returns: The converted project.

        """
        pass


class ScriptProjectArchiveCategories(list):
    """The list of available archive categories.

    Enumerating this object will give
    all categories available in the current installation. Some often used categories
    are defined here, but may be unavailable (throw exceptions) in customized environments.
    An instance of this object is injected into the scriptengine module
    with the name "ArchiveCategories".

    """

    def __getitem__(self, guid_or_name):
        """Gets the class:`ScriptProjectArchiveCategory` with the specified GUID or name.

        :type guid_or_name: Guid or str

        :rtype: ScriptProjectArchiveCategory

        """
        pass

    @property
    def default(self):
        """The default selection of archive categories.

        See also: :attr:`ScriptProjectArchiveCategory.selected_by_default`

        :rtype: list[ScriptProjectArchiveCategory]

        """
        pass

    @property
    def none(self):
        """No categories (empty set).

        This is a special sentinel value, different from passing an arbitrary empty list.

        :rtype: list[ScriptProjectArchiveCategory]

        """
        pass

    @property
    def all(self):
        """A collection of all categories (returns self)."""
        pass

    @property
    def compileinfo(self):
        """Gets the category for the compileinfo.

        This is needed for logins and online changes into an existing application without download.

        :rtype: ScriptProjectArchiveCategory

        """
        pass

    @property
    def libraries(self):
        """Gets the category for the libraries referenced by the project.

        :rtype: ScriptProjectArchiveCategory

        """
        pass

    @property
    def devices(self):
        """Gets the category for the device descriptions of the devices used in the project.

        :rtype: ScriptProjectArchiveCategory

        """
        pass

    @property
    def options(self):
        """Gets the category for the project, user, and machine specific preferences.

        :rtype: ScriptProjectArchiveCategory

        """
        pass

    @property
    def ftd(self):
        """Gets the category for the FDT Bulk Data.

        :rtype: ScriptProjectArchiveCategory

        """
        pass

    @property
    def images(self):
        """Gets the category for the imagepool images of the project.

        :rtype: ScriptProjectArchiveCategory

        """
        pass

    @property
    def bootproject(self):
        """Gets the category for the files containing offline boot applications, that were generated for the current project.

        :rtype: ScriptProjectArchiveCategory

        """
        pass

    @property
    def libraryprofile(self):
        """Gets the category for the library profile that is currently in use with this project.

        :rtype: ScriptProjectArchiveCategory

        """
        pass

    @property
    def visualstyles(self):
        """Gets the category for the visualization styles which are currently referenced by this project.

        :rtype: ScriptProjectArchiveCategory

        """
        pass

    @property
    def visualprofile(self):
        """Gets the category for the active visualization profile.

        :rtype: ScriptProjectArchiveCategory

        """
        pass

    @property
    def visuextensions(self):
        """Gets the category for the active visualization extensions.

        :rtype: ScriptProjectArchiveCategory

        """
        pass


class ScriptProjectArchiveCategory(object):
    """Represents a category of items which can be included into a project archive."""

    @property
    def guid(self):
        """Gets the :class:`Guid` for this category.

        :rtype: Guid

        """
        pass

    @property
    def name(self):
        """Gets a display name for this project category, e.g. "Referenced libraries".

        This string should be localized.

        :rtype: str

        """
        pass

    @property
    def description(self):
        """Gets a description for this project category.

        This string should be localized.

        :rtype: str

        """
        pass

    @property
    def selected_by_default(self):
        """Gets a boolean value indicating whether this category should be selected for project archive inclusion per default.

        This is a hint for the presentation layer.

        :rtype: bool

        """
        pass


def PromptAbsolutePath(self, path):
    """[Delegate]. This method can be used to decide if a project archive item with absolute path
    should be extracted relatively to the project file or not at all. Or if the whole operation should be canceled.

    :type path: str
    :param path: Path to the location where the item wants to be extracted to

    :rtype: :class:`PromptOverwriteResult`
    :returns:
        ``Yes`` if the item should be extracted relatively to the project file.
        ``No`` if the item should not be extracted at all.
        ``Cancel`` if the operation should be canceled.
    """
    pass
