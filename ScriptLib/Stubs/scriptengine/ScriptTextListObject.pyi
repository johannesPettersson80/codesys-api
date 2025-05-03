class ScriptTextListMarker(object):
    """Marker object to check whether an ScriptObject is a textlist object.

    :version added: 3.5.11.0

    """

    @property
    def is_textlist(self):
        """Gets a value indicating whether this :class:`.ScriptApplicationMarker` is a textlist.

        :rtype: bool
        :returns: ``True`` if it is a textlist; otherwise ``False``.

        """
        pass


class ScriptTextListObject(ScriptTextListMarker):
    """ScriptObjects which are a textlist object are extended with this interface.

    :version added: 3.5.11.0

    """

    def addlanguage(self, language):
        """Adds a new language to the text list.

        If the language already exists, it is not added twice.

        """
        pass

    def removelanguage(self, language):
        """Removes a new language to the text list."""
        pass

    @property
    def rows(self):
        """Gets the collection of the rows currently configured within this textlist.

        :rtype: ScriptTextListItemsCollection

        """
        pass

    def languagecount(self):
        """Gets the current number of languages in this textlist.

        :rtype: int

        """
        pass

    def getlanguage(self, index):
        """Returns the language with the given ``index``.

        :type index: int
        :param index: The index of the language to return.

        :raises ArgumentOutOfRangeException: Thrown when the given index is not in the valid range.

        :rtype: str

        """
        pass

    def updatetextids(self):
        """Only for global textlist.

        Calls the command 'Update Visualization Text IDs' for this textlist.
        This command updates all inconsistent IDs in a static text list.

        """
        pass

    def checkids(self):
        """Only for global textlist.

        Calls the command 'Check Visualization Text IDs' for this textlist.
        This command checks whether the ID of a text list entry in the project is correct
        and reports the result.

        """
        pass

    def removeunusedids(self):
        """Only for global textlist.

        Calls the command 'Remove Unused Text List Entries' for this textlist.
        This command checks whether a text list entry in the project is used as static text.
        If not, CODESYS removes it from the text list.

        """
        pass

    def importfile(self, importfile):
        """Like in import/export dialog: The file can contain text list entries both for the global text list and for text lists.

        :type importfile: str

        """
        pass

    def importreplacementfile(self, importfile):
        """Like in import/export dialog: The replacement file contains replacements for the global text list.

        :type importfile: str
        :param importfile: Name and path of a file of type csv.

        """
        pass

    def export(self, exportfile):
        """Like in import/export dialog: exports all the texts from all the text lists in the current project.

        :type exportfile: str

        """
        pass


class ScriptTextListRow(object):
    """A row  within an :class:`ScriptTextListObject`.

    :version added: 3.5.11.0

    """

    @property
    def id(self):
        """The identification of the row.

        :rtype: str

        """
        pass

    @property
    def defaulttext(self):
        """The default text entry in this row.

        :rtype: str

        """
        pass

    def setlanguagetext(self, language, text):
        """Sets the text in the row, for a defined language.

        :type language: str
        :param language: The languagename, which defines the language entry, to use.

        :type text: str
        :param text: The text to set for this language.

        :raises ArgumentOutOfRangeException: Thrown when the language does not yet exist
            in the textlist.

        :rtype: bool
        :returns: ``True`` if the text could be set, otherwise ``False``.

        """
        pass

    def setdefaulttext(self, defaulttext):
        """Sets the defaulttext in this row.

        :type defaulttext: str
        :param defaulttext: The defaultext to set for this row.

        :rtype: bool
        :returns: ``True`` if the text could be set, otherwise ``False``.

        """
        pass

    def languagetextcount(self):
        """Gets the current number of languagetexts in this row.

        :rtype: int

        """
        pass

    def languagetext(self, index):
        """Gets the languagetext.

        :type index: int
        :param index: The index of the languagetext to return.

        :raises ArgumentOutOfRangeException: Thrown when the given index is not in the valid range.

        :rtype: str
        :returns: The language text.

        """
        pass


class ScriptTextListItemsCollection(list):
    """The items currently managed by the textlist object.

    :version added: 3.5.11.0

    """

    def __len__(self):
        """Gets the current number of items(rows) in this textlist.

        :rtype: int

        """
        pass

    def __getitem__(self, index_or_id):
        """Returns the row with the given index or id.

        :type index_or_id: int or str
        :param index_or_id: The index of the row to return or the id to search for.

        :raises ArgumentOutOfRangeException: Thrown when the given index is not in the valid range.

        :raises KeyNotFoundException: Thrown when the given id is not contained in the rows.

        :rtype: :class:`ScriptTextListRow`
        :returns: The matching row.

        """
        pass

    def add(self, id, defaulttext):
        """Adds a new row to the current textlist.

        :type id: str
        :param id: The id to assign to the newly inserted row. Must not yet be existing.

        :type defaulttext: str
        :param defaulttext: The default text.

        :rtype: :class:`ScriptTextListRow`
        :returns: The newly created ScriptTextListRow.

        """
        pass

    def remove(self, id):
        """Removes the ScriptTextListRow with the given ``id``.

        :type id: str
        :param id: The id of the item to remove.

        :raises KeyNotFoundException: Thrown when no entry with the given id exists.

        """
        pass


class ScriptTextListObjectContainer(object):
    """Projects and Application Objects are extended with this interface.

    :version added: 3.5.11.0

    """

    def create_textlist(self, name=None):
        """Creates a new textlist object in the current context (either application or project global).

        :type name: str
        :param name: The name of the new textlist object. In case of ``None``, a default name
            will be generated.

        :raises ArgumentException: Thrown when a textlist with the given name already exists within
            the current context.

        :rtype: :class:`ScriptTextListObject`
        :returns: The newly created textlist object.

        """
        pass

    def get_global_textlist(self):
        """Returns the global textlist object or creates a new one if not yet existing.

        Typically this method can be called on projects only. Only in case of special
        customizations of the programming system, it is allowed to call this on an application too.

        :rtype: :class:`ScriptTextListObject`
        :returns: The global textlist.

        """
        pass

    @property
    def has_global_textlist(self):
        """Checks whether there is already a global textlist in the current location.

        Only in case of special customizations of the programming system, it
        is allowed to call this on an application too.

        :raises InvalidOperationException:
            Thrown when called on applications when this is not allowed.

        :rtype: bool

        """
        pass
