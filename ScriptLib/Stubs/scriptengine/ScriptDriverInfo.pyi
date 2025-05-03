from enum import Enum
from .dotNETs import *
from .ScriptApplication import *
from .ScriptDeviceObject import *
from .ScriptObject import *


class AlwaysUpdateVariablesMode(Enum):
    """Defines always mapping modes on a parameter or connectors."""

    Disabled = 1
    """Disable the always update of the variables."""

    OnlyIfUnused = 2
    """The io channel is mapped in the bus cycle task if no other task is using it.
    If it used in an task then alwaysmapping is ignored, because it is updated in the used task
    only.

    """

    AlwaysInBusCycle = 3
    """The io channel is always updated in the bus cycle task independent of the real task usage.
    Therefore task consistency is not guaranteed.

    """


class ScriptDriverInfo(object):
    """Provides access to the driver info of the device.

    Mostly the visible parts of the tab "PLC Settings" in the device editor.

    """

    @property
    def can_set_io_application(self):
        """Whether the IO application can be set.

        :rtype: bool

        """
        pass

    @property
    def io_application(self):
        """Get/set the object Guid of the application which does the IO handling.

        :rtype: Guid

        """
        pass

    @io_application.setter
    def io_application(self, value: Guid):
        pass

    def set_io_application(self, application):
        """Set the application which does the IO handling.

        :type application: :class:`ScriptApplication`
        :param application: Script object of the application.

        """
        pass

    @property
    def update_ios_while_in_stop(self):
        """Update IOs while in stop.

        :rtype: bool

        """
        pass

    @update_ios_while_in_stop.setter
    def update_ios_while_in_stop(self, value: bool):
        pass

    @property
    def behaviour_for_outputs_on_stop(self):
        """Get/set the behaviour for outputs on stop.

        :rtype: :class:`StopResetBehaviour`

        """
        pass

    @behaviour_for_outputs_on_stop.setter
    def behaviour_for_outputs_on_stop(self, value: StopResetBehaviour):
        pass

    @property
    def user_program_for_stop_reset_behaviour(self):
        """Get/set the behaviour program for stop/reset if :attr:`behaviour_for_outputs_on_stop` is set to ``ExecuteProgram``.

        See also: StopResetBehaviour.ExecuteProgram

        :rtype: str

        """
        pass

    @user_program_for_stop_reset_behaviour.setter
    def user_program_for_stop_reset_behaviour(self, value: str):
        pass

    @property
    def always_update_variables(self):
        """Set the mode for (always) updating variables.

        :rtype: :class:`AlwaysUpdateVariablesMode`

        """
        pass

    @always_update_variables.setter
    def always_update_variables(self, value: AlwaysUpdateVariablesMode):
        pass

    @property
    def bus_cycle_task_by_name(self):
        """Get the name of the bus cycle task.

        :rtype: str

        """
        pass

    @property
    def bus_cycle_task_by_guid(self):
        """Get the object guid of the bus cycle task.

        :rtype: Guid

        """
        pass

    def set_bus_cycle_task(self, name: str):
        """Set the bus cycle task by name or object guid or script object.

        :type name: str
        :param name: Name of the task.

        """
        pass

    def set_bus_cycle_task(self, object_guid: Guid):
        """Set the bus cycle task by name or object guid or script object.

        :type guid: Guid
        :param guid: Object Guid of the task.

        """
        pass

    def set_bus_cycle_task(self, task: ScriptObject):
        """Set the bus cycle task by name or object guid or script object.

        :type task: :class:`ScriptObject`
        :param task: Script Object of the task.

        """
        pass

    @property
    def generate_force_variables(self):
        """Generate force variables for IO mapping.

        :rtype: bool

        """
        pass

    @generate_force_variables.setter
    def generate_force_variables(self, value: bool):
        pass

    @property
    def enable_diagnosis(self):
        """Enable diagnosis for devices.

        :rtype: bool

        """
        pass

    @enable_diagnosis.setter
    def enable_diagnosis(self, value: bool):
        pass

    @property
    def show_io_warnings_as_errors(self):
        """Show IO warnings as errors.

        :rtype: bool

        """
        pass

    @show_io_warnings_as_errors.setter
    def show_io_warnings_as_errors(self, value: bool):
        pass
