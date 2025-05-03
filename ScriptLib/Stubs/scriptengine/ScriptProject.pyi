from enum import Enum
from .ScriptObject import *
from .ScriptProjects import *
from .ScriptTreeObject import *
from .ScriptUserManagement import *


class ComparisonFlags(Enum):
    """Flags controlling the details of the :meth:`ScriptProject.compare_to` method.

    :version added: 3.5.12.0

    """

    NONE = 0
    """No flags set."""

    IGNORE_WHITESPACE = 1
    """Controls whether whitespace changes are ignored
    (some object comparers ignore this parameter).

    """
    IGNORE_COMMENTS = 2
    """Controls whether comment changes are ignored
    (some object comparers ignore this parameter).

    """
    IGNORE_PROPERTIES = 4
    """Controls whether property changes are ignored
    (some object comparers ignore this propertyparameter).

    """
    SPLIT_RENAMES = 8
    """Controls whether renames are split into a add and remove operation.
    If set to ``True``, renamed objects are recorded as addition and deletion.
    If set to ``False``, renamed objects are marked with
    :attr:`ScriptProject.ObjectDifferences.RENAMED`.

    """
    COMPARE_TRANSIENTS = 16
    """Controls whether transient objects are ignored. Transient objects (like task call objects
    sitting below a :class:`.ScriptTaskObject` or SVN_VERSION_INFO objects) are not saved with the
    project, they're based on data stored elsewhere and will be recreated on the fly, thus they're
    not compared by default.

    """
    COMPARE_HIDDEN = 32
    """Controls whether hidden objects are ignored. As they're not visible to the user, and usually
    represented by some other visible objects, they're not compared by default.

    """


class ObjectDifferences(Enum):
    """Representing the object differences.

    :version added: 3.5.12.0

    """

    EQUAL = 0x00
    """The objects are equal."""
    ADDED = 0x01
    """The object was added."""
    DELETED = 0x02
    """The object has been deleted."""
    CONTENT_CHANGED = 0x04
    """The contents of the object are different."""
    FOLDER_CHANGED = 0x08
    """The parent folder of the object is different."""
    ACCESS_RIGHTS_CHANGED = 0x10
    """The acces rights of the object are different."""
    PROPERTIES_CHANGED = 0x20
    """The mets properties of the object are different."""
    RENAMED = 0x40
    """The name of the object was changed."""
    ANY_CHANGES = 0xFFFFFF
    """This covers any changes we can detect now and in the future. (=\ ``0xFFFFFF``\ )"""


class NativeImportResult(Enum):
    """Enum that enumerates the possible results of a native XML import."""

    no_changes = 1
    """The import did not change anything at all."""
    ok = 2
    """The import was successful"""
    skipped = 3
    """The import skipped some entries"""
    errors = 4
    """Errors happened during the import"""


class NativeImportResolve(Enum):
    """How to resolve a conflict."""

    replace = 1
    """Replace the object."""
    skip = 2
    """Skip the object"""
    cancel = 3
    """Cancel the import"""


class Formatting(Enum):
    """DocExport.Formatting"""
    none = 1,
    Indented = 2
    pass


class ConflictResolve(Enum):
    """Possible resolvements in the case that importing a specific PLCopenXML object
        leads to conflicts with an already existing object.
    """

    Replace = 0,
    """The existing object is replaced by the imported object."""

    Copy = 1,
    """The existing object remains with its original name, and the imported object is
        renamed so that is does not conflict any more.
    """

    Skip = 2
    """The object to be imported is skipped."""
    pass


