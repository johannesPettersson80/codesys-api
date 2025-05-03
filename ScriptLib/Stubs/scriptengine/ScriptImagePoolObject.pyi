from enum import Enum
from .ScriptExternalFileObject import *


class ImageLinkType(Enum):
    """This enumeration represents the way an image is embedded or linked into a project.

    :version added: 3.5.9.0

    """

    Linked = 1
    """This value means that the image is linked from the project only."""

    EmbeddedAndLinked = 2
    """This value means that the image is embedded within the project while still linked to the
    according file in the filesystem and thus allowing automatic updates if changed on disk.

    """

    Embedded = 3
    """This value means that the image is embedded within the project."""


class ScriptImagePoolMarker(object):
    """Marker object to check whether an ScriptObject is an imagepool object.

    :version added: 3.5.9.0

    """

    @property
    def is_imagepool(self):
        """Gets a value indicating whether this ScriptApplicationMarker is an imagepool.

        :rtype: bool
        :returns: ``True`` if it is an imagepool; otherwise, ``False``

        """
        pass


class ScriptImagePoolObject(ScriptImagePoolMarker):
    """ScriptObjects which are an imagepool object are extended with this interface.

    :version added: 3.5.9.0

    """

    @property
    def images(self):
        """Gets the collection of the items currently configured within this imagepool.

        :rtype: :class:`ScriptImagePoolItems`

        """
        pass

    @property
    def download_only_used_images(self):
        """Gets or sets a value whether all images or only the explicitly referenced ones should be downloaded to PLCs.

        :rtype: bool

        """
        pass

    @download_only_used_images.setter
    def download_only_used_images(self, value: bool):
        pass

    @property
    def imagepool_is_internal(self):
        """Gets or sets a value whether this image pool is visible for projects embedding the current one as a library.

        This is not relevant when working on a project itself.

        :rtype: bool

        """
        pass

    @imagepool_is_internal.setter
    def imagepool_is_internal(self, value: bool):
        pass

    @property
    def symboltextlist(self):
        """Gets and sets the name of the text list for translation of the symbols in this image pool.

        :rtype: str

        """
        pass

    @symboltextlist.setter
    def symboltextlist(self, value: str):
        pass


class ScriptImagePoolItems(list):
    """Gets the current number of items in this image pool.

    :version added: 3.5.9.0

    """

    def __len__(self):
        """Gets the current number of items in this image pool.

        :rtype: int

        """
        pass

    def __getitem__(self, index: int):
        """Returns the item with the given index or id.

        :type index: int
        :param index: The index of the item to return or the id to search for.

        :raises ArgumentOutOfRangeException: Thrown when the given index is not in the valid range.

        :rtype: :class:`ScriptImagePoolItem`

        """
        pass

    def __getitem__(self, id: str):
        """Returns the item with the given index or id.

        :type id: str
        :param id: The id to search for.

        :raises KeyNotFoundException: Thrown when the given id is not contained in the items.

        :rtype: :class:`ScriptImagePoolItem`

        """
        pass

    def add(self, id, path, linktype, updateMode=None):
        """Adds a new image to the current image pool.

        :type id: str
        :param id: The id to assign to the newly inserted image. Must not yet be existing.

        :type path: str
        :param path: The file path to reference by the new image item.

        :type linktype: :class:`ImageLinkType`
        :param linktype: The way the new image item references the according file.

        :type updateMode: AutoUpdateMode
        :param updateMode: The way the image item is updated automatically,
            relevant only if ``linktype`` is :attr:`ImageLinkType.EmbeddedAndLinked`

        :raises ArgumentException: Thrown when an item with the according ``id`` already existings.

        :rtype: :class:`ScriptImagePoolItem`
        :returns: The newly created ScriptImagePoolItem.

        """
        pass

    def remove(self, id):
        """Removes the :class:`ScriptImagePoolItem` with the given ``id``.

        :type id: str
        :param id: description

        :raises KeyNotFoundException: Thrown when no entry with the given id exists.

        """
        pass

    def move(self, indexSrc, indexDst):
        """Moves a :class:`ScriptImagePoolItem` in the list of items.

        :type indexSrc: int
        :param indexSrc: The index of the item that should be moved.

        :type indexDst: int
        :param indexDst: The index where the item should be located afterwards.

        :raises ArgumentOutOfRangeException: Thrown when the given indices are out of range.

        """
        pass


class ScriptImagePoolItem(object):
    """An item (in fact like a line) within a :class:`ScriptImagePoolObject`.

    :version added: 3.5.9.0

    """

    @property
    def id(self):
        """The identification of the image that can be accessed in the visualization too.

        :raises ArgumentException: Thrown when the id is being set and the new id is already
            contained in the imagepool.

        :rtype: str

        """
        pass

    @id.setter
    def id(self, value: str):
        pass

    @property
    def filepath(self):
        """The path of the referenced image.

        Relevant only if :attr:`linktype` yields :attr:`ImageLinkType.Linked` or :attr:`ImageLinkType.EmbeddedAndLinked`.

        :rtype: str

        """
        pass

    @filepath.setter
    def filepath(self, value: str):
        pass

    @property
    def linktype(self):
        """The way the image is referenced.

        :rtype: :class:`ImageLinkType`

        """
        pass

    @linktype.setter
    def linktype(self, value: ImageLinkType):

        pass

    @property
    def updatemode(self):
        """The way the image is updated automatically while the project is open.

        Relevant only if :attr:`linktype` yields :attr:`ImageLinkType.EmbeddedAndLinked`.

        :rtype: :class:`AutoUpdateMode`

        """
        pass

    @updatemode.setter
    def updatemode(self, value: AutoUpdateMode):
        pass


class ScriptImagePoolObjectContainer(object):
    """Projects and Application Objects are extended with this interface since CoDeSys V3.5.9.0.

    :version added: 3.5.9.0

    """

    def create_imagepool(self, name=None):
        """Creates a new image pool object in the current context (either application or project global).

        :type name: str
        :param name: The name of the new imagepool object. In case of ``None``,
            a default name will be generated.

        :raises ArgumentException: Thrown when an image pool with the given name
            already exists within the current context.

        :rtype: :class:`ScriptImagePoolObject`
        :returns: The newly created imagepool object.

        """
        pass

    def get_global_imagepool(self):
        """Returns the global image pool object or creates a new one if not yet existing.

        Typically this method can be called on projects only. Only in case of special
        customizations of the programming system, it is allowed to call this on an application too.

        :raises InvalidOperationException: Thrown when called on applications when this is not
            allowed.

        :rtype: :class:`ScriptImagePoolObject`
        :returns: The global imagepool.

        """
        pass

    @property
    def has_global_imagepool(self):
        """Checks whether there is already a globalimagepool in the current location.

        Only in case of special customizations of the programming system, it
        is allowed to call this on an application too.

        :raises InvalidOperationException: Thrown when called on applications when this is not
            allowed.

        :rtype: bool

        """
        pass
