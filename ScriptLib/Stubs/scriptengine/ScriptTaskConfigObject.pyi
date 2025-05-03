from enum import Enum
from .dotNETs import *


class KindOfTask(Enum):
    Cyclic = 1,
    Freewheeling = 2,
    Event = 3,
    ExternalEvent = 4,
    Status = 5,
    ParentSynchron = 6


class ScriptTaskConfigObjectMarker(object):
    """Every ScriptObject instance will be extended with this method.

    :version added: 3.5.10.0

    """

    @property
    def is_task_configuration(self):
        """Gets a value indicating whether this instance is a task configuration object.

        :rtype: bool
        :returns: ``True`` if this instance is task config object; otherwise, ``False``.

        """
        pass


class ScriptTaskObjectMarker(object):
    """Every ScriptObject instance will be extended with this method.

    :version added: 3.5.10.0

    """

    @property
    def is_task(self):
        """Gets a value indicating whether this instance is a task object.

        :rtype: bool
        :returns: ``True`` if this instance is task object; otherwise, ``False``

        """
        pass


class ScriptTaskConfigObject(ScriptTaskConfigObjectMarker):
    """Functionality for manipulating task configuration objects.

    :version added: 3.5.10.0

    """

    def create_task(self, name):
        """Add a task object to a task configuration.

        :type name: str

        :rtype: :class:`ScriptTaskObject`

        """
        pass


class ScriptTaskObject(ScriptTaskObjectMarker):
    """Functionality for manipulating task objects.

    :version added: 3.5.10.0

    """

    @property
    def name(self):
        """Name of the task.

        :rtype: str

        """
        pass

    @property
    def kind_of_task(self):
        """Kind of task.

        :rtype: KindOfTask

        """
        pass

    @kind_of_task.setter
    def kind_of_task(self, value: KindOfTask):
        pass

    @property
    def event_pou_guid(self):
        """Guid of POU for event.

        :rtype: Guid

        """
        pass

    @property
    def priority(self):
        """Priority of the task.

        :rtype: str

        """
        pass

    @priority.setter
    def priority(self, value: str):
        pass

    @property
    def interval(self):
        """Interval of the task.

        Requires the property :attr:`kind_of_task` to be set to KindOfTask.Cyclic
        or KindOfTask.ExternalEvent if the device supports it.

        :rtype: str

        """
        pass

    @interval.setter
    def interval(self, value: str):
        pass

    @property
    def interval_unit(self):
        """Unit used for the :attr:`interval`.

        Requires the property :attr:`kind_of_task` to be set to KindOfTask.Cyclic or KindOfTask.ExternalEvent if the device supports it.

        :rtype: str

        """
        pass

    @interval_unit.setter
    def interval_unit(self, value: str):
        pass

    @property
    def watchdog(self):
        """Settings for the watchdog of the task.

        :rtype: :class:`ScriptWatchdog`

        """
        pass

    @property
    def event(self):
        """Use event to trigger the task.

        Requires the property :attr:`kind_of_task` to be set to KindOfTask.Event
        or KindOfTask.Status.

        :rtype: str

        """
        pass

    @event.setter
    def event(self, value: str):
        pass

    @property
    def external_event(self):
        """Use external event to trigger the task.

        Requires the property :attr:`kind_of_task` to be set to KindOfTask.ExternalEvent.

        :rtype: str

        """
        pass

    @external_event.setter
    def external_event(self, value: str):
        pass

    @property
    def core_binding(self):
        """Core binding. On multicore deivce each task can have an optional core binding.

        :rtype: int

        """
        pass

    @core_binding.setter
    def core_binding(self, value: int):
        pass

    @property
    def parent_synchron_task(self):
        """Task of the device application which allows synchronous calls to child application in bus cycle.

        Requires the property :attr:`kind_of_task` to be set to KindOfTask.ParentSynchron.

        :rtype: str

        """
        pass

    @parent_synchron_task.setter
    def parent_synchron_task(self, value: str):
        pass

    @property
    def pous(self):
        """Collection of POUs which are executed by the task.

        :rtype: :class:`ScriptPouObjectCollection`

        """
        pass


class ScriptWatchdog(object):
    """A configuration for a watchdog.

    :version added: 3.5.10.0

    """

    @property
    def enabled(self):
        """Enable the watchdog for a task.

        :rtype: bool

        """
        pass

    @enabled.setter
    def enabled(self, value: bool):
        pass

    @property
    def time(self):
        """Time monitoring for a task.

        :rtype: str

        """
        pass

    @time.setter
    def time(self, value: str):
        pass

    @property
    def time_unit(self):
        """Unit user for the :attr:`time`.

        :rtype: str

        """
        pass

    @time_unit.setter
    def time_unit(self, value: str):
        pass

    @property
    def sensitivity(self):
        """Sensitivity of the watchdog.

        :rtype: str

        """
        pass

    @sensitivity.setter
    def sensitivity(self, value: str):
        pass


class ScriptPouObjectCollection(list):
    """A collection of POUs which are executed by a task.

    :version added: 3.5.10.0

    """

    def add(self, pou_name, comment=None):
        """Add a POU to the list.

        :type pou_name: str
        :param pou_name: Name of the POU.

        :type comment: str
        :param comment: Optional comment about this entry

        """
        pass

    def insert(self, index, pou_name, comment):
        """Insert a POU to the list at the specified index.

        :type index: int
        :param index: Index of a POU at which a new POU should be inserted.

        :type pou_name: str
        :param pou_name: Name of the POU.

        :type comment: str
        :param comment: Optional comment about this entry

        """
        pass

    def replace(self, index, pou_name, comment):
        """Replace the POU in the list at the specified index.

        :type index: int
        :param index: Index of a POU which should be replaced.

        :type pou_name: str
        :param pou_name: Name of the POU.

        :type comment: str
        :param comment: Optional comment about this entry

        """
        pass

    def remove(self, index_or_name):
        """Remove a POU from the list at the specified index OR: Remove the first POU with the specified name from the list.

        :type index_or_name: int or str
        :param index_or_name: Index or name of a POU which should be removed.

        """
        pass

    def __len__(self):
        """Gets the length.

        :rtype: int
        :returns: The number of POUs.

        """
        pass

    def __getitem__(self, index):
        """Gets the name and the comment of the entry at the specifed index as a python tuple.

        :type index: int
        :param index: Index of a POU.

        :rtype: tuple[str, str]
        :returns: Python tuple with the name and the comment of a POU.

        """
        pass