class ScriptProject(ScriptTreeObject):
    """Provides project specific functionality to scripts."""

    def close(self):
        """Closes this project.

        The corresponding Object Manager project
        will also be closed. If this project has got unsaved changes,
        these changes will be discarded.

        """
        pass

    def save(self):
        """Saves this project at its physical location (see path).

        The encryption settings are not changed.

        """
        pass

    def save_as(self, path, password=None):
        """Saves the project under a new filename and with different encryption.

        If no password is given (None is passed), encryption
        stays as it is. If the password given, but an empty string,
        encryption is disabled. Otherwise, the password is used as new
        password to encrypt the project.

        .. note::
            If you want to change password without changing the path, use
            "proj.save_as(proj.path, "myPassword")".

        :type path: str
        :param path: The new path to save the project.
        :type password: str or None
        :param password: The password.

        """
        pass

    def save_archive(self, path, comment=None, additional_files=None, *additional_categories):
        """Saves the project as an archive.

        All additional categories
        which are selected by default are included, but no extra files.

        .. note:: For a definition of the additional items, see ``ScriptProjectArchiveCategories``.
            If you don't pass any ``additional_categories``,
            ``ScriptProjectArchiveCategories.@default`` is used.
            To exclude all additional items, explicitly pass None.

        :type path: str
        :param path: The path to save the archive.
        :type comment: str
        :param comment: The comment to set for the archive.
        :type additional_files: list
        :param additional_files: The additional (external) files to include into the archive.
        :type additional_categories: ScriptProjectArchiveCategory
        :param additional_categories: Version added: 3.5.4.0
            The additional_categories.

        """
        pass

    @property
    def dirty(self):
        """Gets a boolean value indicating whether this project has been changed since the last call to save().

        :rtype: bool
        :returns: ``True`` if this instance is dirty; otherwise, ``False``.

        """
        pass

    @property
    def primary(self):
        """Gets a boolean value indicating whether the primary attribute has been set for this project.

        The primary project is the one the user is currently working with.

        The other, non-primary projects (aka background projects) can serve several
        purposes, for example:

        * Libraries referenced by the primary project.
        * Projects opened for comparison by the "Compare Project" command.
        * Temporary projects created for various purposes, e. G. by the V2.3 import converter,
        * or the CODESYS SVN add-on.

        Those projects are not directly user visible, and you should not modify or close them
        from within your scripts.

        :rtype: bool
        :returns: ``True`` if this instance is primary; otherwise, ``False``.

        """
        pass

    @property
    def library(self):
        """Gets a boolean value indicating whether the project is a background library project.

        Those projects represent a library which was loaded because it is referenced by the
        primary project (directly or indirectly). It will automatically be closed when the
        primary project is closed.

        If you want to check whether the primary project is a library or not, check
        whether the :meth:`path` ends with ".library" or ".project".

        :rtype: bool
        :returns: ``True`` is this instance is a library; otherwise, ``False``

        """
        pass

    @property
    def path(self):
        """Gets the absolute path where this project is physically stored.

        To change that path, use save_as().

        :rtype: str

        """
        pass

    @property
    def active_application(self):
        """Gets or sets the active application.

        This is a property. You can read or assign a :class:`ScriptObject`
        for the application you want to be the active application.

        :rtype: :class:`ScriptObject`

        """
        pass

    @active_application.setter
    def active_application(self, value):
        pass

    def document(self, objects):
        """Prints the specified database objects, including chapter headings and chapter numbering, a title page and table of contents.

        The current printer settings as specified by the user are used. Currently, printing only works when the UI is present, not in --noUI mode.

        :type objects: tuple[ScriptObject]
        :param objects: The objects.
        :raises InvalidOperationException: Is thrown when running in --noUI mode.

        """
        pass

    def export_xml(self, objects, reporter=None, path=None, recursive=False,
                   export_folder_structure=False, declarations_as_plaintext=False):
        """Exports the given objects in PLCopenXML format into a string, or a file at the given path.

        All non-exportable objects are reported as error, but the export may still continue.

        :type objects: tuple[ScriptObject]
        :param objects: The objects to export.

        :type reporter: ExportReporter
        :param reporter: The ExportReporter instance. None can be passed for no reporting.

        :type path: str or None
        :param path: The path of the file we export into. If omitted, we export into
            a string and return that string.

        :type recursive: bool or None
        :param recursive: If set to ``True``, all exportable children of the objects
            are also exported.

        :type export_folder_structure: bool
        :param export_folder_structure: Version added: 3.4.4.0
            if set to ``True``, the folder structure of the objects
            is also exported. This is a proprietary extension to the default schema.

        :type declarations_as_plaintext: bool
        :param declarations_as_plaintext: Version added: 3.5.2.0
            if set to ``true``, the declaration parts will be additionally
            exported as plain text (which is lossless in contrast to the default schema). This is
            a proprietary extension to the default schema. (Import will automatically recognize and
            prefer the plain text format if present.)

        :rtype: str
        :returns: The exported XML as string, or None if a filepath is given.

        """
        pass

    def import_xml(self, dataOrPath, reporter=None, import_folder_structure=False):
        """Imports the contents of the specified PLCopenXML file into the top level of the project.

        The heuristics to find out
        whether the content is a file or directly an XML string
        currently is as follows: if it contains the '&lt;' character,
        it is regarded as an XML file. Rationale: On windows, &lt; is
        an invalid char in path names, and it is contained in every XML
        file. (On other common platforms like unix and OSX, &lt; is
        uncommon and discouraged in file names.) This heuristics may be
        replaced by a more sophisticated heuristics in the
        future.

        :type reporter: ImportReporter
        :param reporter: The import reporter.
        :type dataOrPath: str
        :param dataOrPath: The PLCopenXML file path, or the PLCopenXML as string.
        :type import_folder_structure: bool or None
        :param import_folder_structure: Version added: 3.4.4.0
            if set to ``true``, the folder structure of the objects is also imported.
            This is a proprietary extension to the default schema.

        """
        pass

    def export_native(self, objects, destination, recursive=False, one_file_per_subtree=False,
                      profile_name=None, reporter=None):
        """Export the specified objects in the CoDeSys native export format.

        The parameter ``destination`` must point to a directory
        if ``one_file_per_subtree`` is set to ``True``, and to a file
        in the other case.

        :version added: 3.4.4.0
        :type objects: list
        :param objects: The objects to export.
        :type destination: str
        :param destination: The destination.
        :type recursive: bool
        :param recursive: if set to ``true``, the chilren are included recursively.
        :type one_file_per_subtree: bool
        :param one_file_per_subtree: if set to ``true``, one file per subtree is generated.
        :type profile_name: str
        :param profile_name: The profile_name, or None for the default profile.
        :type reporter: NativeExportReporter
        :param reporter: The reporter. You can pass None for no reporting at all.

        """
        pass

    def import_native(self, filename=None, filenames=None, filter=None, handler=None):
        """Imports the specified files in the native xml format in the top level of this project.

        .. warning:: If ``None`` is passed for both ``filename`` and ``filenames``, this method
            will fail.

        :version added: 3.4.4.0
        :type filename: str
        :param filename: The Filename.
        :type filenames: list
        :param filenames: The Filenames.
        :type filter: :func:`NativeImportFilter`
        :param filter: The filter - if None is passed, all files are imported.
        :type handler: NativeImportHandler
        :param handler: The handler - if None passed, the default handler is used.
        :rtype: NativeImportResult

        """
        pass

    def login(self, username, password):
        """Log into the project using the specified credentials.

        :version added: 3.4.1.10
        :type username: str
        :param username: The username.
        :type password: str
        :param password: The password.

        """
        pass

    def logout(self):
        """Log out from the project (back to the user "nobody").

        :version added: 3.4.1.10

        """
        pass

    @property
    def user_management(self):
        """Returns the user management object for this project.

        :version added: 3.5.1.0
        :raises Exception: If no user management is available.

        :rtype: :class:`ScriptUserManagement`

        """
        pass

    @property
    def has_project_info(self):
        """Gets a value indicating whether this :class:`ScriptProject` already has a project information object.

        :version added: 3.5.2.0
        :rtype: bool
        :returns: ``true`` if it has a project info; otherwise, ``false``.

        """
        pass

    def get_project_info(self):
        """Gets the project information object, implicitly creating one if not existing yet.

        :version added: 3.5.2.0
        :rtype: ScriptObject
        :returns: The project information object.

        """
        pass

    def check_all_pool_objects(self):
        """Checks all pool objects. This command only works reliable for libraries, and when called on primary projects.

        You can use the :meth:`System.get_messages` and :meth:`System.get_message_objects`
        calls to check whether any messages were added.

        :version added: 3.5.2.0

        """
        pass

    def generate_runtime_system_files(self, destination_directory, generate_m4=True, generate_c=False):
        """Generates the specified destination_directory.

        At least one of ``generate_m4`` and ``generate_c`` must be set.

        :version added: 3.5.2.0

        :type destination_directory: str
        :param destination_directory: The destination_directory. Relative pathes are
            interpreted relative to the project location. If you pass None or the empty string,
            the project directory is used.

        :type generate_m4: bool
        :param generate_m4: if set to ``true``, M4 code is generated.

        :type generate_c: bool
        :param generate_c: if set to ``true``, C Code is generated.

        """
        pass

    def clean_all(self):
        """Performs a "Clean All".

        :version added: 3.5.2.0

        """
        pass

    def save_as_compiled_library(self, destination_name=None):
        """Save the current project as a compiled library.

        This command currently only works for the primary project.

        The ``destination_name`` has the following semantics: If it is
        omitted or the empty string, the full project path will be used, with the extension
        changed to ".compiled_library". If the name of an existing directory is given, the
        library will be saved there, using the project base name and the extension changed to
        ".compiled_library". Otherwise, the destination name will be interpreted as the path
        relative to where the current project re.

        :version added: 3.5.2.0

        :type destination_name: str or None
        :param destination_name: The destination name.

        """
        pass

    def create_folder(self, foldername, structured_view=None):
        """Creates a folder with the specified folder name.

        There are three predefined structured views, and the guids are provided as
        constants:

        * SV_DEV  The device view, ``SV_DEV = Guid("{D9B2B2CC-EA99-4c3b-AA42-1E5C49E65B84}")``
        * SV_POU  The POU view, ``SV_POU = Guid("{21AF5390-2942-461a-BF89-951AAF6999F1}")``

        The Modules View currently does not support folders, so no GUID is provided.

        :version added: 3.5.2.0

        :type foldername: str
        :param foldername: The foldername.

        :type structured_view: Guid
        :param structured_view: The structured view. This parameter is optional, if you
            pass Guid.Empty or omit the parameter, the "POU" view is used.

        """
        pass

    def export_doc(self, path=None, ext_path=None, formatting=Formatting.Indented):
        """Exports the documentation for primary project in JSON format into a string, or a file at the given path.

        :version added: 3.5.5.0

        :type path: str or None
        :param path: The path of the file we export into. If omitted, we export into
            a string and return that string.

        :type ext_path: str or None
        :param ext_path: The path where external documentation files should be exported.
            If ommited, the same path as in ``path`` is used.
            If both ommited, the external documentation media is ignored.

        :type formatting: Formatting
        :param formatting: Formatting of the export file.

        :rtype: str
        :returns: The exported JSON as string, or None if a filepath is given.

        """
        pass

    def compare_to(self, right_project, flags=0):   # '0' for ComparisonFlags.None
        """Compares two script projects.

        :version added: 3.5.12.0
        :type right_project: ScriptProject
        :param right_project: The project (base) you want to compare the current project against.
        :type flags: :class:`ComparisonFlags`
        :param flags: Flags controlling the detailed behaviour of the comparison.
        :rtype: ScriptComparisonResult
        :returns: The comparison result.

        """
        pass

    @property
    def project_settings(self):
        """Returns the management object for :class:`ScriptProjectSettings`.

        :version added: 3.5.12.10

        :rtype: :class:`ScriptProjectSettings`

        """
        pass

    def enable_integrity_check(self):
        """Enables the integrity checked project format.

        :version added: 3.5.13.0
        """
        pass

    def disable_encryption(self):
        """Disables password, CodeMeter(TM) dongle and X509 certificate-based encryption or integrity check for the specified project.

        :version added: 3.5.13.0
        """
        pass

    def is_integrity_check_enabled(self):
        """Returns whether the integrity checked project format is is_integrity_check_enabled.

        :version added: 3.5.13.0

        :rtype: bool
        """
        pass


