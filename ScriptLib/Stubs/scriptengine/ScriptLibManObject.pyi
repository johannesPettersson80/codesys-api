from .dotNETs import *
from .ScriptObject import *


class LibManager(object):
    """An instance implementing this interface is injected into the scriptengine scope under the name library manager."""

    @property
    def repositories(self):
        """Gets the list of available library repositories.

        The order of those repositories is configurable by the user in the dialog and the script.

        This list is a snapshot of the current state. When repositories are created,
        removed or moved, those changes are not reflected "live" in the list, and you need to
        get a fresh copy.

        :rtype: tuple[:class:`LibRepository`]
        :returns: The list of available repositories.

        """
        pass

    def insert_repository(self, rootfolder, name, index=-1):
        """Creates a new library repository.

        :type rootfolder: str
        :param rootfolder: The rootfolder for the repository (this must be the full path to an
            existing directory on disk).

        :type name: str
        :param name: The name of the repository.

        :type index: int
        :param index: The index of the repository in the list. -1 means the repository is added to
            the end of the list.

        :rtype: :class:`LibRepository`
        :returns: The newly created repository.

        """
        pass

    def move_repository(self, repository, new_index):
        """Move_repositories the specified repository to a new position in the list.

        Use this to manipulate the search order.

        :type repository: :class:`LibRepository`
        :param repository: The repository.

        :type new_index: int
        :param new_index: The new index. You can pass -1 to move it to the end of the list.

        """
        pass

    def remove_repository(self, repository, delete_on_disk=False):
        """Removes the specified repository.

        :type repository: :class:`LibRepository`
        :param repository: The repository.

        :type delete_on_disk: bool
        :param delete_on_disk: If set to ``True``, the on-disk directory is also deleted.

        """
        pass

    def update_repository(self, repository, new_name=None, new_location=None, copy_libraries=False):
        """Update the specified repository.

        :type repository: :class:`LibRepository`
        :param repository: The repository.

        :type new_name: str
        :param new_name: The new name.

        :type new_location: str
        :param new_location: The new location.

        :type copy_libraries: bool
        :param copy_libraries: if set to ``True``, the libraries from the old location are
            installed at the new location, if they don't exist.

        """
        pass

    def get_file_path(self, library):
        """Gets the file path of the specified library in the library repository.

        :type library: :class:`ManagedLib`
        :param library: The library.

        :rtype: str
        :returns: The file path of the library.

        """
        pass

    @property
    def categories(self):
        """Gets all the known library categories.

        :rtype: tuple[:class:`LibCategory`]
        :returns: All the known library categories.

        """
        pass

    @property
    def top_level_categories(self):
        """Gets the all known top level library categories.

        :rtype: tuple[:class:`LibCategory`]
        :returns: All known top level library categories.

        """
        pass

    def get_category(self, guid):
        """Gets the category with the specified GUID.

        :type guid: Guid
        :param guid: The GUID.

        :rtype: :class:`LibCategory`
        :returns: The library category.

        """
        pass

    def install_library(self, filepath, repository=None, overwrite=False):
        """Installs the library with the specified filepath.

        :type filepath: str
        :param filepath: The filepath of the library to install.

        :type repository: :class:`LibRepository`
        :param repository: The repository. This parameter is optional, if omitted, the first
            repository in the list is used.

        :type overwrite: bool
        :param overwrite: if set to ``True``, existing libraries are replaced.

        :rtype: :class:`ManagedLib`
        :returns: The installed library.

        """
        pass

    def uninstall_library(self, repository, library):
        """Uninstalls a library from the specified repository.

        :type repository: :class:`LibRepository`
        :param repository: The repository.

        :type library: :class:`ManagedLib`
        :param library: The library.

        """
        pass

    def get_library(self, name, repository):
        """Gets all libraries with the specified name.

        :type name: str
        :param name: The name.

        :type repository: :class:`LibRepository`
        :param repository: The repository. If you pass None, all repositories are searched in order.

        :rtype: :class:`ManagedLib`
        :returns: The found library.

        """
        pass

    def get_all_libraries(self, repository: LibRepository):
        """This override is used when parameter is of type *LibRepository*.

        Gets all libraries.

        :type repository: :class:`LibRepository`
        :param repository: The repository.

        :rtype: tuple[:class:`ManagedLib`]

        """
        pass

    def get_all_libraries(self, exclude_shadowed_libs: bool = True):
        """This override is used when parameter is of type *bool*.

        Gets all libraries.

        :type exclude_shadowed_libs: bool
        :param exclude_shadowed_libs: If set to ``True``, shadowed libs are excluded.

        :rtype: tuple[:class:`ManagedLib`]

        """
        pass

    def find_library(self, display_name):
        """Finds the library with the specified display_name.

        :type display_name: str
        :param display_name: The display name to search for.

        :rtype: tuple [:class:`ManagedLib`, :class:`LibRepository`]
        :returns: A python tuple containing the ManagedLib and the LibRepository,
            or None if nothing found.

        """
        pass


