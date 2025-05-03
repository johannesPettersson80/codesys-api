from enum import Enum


class AxisScaleMode(Enum):
	"""
	| The possible scale modes of an axis.
	
	"""
	
	Auto = 0
	"""
	| The axis range is determined based on the range of the data
	| (For the time axis: the latest content of the runtime system
	| buffer, for y-axes: a range that is large enough to show all
	| values.)
	
	"""
	
	FixedLength = 1
	"""
	| The length of the axis range is given, but the position is
	| based on the the data.  Only valid for the time axis, where
	| the most recent data is shown with this option.
	
	"""
	
	Fixed = 2
	"""
	| The axis range is explicitly given.
	
	"""