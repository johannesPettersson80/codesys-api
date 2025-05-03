from enum import Enum
from .dotNETs import *


class ReferenceMode(Enum):
    Link = 0,
    LinkAndEmbed = 1,
    Embed = 2


class AutoUpdateMode(Enum):
    """This enumeration is used to control how changes in a physical file are reflected
        to the embedded data of a _3S.CoDeSys.Core.External.IFileReference.

    """

    Always = 0,
    """Changes on the physical file are automatically reflected in the embedded data."""

    Prompt = 1,
    """When the physical file changes, an event will be triggered in order to obtain
        information whether to automatically update the embedded data or not.
    """

    Never = 2
    """Changes on the physical file are not automatically reflected in the embedded data."""


class ScriptExternalFileObjectMarker(object):
    """Determines whether this object is an external file object or can contain them.

    :version added: 3.5.9.0

    """

    @property
    def is_external_file_object(self):
        """Gets a value indicating whether this :class:`ScriptObject` is is an external file object.

        :rtype: bool
        :returns: ``True`` if it is an external file object; otherwise, ``False``.

        """
        pass

    @property
    def may_contain_external_file_objects(self):
        """Gets a value indicating whether this :class:`ScriptObject` or :class:`ScriptProject` may contain external file objects.

        The project root may always contain external file objects, those are
        not downloaded to the devices.
        Devices and Applications may contain files which are synchronized to the runtime,
        depending on the device description and settings.

        :rtype: bool
        :returns: ``True`` if it may contain external file objects; otherwise, ``False``

        """
        pass


class ScriptExternalFileObject(ScriptExternalFileObjectMarker):
    """Provides the actual functionality of the external file objects.

    :version added: 3.5.9.0

    """

    @property
    def file_path(self):
        """Gets the file path.

        :rtype: str

        """
        pass

    @property
    def reference_mode(self):
        """Gets the reference mode.

        :rtype: ReferenceMode

        """
        pass

    @property
    def auto_update_mode(self):
        """Gets the auto update mode.

        :rtype: AutoUpdateMode

        """
        pass

    def change_modes(self, reference_mode, auto_update_mode = AutoUpdateMode.Never):
        """Changes the modes of the external file object.

        :type reference_mode: ReferenceMode
        :param reference_mode: The reference mode.

        :type auto_update_mode: AutoUpdateMode`
        :param auto_update_mode: The auto update mode. This is optional, and only makes sense if
            ``reference_mode`` is set to ReferenceMode.LinkAndEmbed. Defaults to
            ``AutoUpdateMode.Never`` if omitted.

        """
        pass

    def update(self):
        """Updates this instance."""
        pass

    def calculate_checksum(self):
        """Calculates the checksum of the data.

        :rtype: int
        :returns: The CRC 32 value of the data.

        """
        pass

    @property
    def last_modification(self):
        """Gets the last modification date.

        :rtype: DateTime

        """
        pass

    @property
    def length(self):
        """Gets the length of the data in bytes.

        :rtype: int

        """
        pass

    def get_data(self):
        """Gets the data as a byte array.

        :rtype: list[byte]

        """
        pass

    def get_data(self, stream):
        """Gets the data by writing it into the given stream.

        :type stream: Stream
        :param stream: The stream.

        """
        pass

    def get_data(self, filename):
        """Gets the data by writing it to the specified filename.

        :type filename: str
        :param filename: The filename.

        """
        pass

    def create_edit_path(self):
        """Gets the absolute path where this file reference is edited.

        This is the absolute path itself if the file reference is linked to a file system object,
        or a temporary path if it is embedded into a project.

        :rtype: str
        :returns: The edit path of this file reference.

        """
        pass


class ScriptExternalFileObjectContainer(ScriptExternalFileObjectMarker):
    """This interface is implemented by the project root, and by objects which can contain synchable external file objects.

    The project root may always contain external file objects, those are not downloaded to the devices.
    Devices and Applications may contain files which are synchronized to the runtime, depending on the device description and settings.

    :version added: 3.5.9.0

    """

    def create_external_file_object(self, file_path, name=None,
                                    reference_mode=ReferenceMode.Embed, auto_update_mode=AutoUpdateMode.Never):
        """Creates an external file objects with the specified name.

        :type file_path: str
        :param file_path: The file path with the contents of the external file object.

        :type name: str
        :param name: The name. This is optional, if it is omitted, the filename will be extracted
            from the path.

        :type reference_mode: ReferenceMode
        :param reference_mode: The reference mode.

        :type auto_update_mode: AutoUpdateMode
        :param auto_update_mode: The automatic update mode.

        :rtype: :class:`ScriptExternalFileObject`
        :returns: The newly created external file object.

        """
        pass