class ScriptProjectSettings(object):
    """Interface for project settings.

    :version added: 3.5.12.10

    """

    @property
    def available_download_content(self):
        """Gets a list of all available ScriptProjectArchiveCategories that can be used for :meth:`ScriptProjectSettings.set_sourcedownload`.

        :rtype: list[:class:`ScriptProjectArchiveCategory`]

        """
        pass

    def set_sourcedownload(self, timing, content, compact, device):
        """Sets the source download settings to the project.

        :type timing: int
        :param timing:
            .. csv-table:: The timing behaviour.
                :header: "Value", "Behaviour"
                :widths: 15, 100

                1, "Implicity at download and online change."
                2, "Prompt at program download and online change."
                3, "Implicity at creating boot project."
                4, "Only on demand."
                5, "Implicitly at creating boot project, program download and onlinechange."

        :type content: list[:class:`ScriptProjectArchiveCategory`]
        :param content: An enumerable of :class:`ScriptProjectArchiveCategory` that should be part
            of the source download.

        :type compact: bool
        :param compact: Indicates to use a compact download or not.

        :type device: :class:`ScriptObject`
        :param device: The destination device or ``None`` for all devices in project.

        """
        pass


class ScriptComparedObject(object):
    """Representing the difference of an object."""

    @property
    def left_object(self):
        """The object from the :attr:`ScriptComparison.left_project`, or ``None`` for deleted objects.

        :rtype: ScriptObject

        """
        pass

    @property
    def right_object(self):
        """The object from the :attr:`ScriptComparisonResult.right_project`, or ``None`` for added objects.

        :rtype: ScriptObject

        """
        pass

    @property
    def ObjectDifferences(self):
        """The exact object differences.

        :rtype: :class:`ObjectDifferences`

        """
        pass


