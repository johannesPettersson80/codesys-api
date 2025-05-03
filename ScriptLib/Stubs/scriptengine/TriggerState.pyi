from enum import Enum


class TriggerState(Enum):
	"""
	| Flags field defining the state of the trigger of a trace packet in the runtime system.
	
	"""
	
	Disabled = 0
	"""
	| No trigger defined.
	
	"""
	
	Enabled = 1
	"""
	| Trigger defined.
	
	"""
	
	WaitForTrigger = 2
	"""
	| The trace packet currently records values and a trigger is defined.
	
	"""
	
	TriggerReached = 3
	"""
	| The packet has stopped recording because of the trigger condition.
	
	"""