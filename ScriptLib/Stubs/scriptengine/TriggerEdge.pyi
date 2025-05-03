from enum import Enum


class TriggerEdge(Enum):
	"""
	| Describes the way of trigger detection.
	
	"""
	
	Undefined = 0
	"""
	| No trigger edge defined.
	
	"""
	
	Positive = 1
	"""
	| Positive trigger edge.
	
	"""
	
	Negative = 2
	"""
	| Negative trigger edge.
	
	"""
	
	Both = 3
	"""
	| Detect positive and negative trigger edges.
	
	"""