#!/usr/bin/env python3
"""
Process Manager for Windows
Handles process suspension, resumption, and termination
"""
import psutil
import subprocess
import sys

def suspend_process(pid):
    """Suspend a process by PID"""
    try:
        proc = psutil.Process(pid)
        proc.suspend()
        print(f"SUCCESS: Process {pid} ({proc.name()}) suspended")
        return True
    except psutil.NoSuchProcess:
        print(f"ERROR: Process {pid} not found")
        return False
    except psutil.AccessDenied:
        print(f"ERROR: Access denied for process {pid}. Try running as Administrator.")
        return False
    except Exception as e:
        print(f"ERROR: Failed to suspend process {pid}: {e}")
        return False

def resume_process(pid):
    """Resume a suspended process"""
    try:
        proc = psutil.Process(pid)
        proc.resume()
        print(f"SUCCESS: Process {pid} ({proc.name()}) resumed")
        return True
    except psutil.NoSuchProcess:
        print(f"ERROR: Process {pid} not found")
        return False
    except psutil.AccessDenied:
        print(f"ERROR: Access denied for process {pid}. Try running as Administrator.")
        return False
    except Exception as e:
        print(f"ERROR: Failed to resume process {pid}: {e}")
        return False

def kill_process(pid):
    """Terminate a process"""
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        print(f"SUCCESS: Process {pid} ({proc.name()}) terminated")
        return True
    except psutil.NoSuchProcess:
        print(f"ERROR: Process {pid} not found")
        return False
    except psutil.AccessDenied:
        print(f"ERROR: Access denied for process {pid}. Try running as Administrator.")
        return False
    except Exception as e:
        print(f"ERROR: Failed to kill process {pid}: {e}")
        return False

def list_processes():
    """List all running processes"""
    print(f"\n{'='*80}")
    print(f"{'PID':<10} {'NAME':<30} {'STATUS':<15} {'CPU%':<10}")
    print(f"{'='*80}")
    
    for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent']):
        try:
            print(f"{proc.info['pid']:<10} {proc.info['name']:<30} "
                  f"{proc.info['status']:<15} {proc.info['cpu_percent']:<10.1f}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    print(f"{'='*80}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python process_manager.py suspend <pid>")
        print("  python process_manager.py resume <pid>")
        print("  python process_manager.py kill <pid>")
        print("  python process_manager.py list")
        sys.exit(1)
    
    action = sys.argv[1].lower()
    
    if action == "list":
        list_processes()
    elif len(sys.argv) < 3:
        print("ERROR: PID required")
        sys.exit(1)
    else:
        try:
            pid = int(sys.argv[2])
        except ValueError:
            print("ERROR: PID must be a number")
            sys.exit(1)
        
        if action == "suspend":
            suspend_process(pid)
        elif action == "resume":
            resume_process(pid)
        elif action == "kill":
            kill_process(pid)
        else:
            print(f"ERROR: Unknown action '{action}'")
            sys.exit(1)