#!/usr/bin/env python3
"""
Focus Controller - Main logic for Focus OS
Manages focus sessions and process blocking
"""
import psutil
import time
import json
import os
from datetime import datetime
from process_manager import suspend_process, resume_process

class FocusController:
    def __init__(self):
        self.blacklist = self.load_blacklist()
        self.suspended_pids = []
        self.stats = {
            'total_sessions': 0,
            'total_minutes': 0,
            'processes_blocked': 0
        }
        self.load_stats()
        self.focus_active = False
        
    def load_blacklist(self):
        """Load blacklist from config file"""
        path = 'config/blacklist.txt'
        if not os.path.exists(path):
            # Default blacklist for common distracting apps
            return ['chrome', 'firefox', 'steam', 'discord', 'spotify', 
                    'telegram', 'whatsapp', 'slack', 'teams', 'outlook']
        
        with open(path, 'r') as f:
            return [line.strip().lower() for line in f if line.strip()]
    
    def load_stats(self):
        """Load statistics from file"""
        if os.path.exists('logs/stats.json'):
            try:
                with open('logs/stats.json', 'r') as f:
                    self.stats = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load stats: {e}")
    
    def save_stats(self):
        """Save statistics to file"""
        os.makedirs('logs', exist_ok=True)
        try:
            with open('logs/stats.json', 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save stats: {e}")
    
    def is_blacklisted(self, process_name):
        """Check if process matches blacklist"""
        name = process_name.lower()
        return any(blocked in name for blocked in self.blacklist)
    
    def get_distracting_processes(self):
        """Find all running distracting processes"""
        distracting = []
        for proc in psutil.process_iter(['pid', 'name', 'status']):
            try:
                info = proc.info
                if self.is_blacklisted(info['name']):
                    distracting.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return distracting
    
    def suspend_distracting_process(self, pid):
        """Suspend a distracting process"""
        try:
            if suspend_process(pid):
                if pid not in self.suspended_pids:
                    self.suspended_pids.append(pid)
                    self.stats['processes_blocked'] += 1
                return True
            return False
        except Exception as e:
            print(f"Error suspending PID {pid}: {e}")
            return False
    
    def resume_all_processes(self):
        """Resume all suspended processes"""
        for pid in self.suspended_pids[:]:
            try:
                resume_process(pid)
                self.suspended_pids.remove(pid)
            except Exception as e:
                print(f"Warning: Could not resume PID {pid}: {e}")
    
    def start_focus_mode(self, duration_minutes=25):
        """Start focus mode for specified duration"""
        if self.focus_active:
            print("ERROR: Focus mode already active!")
            return
        
        self.focus_active = True
        
        print(f"\n{'='*70}")
        print(f"🎯 FOCUS MODE ACTIVATED - {duration_minutes} minutes")
        print(f"{'='*70}\n")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        # Initial scan and suspend
        print("📊 Scanning for distracting processes...")
        distracting = self.get_distracting_processes()
        print(f"Found {len(distracting)} distracting process(es)\n")
        
        for proc in distracting:
            print(f"🚫 Blocking: {proc['name']} (PID: {proc['pid']})")
            self.suspend_distracting_process(proc['pid'])
        
        if distracting:
            print()
        
        # Monitor loop
        try:
            while time.time() < end_time and self.focus_active:
                # Calculate remaining time
                remaining_seconds = int(end_time - time.time())
                remaining_minutes = remaining_seconds // 60
                remaining_secs = remaining_seconds % 60
                
                # Display timer
                print(f"\r⏱️  {remaining_minutes:02d}:{remaining_secs:02d}  "
                      f"| 🚫 Blocked: {len(self.suspended_pids)} processes  ", 
                      end='', flush=True)
                
                # Check for new distracting processes every 3 seconds
                time.sleep(3)
                
                if not self.focus_active:
                    break
                
                new_distracting = self.get_distracting_processes()
                for proc in new_distracting:
                    if proc['pid'] not in self.suspended_pids:
                        print(f"\n⚠️  NEW: {proc['name']} (PID: {proc['pid']}) ", end='')
                        if self.suspend_distracting_process(proc['pid']):
                            print("✓ BLOCKED")
                        else:
                            print("✗ FAILED")
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Focus interrupted by user!")
        
        # End session
        print("\n")
        self.end_focus_mode()
        
        # Update statistics
        session_duration = (time.time() - start_time) / 60
        self.stats['total_sessions'] += 1
        self.stats['total_minutes'] += int(session_duration)
        self.save_stats()
        
        print(f"\n{'='*70}")
        print(f"✅ FOCUS SESSION COMPLETED!")
        print(f"{'='*70}")
        print(f"⏱️  Duration: {session_duration:.1f} minutes")
        print(f"🚫 Processes blocked: {self.stats['processes_blocked']}")
        print(f"📊 Total sessions: {self.stats['total_sessions']}")
        print(f"⏲️  Total focus time: {self.stats['total_minutes']} minutes")
        print(f"{'='*70}\n")
    
    def end_focus_mode(self):
        """End focus mode and resume all processes"""
        if not self.focus_active:
            return
        
        self.focus_active = False
        print("🔓 Ending focus mode...")
        print("📋 Resuming all suspended processes...\n")
        
        self.resume_all_processes()
        print("\n✅ All processes resumed")
    
    def get_stats(self):
        """Get current statistics"""
        return self.stats

# Command line interface
if __name__ == "__main__":
    import sys
    
    print("\n" + "="*70)
    print("🎯 FOCUS OS - Operating System Project")
    print("="*70 + "\n")
    
    controller = FocusController()
    
    print(f"🚫 Blacklisted apps: {', '.join(controller.blacklist[:5])}...")
    print(f"📊 Total sessions completed: {controller.stats['total_sessions']}")
    print(f"⏲️  Total focus time: {controller.stats['total_minutes']} minutes\n")
    
    if len(sys.argv) > 1:
        try:
            duration = int(sys.argv[1])
        except ValueError:
            print("ERROR: Duration must be a number (minutes)")
            sys.exit(1)
    else:
        duration = 2  # Default 2 minutes for demo
    
    print(f"Starting {duration} minute focus session...\n")
    controller.start_focus_mode(duration)