class LibRepository(object):
    """Description class for a library repository."""

    @property
    def editable(self):
        """Gets a value indicating whether this LibRepository is editable.

        The default system library repository is not editable - that means, it cannot be removed
        from the list of repositories.

        :rtype: bool
        :returns: ``True`` if editable, otherwise ``False``.

        """
        pass

    @property
    def name(self):
        """Gets the name of the repository.

        :rtype: str

        """
        pass

    @property
    def root_folder(self):
        """Gets the root folder of the repository.

        :rtype: str

        """
        pass


class ManagedLib(object):
    """Description class for a managed library."""

    @property
    def displayname(self):
        """Display name.

        :rtype: str
        """
        pass

    @property
    def company(self):
        """Company.

        :rtype: str
        """
        pass

    @property
    def title(self):
        """Title.

        :rtype: str
        """
        pass

    @property
    def version(self):
        """Version.

        :rtype: Version
        """
        pass

    @property
    def default_namespace(self):
        """Default namespace.

        :rtype: str
        """
        pass

    @property
    def dependencies(self):
        """Gets the dependencies as a list of strings.

        :rtype: tuple[str]

        """
        pass

    @property
    def categories(self):
        """Gets the categories.

        Gets the list of :class:`LibCategory`.

        :rtype: tuple[:class:`LibCategory`]

        """
        pass


class LibCategory(object):
    """Information about a library category."""

    @property
    def guid(self):
        """Gets the guid identifying the category.

        :rtype: Guid

        """
        pass

    @property
    def parent(self):
        """Gets the parent category, or None if the category is top level.

        :rtype: :class:`LibCategory`

        """
        pass

    @property
    def default_name(self):
        """Gets the default name.

        :rtype: str

        """
        pass

    @property
    def name(self):
        """Gets the localized name, or the default name if no localized name is available.

        :rtype: str

        """
        pass

    @property
    def localized_name(self):
        """Gets the localized name for the current UI culture.

        :rtype: str

        """
        pass

    @property
    def version(self):
        """Version.

        :rtype: Version

        """
        pass


class ScriptLibManObjectMarker(object):
    """Every ScriptObject instance will be extended with this method.

    :version added: 3.4.3.0

    """

    @property
    def is_libman(self):
        """Gets a value indicating whether this instance is a lib man object.

        :rtype: bool
        :returns: ``True`` if this instance is lib man object, otherwise ``False``.

        """
        pass


