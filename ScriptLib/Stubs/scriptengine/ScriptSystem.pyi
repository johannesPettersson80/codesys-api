from enum import Enum
from .dotNETs import *
from .ScriptTreeObject import *


class PromptHandling(Enum):
    """Definition flags for prompt handling. Prompts are standard dialog boxes issued by plugins to inform or query the user.

    Simple prompts are those which have only a single button (like a single OK button) and
    don't leave any choices to the user. Simple prompt handling also applies to
    prompts with or without message keys, but prompts actually caught by message keys
    defined in :attr:`System.prompt_answers` are not subject to simple prompt
    handling.
    This enum may be extended in future releases.
    Currently, all handling choices are cumulative, so you can set :attr:`ForwardSimplePrompts`
    and :attr:`LogSimplePrompts` at the same time.

    """

    NONE = 0
    """None of the flags are set. This implies that "simple" prompts are silently suppressed."""

    ForwardSimplePrompts = 1 << 0
    """Handle simple prompts in their original way. Usually, this means, the user is queried with
    a dialog box. (However, other plugins may modify that behaviour.) This flag is set by default
    in UI mode. If you disable this flag, simple promts are not processed in any way.

    """

    LogSimplePrompts = 1 << 1
    """Print simple prompts as a log message, similar to :meth:`System.write_message`.
    Log the prompts to the message view with appropriate priority. This is set by default in
    Non-UI mode.

    """

    EnableTextPrompts = 1 << 2
    """Enables a basic text mode message service implementation in --noUI mode. By default,
    this flag is not set for compatibility reasons with old scripts, and it is ignored if
    :attr:`System.ui_present` is true.

    If this flag is not set, all MessageServicePrompts which ought to query the
    user simply return the default value, while :meth:`ScriptUI.open_file_dialog`,
    :meth:`ScriptUI.save_file_dialog`, :meth:`ScriptUI.browse_directory_dialog`,
    :meth:`ScriptUI.query_string`, :meth:`ScriptUI.query_password` and
    :meth:`ScriptUI.query_credentials` simplypop up the standard graphical dialogs.

    """

    ProcessScriptPrompts = 1 << 3
    """If this flag is set, prompts issued by the Script itself via :attr:`System2.ui` are also
    subject to the :attr:`System2.prompt_handling` and :attr:`System.prompt_answers`
    processing / filtering. This flag is not set by default.

    """

    LogMessageKeys = 1 << 4
    """Logs all MessageService calls with their message key to the message store. Use this to
    catch the message keys you need for :attr:`System.prompt_answers`.

    Calls without a message key are logged with the key "&lt;&lt;No Key&gt;&gt;", calls
    which got passed None as message key are logged with "&lt;&lt;None&gt;&gt;"

    """


class Severity(Enum):
    """Describes the severity of an _3S.CoDeSys.Core.Messages.IMessage."""

    FatalError = 1,
    """Indicates that the corresponding message is a fatal error."""

    Error = 2,
    """Indicates that the corresponding message is an error."""

    Warning = 4,
    """Indicates that the corresponding message is a warning."""

    Information = 8,
    """Indicates that the corresponding message is an information."""

    Text = 16
    """Indicates that the corresponding message is an informational text 
        without corresponding source code position.
    """


class PromptChoice(Enum):
    """ This enumeration denotes possible prompt options for _3S.CoDeSys.Core.IMessageService
        methods.
    """

    OK = 0,
    """The user can choose "OK"."""

    OKCancel = 1,
    """The user can choose "OK" or "Cancel"."""

    YesNo = 2,
    """The user can choose "Yes" and "No"."""

    YesNoCancel = 3,
    """The user can choose "Yes", "No", and "Cancel"."""

    RetryCancel = 4,
    """The user can choose "Retry" or "Cancel"."""

    AbortRetryIgnore = 5
    """The user can choose "Abort", "Retry", and "Ignore"."""


class PromptResult(Enum):
    """ This enumeration denotes possible prompt results from _3S.CoDeSys.Core.IMessageService
        methods.
    """

    OK = 0,
    """The user has selected "OK"."""

    Cancel = 1,
    """The user has selected "Cancel"."""

    Yes = 2,
    """The user has selected "Yes"."""

    No = 3,
    """The user has selected "No"."""

    Retry = 4,
    """The user has selected "Retry"."""

    Abort = 5,
    """The user has selected "Abort"."""

    Ignore = 6
    """The user has selected "Ignored"."""


