from IScriptTraceObjectMarker import *
from TriggerEdge import *
from ScriptAxisSettings import *
from ScriptTraceDiagramCollection import *
from ScriptTraceVariableList import *
from ScriptTraceEditorObject import *


class ScriptTraceObject(IScriptTraceObjectMarker):
	"""
	| Represents one TraceObject.
	
	.. automethod:: __str__
	
	"""
	
	@property
	def is_trace_object(self) -> bool:
		"""
		| Wether the object is a valid trace object.
		"""
		pass
	
	@property
	def task_name(self) -> str:
		"""
		| The task in which the data is recorded.
		| Setting the task name is not allowed for the DeviceTrace.
		
		"""
		pass
	
	@property
	def record_name(self) -> str:
		"""
		| The name of the trace recording in the runtime.
		
		"""
		pass
	
	@property
	def trigger_enabled(self) -> bool:
		"""
		| Indicates whether a trigger condition has to be considered in the trace recording.
		
		"""
		pass
	
	@property
	def trigger_variable(self) -> str:
		"""
		| The trace signal that is used as a trigger. A complete instance path is required..
		
		"""
		pass
	
	@property
	def trigger_edge(self) -> TriggerEdge:
		"""
		| Defines the edge detection for triggering.
		
		"""
		pass
	
	@property
	def trigger_level(self) -> object:
		"""
		| Value that is reached to start the triggering. Any numeric types like int, ulong, double
		| (null represents the absence of a trigger level) are accepted.
		
		:exception: 
		This exception is thrown if the user tries to set the trigger level with an invalid type
		
		"""
		pass
	
	@property
	def post_trigger_samples(self) -> int:
		"""
		| Number of records per trace variable that are buffered after triggering.
		
		"""
		pass
	
	@property
	def resolution(self) -> Resolution:
		"""
		| Unit of measure for the time stamp that is recorded.
		
		"""
		pass
	
	@property
	def record_condition(self) -> str:
		"""
		| At runtime, the application checks the recording condition. If it is fulfilled, then the trace data is buffered.
		
		"""
		pass
	
	@property
	def comment(self) -> str:
		"""
		| The comment of the trace recording.
		
		"""
		pass
	
	@property
	def auto_start(self) -> bool:
		"""
		| Persistently saves the trace configuration and the last contents of the runtime buffer to the target device. After the device has been restarted, the trace is started automatically if the trigger has not occurred yet.
		
		"""
		pass
	
	@property
	def every_n_cycles(self) -> int:
		"""
		| Data is recorded in every n task cycle.
		
		"""
		pass
	
	@property
	def time_axis(self) -> ScriptAxisSettings:
		"""
		| Contains the configuration of the time axis.
		
		"""
		pass
	
	@property
	def diagrams(self) -> ScriptTraceDiagramCollection:
		"""
		| Not allowed for the DeviceTrace.
		
		"""
		pass
	
	@property
	def variable_list(self) -> ScriptTraceVariableList:
		"""
		| Not allowed for the DeviceTrace.
		
		"""
		pass
	
	
	def open_editor(self) -> ScriptTraceEditorObject:
		"""
		| Open the trace editor for this trace object.
		| This is required to perform online operations like starting, stopping and downloading traces.
		| If the editor is already open it is focused.
		| This method even works if no UI is displayed.
		
		:rtype: ScriptTraceEditorObject
		:returns: The trace editor.
		
		"""
		pass
	
	def __str__(self) -> str:
		"""
		
		"""
		pass