from dataclasses import dataclass, field
from typing import Dict, List, Any, Set, Optional, Union
import copy
from redscript.compiler.logical_graph import LogicalGraph, Component, Connection, ComponentType

@dataclass
class DebugContext:
    """Context for debugging session"""
    breakpoints: Set[int] = field(default_factory=set)
    current_tick: int = 0
    history: List[Dict[str, Any]] = field(default_factory=list)
    paused: bool = False

@dataclass
class BlockPowerState:
    """Power state for a single block"""
    block_id: str
    power_level: int  # 0-15
    is_powered: bool  # Convenience flag (power_level > 0)
    source_type: str  # "direct", "strong", "weak"

class RedstoneSimulator:
    """Simulates redstone signal propagation"""
    power_states: Dict[str, BlockPowerState]
    connection_graph: Dict[str, List[str]]  # block_id -> connected block_ids
    debug_context: DebugContext
    graph: Optional[LogicalGraph]
    
    def __init__(self, graph_or_grid):
        self.power_states = {}
        self.connection_graph = {}
        self.debug_context = DebugContext()
        self.graph = None
        
        if isinstance(graph_or_grid, LogicalGraph):
            self.graph = graph_or_grid
            # Initialize states for components
            for comp_id in self.graph.components:
                self.power_states[comp_id] = BlockPowerState(
                    block_id=comp_id,
                    power_level=0,
                    is_powered=False,
                    source_type="none"
                )
        elif hasattr(graph_or_grid, 'blocks'): # VoxelGrid
            for pos, block in graph_or_grid.blocks.items():
                bid = f"{pos[0]}_{pos[1]}_{pos[2]}"
                self.power_states[bid] = BlockPowerState(
                    block_id=bid,
                    power_level=0,
                    is_powered=False,
                    source_type="none"
                )

    def step(self) -> List[str]:
        """Advance simulation by one tick"""
        self.debug_context.current_tick += 1
        messages = []
        
        if self.graph:
            self._simulate_logic()
            failures = self._check_assertions()
            messages.extend(failures)
        else:
            self.propagate()
        
        self._save_history()
        return messages

    def _simulate_logic(self):
        """Simulate logical graph"""
        next_states = {k: copy.deepcopy(v) for k, v in self.power_states.items()}
        
        # Propagate signals
        for conn in self.graph.connections.values():
            source_comp = self._get_component_by_port(conn.source_port_id)
            target_comp = self._get_component_by_port(conn.target_port_id)
            
            if source_comp and target_comp:
                source_state = self.power_states.get(source_comp.id)
                if source_state and source_state.is_powered:
                    target_state = next_states.get(target_comp.id)
                    if target_state:
                        target_state.is_powered = True
                        target_state.power_level = 15
        
        self.power_states = next_states

    def _check_assertions(self) -> List[str]:
        """Check debug assertions"""
        failures = []
        if not self.graph:
            return failures
            
        for assertion in self.graph.assertions:
            try:
                if '==' in assertion.condition:
                    parts = assertion.condition.split('==')
                    lhs = parts[0].strip()
                    rhs = parts[1].strip()
                    
                    if '.' in lhs:
                        comp_id, prop = lhs.split('.')
                        state = self.power_states.get(comp_id)
                        if state:
                            actual = 1 if state.is_powered else 0
                            expected = int(rhs)
                            if actual != expected:
                                failures.append(f"Assertion failed: {assertion.condition} (Actual: {actual})")
            except Exception as e:
                failures.append(f"Error checking assertion '{assertion.condition}': {e}")
        return failures

    def _get_component_by_port(self, port_id: str) -> Optional[Component]:
        if not self.graph:
            return None
        for comp in self.graph.components.values():
            for port in comp.inputs + comp.outputs:
                if port.id == port_id:
                    return comp
        return None

    def _save_history(self):
        """Save current state to history"""
        snapshot = {bid: copy.deepcopy(state) for bid, state in self.power_states.items()}
        self.debug_context.history.append(snapshot)

    def toggle_source(self, block_id: str) -> List[str]:
        """Toggle a source block, return list of updated blocks"""
        if block_id not in self.power_states:
            return []
            
        state = self.power_states[block_id]
        state.is_powered = not state.is_powered
        state.power_level = 15 if state.is_powered else 0
        
        return [block_id]

    def set_state(self, block_id: str, value: int) -> bool:
        """Set state of a component"""
        if block_id not in self.power_states:
            return False
        state = self.power_states[block_id]
        state.power_level = value
        state.is_powered = value > 0
        return True
        
    def propagate(self) -> None:
        """Propagate signals through the connection graph"""
        pass
        
    def get_visual_state(self, block_id: str) -> Dict[str, Any]:
        """Get visual state for rendering (e.g., lamp on/off)"""
        if block_id in self.power_states:
            return {'powered': self.power_states[block_id].is_powered}
        return {}
        
    def get_power_state(self, block_id: str) -> BlockPowerState:
        return self.power_states.get(block_id)
