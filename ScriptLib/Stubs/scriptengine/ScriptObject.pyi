from .dotNETs import *
from .ScriptLibManObject import *
from .ScriptTreeObject import *
from .ScriptProject import *


class ScriptObject(ScriptTreeObject):
    """Modelling of a script object.

    They compare equal if Guid and ProjectHandle (inherited from ScriptTreeObject) are equal.

    """

    @property
    def type(self):
        """Gets the type guid.

        :rtype: Guid

        """
        pass

    @property
    def guid(self):
        """Gets the GUID of the object.

        :rtype: Guid

        """
        pass

    @property
    def embedded_object_types(self):
        """Gets the embedded onject types.

        :rtype: list[Guid]

        """
        pass

    def get_name(self, resolve_localized_display_name=False):
        """Gets the name of the object.

        :type resolve_localized_display_name: bool
        :param resolve_localized_display_name: if set to ``True``, the name is localized.
        :rtype: str
        :returns: The name of the object

        """
        pass

    def rename(self, stNewName):
        """Renames the object to the new name.

        :type stNewName: str
        :param stNewName: New name of the object.

        """
        pass

    @property
    def index(self):
        """Gets the index.

        :rtype: int

        """
        pass

    @property
    def is_folder(self):
        """Gets a value indicating whether this instance is a folder.

        :rtype: bool

        """
        pass

    @property
    def parent(self):
        """Gets the parent ScriptObject, or the Project if we are top-level.

        You can use the is_root property implemented by objects and
        projects to distinct between the two.

        :rtype: object

        """
        pass

    def remove(self):
        """Removes this instance."""
        pass

    def move(self, new_parent: ScriptObject, new_index: int = -1):
        """Moves the object to the specified new parent.

        :type new_parent: :class:`ScriptObject`
        :param new_parent: The new parent.
        :type new_index: int
        :param new_index: New index in the new parent.

        """
        pass

    def move(self, new_parent: ScriptProject, new_index: int = -1):
        """Moves the object to the specified new parent.

        :type new_parent: :class:`ScriptProject`
        :param new_parent: The new parent.
        :type new_index: int
        :param new_index: New index in the new parent.

        """
        pass

    def export_xml(self,
                   reporter=None,
                   path=None,
                   recursive=False,
                   export_folder_structure=False,
                   declarations_as_plaintext=False
                   ):
        """Exports the ScriptObject in PLCopenXML format into a string, or a file at the given path.

        This method internally eliminates duplicates,
        and all non-exportable objects are reported as error.
        Following 3.5.4.0, ``reporter`` can be omitted. The method will then
        report all exportable objects, report everything on progress,
        and throw exceptions on critical errors.

        .. note:: Due to the sheer amount of overrides
            from different versions this function has to offer,
            it is best practice to give even positional arguments with their respective keywords.

        :type reporter: ExportReporter
        :param reporter: The IExportReporter instance.

        :type recursive: bool
        :param recursive: if set to ``true``, all exportable children of the
            objects are also exported.

        :type path: str
        :param path: The path of the file we export into. If omitted, we export into
            a string and return that string.

        :type export_folder_structure: bool
        :param export_folder_structure: Version added: 3.4.4.0
            if set to ``true``, the folder structure of the objects is also exported.
            This is a proprietary extension to the default schema.

        :type declarations_as_plaintext: bool
        :param declarations_as_plaintext: Version added: 3.5.3.0
            if set to ``True``, the declaration parts will be additionally
            exported as plain text (which is lossless in contrast to the default schema). This is
            a proprietary extension to the default schema. (Import will automatically recognize and
            prefer the plain text format if present.)

        :rtype: str
        :returns: The exported XML as string, or None if a filepath is given.

        """
        pass

    def import_xml(self, dataOrPath, conflictResolve=None, import_folder_structure=False,
                   reporter=None):
        """Imports the contents of the specified PLCopenXML file als children of the current object.

        The heuristics to find
        out whether the content is a file or directly an XML string
        currently is as follows: if it contains the '&lt;' character,
        it is regarded as an XML file. Rationale: On windows, &lt; is
        an invalid char in path names, and it is contained in every
        XML. This heuristics may be replaced by a more sophisticated
        heuristics in the future.
        Following 3.5.4.0, ``reporter`` can be omitted.

        .. note:: Due to the sheer amount of overrides
            from different versions this method has to offer,
            it is best practice to give even positional arguments with their respective keywords.

        :type dataOrPath: str
        :param dataOrPath: The PLCopenXML file path, or the PLCOpenXML as string.
        :type conflictResolve: ConflictResolve
        :param conflictResolve: The conflict resolution strategy.
        :type import_folder_structure: bool
        :param import_folder_structure: Version added: 3.4.4.0
            if set to ``true``, the folder structure of the objects is also imported.
            This is a proprietary extension to the default schema.
        :type reporter: ImportReporter
        :param reporter: The import reporter.

        """
        pass

    def export_native(self, destination, recursive=True, profile_name=None, reporter=None):
        """Export the specified objects in the CoDeSys native export format.

        :version added: 3.4.4.0
        :type destination: str
        :param destination: The destination file.
        :type recursive: bool
        :param recursive: if set to ``true``, the chilren are included recursively.
        :type profile_name: str
        :param profile_name: The profile_name, or None for the default profile.
        :type reporter: NativeExportReporter
        :param reporter: The reporter. You can pass None for no reporting at all.

        """
        pass

    def import_native(self, filenames, filter=None, handler=None):
        """Imports the specified files in the native xml format in under the current node.

        :version added: 3.4.4.0
        :type filenames: str or list
        :param filenames: The filename or a list of filenames.
        :type filter: :func:`.NativeImportFilter`
        :param filter: The filter - if None is passed, all files are imported.
        :type handler: NativeImportHandler
        :param handler: The handler - if None passed, the default handler is used.

        """
        pass

    def create_folder(self, foldername):
        """Creates a folder with the specified foldername in the structured view of the parent node.

        The Modules View currently does not support folders, so creating folders
        below module objects is not supported.

        :version added: 3.5.3.0
        :type foldername: str
        :param foldername: The foldername.

        """
        pass

    def get_signature_crc(self, application=None, default_value=None):
        """Gets the signature CRC of the specified pou.

        A successful build is needed for this method to work.

        For POUs which are defined below an application, compile the
        application via :meth:`.ScriptApplication.build`.
        You can omit "application",
        and the parent application will be found automatically.
        For POUs which are in the pool of a library projuect, compile the application via
        :meth:`.ScriptProject.check_all_pool_objects`.
        The pool application guid (:const:`Guid.Empty`) will
        be used automatically in this case, so you can omit "application".
        For pous which are defined in the pool of a project,
        but referenced from within an application,
        compile the application via :meth:`.ScriptApplication.build` and explicitly pass that
        application (or its guid) as "application" parameter.

        :version added: 3.5.4.0
        :type application: object
        :param application: The application which the POU is referenced,
            if necessary (see remarks).
            This parameter accepts the application object or its guid.
        :type default_value: str
        :param default_value: If you pass a value here, this is returned
            instead of throwing an exception when no CRC is found.
        :rtype: string
        :returns: The string representation of the CRC, or the default value when no CRC was found.
        :raises InvalidOperationException: No compile context found for the object -
            maybe the application was not compiled?
        :raises NotSupportedException: No compiled signature found for the object -
            maybe the object is no POU.
        :raises KeyNotFoundException: No CRC attribute found for the object.
        :raises ArgumentException: You passed an invalid object for the application.

        """
        pass

    @property
    def build_properties(self):
        """Gets the build properties of the object, or None.

        Not all objects have editable build properties - this method returns
        None when the object does not have any build properties.

        :version added: 3.5.7.0
        :rtype: ScriptBuildProperties

        """
        pass

    @property
    def effectively_excluded_from_build(self):
        """Gets a boolean indicating whether this object is effectively excluded from the build.

        An object is effectively excluded if either the object itsself or any
        of its parents has the :meth:`ScriptBuildProperties.exclude_from_build` flag set.

        :version added: 3.5.7.0
        :rtype: bool

        """
        pass

    @property
    def exclusion_from_build_is_inherited(self):
        """Gets a boolean indicating whether the build exclusion is inherited from a parent object.

        :version added: 3.5.7.0
        :rtype: bool

        """
        pass