class ScriptComparisonResult(list):
    """Represents the project comparison result.

    Iterating this returns all changed objects.

    :version added: 3.5.12.0

    """

    def __getitem__(self, state_or_object):
        """getitem.

        ``state_or_object`` is of type :class:`ObjectDifferences`.
            Calls :meth:`get_changed_objects`

        ``state_or_object`` is of type :class:`ScriptObject`
            Calls :meth:`get_diff_state`

        """
        pass

    @property
    def left_project(self):
        """The first or left project which was compared.

        :rtype: :class:`ScriptProject`

        """
        pass

    @property
    def right_project(self):
        """The second or right project which was compared.

        :rtype: :class:`ScriptProject`

        """
        pass

    def get_changed_objects(self, state=ObjectDifferences.ANY_CHANGES):
        """Returns all changed objects with a matching diff state (any of the given flags have to be set).

        :type state: :class:`ObjectDifferences`
        :param state: The diff states to filter for objects.
        :rtype: list
        :returns: The objects matching the criteria.

        """
        pass

    def get_diff_state(self, script_object):
        """Gets the diff state for a specific object.

        :type script_object: ScriptObject
        :rtype: ScriptComparedObject
        :returns: The diff state for the object.

        """
        pass


class ExportReporter(object):
    """python classes can implement their own export_xml reporter here. This interface(``IExportReporter``) is exposed under the name ExportReporter."""

    def error(self, obj, message):
        """This method is called when an error has occurred during export_xml.

        :type obj: ScriptObject
        :param obj: The object which caused the error.
        :type message: str
        :param message: The message describing the problem.

        """
        pass

    def warning(self, obj, message):
        """This method is called when a warning has occurred during export_xml.

        :type obj: ScriptObject
        :param obj: The object which caused the warning.
        :type message: str
        :param message: The message describing the problem.

        """
        pass

    def nonexportable(self, obj):
        """This method is called when we find out that a given object is not exportable.

        This is only called for objects given directly
        as parameters - non-exportable children are silently ignored.
        The script can decide to abort the export by setting aborting
        to true during this phase.

        This method will be called for all non-exportable objects even
        when aborting is set to true. The flag will be checked after
        all objects have been checked for exportability, just before
        the actual export is going to start (and thus before the
        destination file is opened). This allows scripts to find out
        about all non-exportable objects in one run.

        :type obj: ScriptObject
        :param obj: The object which is not exportable

        """
        pass

    @property
    def aborting(self):
        """This allows abortion when we report non-exportable objects.

        :rtype: bool

        """
        pass