class System(object):
    """Access to generic CoDeSys system functionality.

    An instance of this object is planted into the scriptengine module with the name "system".

    """

    def exit(self, exitcode=0):
        """Exits the application platform by shutting down the engine and exiting the process.

        If you just want to terminate the script execution without
        exitting the platform, call sys.exit() or raise a
        SystemExitException. (When running the script via --runscript
        command line parameter in --noUI-Mode, this will also terminate
        CoDeSys, as there's nothing else to do after the script exitted.)

        :type exitcode: int or None
        :param exitcode: The exitcode we return to the operating
            system. If omitted, we return the ExitCode 0 which normally
            means success.

        """
        pass

    @property
    def trace(self):
        """Gets or sets a value indicating whether trace :class:`System` is active on the current script execution.

        trace is the replacement for the old "echo" functionality in
        the CoDeSys V2.3 batch mode. It adds log messages (Category
        ScriptMessage, Severity Info) into the IMessageStorage on the
        following events: Change of source code line, entering and
        exitting of python scope, exception thrown in python code.

        This setting may be ignored: For example, due to internal
        restrictions in the IronPython Engine, script tracing is disabled
        in debugging mode.

        :rtype: bool
        :returns: ``True`` if trace is activated; otherwise, ``False``.

        """
        pass

    @trace.setter
    def trace(self, value: bool):
        pass

    @property
    def ui_present(self):
        """Gets a value indicating whether we have an UI.

        If this is false, we're running in a console application or background
        service.

        :rtype: bool
        :returns: ``True`` if [UI present]; otherwise, ``False``.

        """
        pass

    def write_message(self, severity, stMessage, obj=None, position=-1, length=None):
        """Writes the message to the Message Store.

        Position and length are only meaningfull if obj is a
        ScriptObject and are ignored otherwise.

        :type severity: :class:`Severity`
        :param severity: The severity.

        :type stMessage: str
        :param stMessage: The message.

        :type obj: :class:`ScriptTreeObject`
        :param obj: The ScriptObject or ScriptProject the message belongs to.

        :type position: long
        :param position: The position including offset in the data for the message.

        :type length: int
        :param length: The length in the data for the message.

        """
        pass

    def get_messages(self, category="{194B48A9-AB51-43ae-B9A9-51D3EDAADDF3}"):
        """Gets all messages of a given category which are currently in the store.

        :type category: str
        :param category: The category Guid (defaults to the ScriptMessage category)

        :rtype: list
        :returns: The list of message texts

        """
        pass

    @property
    def prompt_answers(self):
        """Gets the prompt answers Dictionary for simulating interactive user input.

        This dictionary is used to intercept the IMessageService
        interface. Whenever a method with a stmessage_key is called, the
        dictionary is searched for the message_key. If found, the
        corresponding value is returned (for prompts), or the call is
        ignored (for errors). All other calls are forwarded to the
        original messageService.

        For this to work, all the keys must be strings matching the
        message_key values. For Prompts, the following possibilities
        exist:

        .. list-table::
            :widths: auto

            * - A :class:`PromptResult` member
              - One of the :class:`PromptResult` enum members, the list is :attr:`PromptResult.OK`,
                :attr:`PromptResult.Cancel`, :attr:`PromptResult.Yes`,:attr:`PromptResult.No`,
                :attr:`PromptResult.Retry`,:attr:`PromptResult.Abort` and
                :attr:`PromptResult.Ignore`. It depends on the exact prompt command which values
                make sense.

            * - An :class:`int`
              - The MultipleChoicePrompt methods will try to
                convert the value to an integer for the choice which was selected.

            * - A :class:`MultipleChoiceSelector` delegate
              - For the MultipleChoicePrompt methods, you can
                also give a delegate which gets the list of strings and returns the result.

            * - A tuple <:class:`PromptResult` member, :class:`PromptChoiceFilter` delegate>
              - Some prompts present a list with possibly multiple selectable
                choices, and return a Prompt Result. For those prompts, a
                PromptResult is accepted as value (with results in none of the
                choices being selected), or a Tuple <list> containing at least
                2 elements: a :class:`PromptResult` followed by a :class:`PromptChoiceFilter`
                delegate which allows the script for fine grained selection.

        If the value given does not make sense in the context of the
        current prompt, an InvalidCastException is raised.

        For errors, the values are not used and don't matter (may be
        ``None`` / None).

        To give best semantics for the scripts, this dictionary is a
        PythonDictionary instance, that means you can easily add
        values::

            # set a value:
            System.prompt_answers["OverWriteFiles"] = PromptResult.Cancel

            # Set multiple values:
            System.prompt_answers.update(
               {"OverWriteFiles": PromptResult.OK,
                "DisFullError": None})

            # Reset everything:
            System.prompt_answers.clear()

        :rtype: dict
        :returns: The prompt answers.

        """
        pass

    @property
    def executable_filename(self):
        """Gets the name of the executable file (the currently running application).

        :rtype: str

        """
        pass

    def process_messageloop(self):
        """Processes the Win32 message loop of the current Thread, if present.

        This allows the UI to be updated during long running
        processes. It should be safe to call this from python scripts
        without reentrancy problems, because the ScriptExecutor calls
        SystemInstances.Engine.Frame.StartLengthyOperation(); to
        prevent the user from triggering more commands while the script is running.

        """
        pass

    def delay(self, milliseconds):
        """Delays the script for the specified amount of milliseconds.

        The message loop is served during the wait to allow background tasks to be processed.
        The actual duration of the delay will not meet hard realtime requirements.

        :type milliseconds: int
        :param milliseconds: The duration to wait

        """
        pass

    @property
    def prompt_handling(self):
        """Gets or sets the way message service prompts are handled.

        :version added: 3.5.1.0

        :rtype: :class:`PromptHandling`

        """
        pass

    @prompt_handling.setter
    def prompt_handling(self, value: PromptHandling):
        pass

    @property
    def ui(self):
        """Gets the script ui instance.

        :version added: 3.5.1.0

        :rtype: :class:`ScriptUI`

        """
        pass

    @property
    def commands(self):
        """Gets the commands.

        :version added: 3.5.1.0

        :rtype: :class:`ScriptCommands`

        """
        pass

    @property
    def factories(self):
        """Gets the factories.

        :version added: 3.5.1.0

        :rtype: :class:`ScriptObjectFactories`

        """
        pass

    def execute_on_primary_thread(self, code, async=False):
        """Executes a specified piece of code in the primary thread.

        !!Experts Only!!

        Advanced users only! Using multiple threads is neither officially supported nor
        encouraged in CoDeSys python scripts, you do that "on your own risk".
        This method is safe to be called from non-primary threads.
        This method relies on the primary thread processes its message queue. (If you
        don't know what the message queue is, threads are probably not the right thing for
        you...)
        Be careful to ensure that all your own threads are finished when the main thread
        exits the script, or strange effects can occur.
        You can use the .NET System.Threading or the python threading module to create new
        threads.

        :version added: 3.5.1.0

        :type code: :class:`PieceOfCode`
        :param code: The code to execute. A python function, which will be called without
            parameters, and should not return any value.

        :type async: bool
        :param async: If true, this method returns immediately, otherwise the this
            method returns after the delegate has been finished.

        """
        pass

    def get_message_objects(self, category=None, severities=0xFFFFFFFF):
        """Gets all messages of a given category and severity which are currently in the store.

        :version added: 3.5.2.0

        :type category: Guid or str
        :param category: The category Guid (defaults to the ScriptMessage category).

        :type severities: :class:`Severity`
        :param severities: The severities (This can be a combination of several severity flags).
            By default, all severities are returned.

        :rtype: list
        :returns: The list of message texts.

        """
        pass

    def get_message_categories(self, bActive=True):
        """Gets all message categories.

        :version added: 3.5.2.0

        :type bActive: bool
        :param bActive: If set to ``True`` (the default), only the active ones (those
            which had at least one message since the current codesys instance was started) are
            returned. If set to false, all categories existing in the current installation are
            returned.

        :rtype: list[Guid]
        :returns: A list of guids.

        """
        pass

    def get_message_category_description(self, category):
        """Gets a description for the specified message category.

        :version added: 3.5.2.0

        :type category: Guid
        :param category: The category.

        :rtype: str
        :returns: The description of that message category.

        """
        pass

    def clear_messages(self, category):
        """Clears the specified category.

        :version added: 3.5.2.0

        :type category: Guid

        """
        pass

    @property
    def abortable(self):
        """Whether the script is abortable.

        Since V3.5.5.0, scripts are abortable by default. The
        user can abort the script by pressing the Cancel button in the progress display.
        This property controls whether this Cancel button is enabled.

        :version added: 3.5.5.0

        :rtype: bool

        """
        pass

    @abortable.setter
    def abortable(self, value: bool):
        pass

    @property
    def abort_autocheck(self):
        """Gets or sets a value indicating whether this script execution automatically checks for aborts.

        If this property is set to True (the default value), the script engine
        uses the python tracing functionality to check for aborts after every line of
        executed python code, and throws an KeyboardInterruptException if aborted.
        You can disable this automatic checks by setting this
        property to false. Certain debuggin modes also disable this check.

        :version added: 3.5.5.0

        :rtype: bool

        """
        pass

    @abort_autocheck.setter
    def abort_autocheck(self, value: bool):
        pass

    @property
    def aborting(self):
        """Gets a value indicating whether this System is aborting.

        This property gets set to true once the user presses an enabled "Cancel" button on
        the progress display, and it cannot be reset by the script. Use this property for
        explicit abortion checks when you disabled :attr:`abort_autocheck`.

        :version added: 3.5.5.0

        :rtype: bool

        """
        pass

    def progress_start(self, description, items=-1, unit=""):
        """Starts the progress information for a specific subtask.

        :version added: 3.5.5.0

        :type description: str
        :param description: The description of the subtask.

        :type items: int
        :param items: The number of items, if known in advance.

        :type unit: str
        :param unit: The unit of items, for example objects or lines.

        """
        pass

    def progress_step(self, item, completed=1):
        """Advances the progress of the current subtask.

        :version added: 3.5.5.0

        :type item: str
        :param item: The item which is currently completed.

        :type completed: int
        :param completed: The number of items completed in this step.

        """
        pass

    def progress_absolute(self, item, absolute_progress):
        """Advances the progress of the current subtask.

        :version added: 3.5.5.0

        :type item: str
        :param item: The item which is currently completed.

        :type absolute_progress: int
        :param absolute_progress: The total number of items completed so far.

        """
        pass

    @property
    def background_loading_of_libraries_finished(self):
        """Is the background loading of libraries finished?

        :version added: 3.5.15.0

        :rtype: bool

        """
        pass


