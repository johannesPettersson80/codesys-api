from enum import Enum


class GraphType(Enum):
	"""
	| Used for ScriptTraceVariable.graph_type. Defines the appearence of a variable in the diagram.
	
	"""
	
	NOTYPE = 0
	"""
	| None.
	
	"""
	
	LINES_POINTS = 1
	"""
	| Line with Points.
	
	"""
	
	CROSSES = 2
	"""
	| No Line, only Crosses.
	
	"""
	
	CURVES = 3
	"""
	| Splines (no longer supported).
	
	"""
	
	STEPS_POINTS = 4
	"""
	| Step with Points.
	
	"""
	
	POINTS = 5
	"""
	| No Line, only Points.
	
	"""
	
	CIRCLE_CROSSES = 6
	"""
	| No Line, only Circles (no longer supported).
	
	"""
	
	BOXPOINTS = 7
	"""
	| No Line, only Boxes (no longer supported).
	
	"""
	
	LINES = 8
	"""
	| Lines only.
	
	"""
	
	STEPS = 9
	"""
	| Steps only.
	
	"""
	
	LINES_CROSSES = 10
	"""
	| Line with Crosses.
	
	"""
	
	STEPS_CROSSES = 11
	"""
	| Steps with Crosses.
	
	"""