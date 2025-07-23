from typing import Dict, Any, Callable, Optional, List
from dataclasses import dataclass, field
import copy
import networkx as nx

@dataclass
class Attribute:
    name: str
    is_input: bool
    value: Any = None
    formula: Optional[Callable[['Block'], Any]] = None
    history: List[Any] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)

    def evaluate(self, block: 'Block'):
        if not self.is_input and self.formula:
            self.value = self.formula(block)
        self.history.append(copy.deepcopy(self.value))
        return self.value

@dataclass
class Block:
    name: str
    attributes: Dict[str, Attribute]

    def evaluate_all(self):
        for attr in self.attributes.values():
            attr.evaluate(self)

    def set_input(self, name: str, value: Any):
        if name in self.attributes and self.attributes[name].is_input:
            self.attributes[name].value = value

    def get_dependencies(self):
        deps = []
        for attr in self.attributes.values():
            deps.extend(attr.dependencies)
        return deps

@dataclass
class SimulationRun:
    name: str
    steps: int
    blocks: Dict[str, Block]
    results: Dict[int, Dict[str, Dict[str, Any]]] = field(default_factory=dict)
    graph: nx.DiGraph = field(default_factory=nx.DiGraph)

    def build_dependency_graph(self):
        for block in self.blocks.values():
            for attr in block.attributes.values():
                for dep in attr.dependencies:
                    self.graph.add_edge(dep, f"{block.name}.{attr.name}")

    def run(self):
        self.build_dependency_graph()
        for t in range(self.steps):
            self.results[t] = {}
            for block_name, block in self.blocks.items():
                block.evaluate_all()
                self.results[t][block_name] = {
                    attr.name: attr.value for attr in block.attributes.values()
                }