class ScriptMessage(object):
    """Represents a message from the message storage."""

    @property
    def project(self):
        """The the project of the message position.

        If this message does not have a position, None is returned.

        :rtype: :class:`ScriptProject`

        """
        pass

    @property
    def object(self):
        """The object of the message position.

        If this message does not have a position, None is returned.

        :rtype: :class:`ScriptObject`

        """
        pass

    @property
    def position(self):
        """The position within the database object of the message position.

        The interpretation of this number is handled privately by the
        object. To get a user-friendly display text for this position, the
        :attr:`position_text` property must be called.
        If this message does not have a position, 0 is returned.

        :rtype: long

        """
        pass

    @property
    def position_text(self):
        """The user-friendly display text for position within the database object of the message position.

        The interpretation of this number is handled privately by the
        object. If this message does not have a position, None is returned.

        :rtype: str

        """
        pass

    @property
    def position_offset(self):
        """Gets an additional character offset to the position returned by the :attr:`position` property.

        :rtype: short

        """
        pass

    @property
    def length(self):
        """Gets length of Position.

        :rtype: int

        """
        pass

    @property
    def text(self):
        """Gets the message text.

        :rtype: str

        """
        pass

    @property
    def severity(self):
        """Gets the severity of this message.

        :rtype: Severity

        """
        pass

    @property
    def FontColor(self):
        """Gets the color of the message text, or :attr:`System.Drawing.Color.Empty` if the default color is defined.

        :rtype: Color

        """
        pass

    @property
    def has_details_handler(self):
        """Gets a value indicating whether this :class:`ScriptMessage` has a details handler.

        This is visually indicated by a [...]-Button in the message view.

        :rtype: bool

        """
        pass

    def call_details_handler(self):
        """Calls the details handler of this message (this will usually open a popup or similar)."""
        pass

    @property
    def icon(self):
        """Specialized Icon. If ``None``, the icon is set according to the severity.

        :rtype: Icon

        """
        pass

    @property
    def number(self):
        """Unambigous number identifying the message according to its category.

        Together with the :attr:`prefix`, the number identifies the message. compile, LINT, IO-Config, etc.
        None is returned if not used.

        :rtype: int or None

        """
        pass

    @property
    def prefix(self):
        """A prefix string identifying the message category (compile, LINT, IO-Config, etc).

        Together with the :attr:`number`, the message is unambigously identified. None is
        returned if not used.

        :rtype: str

        """
        pass