class ScriptLibManObject(ScriptLibManObjectMarker):
    """Functionality for manipulating library managers.

    All objects implementing LibManObject will be extended with this methods.

    """

    def get_libraries(self, recursive=False):
        """Returns a list of all libraries.

        :type recursive: bool
        :param recursive: If set to ``True``, sublibraries are also queried recursively.

        :rtype: list [str]
        :returns: The list of library names.

        """
        pass

    def add_library(self, name: str):
        """Adds the library with the specified name.

        :type name: str
        :param name: The name of the library.

        """
        pass

    def add_library(self, library: ManagedLib):
        """Adds a reference to the specified library.

        :type library: :class:`ManagedLib`
        :param library: The library (since V3.5.5.0).

        """
        pass

    def add_placeholder(self, name: str, default_resolution: str):
        """Adds a placeholder for a library with the specified name.

        :type name: str
        :param name: The name.

        :type default_resolution: str
        :param default_resolution: The default resolution.

        """
        pass

    def add_placeholder(self, name: str, default_resolution: ManagedLib):
        """Adds a placeholder with the specified default resolution.

        :type name: str
        :param name: The name.

        :type default_resolution: :class:`ManagedLib`
        :param default_resolution: The default resolution (since V3.5.5.0).

        """
        pass

    def remove_library(self, name):
        """Removes the librariy with the specified name.

        :type name: str
        :param name: The name.

        """
        pass

    @property
    def references(self):
        """Gets the collection of the references currently configured within this library manager.

        :version added: 3.5.5.0

        :rtype: :class:`ScriptLibraryReferences`

        """
        pass


class ScriptLibraryReferences(list):
    """The references currently managed by the library manager."""

    def __len__(self):
        """Gets the current number of items in this library manager.

        :rtype: int
        :returns: The number of items.

        """
        pass

    def __getitem__(self, name: str):
        """Gets the :class:`ScriptLibraryReference` with the specified name.

        :type name_or_id: str

        :rtype: :class:`ScriptLibraryReference`

        """
        pass

    def __getitem__(self, id: int):
        """Gets the :class:`ScriptLibraryReference` with the specified id.

        :type id: int

        :rtype: :class:`ScriptLibraryReference`

        """
        pass


class ScriptLibraryReference(object):
    """A library reference in the library manager."""

    @property
    def id(self):
        """Id.

        :rtype: int

        """
        pass

    @property
    def is_placeholder(self):
        """Gets a value indicating whether this ScriptLibraryReference is a placeholder.

        :rtype: bool
        :returns: ``True`` if it is a placeholder, otherwise ``False``.

        """
        pass

    @property
    def is_managed(self):
        """Gets a value indicating whether this ScriptLibraryReference is a managed reference to a fixed library version.

        :rtype: bool
        """
        pass

    @property
    def name(self):
        """Gets the name of this library.

        For managed items, this follows the pattern "Name, Version (Company)".
        For placeholder items, this name follows the pattern "#Name".
        See also: :attr:`ScriptPlaceholderReference.placeholder_name`.

        :rtype: str

        """
        pass

    @property
    def namespace(self):
        """Gets or sets the namespace for this library.

        :rtype: str

        """
        pass

    @namespace.setter
    def namespace(self, value: str):
        pass

    @property
    def system_library(self):
        """Gets a boolean value indicating whether this library is a system library or not.

        System libraries have been added implicitly by plug-ins whereas non-system libraries have been
        explicitly added by the user.

        :rtype: bool

        """
        pass

    def get_dependencies(self):
        """Gets the dependencies of this library.

        For libraries containing cyclic dependencies, this may lead to an endless recursion.

        :rtype: list[:class:`ScriptLibraryReference`]
        :returns: A list of dependencies.

        """
        pass

    @property
    def parameters(self):
        """Gets the library parameter set.

        If a global variable list containing only constant values has the attribute
        'parameterlist', its content may be modified in the referencing project using this
        mechanism.

        :rtype: :class:`ScriptLibraryParameters`

        """
        pass

    @property
    def hide_when_referenced_as_dependency(self):
        """Gets or sets a value indicating whether this library node should be hidden in the user interface if it a direct or indirect dependency of a top-level library node.

        :rtype: bool

        """
        pass

    @hide_when_referenced_as_dependency.setter
    def hide_when_referenced_as_dependency(self, value: bool):
        pass

    @property
    def publish_symbols_in_container(self):
        """Gets or sets the qualified-only flag.

        If set, the name of the library is mandatory for any access to the library content.

        The default is true.

        :rtype: bool

        """
        pass

    @publish_symbols_in_container.setter
    def publish_symbols_in_container(self, value: bool):
        pass

    @property
    def qualified_only(self):
        """Gets or sets the qualified-only flag.

        If set, the name of the library is mandatory for any access to the library content.

        Defaults to ``True``.

        :rtype: bool

        """
        pass

    @qualified_only.setter
    def qualified_only(self, value: bool):
        pass

    @property
    def optional(self):
        """Gets or sets the optional flag.

        Libraries which are optional are not reported to the user as missing if they do not exist.

        :rtype: bool

        """
        pass

    @optional.setter
    def optional(self, value: bool):
        pass