class ScriptBuildProperties(object):
    """Defining the build properties of objects contributing to the compiler.

    Note that some objects do not define all
    of those properties. For example, folders only allow the :meth:`exclude_from_build`
    property to be set (which is inherited to POUs below that folder), and devices
    may opt in or out of some properties based on the kind of device. Accessing
    an invalid property will throw an :exc:`InvalidOperationException`.

    """

    @property
    def external(self):
        """Gets or sets the External-flag.

        A POU with this flag is supposed to be linked in runtime system.

        Check the :meth:`external_is_valid` property whether
        this property is currently valid for this object.

        :rtype: bool

        """
        pass

    @external.setter
    def external(self, value: bool):
        pass

    @property
    def external_is_valid(self):
        """Gets wether the :meth:`external` property is valid for this object or not.

        :rtype: bool

        """
        pass

    @property
    def enable_system_call(self):
        """Gets or sets the Enable system call-flag.

        A POU with this flag can be called by C-Code out of the runtime system

        Check the :meth:`enable_system_call_is_valid` property
        whether this property is currently valid for this object.

        :rtype: bool

        """
        pass

    @enable_system_call.setter
    def enable_system_call(self, value: bool):
        pass

    @property
    def enable_system_call_is_valid(self):
        """Gets whether the :meth:`enable_system_call` property is is valid for this object or not.

        :rtype: bool

        """
        pass

    @property
    def compiler_defines(self):
        """Gets or sets compilerdefines for the object.

        The defines may be a list of comma seperated defines like this:
        DEF1, DEF2='value'
        For simple objects the scope of these defines is the object itself
        for applications, the scope of these defines is the whole application.
        Check the :meth:`compiler_defines_is_valid` property
        whether this property is currently valid for this object.

        :rtype: str

        """
        pass

    @compiler_defines.setter
    def compiler_defines(self, value: str):
        pass

    @property
    def compiler_defines_is_valid(self):
        """Gets whether the :meth:`compiler_defines` property is valid for this object or not.

        :rtype: bool

        """
        pass

    @property
    def link_always(self):
        """Gets or sets the flag for linking an object in any case.

        If ``true`` is assigned, the object will be linked into the
        application even when it is not referenced in another way.

        Check the :meth:`link_always_is_valid` property
        whether this property is currently valid for this object.

        :rtype: bool

        """
        pass

    @link_always.setter
    def link_always(self, value: bool):
        pass

    @property
    def link_always_is_valid(self):
        """Gets whether the :meth:`link_always` property is valid for this object or not.

        :rtype: bool

        """
        pass

    @property
    def exclude_from_build(self):
        """Gets or sets the flag Exclude from build.

        Objects which are excluded from the build will be ignored by the compiler.

        In other words, the language model of an object with this
        flag will be removed from language model manager. Note that a false value might be
        overwritten by a true value stored for the parent object. Use
        :meth:`ScriptObject.effectively_excluded_from_build` to query
        the effective value for this object.
        Check the :meth:`exclude_from_build_is_valid` property
        whether this property is currently valid for this object.

        :rtype: bool

        """
        pass

    @exclude_from_build.setter
    def exclude_from_build(self, value: bool):
        pass

    @property
    def exclude_from_build_is_valid(self):
        """Gets whether the :meth:`exclude_from_build` property is valid for this object or not.

        :rtype: bool

        """
        pass


