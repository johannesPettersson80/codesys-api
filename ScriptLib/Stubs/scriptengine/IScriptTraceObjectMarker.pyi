

class IScriptTraceObjectMarker(object):
	"""
	| This is added to every IScriptObject,
	| so the check wether it is a valid trace object can be executed on every IScriptObject.
	
	"""

	@property
	def is_trace_object(self) -> bool:
		"""
		| Wether the object is a valid trace object.
		"""
		pass