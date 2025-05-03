from dotNETs import *
from TriggerState import *
from PacketState import *

class ScriptTraceEditorObject(object):
	"""
	| Represents a open trace editor, used to perform online actions on a trace.
	
	"""
	
	@property
	def is_online(self) -> bool:
		"""
		| Check if the application for the trace is online.
		
		"""
		pass
	
	@property
	def is_logged_in(self) -> bool:
		"""
		| Check if the trace is logged in.
		
		"""
		pass
	
	@property
	def is_running(self) -> bool:
		"""
		| Check if the trace is currently running.
		
		"""
		pass
	
	
	def download(self) -> None:
		"""
		| Download a trace to the device. After this call the trace will be logged in.
		
		:exception: 
		This is exception is throw if the trace can not be downloaded, because it is either a device trace, not online or contains no variables.
		
		"""
		pass
	
	def start(self) -> None:
		"""
		| Start the recording of a downloaded trace
		
		:exception: 
		This exception is thrown if the trace can not be started, because tt is not logged in, is is already running or stopped on a trigger.
		
		"""
		pass
	
	def stop(self) -> None:
		"""
		| Stop the recording of a downloaded trace
		
		:exception: 
		This exception is thrown if the trace can not be stopped, because it is not logged in, is is not running or stopped on a trigger.
		
		"""
		pass
	
	def save(self, file_name: str) -> None:
		"""
		| Save the data of the trace to a file. If the file already exists it is overwriten.
		| The format of the file depends on the fileextension.
		
		:type file_name: str
		:param file_name: 
		Allowed formats are
		*.txt Text file
		*.csv CSV file(data only)
		*.trace Trace file
		
		:exception: 
		This exception is thrown if the trace can not be saved, because it is a device trace.
		
		"""
		pass
	
	def get_trigger_state(self) -> TriggerState:
		"""
		| Returns information about the trigger while the trace is currently running.
		
		:exception: 
		This exception is thrown if the trace has not be downloaded to the device,
		
		"""
		pass
	
	def get_trigger_timestamp(self) -> int:
		"""
		| Returns the (absolute) timestamp of the last trigger event. The resolution is ms or µs, depending on the resolution of the trace.
		
		:exception: 
		This exception is thrown if the trace has not be downloaded to the device,
		
		"""
		pass
	
	def get_trigger_startdate(self) -> DateTime:
		"""
		| Returns the date of the last trigger event in UTC.
		
		:exception: 
		This exception is thrown if the trace has not be downloaded to the device,
		
		"""
		pass
	
	def get_packet_state(self) -> PacketState:
		"""
		| Returns information about the trace packet in the runtime.
		
		:exception: 
		This exception is thrown if the trace has not be downloaded to the device,
		
		"""
		pass
	
	def get_trace_start_timestamp(self) -> int:
		"""
		| Returns the (absolute) timestamp when the packet was started.The resolution is ms or µs, depending on the resolution of the trace.
		
		:exception: 
		This exception is thrown if the trace has not be downloaded to the device,
		
		"""
		pass
	
	def reset_trigger(self) -> None:
		"""
		| Resets the trigger and causes that the trace is running again
		
		"""
		pass
	
	def get_online_traces(self) -> list[str]:
		"""
		| Returns a list of strings with the packet names of trace, that are currently online.
		
		:rtype: list[str]
		:returns: See summary
		
		"""
		pass
	
	def upload_to_device_trace(self, stPacketName: str) -> None:
		"""
		| Uploads the given trace packet to the currently open device trace editor.
		
		:type stPacketName: str
		:param stPacketName: The name of the trace packet to upload
		
		"""
		pass