class ScriptProjectInfoMarker(object):
    """The all objects are extended with this interface, since CoDeSys V3.5 SP2.

    :version added: 3.5.2.0

    """

    @property
    def is_project_info(self):
        """Gets a value indicating whether this :obj:`ScriptProjectInfoMarker` is the project info object.

        :rtype: bool

        """
        pass


class ScriptProjectInfoObject(ScriptProjectInfoMarker):
    """The project information objects are extended with this interface, since CoDeSys V3.5 SP2.

    :version added: 3.5.2.0

    """

    @property
    def generate_accessors(self):
        """Gets a value indicating whether this :obj:`ScriptProjectInfoObject` generates property accessor POU objects or not.

        :returns: ``true` if accessor functions are generated; otherwise, ``false``.
        :rtype: bool

        """
        pass

    def change_accessor_generation(self, generate_accessors):
        """Changes the generate_accessor flag.

        As changing this flag is potentially expensive (genrating several POUs), it is
        an explicit function and no property setter.

        :type generate_accessors: bool
        :param generate_accessors: if set to ``True``, the accessors are generated.

        """
        pass

    @property
    def company(self):
        """Gets or sets the company.

        Libraries are uniquely identified by the
        tuple <:meth:`company`, :meth:`title`, :meth:`version`>

        :rtype: str

        """
        pass

    @company.setter
    def company(self, value: str):
        pass

    @property
    def title(self):
        """Gets or sets the title.

        Libraries are uniquely identified by the
        tuple <:meth:`company`, :meth:`title`, :meth:`version`>.

        :rtype: str

        """
        pass

    @title.setter
    def title(self, value: str):
        pass

    @property
    def version(self):
        """Gets or sets the version.

        remarks

        :rtype: Version or str or tuple[int] or Sequence[int]
        :returns: The version. This returns a System.Version instance.
            For setting, it accepts System.Version instances as well as strings which are parseable
            as version, and tuples / sequences with 2-4 integers.

        """
        pass

    @version.setter
    def version(self, value: object):
        pass

    @property
    def released(self):
        """Gets or sets a value indicating whether the project containing this :obj:`ScriptProjectInfoObject` is released.

        Released library projects should not be modified any more.
        Unset the released flag and change the version if you want to modify a released library.

        :rtype: bool

        """
        pass

    @released.setter
    def released(self, value: bool):
        pass

    @property
    def categories(self):
        """If the project is used as a library, it appears under the following categories.

        :rtype: list[LibCategory]

        """
        pass

    @property
    def default_namespace(self):
        """Gets or sets the default namespace when the project is used as a library.

        :rtype: str

        """
        pass

    @property
    def author(self):
        """Gets or sets the author.

        :rtype: str

        """
        pass

    @author.setter
    def author(self, value: str):
        pass

    @property
    def description(self):
        """Gets or sets the description.

        This string may be multiline.

        :rtype: str

        """
        pass

    @description.setter
    def description(self, value: str):
        pass

    @property
    def dongle_licencing_active(self):
        """Gets or sets a value indicating whether this library has dongle license protection.

        If dongle licensing is activated, the user needs to connect a dongle containing
        the appropriate license in order to use this library. For the licensing to work correctly,
        both firm_code and product_code MUST be specified. Please note that only compiled
        libraries will be protected!

        :rtype: bool
        :returns: ``true`` if license protection is active; otherwise, ``false``
        :raises InvalidOperationException: When setting to True, but
            :meth:`dongle_licensing_firm_code` or
            :meth:`dongle_licensing_product_code` are not set.

        """
        pass

    @dongle_licencing_active.setter
    def dongle_licencing_active(self, value: bool):
        pass

    @property
    def dongle_licensing_firm_code(self):
        """Gets or sets the dongle licensing firm code.

        If dongle licensing is activated, the user needs to connect a dongle containing
        the appropriate license in order to use this library. For the licensing to work correctly,
        both firm_code and product_code MUST be specified. Please note that only compiled
        libraries will be protected!

        :rtype: int or None
        :raises InvalidOperationException: When trying to unset this value
            while :meth:`dongle_licencing_active` is set.
        :raises ArgumentOutOfRangeException: When trying to set this to a negative value.

        """
        pass

    @dongle_licensing_firm_code.setter
    def dongle_licensing_firm_code(self, value: int):
        pass

    @property
    def dongle_licensing_product_code(self):
        """Gets or sets the dongle licensing product code.

        If dongle licensing is activated, the user needs to connect a dongle containing
        the appropriate license in order to use this library. For the licensing to work correctly,
        both firm_code and product_code MUST be specified. Please note that only compiled
        libraries will be protected!

        :rtype: int or None
        :raises InvalidOperationException: When trying to unset this value
            while :meth:`dongle_licencing_active` is set.
        :raises ArgumentOutOfRangeException: When trying to set this to a negative value.

        """
        pass

    @dongle_licensing_product_code.setter
    def dongle_licensing_product_code(self, value: int):
        pass

    @property
    def dongle_licensing_activation_url(self):
        """Gets or sets the dongle licensing activation email address.

        :rtype: str

        """
        pass

    @dongle_licensing_activation_url.setter
    def dongle_licensing_activation_url(self, value: str):
        pass

    @property
    def dongle_licensing_activation_mail(self):
        """Gets or sets the dongle licensing activation email address.

        :rtype: str

        """
        pass

    @dongle_licensing_activation_mail.setter
    def dongle_licensing_activation_mail(self, value: str):
        pass

    @property
    def values(self):
        """Gets the custom property dictionary.

        The following types are allowed:

        =============  ============================================================================================
        Type           Description
        =============  ============================================================================================
        :class:`str`   Textual properties.
        DateTime       Date / time properties.
        :class:`int`   Numerical properties.
        :class:`bool`  Boolean properties.
        Version        Version properties, they may also be passed as :class:`str` or tuple / sequence of integers.
        =============  ============================================================================================

        You're responsible yourself to set the correct type. Any inconsistencies or problems
        introduced by fiddling with this dictionary are your own responsibility.

        Some properties are defined in the online help: See the section "Libraries -> Guidelines
        for creating Libraries -> Library Development Summary -> CODESYS LibDevSummary V3.5.4.0 ->
        Concepts and Elements -> Library Properties":

        ========  ======================  =======  ==============================================================================
        --        Name                    Type     Description
        ========  ======================  =======  ==============================================================================
        Required  Company                 Text     Serves for structuring (filter) in the “Add Library” dialog
        Required  Title                   Text     Name of the library
        Required  Version                 Version  Library verison
        Optional  Released                Bool     A library should not be modified after having been released
        Optional  Author                  Text     Author of the current library version
        Optional  DefaultNamespace        Text     World-wide unique prefix, for defining the scope of the symbols of the library
        Optional  Description             Text     Short description of the purpose of the library
        Optional  Placeholder             Text     which Placeholder should be used for referencing the library
        Optional  IsContainerLibrary      Bool     This library follwos the rules for a Container Library
        Optional  IsInterfaceLibrary      Bool     This library follows the rules for a Interface Library
        Optional  LanguageModelAttribute  Text     The access on symbols of the library is only possible via Namespace/Prefix
        Optional  IsEndUserLibrary        Bool     This Library is especially designed for the needs of end users
        ========  ======================  =======  ==============================================================================

        :rtype: Dictionary(str, object)

        """
        pass
