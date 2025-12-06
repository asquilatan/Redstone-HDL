import cmd
import sys
from typing import List
from redscript.viewer.simulator import RedstoneSimulator

class DebugShell(cmd.Cmd):
    intro = 'Welcome to the RedScript Debugger. Type help or ? to list commands.\n'
    prompt = '(redscript-debug) '

    def __init__(self, simulator: RedstoneSimulator):
        super().__init__()
        self.simulator = simulator
        self.last_step_output = []

    def do_step(self, arg):
        """Step the simulation by one tick."""
        messages = self.simulator.step()
        self.last_step_output = messages
        for msg in messages:
            print(msg)
        print(f"Tick: {self.simulator.debug_context.current_tick}")

    def do_s(self, arg):
        """Alias for step"""
        self.do_step(arg)

    def do_continue(self, arg):
        """Continue execution until a breakpoint is hit or max ticks reached."""
        # For now, just run for a few steps or until assertion failure
        # Since we don't have explicit breakpoints in the graph yet (except assertions which raise errors?)
        # Actually assertions are checked in step().
        
        # Let's run for up to 100 ticks or until an assertion fails
        print("Running...")
        try:
            for _ in range(100):
                messages = self.simulator.step()
                for msg in messages:
                    print(msg)
                    if "Assertion failed" in msg:
                        print("Stopped due to assertion failure.")
                        return
                # Check if we are "done" (stable state)? 
                # The simulator doesn't really know when it's stable unless we check for changes.
                # For now just run 100 ticks.
        except Exception as e:
            print(f"Error during execution: {e}")

    def do_c(self, arg):
        """Alias for continue"""
        self.do_continue(arg)

    def do_reset(self, arg):
        """Reset the simulation."""
        self.simulator.reset()
        print("Simulation reset.")

    def do_r(self, arg):
        """Alias for reset"""
        self.do_reset(arg)

    def do_inspect(self, arg):
        """Inspect a component by ID. Usage: inspect <component_id>"""
        comp_id = arg.strip()
        if not comp_id:
            print("Usage: inspect <component_id>")
            return
        
        state = self.simulator.get_power_state(comp_id)
        if state is None:
            print(f"Component '{comp_id}' not found.")
        else:
            print(f"Component: {comp_id}")
            print(f"State: {state}")

    def do_list(self, arg):
        """List all components and their states."""
        for comp_id, state in self.simulator.power_states.items():
            print(f"{comp_id}: {state}")

    def do_toggle(self, arg):
        """Toggle a component state. Usage: toggle <component_id>"""
        comp_id = arg.strip()
        if not comp_id:
            print("Usage: toggle <component_id>")
            return
        
        if self.simulator.toggle_source(comp_id):
            print(f"Toggled {comp_id}")
            self.do_inspect(comp_id)
        else:
            print(f"Component '{comp_id}' not found.")

    def do_set(self, arg):
        """Set component power level. Usage: set <component_id> <value>"""
        args = arg.split()
        if len(args) != 2:
            print("Usage: set <component_id> <value>")
            return
            
        comp_id = args[0]
        try:
            value = int(args[1])
        except ValueError:
            print("Value must be an integer.")
            return
            
        if self.simulator.set_state(comp_id, value):
            print(f"Set {comp_id} to {value}")
            self.do_inspect(comp_id)
        else:
            print(f"Component '{comp_id}' not found.")

    def do_quit(self, arg):
        """Exit the debugger."""
        print("Exiting debugger.")
        return True

    def do_q(self, arg):
        """Alias for quit"""
        return self.do_quit(arg)

def run_debug_shell(simulator: RedstoneSimulator):
    shell = DebugShell(simulator)
    shell.cmdloop()
