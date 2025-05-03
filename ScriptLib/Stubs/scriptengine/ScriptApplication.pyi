class ScriptApplicationMarker(object):
    """Marker object to check whether a ScriptObject is an application object.

    :version added: 3.5.2.0

    """

    @property
    def is_application(self):
        """Gets a value indicating whether this :class:`ScriptApplicationMarker` is an application.

        :rtype: bool
        :returns: ``True`` if it is an application; otherwise, ``False``.

        """
        pass


class ScriptApplication(ScriptApplicationMarker):
    """ScriptObjects which are an application object are extended with this interface.

    :version added: 3.5.2.0

    """

    @property
    def is_active_application(self):
        """Gets a value indicating whether this.

        :class:`ScriptApplication` is the active application.

        The active application is always in the primary project, so this
        property will always return false for non-primary projects.

        :rtype: bool
        :returns: ``True`` if it is the active application; otherwise, ``False``.

        """
        pass

    def build(self):
        """Builds the application.

        You can use the :meth:`.System.get_messages` and
        :meth:`.System.get_message_objects` calls to check whether
        any messages were added.
        This method only works for applications in the primary project.

        """
        pass

    def clean(self):
        """Cleans the application.

        You can use the :meth:`.System.get_messages` and
        :meth:`.System.get_message_objects` calls to check whether
        any messages were added.
        This method only works for applications in the primary project.

        """
        pass

    def generate_code(self):
        """Generates the code for the application.

        You can use the :meth:`.System.get_messages` and
        :meth:`.System.get_message_objects` calls to check whether
        any messages were added.
        This method only works for applications in the primary project.

        """
        pass

    def rebuild(self):
        """Rebuilds the application.

        You can use the :meth:`.System.get_messages` and
        :meth:`.System.get_message_objects` calls to check whether
        any messages were added.
        This method only works for applications in the primary project.

        """
        pass

    def create_boot_application(self, output_filename):
        """Creates the offline boot project at the specified outputpath.

        Relative output filenames are interpreted relative to the location of the
        project. If you pass None or the empty string, applicationname.app is used.
        This method only works for applications in the primary project.

        :type output_filename: str
        :param output_filename: The filename to write the boot application to.

        """
        pass

    def create_boot_application(self, output_filename, update_compile_info=False, write_visu_files=False):
        """Creates the offline boot project at the specified outputpath.

        If the project was changed since the last download or online change to a PLC, and you
        create a boot application with ``update_compile_info`` set to
        ``true``, this will overwrite the current compiler reference context with the one
        matching the boot project (which no longer matches the one on the PLC). Thus, a direct
        conline change to the PLC will no longer work. On the other hand, the reference context
        now matches the created boot application, so you can login to any PLC on which you
        deploy the generated boot application. This updated compile context is also the one to
        be included into a project archive.

        Relative output filenames are interpreted relative to the location of the
        project. If you pass None or the empty string, applicationname.app is used.
        This method only works for applications in the primary project.

        :version added: 3.5.5.0, available for 3.5.3.x from Patch 1

        :type output_filename: str
        :param output_filename: The filename to write the boot application to.

        :type update_compile_file: bool
        :param update_compile_file: if set to ``true``, also writes the compile
            information (compiler reference context) to the project directory. (This may break
            online change, see below). (The compile information is updated in the directory where the
            project resides, not the output directory.)

        :type write_visu_files: bool
        :param write_visu_files: if set to ``true``, also writes the visualization
            files into the output directory. It will be silently ignored when this application does not
            contain a visualization manager.

        """
        pass

    def create_task_configuration(self):
        """Add the task configuration object to an application.

        :version added: 3.5.10.0

        :rtype: :class:`.ScriptTaskConfigObject`
        :returns: Script object of the task configuration object

        """
        pass

    @property
    def is_uptodate(self):
        """Gets a value indicating whether this application is the same running on the PLC.

        :version added: 3.5.10.0

        :rtype: bool
        :returns: ``True`` if it is the same; otherwise, ``False``.

        """
        pass

    @property
    def is_online_change_possible(self):
        """Gets a value indicating whether an online change is possible or not.

        :version added: 3.5.10.0

        :rtype: bool
        :returns: ``True`` if online change is possible; otherwise, ``False``.

        """
        pass