def PieceOfCode(self):
    """Delegate for a parameterless function without return value."""
    pass


class ScriptUI(object):
    """The script can interact with the user via this instance.

    Please note that some of the functionalities depend on the currently installed
    MessageService instance.

    In --noUI-Mode (console-only mode), a basic, somehow restricted implementation querying the
    user via text input is provided instead. Especially multi-line input is not user friendly,
    and store_key or predefined values for text input do not work. But as --noUI-Mode is primarily
    meant for unattended batch execution, it is a bad idea to ask the user in general.

    """

    def error(self, message, message_key="ScriptMessage", arguments=None):
        """Reports an error message to the user. This method blocks until the user has acknowledged this message.

        :type message: str
        :param message: The message to display the user.

        :type message_key: str
        :param message_key: The message key, for automated filtering / handling by
            prompt_answers or similar mechanism by other plugins (e. G. automated test tools). Most
            users can leave the default here.

        :type arguments: tuple[object]
        :param arguments: Optional objects which build the variable part of the message.
            In other words, if ``message`` is build via a string formatting
            operation, the arguments of that formatting operation should be passed as ``arguments``
            here. This is for advanced usages via automated test tools, most
            users can ignore it.

        """
        pass

    def warning(self, message, message_key="ScriptMessage", arguments=None):
        """Reports an warning message to the user.

        This method blocks until the user has acknowledged this message.

        :type message: str
        :param message: The message to display the user.

        :type message_key: str
        :param message_key: The message key, for automated filtering / handling by
            prompt_answers or similar mechanism by other plugins (e. G. automated test tools). Most
            users can leave the default here.

        :type arguments: tuple[object]
        :param arguments: Optional objects which build the variable part of the message.
            In other words, if ``message`` is build via a string formatting
            operation, the arguments of that formatting operation should be passed as ``arguments``
            here. This is for advanced usages via automated test tools, most
            users can ignore it.

        """
        pass

    def info(self, message, message_key="ScriptMessage", arguments=None):
        """Reports an informational message to the user.

        This method blocks until the user has acknowledged this message.

        :type message: str
        :param message: The message to display the user.

        :type message_key: str
        :param message_key: The message key, for automated filtering / handling by
            prompt_answers or similar mechanism by other plugins (e. G. automated test tools). Most
            users can leave the default here.

        :type arguments: tuple[object]
        :param arguments: Optional objects which build the variable part of the message.
            In other words, if ``message`` is build via a string formatting
            operation, the arguments of that formatting operation should be passed as ``arguments``
            here. This is for advanced usages via automated test tools, most
            users can ignore it.

        """
        pass

    def prompt(self, message, choice, default_result, store_description=None, store_key=None,
               message_key="ScriptMessage", arguments=None):
        """Prompts the user.

        This method blocks until the user has answered the question.

        This method allows the user to store his/her answer. The next time the same question is
        prompted to the user by this method, the method immediately returns with the stored
        result.
        See also: :meth:`reset_stored_result`

        :type message: str
        :param message: The message to display.

        :type choice: :class:`PromptChoice`
        :param choice: The answers the user can chose from.

        :type default_result: :class:`PromptResult`
        :param default_result: The default answer which is displayed to the user
            in a highlighted manner.

        :type store_description: str
        :param store_description: The text which is displayed next to the control where the user
            can decide that (s)he does not want to see that question again (e.g. "Do not show this
            message again", or "Apply for all objects"). This is optional, but you must supply
            either both ``store_description`` and ``store_key`` or none of them.

        :type store_key: str
        :param store_key: A non-``None`` caller-specific key with which the
            prompt can be identified.
            This is optional, but you must supply either both
            ``store_description`` and ``store_key`` or none of them.

        :type message_key: str
        :param message_key: The message key, for automated filtering / handling by
            :attr:`System.prompt_answers` or similar mechanism by other
            plugins (e. G. automated test tools). Most users can leave the default here.

        :type arguments: str
        :param arguments: Optional objects which build the variable part of the message.
            In other words, if ``message`` is build via a string formatting
            operation, the arguments of that formatting operation should be passed as ``arguments``
            here. This is for advanced usages via automated test tools, most
            users can ignore it.

        :rtype: :class:`PromptResult`
        :returns: The answer provided by the user.

        """
        pass

    def select_many(self, message, choice, result, items, message_key="ScriptMessage", *arguments):
        """Prompts the user, allowing the user to select items for which to apply the answer.

        This method blocks until the user has answered the question.

        This method allows the user to store his/her answer. The next time the same question is prompted to the user by this
        method, the method immediately returns with the stored result.

        :type message: str
        :param message: The message to display.

        :type choice: :class:`PromptChoice`
        :param choice: The answers the user can chose from.

        :type result: :class:`PromptResult`
        :param result: The result.

        :type items: list
        :param items: An array containing items which are selectable for the user. The objects'
            ``ToString`` methods are used to get the string to display.

        :type message_key: str
        :param message_key: The message key, for automated filtering / handling by
            :attr:`System.prompt_answers` or similar mechanism by other
            plugins (e. G. automated test tools). Most users can leave the default here.

        :type arguments: str
        :param arguments: Optional objects which build the variable part of the message.
            In other words, if ``message`` is build via a string formatting
            operation, the arguments of that formatting operation should be passed as ``arguments``
            here. This is for advanced usages via automated test tools, most
            users can ignore it.

        :rtype: list
        :returns: A python tuple containing of the PromptResult as the first item, list of booleans
            in parallel to``items`` as second item, and a (possibly empty) sequence of the selected
            objects as third item.

        """
        pass

    def choose(self, message, options, initial_selection=0, cancellable=True,
               message_key="ScriptMessage", *arguments):
        """Lets the user choose one of several listed items.

        :type message: str
        :param message: The message to display.

        :type options: list
        :param options: A list of options to display.
            The objects will be converted to string to show them to the user.

        :type initial_selection: int
        :param initial_selection: The index of the initially selected object of the list.

        :type cancellable: bool
        :param cancellable: if set to ``true``, the user can cancel / abort the dialog.

        :type message_key: str
        :param message_key: The message key, for automated filtering / handling by
            :attr:`System.prompt_answers` or similar mechanism by other
            plugins (e. G. automated test tools). Most users can leave the default here.

        :type arguments: str
        :param arguments: Optional objects which build the variable part of the message.
            In other words, if ``message`` is build via a string formatting
            operation, the arguments of that formatting operation should be passed as ``arguments``
            here. This is for advanced usages via automated test tools, most
            users can ignore it.

        :rtype: list
        :returns: A python tuple containing the index of the selected item, or -1 if
            ``cancellable`` was set to True and the user cancelled the dialog as the first item,
            and the selected item or None as the second item.

        """
        pass

    def reset_stored_result(self, store_key):
        """Resets any prompt results stored by :meth:`prompt` or :meth:`select_many`.

        :type store_key: str
        :param store_key: A non-``None`` caller-specific key with which the prompt
            can be identified.

        """
        pass

    def open_file_dialog(self, title=None, filename=None, directory=None, filter=None,
                         filter_index=None, default_extension=None, stateguid=None, multiselect=False,
                         check_file_exists=True, check_path_exists=True):
        """Displays an "Open File" dialog.

        This method is currently not processed by :attr:`System.prompt_answers`.

        In --NoUI-Mode, the user simply can enter a path here.

        The "filter" string is a list of descriptions and pattern lists,
        separated by a pipe symbol ('|'). The pattern list uses the glob syntax,
        and is separated by a semicolon (';'). For example:
        ``Text files (*.txt)|*.txt|Image Files(*.BMP;*.JPG;*.GIF)|*.BMP;*.JPG;*.GIF|All files (*.*)|*.*``

        :type title: str
        :param title: The title of the dialog window, if you don't pass it, a generic
            "Python Script: Open File" like text will be displayed.

        :type filename: str
        :param filename: The initially selected filename.

        :type directory: str
        :param directory: The directory initially displayed. Default is None, which uses the
            current directory.

        :type filter: str
        :param filter: The list of valid extension filters.

        :type filter_index: str
        :param filter_index: Index of the filter which is active when the user opens the dialog.
            This index is 1-based.

        :type default_extension: str
        :param default_extension: The default extension which is added to the filename if the
            user does not add an extension, and the active filter does not specify one.

        :type stateguid: Guid
        :param stateguid: This GUID is used to store the state inside the CoDeSys configuration
            space when the user closes the Dialog with "ok", and will be used to restore the state
            when the next dialog is opened with the same guid.

        :type multiselect: bool
        :param multiselect: if set to ``True``, the user may select multiple files.

        :type check_file_exists: bool
        :param check_file_exists: if set to ``True``, the dialog displays a warning if the user
            enters a file which does not exist.

        :type check_path_exists: bool
        :param check_path_exists: if set to ``True``, the dialog displays a warning if the user
            enters a path which does not exist.

        :rtype: obj
        :returns: The path for the selected file, or a list of pathes if multiselect is allowed,
            or None if the user cancelled the dialog.

        """
        pass

    def save_file_dialog(self, title=None, filename=None, directory=None, filter=None,
                         filter_index=None, default_extension=None, stateguid=None, check_file_exists=True,
                         check_path_exists=True, check_overwrite=True, check_create=False):
        """Displays a "Save File" dialog.

        This method is currently not processed by :attr:`System.prompt_answers`.

        In --NoUI-Mode, the user simply can enter a path here.

        The "filter" string is a list of descriptions and pattern lists,
        separated by a pipe symbol ('|'). The pattern list uses the glob syntax,
        and is separated by a semicolon (';'). For example:
        ``Text files (*.txt)|*.txt|Image Files(*.BMP;*.JPG;*.GIF)|*.BMP;*.JPG;*.GIF|All files (*.*)|*.*``

        :type title: str
        :param title: The title of the dialog window, if you don't pass it, a generic
            "Python Script: Save File" like text will be displayed.

        :type filename: str
        :param filename: The initially selected filename.

        :type directory: str
        :param directory: The directory initially displayed. Default is None, which uses the
            current directory.

        :type filter: str
        :param filter: The list of valid extension filters.

        :type filter_index: str
        :param filter_index: Index of the filter which is active when the user opens the dialog.
            This index is 1-based.

        :type default_extension: str
        :param default_extension: The default extension which is added to the filename if the
            user does not add an extension, and the active filter does not specify one.

        :type stateguid: Guid
        :param stateguid: This GUID is used to store the state inside the CoDeSys configuration
            space when the user closes the Dialog with "ok", and will be used to restore the state
            when the next dialog is opened with the same guid.

        :type check_file_exists: bool
        :param check_file_exists: if set to ``True``, the dialog displays a warning if the user
            enters a file which does not exist.

        :type check_path_exists: bool
        :param check_path_exists: if set to ``True``, the dialog displays a warning if the user
            enters a path which does not exist.

        :type check_overwrite: bool
        :param check_overwrite: if set to ``True``, the dialog displays a warning if the user
            selection will overwrite an existing file.

        :type check_create: bool
        :param check_create: if set to ``True`` [check_create].

        :rtype: str
        :returns: The path for the selected file, or None if the user cancelled the dialog.

        """
        pass

    def browse_directory_dialog(self, message, path="",
                                root_folder="Environment.SpecialFolder.MyComputer", new_folder_button=True):
        """Opens a browse directory dialog.

        This method is currently not processed by :attr:`System.prompt_answers`.

        In --NoUI-Mode, the user simply can enter a path here.

        The microsoft documentation for the root folder says: "Only the specified folder and any
        subfolders that are beneath it will appear in the dialog box and be selectable. The
        SelectedPath property, along with RootFolder, determines what the selected folder will
        be when the dialog box is displayed, as long as SelectedPath is an absolute path that is
        a subfolder of RootFolder (or more accurately, points to a subfolder of the shell
        namespace represented by RootFolder)."

        :type message: str
        :param message: The message to display.

        :type path: str
        :param path: The path to be preselected when the dialog opens.

        :type root_folder: Environment.SpecialFolder
        :param root_folder: The root folder for the browsing dialog.

        :type new_folder_button: bool
        :param new_folder_button: if set to ``True``, a button which allows the users
            to create new folders appears in the dialog box.

        :rtype: str
        :returns: The path for the selected directory, or None if the user cancelled the dialog.

        """
        pass

    def query_string(self, message="", text="", multi_line=False, cancellable=False):
        """Queries the user to input or edit a text string.

        This method is currently not processed by :attr:`System.prompt_answers`.

        :type message: str
        :param message: The message to display for the user.

        :type text: str
        :param text: The text to be prefilled in the textbox.

        :type multi_line: bool
        :param multi_line: if set to ``True``, the user can enter a multiline text.

        :type cancellable: bool
        :param cancellable: if set to ``True``, the user can cancel / abort the dialog.

        :rtype: str
        :returns: The entered string, or None if the user cancelled the dialog.

        """
        pass

    def query_password(self, message="", password="", cancellable=False):
        """Queries the user to input a password.

        This method is currently not processed by :attr:`System.prompt_answers`.

        :type message: str
        :param message: The message to display for the user.

        :type password: str
        :param password: The password to be prefilled in the textbox.

        :type cancellable: bool
        :param cancellable: if set to ``True``, the user can cancel / abort the dialog.

        :rtype: str
        :returns: The entered password, or None if the user cancelled the dialog.

        """
        pass

    def query_credentials(self, message="", username="", password="", cancellable=False):
        """Queries the user to input a password.

        This method is currently not processed by :attr:`System.prompt_answers`.

        :type message: str
        :param message: The message to display for the user.

        :type username: str
        :param username: The username to be prefilled in the textbox.

        :type password: str
        :param password: The password to be prefilled in the textbox.

        :type cancellable: bool
        :param cancellable: if set to ``True``, the user can cancel / abort the dialog.

        :rtype: list
        :returns: A tuple containing the username and password,
            or None if the user did cancel the dialog.

        """
        pass


