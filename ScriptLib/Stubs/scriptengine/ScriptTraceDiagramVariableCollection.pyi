from collections.abc import Iterable
from ScriptTraceDiagramVariable import *
from ScriptTraceVariable import *
from typing import overload


class ScriptTraceDiagramVariableCollection(list):
	"""
	| Represents a collection of ScriptTraceDiagramVariables, used in a diagram.
	
	.. automethod:: __iter__
	.. automethod:: __next__
	.. automethod:: __len__
	.. automethod:: __contains__
	.. automethod:: __getitem__
	
	"""
	
	def __iter__(self) -> Iterable[ScriptTraceDiagramVariable]:
		"""
		
		"""
		pass
	
	def __next__(self) -> ScriptTraceDiagramVariable:
		"""
		
		"""
		pass
	
	def add(self, variable: ScriptTraceVariable) -> ScriptTraceDiagramVariable:
		"""
		| Creates and adds a ScriptTraceVariable to the diagram. Returns the new ScriptTraceDiagramVariable.
		
		"""
		pass
	
	def __len__(self) -> int:
		"""
		| Returns the number of variables, used in this diagram.
		
		"""
		pass
	
	@overload
	def remove(self, index: int) -> None:
		"""
		| Removes the ScriptTraceDiagramVariable at the given index.
		
		"""
		pass
	
	@overload
	def remove(self, diagramVariable: ScriptTraceDiagramVariable) -> None:
		"""
		| Removes the given ScriptTraceDiagramVariable from the diagram.
		
		"""
		pass
	
	def remove(self) -> None:
		"""
		| Removes the ScriptTraceDiagramVariable at the given index.
		
		"""
		pass
	
	def clear(self) -> None:
		"""
		| Removes all ScriptTraceDiagramVariables from the diagram.
		
		"""
		pass
	
	def index_of(self, diagramVariable: ScriptTraceDiagramVariable) -> int:
		"""
		| Returns the index of the ScriptTraceDiagramVariable in the collection or -1,
		| if the diagramVariable is not part of this diagram.
		
		"""
		pass
	
	def __contains__(self, diagramVariable: ScriptTraceDiagramVariable) -> bool:
		"""
		| Returns, wether this collection contains the given ScriptTraceDiagramVariable.
		| Allows usage of 'in' and 'not in' operators.
		
		"""
		pass
	
	def contains(self, diagramVariable: ScriptTraceDiagramVariable) -> bool:
		"""
		| Returns, wether this collection contains the given ScriptTraceDiagramVariable.
		
		"""
		pass
	
	def __getitem__(self, index: int) -> ScriptTraceDiagramVariable:
		"""
		| Gets or sets the diagram variable at the given index.
		
		"""
		pass