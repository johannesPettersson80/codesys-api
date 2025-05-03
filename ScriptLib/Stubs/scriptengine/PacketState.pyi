from enum import Enum


class PacketState(Enum):
	"""
	
	"""
	
	NoConfig = 0
	"""
	| The configuration of a trace packet is incomplete
	
	"""
	
	Disabled = 1
	"""
	| The trace packet is currently disabled
	
	"""
	
	Enabled = 2
	"""
	| The trace packet is currently enabled
	
	"""
	
	Started = 3
	"""
	| The trace packet is recording values
	
	"""
	
	Stopped = 4
	"""
	| The recording is stopped
	
	"""