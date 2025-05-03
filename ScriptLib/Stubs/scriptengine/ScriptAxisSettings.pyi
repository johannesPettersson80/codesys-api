from ScriptFontDesc import *
from AxisScaleMode import *


class ScriptAxisSettings(object):
	"""
	| Bundles settings of the x-axis of a traceObject or the y-axis of a diagram.
	
	"""
	
	@property
	def mode(self) -> AxisScaleMode:
		"""
		| Scale mode of the axis. Possible values and their behaviours are:
		| Auto: the axis range is determined based on the range of the data.
		| FixedLength: the length of the range is fixed, but the position is based on the data.
		| Fixed: The axis range is explicitly given.
		
		"""
		pass
	
	@property
	def min_val(self) -> float:
		"""
		| Gets or sets the minimum value of the axis range.
		| This is only used, if mode == Fixed.
		| For the time axis, the resolution is ms.
		
		"""
		pass
	
	@property
	def max_val(self) -> float:
		"""
		| Gets or sets the maximum value of the axis range.
		| This is only used, if mode == Fixed.
		| For the time axis, the resolution is ms.
		
		"""
		pass
	
	@property
	def range(self) -> float:
		"""
		| Gets or sets the range of the axis.
		| This is only used, if mode == FixedLength.
		| For the time axis, the resolution is ms.
		
		"""
		pass
	
	@property
	def draw_description(self) -> bool:
		"""
		| Gets or sets wether the description text is drawn.
		
		"""
		pass
	
	@property
	def description(self) -> str:
		"""
		| Gets or sets the description text.
		
		"""
		pass
	
	@property
	def color(self) -> int:
		"""
		| Gets or sets the 32bit-ARGB representation of the color, used to draw the axis, tick marks, and labels.
		
		"""
		pass
	
	@property
	def font(self) -> ScriptFontDesc:
		"""
		| Contains settings for font, used for the label and axis descriptions.
		
		"""
		pass
	
	@property
	def draw_grid(self) -> bool:
		"""
		| Gets or sets, wether the grid is drawn.
		
		"""
		pass
	
	@property
	def grid_color(self) -> int:
		"""
		| Gets or sets the 32bit-ARGB representation of the color, used to draw the grid lines of the major tick.
		
		"""
		pass
	
	@property
	def tickmark_fixed_spacing(self) -> bool:
		"""
		| Gets or sets, wether a fixed spacing is used for the tick marks.
		
		"""
		pass
	
	@property
	def tickmark_fixed_distance(self) -> float:
		"""
		| Gets or sets the distance of major tick marks, if tickmark_fixed_spacing is true.
		| For the time axis, the resolution is ms.
		
		"""
		pass
	
	@property
	def tickmark_fixed_subdivisions(self) -> int:
		"""
		| Gets or sets the number of subdivisions of a major tick mark, if tickmark_fixed_spacing is true.
		
		"""
		pass
	
	
	def copy_from(self, source: ScriptAxisSettings) -> None:
		"""
		| Convenient method for copying all properties, accessable by scripting, from the source to this ScriptAxisSettings.
		
		"""
		pass