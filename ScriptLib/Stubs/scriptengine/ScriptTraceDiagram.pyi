from ScriptAxisSettings import *
from ScriptTraceDiagramVariableCollection import *
from ScriptTraceDiagramVariable import *
from ScriptTraceVariable import *


class ScriptTraceDiagram(object):
	"""
	| Contains the settings for a diagram of the trace.
	
	"""
	
	@property
	def background_color(self) -> int:
		"""
		| Gets or sets the 32bit-ARGB representation of the background color.
		
		"""
		pass
	
	@property
	def background_color_sel(self) -> int:
		"""
		| Gets or sets the 32bit-ARGB representation of the background color, used, while the diagram is selected.
		
		"""
		pass
	
	@property
	def y_axis(self) -> ScriptAxisSettings:
		"""
		| Bundled settings for the y axis.
		
		"""
		pass
	
	@property
	def variables(self) -> ScriptTraceDiagramVariableCollection:
		"""
		| The variables, used in this diagram.
		
		"""
		pass
	
	@property
	def name(self) -> str:
		"""
		| Gets or sets the name of the diagram.
		
		"""
		pass
	
	@property
	def can_rename(self) -> bool:
		"""
		| Gets wether the diagram can be renamed.
		
		"""
		pass
	
	@property
	def visible(self) -> bool:
		"""
		| Gets or sets wether die diagram is visible.
		
		"""
		pass
	
	
	def add_diagram_variable(self, variable: ScriptTraceVariable, visible: bool=True) -> ScriptTraceDiagramVariable:
		"""
		| Adds an existing ScriptTraceVariable with the given visibility to the diagram.
		
		:rtype: ScriptTraceDiagramVariable
		:returns: The created ScriptTraceDiagramVariable, which can be used to change the visibility of the variable in the diagram.
		
		"""
		pass