class ScriptManagedLibraryReference(ScriptLibraryReference):
    """A managed library reference which points to a fixed version of the library.

    :attr:`ScriptLibraryReference.is_managed` is true for those instances.

    """

    @property
    def managed_library(self):
        """Gets the managed library.

        :rtype: :class:`ManagedLib`

        """
        pass


class ScriptPlaceholderReference(ScriptLibraryReference):
    """A placeholder reference. :class`ScriptLibraryReference` instances with :attr:`ScriptLibraryReference.is_placeholder` == True implement this interface."""

    @property
    def placeholder_name(self):
        """Gets the name of the placeholder.

        In contrast to :attr:`ScriptLibraryReference.name`,
        this name does not include the leading '#' character.

        :rtype: str

        """
        pass

    @property
    def default_resolution(self):
        """Gets or sets the default resolution of the library.

        :rtype: str

        """
        pass

    @default_resolution.setter
    def default_resolution(self, value: str):

        pass

    @property
    def effective_resolution(self):
        """Effective resolution.

        :rtype: str
        """
        pass

    @property
    def is_redirected(self):
        """Gets a value indicating whether this ScriptPlaceholderReference is redirected.

        :rtype: bool

        """
        pass

    def get_redirection(self):
        """Gets the redirection setting for this library.

        :rtype: str
        :returns: The redirection.

        """
        pass

    def set_redirection(self, fixed_resolution = ""):
        """Sets the redirection for this library.

        :type fixed_resolution: str
        :param fixed_resolution: The fixed resolution. Use ``None`` or an empty string to delete
            the redirection.

        """
        pass

    @property
    def resolution_info(self):
        """Gets a human readable information how this placeholder is resolved.

        :rtype: str

        """
        pass

    @property
    def resolver_guid(self):
        """Gets a machinable readable information how this placeholder is resolved.

        :rtype: Guid

        """
        pass


class ScriptLibraryParameters(list):
    """The library parameters interface. This is a sequence of the parameter names.

    If a global variable list containing only constant values has the attribute 'parameterlist',
    its content may be modified in the referencing project using this mechanism.

    """

    def __len__(self):
        """Gets the length (number of parameters).

        :rtype: int

        """
        pass

    def __getitem__(self, name):
        """Gets the parameter with the specified name.

        :type name: str

        :rtype: str

        """
        pass

    def __setitem__(self, name, expression: str):
        """Sets the parameter with the specified name to an valid IEC expression.

        :type name: str

        :rtype: str

        """
        pass


class ScriptLibManObjectContainer(object):
    """Projects and Application Objects are extended with this interface.

    :version added: 3.5.2.0

    """

    @property
    def has_library_manager(self):
        """Gets a value indicating whether this ScriptLibManObjectContainer has a library manager.

        :rtype: bool
        :returns: ``True`` if there is a library manager, otherwise ``False``.

        """
        pass

    def get_library_manager(self):
        """Gets the library manager for this application or project, implicitly creating one if none is existing yet.

        :rtype: :class:`ScriptObject`
        :returns: The library manager object. (ScriptObject)

        """
        pass
