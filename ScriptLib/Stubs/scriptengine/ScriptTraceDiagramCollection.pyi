from collections.abc import Iterable
from ScriptTraceDiagram import *
from typing import overload


class ScriptTraceDiagramCollection(list):
	"""
	| Represents the collection of Diagrams in one TraceObject.
	
	.. automethod:: __iter__
	.. automethod:: __next__
	.. automethod:: __len__
	.. automethod:: __contains__
	.. automethod:: __getitem__
	
	"""
	
	def __iter__(self) -> Iterable[ScriptTraceDiagram]:
		"""
		
		"""
		pass
	
	def __next__(self) -> ScriptTraceDiagram:
		"""
		
		"""
		pass
	
	def add(self) -> ScriptTraceDiagram:
		"""
		| Creates and adds a ScriptTraceDiagram to the collection. Returns the ScriptTraceDiagram.
		| Not allowed for the ScriptTraceDiagramCollection of the DeviceTrace.
		
		"""
		pass
	
	def __len__(self) -> int:
		"""
		| Returns the number of ScriptTraceDiagrams in this ScriptTraceDiagramCollection.
		
		"""
		pass
	
	@overload
	def remove(self, index: int) -> None:
		"""
		| Removes the ScriptTraceDiagram at the given index.
		
		"""
		pass
	
	@overload
	def remove(self, diagram: ScriptTraceDiagram) -> None:
		"""
		| Removes the given ScriptTraceDiagram from this ScriptTraceDiagramCollection.
		
		"""
		pass
	
	def remove(self) -> None:
		"""
		| Removes the ScriptTraceDiagram at the given index.
		
		"""
		pass
	
	def clear(self) -> None:
		"""
		| Removes all ScriptTraceDiagrams from this ScriptTraceDiagramCollection.
		
		"""
		pass
	
	def index_of(self, diagram: ScriptTraceDiagram) -> int:
		"""
		| Returns the index of the ScriptTraceDiagram in the collection or -1, if the Variable could not be found.
		
		"""
		pass
	
	def __contains__(self, diagram: ScriptTraceDiagram) -> bool:
		"""
		| Returns, wether the ScriptTraceDiagramCollection contains the ScriptTraceDiagram.
		| Allows usage of 'in' and 'not in' operators.
		
		"""
		pass
	
	def contains(self, diagram: ScriptTraceDiagram) -> bool:
		"""
		| Returns, wether the ScriptTraceDiagramCollection contains the ScriptTraceDiagram.
		
		"""
		pass
	
	def __getitem__(self, index: int) -> ScriptTraceDiagram:
		"""
		| Gets or sets the diagram at the given index.
		
		"""
		pass