class ImportReporter(object):
    """Python classes can implement their own import_xml reporter here.

    This interface(IImportReporter) is exposed under the name ImportReporter.
    """

    def error(self, message):
        """This method is called when an error has occurred during import_xml.

        :type message: str
        :param message: The message describing the problem.

        """
        pass

    def warning(self, message):
        """This method is called when a warning has occurred during import_xml.

        :type message: str
        :param message: The message describing the problem.

        """
        pass

    def resolve_conflict(self, obj):
        """This method is called when an object to import is already existing.

        :type obj: ScriptObject
        :param obj: The already existing object.

        :rtype: ConflictResolve
        :returns: How to resolve the conflict: rename the new object, replace the
            existing object, or skip the new object.

        """
        pass

    def added(self, obj):
        """This method is called whenever an object has been successfully added during import.

        :type obj: ScriptObject
        :param obj: The newly added object.

        """
        pass

    def replaced(self, obj):
        """This method is called whenever an object has been successfully replaced during import.

        :type obj: ScriptObject
        :param obj: The replacing object.

        """
        pass

    def skipped(self, objectname):
        """This method is called whenever an object has been skipped during import.

        :type objectname: str
        :param objectname: The name of the skipped object.

        """
        pass

    @property
    def aborting(self):
        """Gets a boolean value indicating whether importing should be aborted or not.

        :rtype: bool

        """
        pass


