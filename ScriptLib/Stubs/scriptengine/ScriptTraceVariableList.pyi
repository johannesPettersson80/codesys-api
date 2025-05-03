from collections.abc import Iterable
from ScriptTraceVariable import *
from typing import overload


class ScriptTraceVariableList(list):
	"""
	| Provides functionality for the modification of the list of variables, traced by the corresponding ScriptTraceObject.
	
	.. automethod:: __iter__
	.. automethod:: __next__
	.. automethod:: __len__
	.. automethod:: __contains__
	.. automethod:: __getitem__
	
	"""
	
	def __iter__(self) -> Iterable[ScriptTraceVariable]:
		"""
		
		"""
		pass
	
	def __next__(self) -> ScriptTraceVariable:
		"""
		
		"""
		pass
	
	def add(self) -> ScriptTraceVariable:
		"""
		| Creates and adds a ScriptTraceVariable to the list. Returns the ScriptTraceVariale.
		| Not allowed for the variable list of the DeviceTrace.
		
		"""
		pass
	
	def __len__(self) -> int:
		"""
		| Returns the number of ScriptTraceVariables in this ScriptTraceVariableList.
		
		"""
		pass
	
	@overload
	def remove(self, index: int) -> None:
		"""
		
		"""
		pass
	
	@overload
	def remove(self, traceVariable: ScriptTraceVariable) -> None:
		"""
		| Removes the given ScriptTraceVariable from this ScriptTraceVariableList.
		
		"""
		pass
	
	def remove(self) -> None:
		"""
		| Removes the given ScriptTraceVariable from this ScriptTraceVariableList.
		
		"""
		pass
	
	def clear(self) -> None:
		"""
		| Removes all ScriptTraceVariables from this ScriptTraceVariableList.
		
		"""
		pass
	
	def index_of(self, variable: ScriptTraceVariable) -> int:
		"""
		| Returns the index of the ScriptTraceVariable in the list or -1, if the Variable could not be found.
		
		"""
		pass
	
	def __contains__(self, variable: ScriptTraceVariable) -> bool:
		"""
		| Returns, wether the ScriptTraceVariableList contains the ScriptTraceVariable.
		| Allows usage of 'in' and 'not in' operators.
		
		"""
		pass
	
	def contains(self, variable: ScriptTraceVariable) -> bool:
		"""
		| Returns, wether the ScriptTraceVariableList contains the ScriptTraceVariable.
		
		"""
		pass
	
	def __getitem__(self, index: int) -> ScriptTraceVariable:
		"""
		| Gets or sets the trace variable at the given index.
		
		"""
		pass