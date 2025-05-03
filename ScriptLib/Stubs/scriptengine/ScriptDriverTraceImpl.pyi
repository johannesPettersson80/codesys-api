from IScriptTraceObjectMarker import *
from ScriptObject import *


class ScriptDriverTraceImpl(object):
	"""
	| Top level "trace" API. Offers actions, independent of concrete trace objects.
	
	"""
	
	def create(self, parentObject: IScriptObject, traceName: str, taskName: str="") -> IScriptTraceObjectMarker:
		"""
		| Creates an empty trace object in the given project/application or project/device.
		| The Task of the trace object is set, if a task with the given taskname exists.
		
		"""
		pass