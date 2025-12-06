#!/usr/bin/env python3
"""
RedScript Compiler CLI
"""
import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description="RedScript Compiler - Translate kinematic intent to Minecraft schematics"
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Compile command
    compile_parser = subparsers.add_parser('compile', help='Compile RedScript to schematic')
    compile_parser.add_argument('input', type=str, help='Input .rs file')
    compile_parser.add_argument('--output', '-o', type=str, help='Output .litematic file')
    compile_parser.add_argument('--optimize', action='store_true', help='Enable optimization')
    compile_parser.add_argument('--view', action='store_true', help='Launch 3D viewer after compiling')
    compile_parser.add_argument('--debug', action='store_true', help='Run in interactive debug mode')
    
    # View command
    view_parser = subparsers.add_parser('view', help='Launch 3D viewer')
    view_parser.add_argument('schematic', type=str, help='Schematic file to view')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export existing design to .litematic')
    export_parser.add_argument('input', type=str, help='Input .rs file')
    export_parser.add_argument('--output', '-o', type=str, help='Output .litematic file (defaults to input name)')
    export_parser.add_argument('--name', type=str, help='Schematic name')
    
    args = parser.parse_args()
    
    if args.command == 'compile':
        from redscript.compiler import compile_file
        try:
            result = compile_file(args.input, args.output, optimize=args.optimize)
            if args.output:
                print(f"[+] Compiled to {args.output}")
            else:
                print(f"[+] Compiled successfully")

            if args.debug:
                from redscript.viewer.simulator import RedstoneSimulator
                from redscript.cli.debug import run_debug_shell
                
                print(f"[+] Starting interactive debugger...")
                # Initialize simulator with the compiled logical graph
                sim = RedstoneSimulator(result.schematic.logical_graph)
                run_debug_shell(sim)

            elif args.view:
                from redscript.viewer.app import VoxelViewer
                viewer = VoxelViewer()
                viewer.load_grid(result.schematic.voxel_grid)
                viewer.run()
        except Exception as e:
            print(f"[-] Compilation failed: {e}", file=sys.stderr)
            sys.exit(1)
    
    elif args.command == 'view':
        from redscript.viewer import launch_viewer
        try:
            launch_viewer(args.schematic)
        except Exception as e:
            print(f"[-] Viewer failed: {e}", file=sys.stderr)
            sys.exit(1)
            
    elif args.command == 'export':
        from redscript.compiler import compile_file
        try:
            # For now, export just compiles .rs to .litematic
            # If we had a JSON format, we would load it here.
            if not args.input.endswith('.rs'):
                print("Error: Only .rs files are supported for export currently.", file=sys.stderr)
                sys.exit(1)
            
            # Default output to input filename with .litematic extension
            output_path = args.output if args.output else args.input.replace('.rs', '.litematic')
                
            result = compile_file(args.input, output_path)
            if result.success:
                print(f"[+] Exported to {output_path}")
            else:
                print(f"[-] Export failed: {result.errors}", file=sys.stderr)
                sys.exit(1)
        except Exception as e:
            print(f"[-] Export failed: {e}", file=sys.stderr)
            sys.exit(1)
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