def MultipleChoiceSelector(self, choices):
    """Delegate for selecting one of multiple choices for simulating interactive user input via system.promt_answers.

    Script authors have to cast their delegates to this type by wrapping them via a
    call to MultipleChoiceSelector().

    Example::
        def MyFilter(choice):

            return choice in ("erste", "zweite", "dritte")

        system.prompt_answers["my message key"] = PromptChoiceFilter(MyFilter)

    :type choices: list[str]
    :param choices: The choices.

    :rtype: int
    :returns: The index of the accepted choice.

    """
    pass


class ScriptCommand(object):
    """Represents a CoDeSys command (Menu, Toolbar, Context Menu)."""

    @property
    def name(self):
        """Gets the display text of this command. This string is used as menu item label and usually is localized.

        :rtype: str

        """
        pass

    @property
    def description(self):
        """Gets the description for this command. This string is used as statusbar text and usually is localized.

        :rtype: str

        """
        pass

    @property
    def tokens(self):
        """Gets the tokens which introduce a corresponding batch instruction.

        For example, a batch command which opens a project file would probably return the two tokens "file" and
        "open" here.

        :rtype: list[str]

        """
        pass

    @property
    def guid(self):
        """Gets the GUID.

        :rtype: Guid

        """
        pass


class ScriptCommands(list):
    """A sequence of all known Commands in CoDeSys."""

    def __getitem__(self, tokens):
        """Searches a specific command by its tokens.

        :type tokens: list[str]
        :param tokens: The command tokens (either separated by space, or a list of strings
            containing one token each), or the string representation of the command Guid.

        :raises KeyNotFoundException: Thrown if no command with the given tokens was found.

        :rtype: :class:`ScriptCommand`
        :returns: The command.

        """
        pass


