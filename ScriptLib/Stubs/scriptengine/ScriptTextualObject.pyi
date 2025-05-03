class ScriptTextualObjectMarker(object):
    """All tree objects get amended with this marker.

    :version added: 3.5.6.0

    """

    @property
    def has_textual_declaration(self):
        """Gets a value indicating whether this :class:`ScriptObject` has a textual declaration part.

        :rtype: bool
        :returns: ``True`` if it has a textual declaration; otherwise ``False``.

        """
        pass

    @property
    def has_textual_implementation(self):
        """Gets a value indicating whether this :class:`ScriptObject` has a textual implementation part.

        :rtype: bool
        :returns: ``True`` if it has a textual implementation; otherwise ``False``.

        """
        pass


class ScriptTextDocument(object):
    r"""Interface for a text document, as it is used e. G. in textual declaration and implementation parts.

    Line endings ('\\n', '\\r', '\\r\\n') are normalized to '\\n'.
    Lines do not include the line ending character. The first
    character has offset 0, the first line has lineno 0.

    :version added: 3.5.6.0

    """

    @property
    def length(self):
        """Gets the length of the text document in bytes.

        :rtype: int

        """
        pass

    @property
    def linecount(self):
        r"""Gets the number of lines in the current text document.

        Line endings ('\\n', '\\r', '\\r\\n') are normalized to '\\n'.
        Lines do not include the line ending character. The first line has lineno 0.

        :rtype: int

        """
        pass

    @property
    def text(self):
        """Gets the complete text as a string.

        :rtype: str

        """
        pass

    def get_line(self, lineno):
        """Gets the line with the specified lineno.

        Lines do not include the line ending character. The first line has lineno 0.

        :type lineno: int
        :param lineno: The line number.

        :rtype: str
        :returns: The line.

        """
        pass

    def get_text(self, length, offset=None, lineno=None, lineoffset=None):
        """Gets the text.

        .. warning:: The original C# function that is called with this method contains 2 overloads.
            It is strongly advised to pass *all* arguments with their respective keywords.
            ``offset``, ``lineno`` and ``lineoffset`` are not actually optional, they just aren't
            required in every overload. Pass them if your overload needs them!

        **get_text(self, offset, length) (1/2)**

        Gets the text at the specified offset.

        :type offset: int

        :type length: int

        :rtype: str


        **get_text(self, lineno, lineoffset, length) (2/2)**

        Gets the text at the specified lineno.

        :type lineno: int

        :type lineoffset: int
        :param lineoffset: The offset within the line.

        :type length: int

        :rtype: str

        """
        pass

    def replace_line(self, lineno, line):
        """Replaces the complete line with the specified line number with the new text.

        This method retains the position info of the text lines which are not modified.

        :type lineno: int

        :type line: str

        """
        pass

    def append(self, text):
        """Appends the specified text at the end of the buffer.

        This method retains the position info of the text lines which are not modified.

        :type text: str
        :param text: The text.

        """
        pass

    def insert(self, text, offset=None, lineno=None, lineoffset=None):
        """Insert text.

        .. warning:: The original C# function that is called with this method contains 2 overloads.
            It is strongly advised to pass *all* arguments with their respective keywords.
            ``offset``, ``lineno`` and ``lineoffset`` are not actually optional, they just aren't
            required in every overload. Pass them if your overload needs them!

        **insert(self, offset, text) (1/2)**

        Inserts the text at the specified offset.

        This method retains the position info of the text lines which are not modified.

        :type offset: int

        :type text: str


        **insert(self, lineno, lineoffset, text) (2/2)**

        Inserts the text at the offset of the specified line.

        This method retains the position info of the text lines which are not modified.

        :type lineno: int

        :type lineoffset: int
        :param lineoffset: The offset within the line.

        :type text: str

        :rtype: str

        """
        pass

    def remove(self, length, offset=None, lineno=None, lineoffset=None):
        """Remove text.

        .. warning:: The original C# function that is called with this method contains 2 overloads.
            It is strongly advised to pass *all* arguments with their respective keywords.
            ``offset``, ``lineno`` and ``lineoffset`` are not actually optional, they just aren't
            required in every overload. Pass them if your overload needs them!


        **remove(self, offset, length) (1/2)**

        Removes the text at the specified offset.

        This method retains the position info of the text lines which are not modified.

        :type offset: int

        :type length: int


        **remove(self, lineno, lineoffset, length) (2/2)**

        Removes the text at the specified offset of the specified line.

        This method retains the position info of the text lines which are not modified.

        :type lineno: int

        :type lineoffset: int
        :param lineoffset: The offset within the line.

        :type length: int

        """
        pass

    def replace(self, new_text=None, newtext=None, length=None, offset=None, lineno=None,
                lineoffset=None):
        """Replace text.

        .. warning:: The original C# function that is called with this method contains 3 overloads.
            It is strongly advised to pass *all* arguments with their respective keywords.
            No argument is actually optional, they just aren't
            required in every overload. Pass them if your overload needs them!


        **replace(self, offset, length, newtext) (1/3)**

        Removes the text at the specified offset.

        This method retains the position info of the text lines which are not modified.

        :type offset: int

        :type length: int

        :type newtext: str
        :param newtext: The new text.


        **replace(self, lineno, lineoffset, length, newtext) (2/3)**

        Removes the text at the specified offset of the specified line.

        This method retains the position info of the text lines which are not modified.

        :type lineno: int

        :type lineoffset: int
        :param lineoffset: The offset within the line.

        :type length: int

        :type newtext: str
        :param newtext: The new text.


        **replace (self, new_text) (3/3)**

        Sets the specified new text.

        This method erases the position info (used for bookmarks etc).

        :type new_text: str
        :param new_text: The new text.

        """
        pass


class ScriptObjectWithTextualDeclaration(ScriptTextualObjectMarker):
    """Accessor interface for textual declaration parts.

    :version added: 3.5.6.0

    """

    @property
    def textual_declaration(self):
        """Gets the textual declaration.

        :rtype: :class:`ScriptTextDocument`

        """
        pass


class ScriptObjectWithTextualImplementation(ScriptTextualObjectMarker):
    """Accessor interface for textual implementation parts.

    :version added: 3.5.6.0

    """

    @property
    def textual_implementation(self):
        """Gets the textual implementation.

        :rtype: :class:`ScriptTextDocument`

        """
        pass