class NativeExportReporter(object):
    """This reporter is used for the native XML export. This interface is exposed under the name NativeExportReporter."""

    def skipped(self, type_name, serializable_value_name):
        """This method is called when data has been effectively skipped during serialization or deserialization.

        :type type_name: str
        :param type_name: The typename of the object that was not stored or restored completely.
        :type serializable_value_name: str
        :param serializable_value_name: The serializable value name of the member or property
            that has been skipped.

        """
        pass

    def warn(self, message):
        """This method is called when a warning occurs during serialization or deserialization.

        :type message: str
        :param message: A message describing the reason of the warning.

        """
        pass

    def cancel(self, message):
        """This method is called when an error occurs during serialization or deserialization.

        The code that triggered the serialization should discard the resulting stream because it
        will not be correctly formatted in this case. The code that triggered the
        deserialization should discard the resulting object because it might be inconsistent.

        :type message: str
        :param message: A message describing the reason of the error.

        """
        pass


def NativeImportFilter(self, name, guid, type, path):
    """[Delegate]. This method can be used to filter the imported objects.

    :type name: str

    :type guid: Guid

    :type type: string

    :type path: tuple[object]
    :param path: A python tuple containing the object path.

    :rtype: bool
    :returns: ``True`` if the item is to be imported.

    """
    pass


class NativeImportHandler(object):
    """Handler callback for the native XML import.

    This interface is exposed under the name NativeImportHandler.

    """

    def conflict(self, name, existingObject, newguid):
        """Queries how to resolve a conflict.

        :type name: str
        :type existingObject: ScriptObject
        :type newguid: Guid
        :rtype: NativeImportResolve
        :returns: The resolution for this conflict.

        """
        pass

    def progress(self, name, pastedObject, exception):
        """Reports progress of import.

        :type name: str
        :type pastedObject: ScriptObject
        :type exception: Exception

        """
        pass

    def skipped(self, name):
        """Informs about skipped objects.

        :type name: tuple[object]
        :param name: A python tuple with the names..

        """
        pass
