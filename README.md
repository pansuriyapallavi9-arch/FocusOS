# 🎯 Focus OS - Operating System Project

## Overview
Focus OS is an operating system-level distraction management system demonstrating core OS concepts: process management, system-level control, and resource monitoring.

## 🔑 Key OS Concepts Demonstrated

### 1. Process Management
- **Process Control**: Suspend/Resume processes using psutil
- **Process State Management**: Change process states (running ↔ suspended)
- **Process Monitoring**: Real-time tracking of all system processes

### 2. System-Level Operations
- **Direct Process Manipulation**: Control any running process
- **Resource Monitoring**: CPU and memory usage tracking
- **Process Discovery**: Scan and identify running processes

### 3. Scheduling & Priority
- **Process Suspension**: Temporarily halt process execution
- **Resource Allocation**: Manage which processes can run

## 🏗️ Architecture
```
┌──────────────────────┐
│   Web Dashboard      │  ← User Interface
│   (Flask/HTML)       │
└──────────────────────┘
          ↓
┌──────────────────────┐
│  Focus Controller    │  ← Session Management
│  (Python)            │
└──────────────────────┘
          ↓
┌──────────────────────┐
│  Process Manager     │  ← OS-Level Control
│  (psutil library)    │
└──────────────────────┘
          ↓
┌──────────────────────┐
│  Operating System    │  ← Windows API
│  (Windows)           │
└──────────────────────┘
```
# 🎯 Focus OS - Operating System Project

## 📸 Screenshots

### Dashboard
![Dashboard](screenshots/1.png)

### Focus Mode Active
![Active](screenshots/2.png)

### Process Monitor
![Processes](screenshots/3.png)

---

## Overview

## 📦 Installation

### Prerequisites
- Windows 10/11
- Python 3.8+
- Administrator privileges

### Setup
```bash
# 1. Install Python from python.org

# 2. Install dependencies
pip install psutil flask

# 3. Clone/Download this project
cd Desktop
git clone <your-repo-url>
cd FocusOS
```

## 🚀 Usage

### Method 1: Web Dashboard (Recommended)
```bash
# Double-click run.bat
# OR in command prompt:
python src\ui\dashboard.py
```
Then open browser: `http://localhost:5000`

### Method 2: Command Line
```bash
# Start 25-minute focus session
python src\controller\focus_controller.py 25

# Start 5-minute demo
python src\controller\focus_controller.py 5
```

### Method 3: Process Manager
```bash
# List all processes
python src\controller\process_manager.py list

# Suspend specific process
python src\controller\process_manager.py suspend <PID>

# Resume process
python src\controller\process_manager.py resume <PID>
```

## ⚙️ Configuration

Edit `config/blacklist.txt` to customize blocked applications:
```
chrome
firefox
steam
discord
spotify
```

## 🎮 How It Works

1. **Scan Phase**: System scans all running processes
2. **Match Phase**: Compares process names against blacklist
3. **Control Phase**: Suspends matching processes using OS APIs
4. **Monitor Phase**: Continuously checks for new distracting processes
5. **Resume Phase**: Restores all processes when focus ends

## 📊 Features

✅ Real-time process monitoring  
✅ Automatic distraction blocking  
✅ Web-based dashboard  
✅ Session statistics tracking  
✅ Configurable blacklist  
✅ Command-line interface  
✅ Background monitoring  

## 🔬 Technical Details

### Core Technologies
- **Language**: Python 3
- **Web Framework**: Flask
- **Process Control**: psutil library
- **Frontend**: HTML5, CSS3, JavaScript

### Key Functions
- `suspend_process()`: Suspends process execution
- `resume_process()`: Resumes suspended process
- `get_distracting_processes()`: Scans for blacklisted apps
- `start_focus_mode()`: Initiates blocking session

### OS Interactions
- Process enumeration via psutil
- Process state manipulation
- System resource monitoring
- Inter-process communication

## 📁 Project Structure
```
FocusOS/
├── src/
│   ├── controller/
│   │   ├── focus_controller.py    # Main logic
│   │   └── process_manager.py     # Process control
│   └── ui/
│       ├── dashboard.py           # Web server
│       └── templates/
│           └── index.html         # Frontend
├── config/
│   └── blacklist.txt             # Blocked apps
├── logs/
│   └── stats.json                # Statistics
├── run.bat                       # Launcher
└── README.md
```

## 🎓 Educational Value

This project demonstrates understanding of:
- Operating system process management
- System-level programming
- Resource monitoring and control
- Multi-threading
- Web development
- Software architecture

## ⚠️ Important Notes

- Requires **Administrator privileges** for full functionality
- Some system processes cannot be suspended
- Antivirus may flag process manipulation (false positive)
- Works best on Windows 10/11

## 👤 Author

**Your Name**  
Operating Systems Course Project  
Date: 2024

## 📄 License

Educational Project - For Academic Use