

class ScriptTraceDiagramVariable(object):
	"""
	| Represents the connection between one ScriptTraceVariable and one ScriptTraceDiagram.
	| One ScriptTraceVariable can be used in multiple diagrams, and a diagram usually consists of multiple variables.
	
	"""
	
	@property
	def visible(self) -> bool:
		"""
		| Gets or sets the visibility of the variable in the diagram.
		
		"""
		pass