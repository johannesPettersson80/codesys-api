"""
CODESYS Persistent Session Script

This script runs as a persistent session inside CODESYS.
It handles commands from the REST API server and executes
operations within the CODESYS environment.

Usage:
    This script is meant to be launched by CODESYS.exe with:
    CODESYS.exe -script PERSISTENT_SESSION.py

Note:
    This script is written for Python 2.7 compatibility since
    CODESYS uses IronPython 2.7.
"""

import scriptengine
import os
import sys
import time
import json
import traceback
import threading

# Constants
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REQUEST_DIR = os.path.join(SCRIPT_DIR, "requests")
RESULT_DIR = os.path.join(SCRIPT_DIR, "results")
TERMINATION_SIGNAL_FILE = os.path.join(SCRIPT_DIR, "terminate.signal")
STATUS_FILE = os.path.join(SCRIPT_DIR, "session_status.json")
LOG_FILE = os.path.join(SCRIPT_DIR, "session.log")

# Ensure directories exist
for directory in [REQUEST_DIR, RESULT_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

class CodesysPersistentSession(object):
    """Maintains a persistent CODESYS session."""
    
    def __init__(self):
        self.system = None
        self.active_project = None
        self.running = True
        self.request_thread = None
        self.init_success = False
        
    def initialize(self):
        """Initialize the CODESYS environment."""
        try:
            # Log initialization
            self.log("Initializing CODESYS session")
            
            # Initialize the system
            self.system = scriptengine.ScriptSystem()
            
            # Update status
            self.update_status({
                "state": "initialized",
                "timestamp": time.time(),
                "project": None
            })
            
            self.init_success = True
            self.log("Initialization successful")
            return True
        except Exception, e:
            self.log("Initialization failed: %s" % str(e))
            self.log(traceback.format_exc())
            return False
            
    def run(self):
        """Run the persistent session."""
        if not self.init_success:
            self.log("Cannot run - initialization failed")
            return False
            
        # Start request processing thread
        self.request_thread = threading.Thread(target=self.process_requests)
        self.request_thread.daemon = True
        self.request_thread.start()
        
        # Main loop
        try:
            self.log("Entering main loop")
            
            while self.running:
                # Check for termination signal
                if os.path.exists(TERMINATION_SIGNAL_FILE):
                    self.log("Termination signal detected")
                    self.running = False
                    try:
                        os.remove(TERMINATION_SIGNAL_FILE)
                    except:
                        pass
                    break
                    
                # Perform periodic tasks
                self.periodic_tasks()
                
                # Sleep to prevent CPU hogging
                time.sleep(0.1)
                
            self.log("Exiting main loop")
            return True
        except Exception, e:
            self.log("Error in main loop: %s" % str(e))
            self.log(traceback.format_exc())
            return False
        finally:
            # Cleanup
            self.cleanup()
            
    def process_requests(self):
        """Process script execution requests."""
        while self.running:
            try:
                # Look for request files
                for filename in os.listdir(REQUEST_DIR):
                    if filename.endswith(".request"):
                        request_path = os.path.join(REQUEST_DIR, filename)
                        
                        # Process request
                        self.process_request(request_path)
                        
                        # Remove request file
                        try:
                            os.remove(request_path)
                        except:
                            pass
            except Exception, e:
                self.log("Error processing requests: %s" % str(e))
                self.log(traceback.format_exc())
                
            # Sleep briefly
            time.sleep(0.1)
            
    def process_request(self, request_path):
        """Process a single request."""
        result_path = None
        try:
            # Read request
            with open(request_path, 'r') as f:
                request = json.loads(f.read())
                
            # Get script path and result path
            script_path = request.get("script_path")
            result_path = request.get("result_path")
            
            if not script_path or not result_path:
                raise ValueError("Invalid request - missing script_path or result_path")
                
            # Log request
            self.log("Processing request: %s" % os.path.basename(script_path))
            
            # Check if script file exists
            if not os.path.exists(script_path):
                raise IOError("Script file not found: %s" % script_path)
                
            # Execute script
            result = self.execute_script(script_path)
            
            # Write result
            with open(result_path, 'w') as f:
                f.write(json.dumps(result))
                
            # Log completion
            self.log("Request completed: %s" % os.path.basename(script_path))
        except Exception, e:
            self.log("Error processing request: %s" % str(e))
            self.log(traceback.format_exc())
            
            # Write error result if result_path is available
            if result_path:
                try:
                    with open(result_path, 'w') as f:
                        f.write(json.dumps({
                            "success": False,
                            "error": str(e),
                            "traceback": traceback.format_exc()
                        }))
                except:
                    pass
                    
    def execute_script(self, script_path):
        """Execute a Python script in the CODESYS environment."""
        try:
            # Create globals dict with access to the session
            globals_dict = {
                "session": self,
                "system": self.system,
                "active_project": self.active_project,
                "json": json,
                "os": os,
                "time": time,
                "scriptengine": scriptengine
            }
            
            # Load script
            with open(script_path, 'r') as f:
                script_code = f.read()
                
            # Execute script
            local_vars = {}
            exec(script_code, globals_dict, local_vars)
            
            # Check for result
            if "result" in local_vars:
                return local_vars["result"]
            else:
                return {"success": True, "message": "Script executed successfully"}
        except Exception, e:
            return {
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc()
            }
            
    def periodic_tasks(self):
        """Perform periodic tasks."""
        # Update session status
        project_path = None
        if self.active_project:
            try:
                project_path = self.active_project.path
            except:
                project_path = "Unknown"
                
        self.update_status({
            "state": "running",
            "timestamp": time.time(),
            "project": project_path
        })
        
    def cleanup(self):
        """Clean up resources before termination."""
        self.log("Cleaning up session")
        
        # Close active project
        if self.active_project:
            try:
                self.log("Closing project: %s" % self.active_project.path)
                
                # Save project if dirty
                if self.active_project.dirty:
                    self.active_project.save()
                    
                # Close project
                self.active_project = None
            except Exception, e:
                self.log("Error closing project: %s" % str(e))
                
        # Update status
        self.update_status({
            "state": "terminated",
            "timestamp": time.time(),
            "project": None
        })
        
        self.log("Cleanup complete")
        
    def update_status(self, status):
        """Update session status file."""
        try:
            with open(STATUS_FILE, 'w') as f:
                f.write(json.dumps(status))
        except Exception, e:
            self.log("Error updating status: %s" % str(e))
            
    def log(self, message):
        """Log a message."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_message = "[%s] %s\n" % (timestamp, message)
        
        try:
            with open(LOG_FILE, 'a') as f:
                f.write(log_message)
        except:
            # Fall back to stdout if log file is not accessible
            print log_message
            
# Main entry point
if __name__ == "__main__":
    # Create and run session
    session = CodesysPersistentSession()
    
    if session.initialize():
        session.run()
    
    # Exit with appropriate code
    sys.exit(0 if session.init_success else 1)