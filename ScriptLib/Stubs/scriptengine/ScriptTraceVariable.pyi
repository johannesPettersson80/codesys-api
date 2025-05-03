from GraphType import *


class ScriptTraceVariable(object):
	"""
	
	"""
	
	@property
	def variable_name(self) -> str:
		"""
		| Gets or sets the name of the variable. Must only contain ASCII characters.
		
		"""
		pass
	
	@property
	def graph_color(self) -> int:
		"""
		| Gets or sets the color of the graph. Expects the 32bit-ARGB color representation.
		
		"""
		pass
	
	@property
	def graph_type(self) -> GraphType:
		"""
		| Gets or sets the graph type, used to display the values.
		
		"""
		pass
	
	@property
	def max_warning_area(self) -> float:
		"""
		| Gets or sets the limit, above which values can be displayed using max_color, depending on activate_max_warning.
		
		"""
		pass
	
	@property
	def activate_max_warning(self) -> bool:
		"""
		| Gets or sets wether values above max_warning_area should be displayed using max_color.
		
		"""
		pass
	
	@property
	def max_color(self) -> int:
		"""
		| Gets or sets the graph color for values greater than max_warning_area. Expects the 32bit-ARGB color representation.
		
		"""
		pass
	
	@property
	def min_warning_area(self) -> float:
		"""
		| Gets or sets the limit, below which values can be displayed using min_color, depending on activate_min_warning.
		
		"""
		pass
	
	@property
	def activate_min_warning(self) -> bool:
		"""
		| Gets or sets wether values below min_warning_area should be displayed using min_color.
		
		"""
		pass
	
	@property
	def min_color(self) -> int:
		"""
		| Gets or sets the graph color for values less than min_warning_area. Expects the 32bit-ARGB color representation.
		
		"""
		pass
	
	@property
	def enabled(self) -> bool:
		"""
		| Indicates, whether the variable should be included in the trace recording.
		
		"""
		pass