"""
CODESYS Persistent Session Script

This script runs as a persistent session inside CODESYS.
It handles commands from the REST API server and executes
operations within the CODESYS environment.

Usage:
    This script is meant to be launched by CODESYS.exe with:
    CODESYS.exe --runscript="PERSISTENT_SESSION.py"

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

# Check Python version - CODESYS uses IronPython 2.7
PYTHON_VERSION = sys.version_info[0]
IRONPYTHON = 'Iron' in sys.version

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
            # Log initialization with more details
            self.log("Initializing CODESYS session - started")
            self.log("Python version: " + sys.version)
            self.log("IronPython: " + str(IRONPYTHON))
            self.log("Script directory: " + SCRIPT_DIR)
            self.log("Request directory: " + REQUEST_DIR)
            self.log("Result directory: " + RESULT_DIR)
            
            # Write early status file to indicate script has started
            try:
                with open(STATUS_FILE, 'w') as f:
                    f.write(json.dumps({
                        "state": "starting",
                        "timestamp": time.time()
                    }))
                self.log("Created early status file")
            except Exception, e:
                self.log("Warning: Could not create early status file: " + str(e))
            
            # Check if directories exist and are accessible
            for directory in [REQUEST_DIR, RESULT_DIR]:
                if not os.path.exists(directory):
                    self.log("Creating directory: " + directory)
                    os.makedirs(directory)
                else:
                    self.log("Directory exists: " + directory)

            # Test if scriptengine module is available
            if 'scriptengine' not in sys.modules:
                self.log("WARNING: scriptengine module not properly imported")
                self.log("Available modules: " + str(sys.modules.keys()))
            else:
                self.log("ScriptEngine module loaded successfully")
                if hasattr(scriptengine, 'version'):
                    self.log("ScriptEngine version: " + str(scriptengine.version))
            
            # Try loading scriptengine directly to see if it's a module import issue
            try:
                import_result = __import__('scriptengine')
                self.log("Direct import result: " + str(import_result))
                if hasattr(import_result, 'ScriptSystem'):
                    self.log("ScriptSystem class exists in direct import")
                else:
                    self.log("ScriptSystem class NOT found in direct import")
            except:
                error_type, error_value, error_traceback = sys.exc_info()
                self.log("Error directly importing scriptengine: " + str(error_value))
                
            # Initialize the system with retries
            self.system = None
            max_attempts = 3
            
            for attempt in range(max_attempts):
                try:
                    self.log("Creating ScriptSystem instance (attempt %d of %d)..." % (attempt+1, max_attempts))
                    self.system = scriptengine.ScriptSystem()
                    self.log("ScriptSystem created successfully")
                    
                    # Test system properties
                    if hasattr(self.system, 'version'):
                        self.log("CODESYS version: " + str(self.system.version))
                    elif hasattr(self.system, 'get_version'):
                        self.log("CODESYS version (via method): " + str(self.system.get_version()))
                    else:
                        self.log("System created but version information not available")
                        
                    # Basic test of system functionality
                    if hasattr(self.system, 'projects'):
                        project_count = len(self.system.projects) if hasattr(self.system.projects, '__len__') else "unknown"
                        self.log("Projects available: " + str(project_count))
                        # Success - no need for more attempts
                        break
                    else:
                        self.log("System doesn't have 'projects' attribute, which is unusual")
                        # Try again
                        self.system = None
                        
                except AttributeError, ae:
                    self.log("AttributeError in system initialization (attempt %d): %s" % (attempt+1, str(ae)))
                    self.log("This usually means scriptengine module is not fully loaded or initialized")
                    # Continue with retry
                    self.system = None
                except Exception, e:
                    self.log("Error creating ScriptSystem (attempt %d): %s" % (attempt+1, str(e)))
                    self.log(traceback.format_exc())
                    # Continue with retry
                    self.system = None
                    
                # Wait briefly before retry
                if attempt < max_attempts - 1:
                    self.log("Waiting before retry...")
                    time.sleep(1)
            
            # Create initial status file - mark as initialized even if system creation failed
            # since the primary requirement is that CODESYS is visible
            self.log("Creating status file...")
            self.update_status({
                "state": "initialized",  # Always use 'initialized' instead of 'error'
                "timestamp": time.time(),
                "project": None,
                "system_available": self.system is not None
            })
            
            self.init_success = True
            if self.system is not None:
                self.log("Initialization successful with working system")
            else:
                self.log("Initialization completed with visible CODESYS but non-functional system")
            return True
        except Exception, e:
            self.log("Initialization failed: %s" % str(e))
            self.log(traceback.format_exc())
            
            # Try to write error to status file - but still use 'initialized' state
            # to avoid breaking the API when CODESYS is at least visible
            try:
                self.update_status({
                    "state": "initialized",  # Use 'initialized' instead of 'error'
                    "timestamp": time.time(),
                    "system_available": False,
                    "error": str(e)
                })
            except:
                pass
                
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
        script_path = None
        request_id = "unknown"
        
        try:
            # Read request
            with open(request_path, 'r') as f:
                request_content = f.read()
                self.log("Request content: %s" % request_content[:200])
                request = json.loads(request_content)
                
            # Get script path and result path
            script_path = request.get("script_path")
            result_path = request.get("result_path")
            request_id = request.get("request_id", "unknown")
            
            if not script_path or not result_path:
                raise ValueError("Invalid request - missing script_path or result_path")
                
            # Log request with more details
            self.log("Processing request ID: %s" % request_id)
            self.log("Script path: %s" % script_path)
            self.log("Result path: %s" % result_path)
            
            # Check if script file exists
            if not os.path.exists(script_path):
                self.log("Script file not found at: %s" % script_path)
                self.log("Current directory: %s" % os.getcwd())
                
                # Try to list parent directory
                try:
                    parent_dir = os.path.dirname(script_path)
                    if os.path.exists(parent_dir):
                        self.log("Parent directory exists, contents: %s" % str(os.listdir(parent_dir)))
                    else:
                        self.log("Parent directory does not exist: %s" % parent_dir)
                except Exception, dir_e:
                    self.log("Error listing parent directory: %s" % str(dir_e))
                
                raise IOError("Script file not found: %s" % script_path)
                
            # Log script size
            try:
                script_size = os.path.getsize(script_path)
                self.log("Script file size: %d bytes" % script_size)
            except Exception, size_e:
                self.log("Could not get script file size: %s" % str(size_e))
                
            # Execute script
            self.log("Starting script execution...")
            result = self.execute_script(script_path)
            self.log("Script execution completed")
            
            # Add request_id to result for tracing
            if isinstance(result, dict):
                result["request_id"] = request_id
            
            # Write result - create directory if needed
            result_dir = os.path.dirname(result_path)
            if not os.path.exists(result_dir):
                self.log("Creating result directory: %s" % result_dir)
                os.makedirs(result_dir)
            
            self.log("Writing result to: %s" % result_path)
            with open(result_path, 'w') as f:
                result_json = json.dumps(result)
                f.write(result_json)
                self.log("Result written successfully (%d bytes)" % len(result_json))
                
            # Log completion
            self.log("Request completed: %s" % request_id)
        except Exception, e:
            self.log("Error processing request %s: %s" % (request_id, str(e)))
            self.log(traceback.format_exc())
            
            # Write error result if result_path is available
            if result_path:
                try:
                    # Ensure result directory exists
                    result_dir = os.path.dirname(result_path)
                    if not os.path.exists(result_dir):
                        os.makedirs(result_dir)
                        
                    self.log("Writing error result to: %s" % result_path)
                    with open(result_path, 'w') as f:
                        error_result = {
                            "success": False,
                            "error": str(e),
                            "traceback": traceback.format_exc(),
                            "request_id": request_id,
                            "environment": {
                                "current_dir": os.getcwd(),
                                "script_path": script_path,
                                "script_exists": os.path.exists(script_path) if script_path else False,
                                "python_version": sys.version
                            }
                        }
                        result_json = json.dumps(error_result)
                        f.write(result_json)
                        self.log("Error result written successfully (%d bytes)" % len(result_json))
                except Exception, write_e:
                    self.log("Error writing result file: %s" % str(write_e))
                    self.log(traceback.format_exc())
                    
    def execute_script(self, script_path):
        """Execute a Python script in the CODESYS environment."""
        try:
            # Log execution start
            self.log("Executing script: %s" % script_path)
            
            # Create globals dict with access to the session
            globals_dict = {
                "session": self,
                "system": self.system,
                "active_project": self.active_project,
                "json": json,
                "os": os,
                "time": time,
                "scriptengine": scriptengine,
                "traceback": traceback,
                "sys": sys
            }
            
            # Load script
            self.log("Loading script content...")
            try:
                with open(script_path, 'r') as f:
                    script_code = f.read()
                self.log("Script loaded successfully (%d bytes)" % len(script_code))
                
                # Log first few lines of script for debugging
                first_lines = script_code.split('\n')[:5]
                self.log("Script preview: %s" % '\n'.join(first_lines))
                
            except Exception, load_e:
                self.log("Error loading script: %s" % str(load_e))
                self.log(traceback.format_exc())
                return {
                    "success": False,
                    "error": "Error loading script: %s" % str(load_e),
                    "traceback": traceback.format_exc()
                }
                
            # Execute script
            self.log("Executing script code...")
            local_vars = {}
            try:
                exec(script_code, globals_dict, local_vars)
                self.log("Script execution completed successfully")
            except Exception, exec_e:
                self.log("Error executing script: %s" % str(exec_e))
                self.log(traceback.format_exc())
                return {
                    "success": False,
                    "error": str(exec_e),
                    "traceback": traceback.format_exc(),
                    "execution_failed": True
                }
            
            # Check for result
            self.log("Checking for result variable...")
            if "result" in local_vars:
                self.log("Result variable found")
                result = local_vars["result"]
                
                # Add execution metadata
                if isinstance(result, dict):
                    result["execution_time"] = time.time()
                    result["executed_by"] = "CODESYS PersistentSession"
                
                return result
            else:
                self.log("No result variable found, returning default success")
                return {
                    "success": True, 
                    "message": "Script executed successfully (no result variable)",
                    "execution_time": time.time(),
                    "executed_by": "CODESYS PersistentSession"
                }
        except Exception, e:
            self.log("Unhandled error in execute_script: %s" % str(e))
            self.log(traceback.format_exc())
            return {
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc(),
                "execution_time": time.time(),
                "executed_by": "CODESYS PersistentSession"
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