class ScriptObjectFactory(object):
    """An Object factory."""

    @property
    def guid(self):
        """Gets the GUID of the object factory.

        :rtype: Guid

        """
        pass

    @property
    def object_type(self):
        """Gets the guid of the produced object type.

        :rtype: Guid

        """
        pass

    @property
    def object_namespace(self):
        """Gets a GUID identifying the namespace the created object will belong to.

        :rtype: Guid

        """
        pass

    @property
    def name(self):
        """Gets the display text of this object factory. This string should be localized.

        :rtype: str

        """
        pass

    @property
    def description(self):
        """Gets the description for this object factory. This string should be localized.

        :rtype: str

        """
        pass


class ScriptObjectFactories(list):
    """A sequence of all known object factories."""

    def __getitem__(self, factory_guid):
        """Searches for an object factory by its guid.

        :type factory_guid: Guid
        :param factory_guid: The factory Guid.

        :rtype: :class:`ScriptObjectFactory`

        """
        pass

    def search_factories_for(self, typeguid):
        """Returns all known object factories for a given object type.

        The list is ordered, so that perfect matches (which produce exactly the queried type)
        come before factories which produce subclasses of the queried type. For object permission
        management, permissions are tested for the first factory of that list which produces that
        actual type.

        :type typeguid: Guid
        :param typeguid: The typeguid

        :rtype: list
        :returns: A (possibly empty) sequence of object factories.

        """
        pass
