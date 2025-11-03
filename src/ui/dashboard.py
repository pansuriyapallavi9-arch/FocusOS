#!/usr/bin/env python3
"""
Web Dashboard for Focus OS
Flask-based web interface
"""
from flask import Flask, render_template, jsonify, request
import psutil
import threading
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'controller'))
from focus_controller import FocusController

app = Flask(__name__)
controller = FocusController()
focus_thread = None

@app.route('/')
def index():
    """Serve main dashboard"""
    return render_template('index.html')

@app.route('/api/processes')
def get_processes():
    """Get list of running processes"""
    processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
        try:
            info = proc.info
            info['blacklisted'] = controller.is_blacklisted(info['name'])
            info['cpu_percent'] = round(info.get('cpu_percent', 0), 1)
            info['memory_percent'] = round(info.get('memory_percent', 0), 1)
            processes.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    # Sort by CPU usage
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    return jsonify(processes[:100])

@app.route('/api/focus/start', methods=['POST'])
def start_focus():
    """Start focus mode"""
    global focus_thread
    
    if controller.focus_active:
        return jsonify({'status': 'error', 'message': 'Already active'}), 400
    
    data = request.json
    duration = int(data.get('duration', 25))
    
    if duration < 1 or duration > 240:
        return jsonify({'status': 'error', 'message': 'Duration: 1-240 min'}), 400
    
    focus_thread = threading.Thread(target=controller.start_focus_mode, args=(duration,), daemon=True)
    focus_thread.start()
    
    return jsonify({'status': 'started', 'duration': duration})

@app.route('/api/focus/stop', methods=['POST'])
def stop_focus():
    """Stop focus mode"""
    if not controller.focus_active:
        return jsonify({'status': 'error', 'message': 'Not active'}), 400
    
    controller.end_focus_mode()
    return jsonify({'status': 'stopped'})

@app.route('/api/focus/status')
def focus_status():
    """Get focus mode status"""
    return jsonify({
        'active': controller.focus_active,
        'suspended_count': len(controller.suspended_pids)
    })

@app.route('/api/stats')
def get_stats():
    """Get statistics"""
    return jsonify(controller.get_stats())

@app.route('/api/blacklist')
def get_blacklist():
    """Get blacklist"""
    return jsonify({'blacklist': controller.blacklist})

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🎯 FOCUS OS - Web Dashboard")
    print("="*70)
    print(f"🌐 Open in browser: http://localhost:5000")
    print(f"🚫 Blacklist: {', '.join(controller.blacklist[:5])}...")
    print(f"📊 Sessions: {controller.stats['total_sessions']}")
    print("="*70 + "\n")
    print("⚠️  NOTE: Run as Administrator for full functionality\n")
    
    app.run(debug=False, host='127.0.0.1', port=5000, threaded=True)


