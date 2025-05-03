from .ScriptProject import *


class ScriptTreeObject(object):
    """Common base functionality for ScriptObject and ScriptProject."""

    @property
    def project(self):
        """Gets the project.

        This returns "this" rsp. "self" if called on Projects.

        :rtype: ScriptProject

        """
        pass

    @property
    def handle(self):
        """Gets the internal Automation Platform handle of the Project.

        This handle is primarily useful for other Atomation Platform plugins which provide
        functionality for scripts via ScriptDriver. When they consume :class:`ScriptProject`
        as their parameters, they can use the handle to gain access to the underlying Automation
        Platform object.

        :rtype: int

        """
        pass

    def find(self, name, recursive=False):
        """Finds objects matching the given name.

        Names are not unique in the tree, so several Objects can be
        delivered. The search is against the nonlocalized name.

        :type name: str
        :param name: The Name.
        :type recursive: bool
        :param recursive: Whether we search recursively.
        :rtype: list[ScriptObject]
        :returns: The collection of objects.

        """
        pass

    def get_children(self, recursive=False):
        """Gets the children of our object.

        :type recursive: bool
        :param recursive: If set to ``True``, we work recursively.
        :rtype: list[ScriptObject]
        :returns: All child objects.

        """
        pass

    @property
    def is_root(self):
        """Gets a value indicating whether this instance is the root of the object tree.

        This returns true for all :class:`.ScriptProject` instances,
        and false for all :class:`.ScriptObject` instances.

        :rtype: bool

        """
        pass
