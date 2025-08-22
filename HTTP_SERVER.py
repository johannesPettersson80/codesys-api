#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CODESYS API HTTP Server

This script implements a HTTP server for the CODESYS API wrapper.
It provides RESTful endpoints to interact with CODESYS through
a persistent session.

Note: This script requires Python 3.x.
Only the PERSISTENT_SESSION.py script maintains compatibility with
CODESYS IronPython environment.
"""

import sys
import os
import json
import time
import subprocess
import threading
import tempfile
import uuid
import shutil
import logging
import traceback

# Python 3 compatibility imports
try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import urllib.parse as urlparse
except ImportError:
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
    import urlparse

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='codesys_api_server.log'
)
logger = logging.getLogger('codesys_api_server')

# Constants
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080
CODESYS_PATH = r"C:\Program Files\CODESYS 3.5.21.0\CODESYS\Common\CODESYS.exe"  # Path provided by user
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PERSISTENT_SCRIPT = os.path.join(SCRIPT_DIR, "PERSISTENT_SESSION.py")
API_KEY_FILE = os.path.join(SCRIPT_DIR, "api_keys.json")
REQUEST_DIR = os.path.join(SCRIPT_DIR, "requests")
RESULT_DIR = os.path.join(SCRIPT_DIR, "results")
TERMINATION_SIGNAL_FILE = os.path.join(SCRIPT_DIR, "terminate.signal")
STATUS_FILE = os.path.join(SCRIPT_DIR, "session_status.json")
LOG_FILE = os.path.join(SCRIPT_DIR, "session.log")

# Ensure directories exist with proper permissions
def ensure_directory(path):
    """Ensure directory exists with proper permissions."""
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            logger.info("Created directory: %s", path)
        except Exception as e:
            logger.error("Error creating directory %s: %s", path, str(e))
            raise
    
    # Check if directory is writable
    if not os.access(path, os.W_OK):
        logger.error("Directory %s is not writable", path)
        raise PermissionError("Directory {} is not writable".format(path))
    
    return path

# Create necessary directories
ensure_directory(REQUEST_DIR)
ensure_directory(RESULT_DIR)
temp_dir = tempfile.gettempdir()
ensure_directory(temp_dir)

class CodesysProcessManager:
    """Manages the CODESYS process."""
    
    def __init__(self, codesys_path, script_path):
        self.codesys_path = codesys_path
        self.script_path = script_path
        self.process = None
        self.running = False
        self.lock = threading.Lock()
        
    def start(self):
        """Start the CODESYS process.
        
        Returns:
            bool: True if process started successfully, False otherwise
        """
        with self.lock:
            try:
                # Check if CODESYS is already running
                if self.is_running():
                    logger.info("CODESYS process already running")
                    return True
                
                # Verify CODESYS executable exists
                if not os.path.exists(self.codesys_path):
                    logger.error("CODESYS executable not found at path: %s", self.codesys_path)
                    return False
                
                # Verify script exists
                if not os.path.exists(self.script_path):
                    logger.error("CODESYS script not found at path: %s", self.script_path)
                    return False
                    
                logger.info("Starting CODESYS process with script: %s", self.script_path)
                
                # Clear any existing termination signal
                if os.path.exists(TERMINATION_SIGNAL_FILE):
                    os.remove(TERMINATION_SIGNAL_FILE)
                
                # Delete any existing status file to ensure we don't detect an old one
                if os.path.exists(STATUS_FILE):
                    try:
                        os.remove(STATUS_FILE)
                        logger.info("Removed existing status file")
                    except Exception as e:
                        logger.warning("Could not remove existing status file: %s", str(e))
                
                # Create logs directory if needed
                log_dir = os.path.dirname(LOG_FILE)
                if log_dir and not os.path.exists(log_dir):
                    os.makedirs(log_dir)
                
                # Start CODESYS with script and proper Python path
                try:
                    # Get ScriptLib directory path for Python imports
                    script_lib_path = os.path.join(SCRIPT_DIR, "ScriptLib")
                    
                    # Set up environment with PYTHONPATH
                    env = os.environ.copy()
                    if "PYTHONPATH" in env:
                        env["PYTHONPATH"] = script_lib_path + os.pathsep + env["PYTHONPATH"]
                    else:
                        env["PYTHONPATH"] = script_lib_path
                    
                    logger.info("Starting CODESYS with PYTHONPATH: %s", env["PYTHONPATH"])
                    # Use the exact command format that worked in pure_test.bat
                    # Construct full command with proper quoting
                    command = f"\"{self.codesys_path}\" --runscript=\"{self.script_path}\""
                    
                    logger.info("Starting CODESYS with command: %s", command)
                    self.process = subprocess.Popen(
                        command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        env=env,
                        shell=True  # Use shell to handle the command as a string
                    )
                except subprocess.SubprocessError as se:
                    logger.error("SubprocessError starting CODESYS: %s", str(se))
                    return False
                except FileNotFoundError:
                    logger.error("CODESYS executable not found. Check the path: %s", self.codesys_path)
                    return False
                
                # Wait for process to be visibly running
                logger.info("Waiting for CODESYS process to start...")
                max_wait = 30  # seconds
                wait_interval = 1
                total_waited = 0
                
                while total_waited < max_wait:
                    time.sleep(wait_interval)
                    total_waited += wait_interval
                    
                    # Check if process is still running
                    if not self.is_running():
                        try:
                            stdout, stderr = self.process.communicate(timeout=1)
                            stderr_text = stderr.decode('utf-8', errors='replace') if stderr else "No error output"
                            stdout_text = stdout.decode('utf-8', errors='replace') if stdout else "No standard output"
                            logger.error("CODESYS process failed to start:\nStderr: %s\nStdout: %s", stderr_text, stdout_text)
                        except Exception as e:
                            logger.error("Error communicating with failed process: %s", str(e))
                        return False
                    
                    # Check if status file exists, indicating the script has started
                    if os.path.exists(STATUS_FILE):
                        logger.info("Status file detected after %.1f seconds", total_waited)
                        break
                    
                    logger.debug("Waiting for CODESYS initialization... (%.1f seconds elapsed)", total_waited)
                
                # Now wait for CODESYS to fully initialize
                # Even if status file exists, we want to wait a bit longer for full initialization
                logger.info("CODESYS process has started. Waiting for full initialization...")
                
                # Additional wait to ensure CODESYS is fully initialized
                additional_wait = 10  # seconds
                logger.info("Waiting additional %d seconds for full initialization...", additional_wait)
                time.sleep(additional_wait)
                
                # Final check if the process is running
                if not self.is_running():
                    logger.error("CODESYS process failed to initialize properly")
                    return False
                    
                # Create a status file if it doesn't exist
                # This is a workaround for when CODESYS starts but doesn't create the status file
                if not os.path.exists(STATUS_FILE):
                    logger.warning("CODESYS started but didn't create status file. Creating a default one.")
                    try:
                        with open(STATUS_FILE, 'w') as f:
                            f.write(json.dumps({
                                "state": "initialized",
                                "timestamp": time.time()
                            }))
                    except Exception as e:
                        logger.error("Error creating default status file: %s", str(e))
                    
                self.running = True
                logger.info("CODESYS process started and fully initialized")
                return True
            except Exception as e:
                logger.error("Error starting CODESYS process: %s", str(e))
                return False
                
    def stop(self):
        """Stop the CODESYS process.
        
        Returns:
            bool: True if process stopped successfully or was not running, False otherwise
        """
        with self.lock:
            if not self.is_running():
                logger.info("CODESYS process not running")
                return True
                
            try:
                logger.info("Stopping CODESYS process")
                
                # Signal termination through file
                try:
                    with open(TERMINATION_SIGNAL_FILE, 'w') as f:
                        f.write("TERMINATE")
                    logger.debug("Created termination signal file")
                except Exception as e:
                    logger.warning("Could not create termination signal file: %s", str(e))
                    # Continue with process termination anyway
                    
                # Wait for process to terminate gracefully
                max_wait = 10  # seconds
                wait_interval = 0.5
                waited = 0
                
                while waited < max_wait:
                    if not self.is_running():
                        break
                    time.sleep(wait_interval)
                    waited += wait_interval
                
                # Force termination if still running
                if self.is_running():
                    logger.info("Process still running after %s seconds, sending TERMINATE signal", waited)
                    try:
                        self.process.terminate()
                    except Exception as e:
                        logger.warning("Error terminating process: %s", str(e))
                        
                    # Wait again for termination
                    time.sleep(2)
                    
                    # Kill if still running
                    if self.is_running():
                        logger.warning("Process still running after TERMINATE signal, sending KILL signal")
                        try:
                            self.process.kill()
                        except Exception as e:
                            logger.error("Error killing process: %s", str(e))
                            return False
                
                # Clean up
                self.process = None
                self.running = False
                
                # Remove termination signal file if it exists
                if os.path.exists(TERMINATION_SIGNAL_FILE):
                    try:
                        os.remove(TERMINATION_SIGNAL_FILE)
                    except Exception as e:
                        logger.warning("Could not remove termination signal file: %s", str(e))
                
                logger.info("CODESYS process stopped successfully")
                return True
            except Exception as e:
                logger.error("Error stopping CODESYS process: %s", str(e))
                return False
                
    def is_running(self):
        """Check if CODESYS process is running."""
        if self.process is None:
            return False
            
        return self.process.poll() is None
        
    def get_status(self):
        """Get CODESYS session status."""
        try:
            if not os.path.exists(STATUS_FILE):
                return {"state": "unknown", "timestamp": time.time()}
                
            with open(STATUS_FILE, 'r') as f:
                return json.loads(f.read())
        except Exception as e:
            logger.error("Error getting CODESYS status: %s", str(e))
            return {"state": "error", "timestamp": time.time(), "error": str(e)}


class ScriptExecutor:
    """Executes scripts through the CODESYS persistent session."""
    
    def __init__(self, request_dir, result_dir):
        self.request_dir = request_dir
        self.result_dir = result_dir
        
    def execute_script(self, script_content, timeout=60):
        """Execute a script and return the result.
        
        Args:
            script_content (str): The script content to execute
            timeout (int): Timeout in seconds (default: 60 seconds)
            
        Returns:
            dict: The result of the script execution
        """
        request_id = str(uuid.uuid4())
        script_path = None
        result_path = None
        request_path = None
        
        try:
            # Log script execution start with more info
            logger.info("Executing script (request ID: %s, timeout: %s seconds)", request_id, timeout)
            script_preview = script_content[:500].replace('\n', ' ')
            logger.info("Script preview: %s...", script_preview)
            
            # Create dedicated directory for this request to avoid path issues
            request_dir = os.path.join(tempfile.gettempdir(), f"codesys_req_{request_id}")
            if not os.path.exists(request_dir):
                os.makedirs(request_dir)
                logger.debug("Created request directory: %s", request_dir)
            
            # Create temporary script file with UTF-8 encoding explicitly
            script_path = os.path.join(request_dir, "script.py")
            try:
                with open(script_path, 'w', encoding='utf-8') as f:
                    f.write(script_content)
                logger.info("Created script file: %s", script_path)
                logger.debug("Script file size: %d bytes", os.path.getsize(script_path))
            except Exception as e:
                logger.error("Failed to write script file: %s", str(e))
                return {"success": False, "error": "Failed to write script file: " + str(e)}
                
            # Create result file path in same dedicated directory
            result_path = os.path.join(request_dir, "result.json")
            
            # Create request file with backslash-escaped paths for Windows
            request_path = os.path.join(self.request_dir, "{0}.request".format(request_id))
            try:
                with open(request_path, 'w', encoding='utf-8') as f:
                    # Use double backslashes for Windows path escaping
                    request_data = {
                        "script_path": script_path.replace("\\", "\\\\"),
                        "result_path": result_path.replace("\\", "\\\\"),
                        "timestamp": time.time(),
                        "request_id": request_id
                    }
                    f.write(json.dumps(request_data))
                logger.info("Created request file: %s", request_path)
                logger.debug("Request data: %s", json.dumps(request_data))
            except Exception as e:
                logger.error("Failed to write request file: %s", str(e))
                return {"success": False, "error": "Failed to write request file: " + str(e)}
                
            # Wait for result with progressive polling
            logger.info("Waiting for script execution to complete (max: %s seconds)...", timeout)
            start_time = time.time()
            check_count = 0
            last_log_time = start_time
            
            # Use progressive polling intervals - start fast, then get slower
            poll_interval = 0.1  # Start with checking every 100ms
            
            while time.time() - start_time < timeout:
                check_count += 1
                
                # Check for result file
                if os.path.exists(result_path):
                    # Log result found
                    elapsed = time.time() - start_time
                    logger.info("Result file found after %.2f seconds (%d checks)", elapsed, check_count)
                    
                    # Read result with retry for potentially incomplete files
                    retry_count = 0
                    max_retries = 5
                    file_size = os.path.getsize(result_path)
                    
                    while retry_count < max_retries:
                        try:
                            # Wait a moment for the file to be fully written
                            time.sleep(0.2)
                            
                            # Check if file size changed
                            new_size = os.path.getsize(result_path)
                            if new_size != file_size:
                                logger.debug("Result file size changed from %d to %d bytes, waiting...", 
                                            file_size, new_size)
                                file_size = new_size
                                retry_count += 1
                                continue
                            
                            with open(result_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                try:
                                    result = json.loads(content)
                                    
                                    # Log result summary
                                    if result.get('success', False):
                                        logger.info("Script execution successful")
                                    else:
                                        error = result.get('error', 'Unknown error')
                                        logger.warning("Script execution failed: %s", error)
                                    
                                    # Cleanup files
                                    self._cleanup_files(script_path, result_path, request_path, request_dir)
                                    
                                    return result
                                except json.JSONDecodeError as je:
                                    logger.warning("Invalid JSON in result file (attempt %d/%d): %s", 
                                                 retry_count+1, max_retries, str(je))
                                    logger.debug("Result file content: %s", content)
                                    
                                    # Try again after a short delay
                                    retry_count += 1
                                    time.sleep(0.5)
                        except Exception as e:
                            logger.warning("Error reading result file (attempt %d/%d): %s", 
                                         retry_count+1, max_retries, str(e))
                            retry_count += 1
                            time.sleep(0.5)
                    
                    # If we get here, we've exhausted retries
                    logger.error("Failed to read valid result after %d retries", max_retries)
                    return {"success": False, "error": f"Failed to read valid result after {max_retries} retries"}
                
                # Periodic status logging
                current_time = time.time()
                if current_time - last_log_time > 10:  # Log every 10 seconds
                    elapsed = current_time - start_time
                    logger.info("Still waiting for script execution (elapsed: %.2f seconds, checks: %d)", 
                               elapsed, check_count)
                    
                    # Log if script and request files still exist
                    if os.path.exists(script_path):
                        logger.debug("Script file still exists (%d bytes)", os.path.getsize(script_path))
                    else:
                        logger.warning("Script file no longer exists!")
                        
                    if os.path.exists(request_path):
                        logger.debug("Request file still exists (%d bytes)", os.path.getsize(request_path))
                    else:
                        logger.warning("Request file no longer exists!")
                    
                    last_log_time = current_time
                            
                # Progressive polling - start fast, then slow down
                current_elapsed = time.time() - start_time
                if current_elapsed < 5:
                    poll_interval = 0.1  # First 5 seconds: check every 100ms
                elif current_elapsed < 30:
                    poll_interval = 0.5  # 5-30 seconds: check every 500ms
                else:
                    poll_interval = 1.0  # After 30 seconds: check every second
                
                time.sleep(poll_interval)
            
            # If we've timed out, don't create a fake success - report the timeout as an error
            logger.error("Script execution timed out after %.2f seconds", time.time() - start_time)
            
            # Create an error result file for future reference
            try:
                with open(result_path, 'w', encoding='utf-8') as f:
                    error_result = {
                        "success": False, 
                        "error": "Script execution timed out after {:.2f} seconds".format(time.time() - start_time),
                        "timeout": True
                    }
                    json.dump(error_result, f)
            except Exception as e:
                logger.error("Error creating timeout result file: %s", str(e))
            
            # Clean up files
            self._cleanup_files(script_path, None, request_path, request_dir)
            
            # Return error response
            return {
                "success": False, 
                "error": "Script execution timed out after {:.2f} seconds".format(time.time() - start_time),
                "timeout": True
            }
            
            # Timeout
            elapsed = time.time() - start_time
            logger.error("Script execution timed out after %.2f seconds (%d checks)", elapsed, check_count)
            
            # Create error result file for reference
            try:
                with open(result_path, 'w', encoding='utf-8') as f:
                    error_result = {
                        "success": False,
                        "error": f"Script execution timed out after {timeout} seconds",
                        "checks": check_count,
                        "request_id": request_id
                    }
                    json.dump(error_result, f)
                logger.debug("Created timeout error result file")
            except Exception as e:
                logger.error("Error creating timeout error result file: %s", str(e))
            
            # Clean up files but keep script for debugging
            self._cleanup_files(None, None, request_path, None)
            logger.info("Kept script file for debugging: %s", script_path)
            
            return {
                "success": False, 
                "error": f"Script execution timed out after {timeout} seconds",
                "script_path": script_path,
                "result_path": result_path,
                "request_id": request_id
            }
        except Exception as e:
            logger.error("Error executing script (request ID: %s): %s", request_id, str(e))
            logger.error(traceback.format_exc())
            # Attempt to clean up files
            if script_path or result_path or request_path:
                self._cleanup_files(script_path, result_path, request_path, request_dir)
            return {"success": False, "error": str(e)}
            
    def _cleanup_files(self, script_path, result_path, request_path, request_dir=None):
        """Clean up temporary files.
        
        Args:
            script_path (str): Path to the script file
            result_path (str): Path to the result file
            request_path (str): Path to the request file
            request_dir (str): Path to the request directory (optional)
        """
        # First clean up individual files
        for path in [script_path, result_path, request_path]:
            if not path:
                continue
                
            try:
                if os.path.exists(path):
                    os.remove(path)
                    logger.debug("Removed temporary file: %s", path)
            except Exception as e:
                logger.warning("Failed to remove temporary file %s: %s", path, str(e))
        
        # Then clean up the request directory if specified
        if request_dir and os.path.exists(request_dir):
            try:
                # Check if directory is empty
                if not os.listdir(request_dir):
                    os.rmdir(request_dir)
                    logger.debug("Removed empty request directory: %s", request_dir)
                else:
                    logger.warning("Request directory not empty, not removing: %s", request_dir)
                    # List files left in directory
                    logger.debug("Files remaining in request directory: %s", os.listdir(request_dir))
            except Exception as e:
                logger.warning("Failed to remove request directory %s: %s", request_dir, str(e))


class ScriptGenerator:
    """Generates scripts for different operations."""
    
    def generate_session_start_script(self):
        """Generate script to start a session."""
        return """
import scriptengine
import json
import sys
import warnings

# Silence deprecation warnings for sys.exc_clear() in IronPython 2.7
warnings.filterwarnings("ignore", category=DeprecationWarning)

try:
    # Use the global system instance provided by scriptengine
    # IMPORTANT: scriptengine.system is a pre-existing instance
    print("Using global scriptengine.system instance")
    system = scriptengine.system
    
    # Store system instance
    session.system = system
    
    # Return success
    result = {"success": True, "message": "Session started"}
except:
    # IronPython 2.7 style exception handling (no 'as e' syntax)
    error_type, error_value, error_traceback = sys.exc_info()
    result = {"success": False, "error": str(error_value)}
"""
        
    def generate_session_status_script(self):
        """Generate script to get session status."""
        return """
import scriptengine
import json

try:
    # Get system status
    system = session.system
    
    result = {
        "success": True,
        "status": {
            "session_active": system is not None,
            "project_open": session.active_project is not None
        }
    }
    
    if session.active_project:
        result["status"]["project"] = {
            "path": session.active_project.path,
            "dirty": session.active_project.dirty
        }
except Exception as e:
    result = {"success": False, "error": str(e)}
"""
        
    def generate_project_create_script(self, params):
        """Generate script to create a project."""
        path = params.get("path", "")
        # Normalize path to use backslashes for Windows
        path = path.replace("/", "\\")
        
        # Get template_path parameter or build from CODESYS_PATH
        template_path = params.get("template_path", "")
        if not template_path:
            # Derive template path from CODESYS executable path
            codesys_dir = os.path.dirname(CODESYS_PATH)  # Get directory containing CODESYS.exe
            if "Common" in codesys_dir:  # Handle "Common" subfolder case
                codesys_dir = os.path.dirname(codesys_dir)  # Go up one level
            template_path = os.path.join(codesys_dir, "Templates", "Standard.project")
            logger.info("Using derived template path: %s", template_path)
            
        # Pass CODESYS_PATH to the script to help find templates
        codesys_path = CODESYS_PATH
            
        # Create a super simple script - just open the template and save as the new name
        return """
# Simple script to create a project from template - IronPython 2.7 compatible
import scriptengine
import json
import os
import sys
import warnings
import traceback

# Silence deprecation warnings for sys.exc_clear() in IronPython 2.7
warnings.filterwarnings("ignore", category=DeprecationWarning)

try:
    print("Starting project creation script")
    
    # Check if standard template exists at the provided path
    template_path = "{1}"
    print("Looking for template at: " + template_path)
    
    if not os.path.exists(template_path):
        print("Template not found at: " + template_path)
        
        # Try to determine template location directly from CODESYS_PATH
        codesys_path = r"{2}"
        print("CODESYS path: " + codesys_path)
        
        # Derive template path from CODESYS executable path
        codesys_dir = os.path.dirname(codesys_path)  # Get directory containing CODESYS.exe
        if "Common" in codesys_dir:  # Handle "Common" subfolder case
            codesys_dir = os.path.dirname(codesys_dir)  # Go up one level
            
        template_path = os.path.join(codesys_dir, "Templates", "Standard.project")
        print("Trying template at: " + template_path)
    
    if not os.path.exists(template_path):
        print("Template not found! Cannot create project from template.")
        raise Exception("Template not found at: " + template_path)
    
    # Simple approach: open template, save as new name
    print("Opening template: " + template_path)
    project = scriptengine.projects.open(template_path)
    if project is None:
        print("Failed to open template project")
        raise Exception("Failed to open template project at: " + template_path)
    
    print("Template opened successfully")
    
    # Save as new project name
    print("Saving as new project: {0}")
    if hasattr(project, 'save_as'):
        project.save_as("{0}")
        print("Project saved successfully as: {0}")
        # That's it! The project is now saved with our desired name and is already the active project
    else:
        print("Project has no save_as method")
        raise Exception("Project object does not have a save_as method")
    
    # Set as active project
    print("Setting as active project")
    session.active_project = project
    
    # Check active application
    print("Checking for active application")
    if hasattr(project, 'active_application') and project.active_application is not None:
        app = project.active_application
        print("Found active application: " + str(app))
    else:
        print("No active application found in project")
    
    print("Project creation completed")
    
    # Return success result
    # Note: Project is already saved to disk at this point (save_as operation handles this)
    # There's no need to call save_project() immediately after create_project()
    result = {{
        "success": True,
        "project": {{
            "path": project.path if hasattr(project, 'path') else "{0}",
            "name": project.name if hasattr(project, 'name') else os.path.basename("{0}"),
            "dirty": project.dirty if hasattr(project, 'dirty') else False
        }}
    }}
except:
    # IronPython 2.7 style exception handling (no 'as e' syntax)
    error_type, error_value, error_traceback = sys.exc_info()
    print("Error creating project: " + str(error_value))
    print(traceback.format_exc())
    
    result = {{
        "success": False,
        "error": str(error_value)
    }}
""".format(path.replace("\\", "\\\\"), template_path.replace("\\", "\\\\"), codesys_path.replace("\\", "\\\\"))
        
    def generate_project_open_script(self, params):
        """Generate script to open a project."""
        path = params.get("path", "")
        
        return """
import scriptengine
import json
import sys
import os
import traceback

try:
    print("Starting project open script")
    print("Opening project at path: {0}")
    
    # Check if global instances are available
    if not hasattr(scriptengine, 'projects'):
        print("Global scriptengine.projects instance not found")
        result = {{"success": False, "error": "Global scriptengine.projects instance not found"}}
    else:
        try:
            # Open project using the global projects instance
            print("Using global scriptengine.projects instance to open project")
            project = scriptengine.projects.open("{0}")
            
            if project is None:
                print("Project open returned None")
                result = {{"success": False, "error": "Project open operation returned None"}}
            else:
                print("Project opened successfully")
                
                # Store as active project in session
                print("Storing project as active project in session")
                session.active_project = project
                
                # Get project info for result, with careful attribute checking
                project_info = {{"path": "{0}"}}  # Always include the path that was requested
                
                # Get actual path from project object if available
                if hasattr(project, 'path'):
                    project_info['path'] = project.path
                    print("Project path: " + project.path)
                    
                    # Try to extract name from path if name attribute is missing
                    if not hasattr(project, 'name'):
                        try:
                            project_info['name'] = os.path.basename(project.path)
                            print("Extracted name from path: " + project_info['name'])
                        except Exception as name_error:
                            project_info['name'] = os.path.basename("{0}")
                            print("Error extracting name from path, using request path basename instead")
                else:
                    print("Project has no path attribute, using request path")
                
                # Check for name attribute (if not already set above)
                if 'name' not in project_info and hasattr(project, 'name'):
                    project_info['name'] = project.name
                    print("Project name: " + project.name)
                elif 'name' not in project_info:
                    # Last resort - extract from the requested path
                    project_info['name'] = os.path.basename("{0}")
                    print("Using name from request path: " + project_info['name'])
                
                # Check for dirty attribute
                if hasattr(project, 'dirty'):
                    project_info['dirty'] = project.dirty
                    print("Project dirty flag: " + str(project.dirty))
                else:
                    project_info['dirty'] = False
                    print("Project has no dirty attribute, assuming False")
                
                # Return project info
                result = {{
                    "success": True,
                    "project": project_info
                }}
                print("Project open completed successfully")
        except Exception as e:
            print("Error opening project: " + str(e))
            print(traceback.format_exc())
            result = {{"success": False, "error": "Error opening project: " + str(e)}}
except Exception as e:
    error_type, error_value, error_traceback = sys.exc_info()
    print("Error in project open script: " + str(error_value))
    print(traceback.format_exc())
    result = {{"success": False, "error": str(error_value)}}
""".format(path.replace("\\", "\\\\"))
        
    def generate_project_save_script(self):
        """Generate script to save current project."""
        return """
import scriptengine
import json
import sys
import os
import traceback

try:
    print("Starting project save script")
    
    # Check if we have an active project
    if not hasattr(session, 'active_project') or session.active_project is None:
        print("No active project in session")
        result = {"success": False, "error": "No active project in session"}
    else:
        # Get active project
        project = session.active_project
        print("Got active project")
        
        # Check if project has save method
        if not hasattr(project, 'save'):
            print("Project has no save method")
            result = {"success": False, "error": "Project object has no save method"}
        else:
            # Save project
            print("Saving project...")
            project.save()
            print("Project saved successfully")
            
            # Get project info for result, with careful attribute checking
            project_info = {}
            
            # Check for path attribute
            if hasattr(project, 'path'):
                project_info['path'] = project.path
                # Try to extract name from path if name attribute is missing
                if not hasattr(project, 'name'):
                    try:
                        project_info['name'] = os.path.basename(project.path)
                        print("Extracted name from path: " + project_info['name'])
                    except Exception as name_error:
                        project_info['name'] = "Unknown"
                        print("Error extracting name from path: " + str(name_error))
            else:
                project_info['path'] = "Unknown"
                print("Project has no path attribute")
            
            # Check for name attribute (if not already set above)
            if 'name' not in project_info and hasattr(project, 'name'):
                project_info['name'] = project.name
            
            # Check for dirty attribute
            if hasattr(project, 'dirty'):
                project_info['dirty'] = project.dirty
            else:
                project_info['dirty'] = False
                print("Project has no dirty attribute, assuming False")
            
            # Return project info
            result = {
                "success": True,
                "project": project_info
            }
            print("Project info prepared for result")
except Exception as e:
    error_type, error_value, error_traceback = sys.exc_info()
    print("Error in project save script: " + str(error_value))
    print(traceback.format_exc())
    result = {"success": False, "error": str(error_value)}
"""
        
    def generate_project_close_script(self):
        """Generate script to close current project."""
        return """
import scriptengine
import json
import sys
import os
import traceback

try:
    print("Starting project close script")
    
    # Check if we have an active project
    if not hasattr(session, 'active_project') or session.active_project is None:
        print("No active project in session")
        result = {"success": False, "error": "No active project in session"}
    else:
        # Get active project
        project = session.active_project
        print("Got active project")
        
        # Store project info for result, with careful attribute checking
        project_info = {}
        
        # Check for path attribute
        if hasattr(project, 'path'):
            project_info['path'] = project.path
            print("Project path: " + project.path)
            
            # Try to extract name from path if name attribute is missing
            if not hasattr(project, 'name'):
                try:
                    project_info['name'] = os.path.basename(project.path)
                    print("Extracted name from path: " + project_info['name'])
                except Exception as name_error:
                    project_info['name'] = "Unknown"
                    print("Error extracting name from path: " + str(name_error))
        else:
            project_info['path'] = "Unknown"
            print("Project has no path attribute")
        
        # Check for name attribute (if not already set above)
        if 'name' not in project_info and hasattr(project, 'name'):
            project_info['name'] = project.name
            print("Project name: " + project.name)
        
        # Try to close project if it has a close method
        if hasattr(project, 'close'):
            try:
                print("Closing project using project.close() method")
                project.close()
                print("Project closed via close() method")
            except Exception as close_error:
                print("Error closing project via close() method: " + str(close_error))
                print("Will still try to clear session.active_project")
        else:
            print("Project has no close() method, will just clear session.active_project")
        
        # Clear session active project
        print("Clearing session.active_project reference")
        session.active_project = None
        print("Project reference cleared from session")
        
        # Return project info
        result = {
            "success": True,
            "project": project_info
        }
        print("Project close completed successfully")
except Exception as e:
    error_type, error_value, error_traceback = sys.exc_info()
    print("Error in project close script: " + str(error_value))
    print(traceback.format_exc())
    result = {"success": False, "error": str(error_value)}
"""

    def generate_project_list_script(self):
        """Generate script to list recent projects."""
        return """
import scriptengine
import json
import os
import sys
import traceback

try:
    print("Starting project list script")
    
    # Check if global instances are available
    if not hasattr(scriptengine, 'projects'):
        print("Global scriptengine.projects instance not found")
        result = {{"success": False, "error": "Global scriptengine.projects instance not found"}}
    else:
        print("Using global scriptengine.projects instance for project listing")
        
        # Get recent projects list
        recent_projects = []
        
        try:
            # Check for recent_projects attribute on global projects instance
            if hasattr(scriptengine.projects, 'recent_projects'):
                # Direct access if available
                print("Getting projects via scriptengine.projects.recent_projects attribute")
                recent_projects = scriptengine.projects.recent_projects
            elif hasattr(scriptengine.projects, 'get_recent_projects'):
                # Function call if available
                print("Getting projects via scriptengine.projects.get_recent_projects() method")
                recent_projects = scriptengine.projects.get_recent_projects()
            else:
                print("No method found to get recent projects list")
            
            # Format project list
            print("Processing project list with " + str(len(recent_projects) if recent_projects else 0) + " projects")
            projects = []
            
            if recent_projects:
                for project in recent_projects:
                    try:
                        project_info = {{"name": "Unknown", "path": "Unknown"}}
                        
                        # Get path
                        if hasattr(project, 'path'):
                            project_info["path"] = project.path
                            print("Project path: " + project.path)
                            
                            # Try to extract name from path
                            try:
                                project_info["name"] = os.path.basename(project.path)
                                print("Extracted name from path: " + project_info["name"])
                            except Exception as name_error:
                                print("Error extracting name from path: " + str(name_error))
                        
                        # Get name if explicitly available
                        if hasattr(project, 'name'):
                            project_info["name"] = project.name
                            print("Project name: " + project.name)
                        
                        # Get last opened date if available
                        if hasattr(project, 'last_opened_date'):
                            project_info["last_opened"] = project.last_opened_date
                            print("Last opened date: " + str(project.last_opened_date))
                        
                        # Add to list
                        projects.append(project_info)
                        print("Added project to list: " + project_info["name"])
                    except Exception as project_error:
                        print("Error processing project item: " + str(project_error))
            else:
                print("No recent projects found")
            
            # Return projects list
            result = {{
                "success": True,
                "projects": projects
            }}
            print("Project list processing completed successfully")
        except Exception as e:
            print("Error processing projects list: " + str(e))
            print(traceback.format_exc())
            result = {{"success": False, "error": "Error processing projects list: " + str(e)}}
except Exception as e:
    error_type, error_value, error_traceback = sys.exc_info()
    print("Error in project list script: " + str(error_value))
    print(traceback.format_exc())
    result = {{"success": False, "error": str(error_value)}}
"""

    def generate_project_compile_script(self, params):
        """Generate script to compile a project."""
        clean_build = params.get("clean_build", False)
        
        return """
import scriptengine
import json
import time
import sys
import traceback

try:
    print("Starting project compile script")
    print("Clean build requested: {0}")
    
    # Check if we have an active project
    if not hasattr(session, 'active_project') or session.active_project is None:
        print("No active project in session")
        result = {{"success": False, "error": "No active project in session"}}
    else:
        # Get active project
        project = session.active_project
        print("Got active project")
        
        # Try to get application
        if not hasattr(project, 'active_application') or project.active_application is None:
            print("Project has no active application")
            result = {{"success": False, "error": "Project has no active application"}}
        else:
            # Get application
            application = project.active_application
            print("Got active application")
            
            # Check if application has build method
            if not hasattr(application, 'build'):
                print("Application has no build method")
                result = {{"success": False, "error": "Application object has no build method"}}
            else:
                # Start time for compilation
                start_time = time.time()
                print("Starting build process...")
                
                # Clean build if requested
                if "{0}" == "true" and hasattr(application, 'clean'):
                    try:
                        print("Performing clean build")
                        application.clean()
                        print("Clean operation completed")
                    except Exception as clean_error:
                        print("Error during clean operation: " + str(clean_error))
                        print("Will attempt to continue with build anyway")
                
                try:
                    # Compile application
                    print("Building application...")
                    build_result = application.build()
                    print("Build operation completed")
                    
                    # Calculate compilation time
                    compilation_time = time.time() - start_time
                    print("Build duration: " + str(compilation_time) + " seconds")
                    
                    # Check for errors
                    has_errors = False
                    error_count = 0
                    warning_count = 0
                    
                    # Get error information, with careful attribute checking
                    if build_result is None:
                        print("Build result is None, assuming no errors")
                    else:
                        if hasattr(build_result, 'has_errors'):
                            has_errors = build_result.has_errors
                            print("Has errors: " + str(has_errors))
                        else:
                            print("Build result has no has_errors attribute, assuming False")
                        
                        if hasattr(build_result, 'error_count'):
                            error_count = build_result.error_count
                            print("Error count: " + str(error_count))
                        else:
                            print("Build result has no error_count attribute, assuming 0")
                        
                        if hasattr(build_result, 'warning_count'):
                            warning_count = build_result.warning_count
                            print("Warning count: " + str(warning_count))
                        else:
                            print("Build result has no warning_count attribute, assuming 0")
                    
                    # If has_errors is not available, try to determine from error_count
                    if not hasattr(build_result, 'has_errors') and error_count > 0:
                        has_errors = True
                        print("Setting has_errors=True based on error_count")
                    
                    # Return compilation result
                    result = {{
                        "success": not has_errors,
                        "compilation": {{
                            "duration_seconds": compilation_time,
                            "errors": error_count,
                            "warnings": warning_count,
                            "has_errors": has_errors
                        }}
                    }}
                    print("Compilation result prepared")
                except Exception as build_error:
                    print("Error during build operation: " + str(build_error))
                    print(traceback.format_exc())
                    result = {{"success": False, "error": "Build operation failed: " + str(build_error)}}
except Exception as e:
    error_type, error_value, error_traceback = sys.exc_info()
    print("Error in project compile script: " + str(error_value))
    print(traceback.format_exc())
    result = {{"success": False, "error": str(error_value)}}
""".format("true" if clean_build else "false")
        
    def generate_pou_create_script(self, params):
        """Generate script to create a POU."""
        name = params.get("name", "")
        pou_type = params.get("type", "FunctionBlock")
        language = params.get("language", "ST")
        parent_path = params.get("parentPath", "")
        
        # Create a more robust script that handles potential enum issues
        return """
import scriptengine
import json
import sys
import traceback

try:
    print("Starting POU creation script for {0}")
    
    # Check if we have an active project
    if not hasattr(session, 'active_project') or session.active_project is None:
        print("No active project in session")
        result = {{"success": False, "error": "No active project in session"}}
    else:
        # Get active project
        project = session.active_project
        print("Got active project")
        
        # Try to get application
        if not hasattr(project, 'active_application') or project.active_application is None:
            print("Project has no active application")
            result = {{"success": False, "error": "Project has no active application"}}
        else:
            # Get application
            application = project.active_application
            print("Got active application")
            
            # The application itself should implement IecLanguageObjectContainer
            # We'll try to use it directly
            container = application
            print("Using application object directly for POU creation")
            
            # Handle parent path navigation if needed
            if "{2}":
                print("Navigating to parent path: {2}")
                try:
                    # Navigate to parent container
                    path_parts = "{2}".split('/')
                    current = application
                    for part in path_parts:
                        if not part:
                            continue
                        if hasattr(current, 'find_object'):
                            current = current.find_object(part)
                        elif hasattr(current, 'get_object'):
                            current = current.get_object(part)
                        else:
                            raise ValueError("Cannot navigate to " + part)
                    
                    if hasattr(current, 'pou_container'):
                        container = current.pou_container
                    else:
                        container = current
                    print("Navigation to parent path successful")
                except Exception as e:
                    print("Error navigating to parent path: " + str(e))
                    result = {{"success": False, "error": "Error navigating to parent path: " + str(e)}}
            
            # Use the properly defined POU types and implementation languages
            if not 'result' in locals():  # Only proceed if we haven't set an error result
                try:
                    # Map the string name to the actual PouType enum value
                    print("Determining POU type for: {1}")
                    
                    # Define POU type map according to the working example code
                    pou_type_map = {{
                        "Program": scriptengine.PouType.Program,
                        "FunctionBlock": scriptengine.PouType.FunctionBlock,
                        "Function": scriptengine.PouType.Function
                    }}
                    
                    # Get the POU type from the map
                    if "{1}" in pou_type_map:
                        pou_type_value = pou_type_map["{1}"]
                        print("Set POU type to {1}")
                    else:
                        print("Unknown POU type: {1}")
                        result = {{"success": False, "error": "Unknown POU type: {1}"}}
                        
                    # Set language to None (let CODESYS default based on parent/settings)
                    language_value = None
                    print("Using default language: ST (None)")
                    
                    # Handle return type for functions
                    return_type = None
                    if "{1}" == "Function":
                        # For functions, return type is required - use INT as default
                        return_type = "INT" 
                        print("Setting return type for function: INT")
                except Exception as e:
                    print("Error resolving type values: " + str(e))
                    result = {{"success": False, "error": "Error resolving type values: " + str(e)}}
            
            # Create POU with the correct parameters
            if not 'result' in locals() and 'pou_type_value' in locals() and pou_type_value is not None:
                try:
                    print("Creating POU: {0}")
                    
                    # Call with keyword arguments as shown in the example
                    if "{1}" == "Function":
                        # For functions, return_type is required
                        pou = container.create_pou(
                            name="{0}",
                            type=pou_type_value,
                            language=language_value,
                            return_type=return_type
                        )
                        print("Created function with return type")
                    else:
                        # For programs and function blocks, return_type should not be specified
                        pou = container.create_pou(
                            name="{0}",
                            type=pou_type_value,
                            language=language_value
                        )
                        print("Created POU without return type")
                    
                    if pou is not None:
                        print("POU created successfully")
                        result = {{
                            "success": True,
                            "pou": {{
                                "name": "{0}",
                                "type": "{1}",
                                "language": "{3}"
                            }}
                        }}
                    else:
                        print("POU creation failed - returned None")
                        result = {{"success": False, "error": "POU creation failed - returned None"}}
                except Exception as e:
                    print("Error creating POU: " + str(e))
                    result = {{"success": False, "error": "Error creating POU: " + str(e)}}
except Exception as e:
    error_type, error_value, error_traceback = sys.exc_info()
    print("Error in POU creation script: " + str(error_value))
    print(traceback.format_exc())
    result = {{"success": False, "error": str(error_value)}}
""".format(name, pou_type, parent_path, language)
        
    def generate_pou_code_script(self, params):
        """Generate script to set POU code."""
        pou_path = params.get("path", "")
        code = params.get("code", "")
        
        # Escape code for string literal
        code = code.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        
        # Ensure path includes Application prefix if not present
        if not pou_path.startswith("Application/") and not pou_path.startswith("application/"):
            # Add Application/ prefix if not already there
            full_pou_path = "Application/" + pou_path
        else:
            full_pou_path = pou_path
            
        return """
import scriptengine
import json
import sys
import traceback

# Robust object finding function based on working implementation 
def find_object_by_path_robust(start_node, full_path, target_type_name="object"):
    print("Finding " + target_type_name + " by path: '" + full_path + "'")
    normalized_path = full_path.replace('\\\\\\\\', '/').strip('/')
    path_parts = normalized_path.split('/')
    if not path_parts:
        print("ERROR: Path is empty.")
        return None

    # Determine the actual starting node (project or application)
    project = start_node  # Assume start_node is project initially
    if not hasattr(start_node, 'active_application') and hasattr(start_node, 'project'):
         # If start_node is not project but has project ref (e.g., an application), get the project
         try: 
             project = start_node.project
         except Exception as proj_ref_err:
             print("WARN: Could not get project reference from start_node: " + str(proj_ref_err))
             # Proceed assuming start_node might be the project anyway or search fails

    # Try to get the application object robustly if we think we have the project
    app = None
    if hasattr(project, 'active_application'):
        try: 
            app = project.active_application
        except Exception: 
            pass  # Ignore errors getting active app
        
        if not app:
            try:
                 # Try to find the application by traversing objects
                 if hasattr(project, 'objects'):
                     for obj in project.objects:
                         if hasattr(obj, 'get_name') and obj.get_name() == "Application":
                             app = obj
                             break
            except Exception: 
                pass

    # Check if the first path part matches the application name
    app_name_lower = ""
    if app:
        try: 
            app_name_lower = (app.get_name() or "application").lower()
        except Exception: 
            app_name_lower = "application"  # Fallback

    # Decide where to start the traversal
    current_obj = start_node  # Default to the node passed in
    if hasattr(project, 'active_application'):  # Only adjust if start_node was likely the project
        if app and path_parts[0].lower() == app_name_lower:
             print("Path starts with Application name '" + path_parts[0] + "'. Beginning search there.")
             current_obj = app
             path_parts = path_parts[1:]  # Consume the app name part
             # If path was *only* the application name
             if not path_parts:
                 print("Target path is the Application object itself.")
                 return current_obj
        else:
            print("Path does not start with Application name. Starting search from project root.")
            current_obj = project  # Start search from the project root
    else:
         print("Starting search from originally provided node.")

    # Traverse the remaining path parts
    parent_path_str = current_obj.get_name() if hasattr(current_obj, 'get_name') else str(current_obj)

    for i, part_name in enumerate(path_parts):
        is_last_part = (i == len(path_parts) - 1)
        print("Searching for part [" + str(i+1) + "/" + str(len(path_parts)) + "]: '" + part_name + "' under '" + parent_path_str + "'")
        found_in_parent = None
        
        try:
            # Try various methods to find the child object by name
            if hasattr(current_obj, 'find_object'):
                try:
                    found_in_parent = current_obj.find_object(part_name)
                    if found_in_parent:
                        print("Found via find_object")
                except Exception as e:
                    print("Error with find_object: " + str(e))
            
            if not found_in_parent and hasattr(current_obj, 'get_object'):
                try:
                    found_in_parent = current_obj.get_object(part_name)
                    if found_in_parent:
                        print("Found via get_object")
                except Exception as e:
                    print("Error with get_object: " + str(e))
            
            if not found_in_parent and hasattr(current_obj, 'objects'):
                try:
                    for obj in current_obj.objects:
                        if hasattr(obj, 'name') and obj.name == part_name:
                            found_in_parent = obj
                            print("Found via objects collection")
                            break
                        if hasattr(obj, 'get_name') and obj.get_name() == part_name:
                            found_in_parent = obj
                            print("Found via get_name method")
                            break
                except Exception as e:
                    print("Error iterating objects: " + str(e))
            
            # Update current object if found
            if found_in_parent:
                current_obj = found_in_parent
                parent_path_str = current_obj.get_name() if hasattr(current_obj, 'get_name') else part_name
                print("Stepped into '" + parent_path_str + "'")
            else:
                # If not found at any point, the path is invalid from this parent
                print("ERROR: Path part '" + part_name + "' not found under '" + parent_path_str + "'")
                return None  # Path broken

        except Exception as find_err:
            print("ERROR: Exception while searching for '" + part_name + "' under '" + parent_path_str + "': " + str(find_err))
            print(traceback.format_exc())
            return None  # Error during search

    print("Found object: " + (current_obj.get_name() if hasattr(current_obj, 'get_name') else "Unnamed"))
    return current_obj


try:
    print("Starting POU code setting script for {0}")
    
    # Check if we have an active project
    if not hasattr(session, 'active_project') or session.active_project is None:
        print("No active project in session")
        result = {{"success": False, "error": "No active project in session"}}
    else:
        # Get active project
        project = session.active_project
        print("Got active project")
        
        # Use robust object finding method
        try:
            full_path = "{1}"
            print("Using full POU path: " + full_path)
            
            # Find the POU using the robust path finder
            pou = find_object_by_path_robust(project, full_path, "POU")
            
            if not pou:
                print("POU not found using robust path finder: " + full_path)
                result = {{"success": False, "error": "POU not found: " + full_path}}
            else:
                # POU was found
                pou_name = pou.get_name() if hasattr(pou, 'get_name') else full_path.split('/')[-1]
                print("Found POU: " + pou_name)
                
                # Set implementation code using textual_implementation approach as shown in working example
                print("Found POU, setting implementation code")
                
                # Try to use the working approach from set_pou_code.py
                if hasattr(pou, 'textual_implementation'):
                    impl_obj = pou.textual_implementation
                    if impl_obj and hasattr(impl_obj, 'replace'):
                        try:
                            print("Setting implementation using textual_implementation.replace()")
                            impl_obj.replace("{2}")
                            print("Updated POU implementation code successfully")
                            
                            # Save the project to persist changes
                            try:
                                print("Saving project after code change...")
                                project.save()
                                print("Project saved successfully")
                            except Exception as save_err:
                                print("Warning: Failed to save project after code change: " + str(save_err))
                            
                            # Return success
                            result = {{
                                "success": True,
                                "message": "POU code updated",
                                "pou": {{
                                    "name": pou_name,
                                    "path": "{0}"
                                }}
                            }}
                        except Exception as impl_err:
                            print("Error setting implementation: " + str(impl_err))
                            print(traceback.format_exc())
                            result = {{
                                "success": False,
                                "error": "Error setting implementation: " + str(impl_err)
                            }}
                    else:
                        print("textual_implementation exists but lacks replace method")
                        result = {{
                            "success": False,
                            "error": "POU textual_implementation doesn't have replace method"
                        }}
                else:
                    # Fall back to other methods as a last resort
                    print("POU doesn't have textual_implementation attribute, trying alternatives")
                    if hasattr(pou, 'set_implementation_code'):
                        try:
                            pou.set_implementation_code("{2}")
                            print("Updated POU implementation via set_implementation_code")
                            result = {{
                                "success": True,
                                "message": "POU code updated",
                                "pou": {{
                                    "name": pou_name,
                                    "path": "{0}"
                                }}
                            }}
                        except Exception as e:
                            print("Error using set_implementation_code: " + str(e))
                            result = {{"success": False, "error": str(e)}}
                    else:
                        # No suitable method found
                        print("No method found to update POU code, object type: " + str(type(pou)))
                        result = {{
                            "success": False,
                            "error": "POU found but no method to update its code was found"
                        }}
        except Exception as e:
            print("Error processing POU path: " + str(e))
            print(traceback.format_exc())
            result = {{"success": False, "error": "Error processing POU path: " + str(e)}}
except Exception as e:
    error_type, error_value, error_traceback = sys.exc_info()
    print("Error in POU code setting script: " + str(error_value))
    print(traceback.format_exc())
    result = {{"success": False, "error": str(error_value)}}
""".format(pou_path, full_pou_path, code)

    def generate_pou_list_script(self, params):
        """Generate script to list POUs in the project."""
        parent_path = params.get("parentPath", "")
        
        return """
import scriptengine
import json
import sys
import traceback

try:
    print("Starting POU listing script")
    # Don't use walrus operator (:=) as it's not compatible with IronPython
    parent_path = "{0}"
    if parent_path:
        print("Looking for POUs in parent path: " + parent_path)
    else:
        print("Looking for POUs at application level")
    
    # Check if we have an active project
    if not hasattr(session, 'active_project') or session.active_project is None:
        print("No active project in session")
        result = {{"success": False, "error": "No active project in session"}}
    else:
        # Get active project
        project = session.active_project
        print("Got active project")
        
        # Try to get application
        if not hasattr(project, 'active_application') or project.active_application is None:
            print("Project has no active application")
            result = {{"success": False, "error": "Project has no active application"}}
        else:
            # Get application
            application = project.active_application
            print("Got active application")
            
            # Start with application as container
            container = application
            container_name = "application"
            
            # Navigate to parent container if specified
            if "{0}":
                try:
                    print("Navigating to parent path...")
                    path_parts = "{0}".split('/')
                    for part in path_parts:
                        if not part:
                            continue
                        
                        print("Navigating to: " + part)
                        found = False
                        
                        # Try find_object method
                        if hasattr(container, 'find_object'):
                            try:
                                obj = container.find_object(part)
                                if obj is not None:
                                    container = obj
                                    container_name = part
                                    found = True
                                    print("Found via find_object")
                            except Exception as nfe:
                                print("Error using find_object: " + str(nfe))
                        
                        # Try get_object method if find_object failed or doesn't exist
                        if not found and hasattr(container, 'get_object'):
                            try:
                                obj = container.get_object(part)
                                if obj is not None:
                                    container = obj
                                    container_name = part
                                    found = True
                                    print("Found via get_object")
                            except Exception as nge:
                                print("Error using get_object: " + str(nge))
                        
                        # Try to iterate through objects collection if other methods failed
                        if not found and hasattr(container, 'objects'):
                            for obj in container.objects:
                                if hasattr(obj, 'name') and obj.name == part:
                                    container = obj
                                    container_name = part
                                    found = True
                                    print("Found via objects collection")
                                    break
                        
                        # If still not found, raise error
                        if not found:
                            raise ValueError("Cannot navigate to " + part + ", object not found by any method")
                    
                    print("Navigation complete, at container: " + container_name)
                except Exception as e:
                    print("Error navigating to path: " + str(e))
                    print(traceback.format_exc())
                    result = {{"success": False, "error": "Error navigating to path: " + str(e)}}
            
            # Only proceed if we haven't set an error result yet
            if 'result' not in locals():
                print("Looking for POUs in container: " + container_name)
                
                # Get POUs
                pous = []
                
                # Try different methods to get POUs depending on CODESYS API version
                try:
                    # Method 1: Get POUs from container's pou_container
                    if hasattr(container, 'pou_container'):
                        print("Container has pou_container")
                        pou_container = container.pou_container
                        
                        if hasattr(pou_container, 'pous'):
                            print("Getting POUs from pou_container.pous")
                            pous_list = pou_container.pous
                            for pou in pous_list:
                                try:
                                    pou_type = "Unknown"
                                    if hasattr(pou, 'type'):
                                        pou_type = str(pou.type).split('.')[-1]
                                    
                                    language = "Unknown"
                                    if hasattr(pou, 'implementation_language'):
                                        language = str(pou.implementation_language).split('.')[-1]
                                    
                                    pou_name = str(pou.name) if hasattr(pou, 'name') else "UnknownName"
                                    
                                    pous.append({{
                                        "name": pou_name,
                                        "type": pou_type,
                                        "language": language
                                    }})
                                    print("Added POU: " + pou_name)
                                except Exception as pou_error:
                                    print("Error processing POU: " + str(pou_error))
                    
                    # Method 2: Direct access to pous attribute
                    elif hasattr(container, 'pous'):
                        print("Getting POUs from container.pous")
                        pous_list = container.pous
                        for pou in pous_list:
                            try:
                                pou_type = "Unknown"
                                if hasattr(pou, 'type'):
                                    pou_type = str(pou.type).split('.')[-1]
                                
                                language = "Unknown"
                                if hasattr(pou, 'implementation_language'):
                                    language = str(pou.implementation_language).split('.')[-1]
                                
                                pou_name = str(pou.name) if hasattr(pou, 'name') else "UnknownName"
                                
                                pous.append({{
                                    "name": pou_name,
                                    "type": pou_type,
                                    "language": language
                                }})
                                print("Added POU: " + pou_name)
                            except Exception as pou_error:
                                print("Error processing POU: " + str(pou_error))
                    
                    # Method 3: Get POUs through get_pous method
                    elif hasattr(container, 'get_pous'):
                        print("Getting POUs from container.get_pous()")
                        pous_list = container.get_pous()
                        for pou in pous_list:
                            try:
                                pou_type = "Unknown"
                                if hasattr(pou, 'type'):
                                    pou_type = str(pou.type).split('.')[-1]
                                
                                language = "Unknown"
                                if hasattr(pou, 'implementation_language'):
                                    language = str(pou.implementation_language).split('.')[-1]
                                
                                pou_name = str(pou.name) if hasattr(pou, 'name') else "UnknownName"
                                
                                pous.append({{
                                    "name": pou_name,
                                    "type": pou_type,
                                    "language": language
                                }})
                                print("Added POU: " + pou_name)
                            except Exception as pou_error:
                                print("Error processing POU: " + str(pou_error))
                    
                    # Method 4: Try to iterate over objects
                    elif hasattr(container, 'objects'):
                        print("Trying to find POUs by iterating through container.objects")
                        try:
                            for obj in container.objects:
                                try:
                                    # Check if this looks like a POU
                                    if (hasattr(obj, 'name') and 
                                        (hasattr(obj, 'type') or 
                                         hasattr(obj, 'implementation_language') or
                                         hasattr(obj, 'implementation'))):
                                        
                                        pou_type = "Unknown"
                                        if hasattr(obj, 'type'):
                                            pou_type = str(obj.type).split('.')[-1]
                                        
                                        language = "Unknown"
                                        if hasattr(obj, 'implementation_language'):
                                            language = str(obj.implementation_language).split('.')[-1]
                                        elif hasattr(obj, 'implementation') and hasattr(obj.implementation, 'language'):
                                            language = str(obj.implementation.language).split('.')[-1]
                                        
                                        pou_name = str(obj.name)
                                        
                                        pous.append({{
                                            "name": pou_name,
                                            "type": pou_type,
                                            "language": language
                                        }})
                                        print("Added potential POU: " + pou_name)
                                except Exception as obj_error:
                                    print("Error processing object: " + str(obj_error))
                        except Exception as iter_error:
                            print("Error iterating container objects: " + str(iter_error))
                    else:
                        print("No method found to list POUs in this container")
                        
                    # Return POUs list, even if empty
                    print("Found " + str(len(pous)) + " POUs")
                    result = {{
                        "success": True,
                        "pous": pous,
                        "container": container_name
                    }}
                except Exception as e:
                    print("Error getting POUs: " + str(e))
                    print(traceback.format_exc())
                    result = {{"success": False, "error": "Error getting POUs: " + str(e)}}
except Exception as e:
    error_type, error_value, error_traceback = sys.exc_info()
    print("Error in POU listing script: " + str(error_value))
    print(traceback.format_exc())
    result = {{"success": False, "error": str(error_value)}}
""".format(parent_path)
        
    def generate_script_execute_script(self, params):
        """Generate script to execute custom script."""
        script = params.get("script", "")
        
        return script


class ApiKeyManager:
    """Manages API keys for authentication."""
    
    def __init__(self, key_file_path):
        self.key_file_path = key_file_path
        self.keys = self._load_keys()
        
    def _load_keys(self):
        """Load API keys from file."""
        if not os.path.exists(self.key_file_path):
            # Create default admin key
            keys = {"admin": {"name": "Admin", "created": time.time()}}
            self._save_keys(keys)
            return keys
            
        try:
            with open(self.key_file_path, 'r') as f:
                return json.loads(f.read())
        except:
            return {}
            
    def _save_keys(self, keys):
        """Save API keys to file."""
        with open(self.key_file_path, 'w') as f:
            f.write(json.dumps(keys))
            
    def validate_key(self, key):
        """Validate an API key."""
        return key in self.keys


class CodesysApiHandler(BaseHTTPRequestHandler):
    """HTTP request handler for CODESYS API."""
    
    server_version = "CodesysApiServer/0.1"
    
    def __init__(self, *args, **kwargs):
        self.process_manager = kwargs.pop('process_manager', None)
        self.script_executor = kwargs.pop('script_executor', None)
        self.script_generator = kwargs.pop('script_generator', None)
        self.api_key_manager = kwargs.pop('api_key_manager', None)
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)
        
    def do_GET(self):
        """Handle GET requests."""
        try:
            # Parse URL
            parsed_url = urlparse.urlparse(self.path)
            path = parsed_url.path.strip('/')
            query = urlparse.parse_qs(parsed_url.query)
            
            # Single-value query params
            params = {}
            for key, values in query.items():
                if values:
                    params[key] = values[0]
                    
            # Check authentication
            if not self.authenticate():
                self.send_error(401, "Unauthorized")
                return
                
            # Route request
            if path == "api/v1/session/status":
                self.handle_session_status()
            elif path == "api/v1/project/list":
                self.handle_project_list()
            elif path == "api/v1/pou/list":
                self.handle_pou_list(params)
            elif path == "api/v1/system/info":
                self.handle_system_info()
            elif path == "api/v1/system/logs":
                self.handle_system_logs()
            else:
                self.send_error(404, "Not Found")
        except ConnectionAbortedError as e:
            logger.warning("Connection aborted during GET request: %s", str(e))
            # Don't try to send an error response as the connection is already broken
        except BrokenPipeError as e:
            logger.warning("Broken pipe during GET request: %s", str(e))
            # Don't try to send an error response as the connection is already broken
        except ConnectionResetError as e:
            logger.warning("Connection reset during GET request: %s", str(e))
            # Don't try to send an error response as the connection is already broken
        except Exception as e:
            logger.error("Error handling GET request: %s", str(e))
            try:
                self.send_error(500, str(e))
            except (ConnectionAbortedError, BrokenPipeError, ConnectionResetError):
                # Connection already closed, can't send error
                pass
            
    def do_POST(self):
        """Handle POST requests."""
        try:
            # Parse URL
            parsed_url = urlparse.urlparse(self.path)
            path = parsed_url.path.strip('/')
            
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            
            # Python 3 compatibility for reading binary data
            if sys.version_info[0] >= 3:
                post_data = self.rfile.read(content_length).decode('utf-8')
            else:
                post_data = self.rfile.read(content_length)
            
            params = {}
            if content_length > 0:
                params = json.loads(post_data)
                
            # Check authentication
            if not self.authenticate():
                self.send_error(401, "Unauthorized")
                return
                
            # Route request
            if path == "api/v1/session/start":
                self.handle_session_start()
            elif path == "api/v1/session/stop":
                self.handle_session_stop()
            elif path == "api/v1/session/restart":
                self.handle_session_restart()
            elif path == "api/v1/project/create":
                self.handle_project_create(params)
            elif path == "api/v1/project/open":
                self.handle_project_open(params)
            elif path == "api/v1/project/save":
                self.handle_project_save()
            elif path == "api/v1/project/close":
                self.handle_project_close()
            elif path == "api/v1/project/compile":
                self.handle_project_compile(params)
            elif path == "api/v1/pou/create":
                self.handle_pou_create(params)
            elif path == "api/v1/pou/code":
                self.handle_pou_code(params)
            elif path == "api/v1/script/execute":
                self.handle_script_execute(params)
            else:
                self.send_error(404, "Not Found")
        except ConnectionAbortedError as e:
            logger.warning("Connection aborted during POST request: %s", str(e))
            # Don't try to send an error response as the connection is already broken
        except BrokenPipeError as e:
            logger.warning("Broken pipe during POST request: %s", str(e))
            # Don't try to send an error response as the connection is already broken
        except ConnectionResetError as e:
            logger.warning("Connection reset during POST request: %s", str(e))
            # Don't try to send an error response as the connection is already broken
        except Exception as e:
            logger.error("Error handling POST request: %s", str(e))
            try:
                self.send_error(500, str(e))
            except (ConnectionAbortedError, BrokenPipeError, ConnectionResetError):
                # Connection already closed, can't send error
                pass
            
    def authenticate(self):
        """Validate API key."""
        auth_header = self.headers.get('Authorization', '')
        
        if auth_header.startswith('ApiKey '):
            api_key = auth_header[7:]  # Remove 'ApiKey ' prefix
            return self.api_key_manager.validate_key(api_key)
            
        return False
        
    def send_json_response(self, data, status=200):
        """Send JSON response."""
        try:
            response = json.dumps(data)
            
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            
            # Python 3 compatibility for content length
            if sys.version_info[0] >= 3:
                self.send_header('Content-Length', len(response.encode('utf-8')))
            else:
                self.send_header('Content-Length', len(response))
                
            self.end_headers()
            
            # Python 3 compatibility for writing binary data
            if sys.version_info[0] >= 3:
                self.wfile.write(response.encode('utf-8'))
            else:
                self.wfile.write(response)
        except ConnectionAbortedError as e:
            logger.warning("Connection aborted while sending response: %s", str(e))
        except BrokenPipeError as e:
            logger.warning("Broken pipe while sending response: %s", str(e))
        except ConnectionResetError as e:
            logger.warning("Connection reset while sending response: %s", str(e))
        except Exception as e:
            logger.error("Error sending JSON response: %s", str(e))
        
    # Handler methods
    
    def handle_session_start(self):
        """Handle session/start endpoint."""
        try:
            logger.info("Session start requested - checking CODESYS process")
            
            # First check if the process is already running
            if self.process_manager.is_running():
                logger.info("CODESYS process already running, using existing process")
            else:
                logger.info("CODESYS process not running, attempting to start")
                
                # Start the CODESYS process
                if not self.process_manager.start():
                    error_msg = "Failed to start CODESYS process"
                    logger.error(error_msg)
                    self.send_json_response({
                        "success": False,
                        "error": error_msg
                    }, 500)
                    return
                    
                logger.info("CODESYS process started successfully")
            
            # Generate the session start script
            script = self.script_generator.generate_session_start_script()
            
            # Execute the script to properly initialize the session
            logger.info("Executing session start script in CODESYS")
            result = self.script_executor.execute_script(script)
            
            # Return the result from the script execution
            self.send_json_response(result)
            
            # Remove all the commented out code that was causing indentation errors
                
        except Exception as e:
            logger.error("Unhandled error in session start: %s", str(e), exc_info=True)
            self.send_json_response({
                "success": False,
                "error": f"Internal server error: {str(e)}"
            }, 500)
            
    def handle_session_stop(self):
        """Handle session/stop endpoint."""
        if not self.process_manager.stop():
            self.send_json_response({
                "success": False,
                "error": "Failed to stop CODESYS session"
            }, 500)
            return
            
        self.send_json_response({
            "success": True,
            "message": "Session stopped"
        })
        
    def handle_session_restart(self):
        """Handle session/restart endpoint."""
        self.process_manager.stop()
        time.sleep(2)
        
        if not self.process_manager.start():
            self.send_json_response({
                "success": False,
                "error": "Failed to restart CODESYS session"
            }, 500)
            return
            
        # Generate the session start script
        script = self.script_generator.generate_session_start_script()
        
        # Execute the script to properly initialize the session
        logger.info("Executing session start script in CODESYS after restart")
        result = self.script_executor.execute_script(script)
        
        # Return the result from the script execution
        self.send_json_response(result)
            
    def handle_session_status(self):
        """Handle session/status endpoint."""
        # Check process status
        process_running = self.process_manager.is_running()
        process_status = self.process_manager.get_status()
        
        # Execute the script to get actual session status
        if process_running:
            script = self.script_generator.generate_session_status_script()
            logger.info("Executing session status script in CODESYS")
            status_result = self.script_executor.execute_script(script)
            
            if status_result.get("success", False) and "status" in status_result:
                session_status = status_result["status"]
            else:
                session_status = {"active": process_running, "session_active": process_running, "project_open": False}
        else:
            session_status = {"active": False, "session_active": False, "project_open": False}
                
        # Combine status information
        status = {
            "process": {
                "running": process_running,
                "state": process_status.get("state", "unknown"),
                "timestamp": process_status.get("timestamp", time.time())
            },
            "session": session_status
        }
        
        self.send_json_response({
            "success": True,
            "status": status
        })
        
    def handle_project_create(self, params):
        """Handle project/create endpoint."""
        if "path" not in params:
            # If path is not provided, use the current directory
            script_dir = os.path.dirname(os.path.abspath(__file__))
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            default_path = os.path.join(script_dir, f"CODESYS_Project_{timestamp}.project")
            logger.info("No path provided, using default path: %s", default_path)
            params["path"] = default_path
        
        # Allow specifying a template path (optional)
        template_path = params.get("template_path", "")
        if template_path:
            logger.info("Using template from: %s", template_path)
        else:
            logger.info("No template specified, will try to use standard template")
        
        path = params.get("path", "")
        # Normalize path to use backslashes for Windows
        path = path.replace("/", "\\")
        logger.info("Project creation request for path: %s (executing script in CODESYS)", path)
        
        # Make sure CODESYS is running and fully initialized
        if not self.process_manager.is_running():
            logger.warning("CODESYS not running, attempting to start it")
            if not self.process_manager.start():
                error_msg = "Failed to start CODESYS process"
                logger.error(error_msg)
                self.send_json_response({
                    "success": False,
                    "error": error_msg
                }, 500)
                return
            # The start method now includes a wait for full initialization
        
        # Generate the script (IronPython 2.7 compatible)
        script = self.script_generator.generate_project_create_script(params)
        
        logger.info("Executing project creation script in CODESYS")
        # Execute the script with a reasonable timeout
        result = self.script_executor.execute_script(script, timeout=30)
        
        logger.info("Script execution result: %s", result)
        
        if result.get("success", False):
            logger.info("Project creation successful")
            self.send_json_response(result)
        else:
            error_msg = result.get("error", "Unknown error")
            logger.error("Error creating project: %s", error_msg)
            
            # Send error response
            self.send_json_response({
                "success": False,
                "error": error_msg
            }, 500)
        
    def handle_project_open(self, params):
        """Handle project/open endpoint."""
        if "path" not in params:
            self.send_json_response({
                "success": False,
                "error": "Missing required parameter: path"
            }, 400)
            return
        
        path = params.get("path", "")
        logger.info("Project open request for path: %s (executing script in CODESYS)", path)
        
        # Generate and execute project open script
        script = self.script_generator.generate_project_open_script(params)
        result = self.script_executor.execute_script(script, timeout=30)
        
        if result.get("success", False):
            logger.info("Project opening successful")
            self.send_json_response(result)
        else:
            error_msg = result.get("error", "Unknown error")
            logger.error("Error opening project: %s", error_msg)
            self.send_json_response({
                "success": False,
                "error": error_msg
            }, 500)
        
        
    def handle_project_save(self):
        """Handle project/save endpoint."""
        logger.info("Project save request (executing script in CODESYS)")
        
        # Generate and execute project save script
        script = self.script_generator.generate_project_save_script()
        result = self.script_executor.execute_script(script, timeout=30)
        
        if result.get("success", False):
            logger.info("Project save successful")
            self.send_json_response(result)
        else:
            error_msg = result.get("error", "Unknown error")
            logger.error("Error saving project: %s", error_msg)
            self.send_json_response({
                "success": False,
                "error": error_msg
            }, 500)
        
        
    def handle_project_close(self):
        """Handle project/close endpoint."""
        logger.info("Project close request (executing script in CODESYS)")
        
        # Generate and execute project close script
        script = self.script_generator.generate_project_close_script()
        result = self.script_executor.execute_script(script, timeout=30)
        
        if result.get("success", False):
            logger.info("Project close successful")
            self.send_json_response(result)
        else:
            error_msg = result.get("error", "Unknown error")
            logger.error("Error closing project: %s", error_msg)
            self.send_json_response({
                "success": False,
                "error": error_msg
            }, 500)
        
        
    def handle_project_list(self):
        """Handle project/list endpoint."""
        logger.info("Project list request (executing script in CODESYS)")
        
        # Generate and execute project list script
        script = self.script_generator.generate_project_list_script()
        result = self.script_executor.execute_script(script, timeout=30)
        
        if result.get("success", False):
            logger.info("Project listing successful")
            self.send_json_response(result)
        else:
            error_msg = result.get("error", "Unknown error")
            logger.error("Error listing projects: %s", error_msg)
            self.send_json_response({
                "success": False,
                "error": error_msg
            }, 500)
        
        
    def handle_project_compile(self, params):
        """Handle project/compile endpoint."""
        logger.info("Project compile request (executing script in CODESYS)")
        
        # Generate and execute project compilation script
        script = self.script_generator.generate_project_compile_script(params)
        result = self.script_executor.execute_script(script, timeout=60)  # Compilation can take longer
        
        if result.get("success", False):
            logger.info("Project compilation successful")
            self.send_json_response(result)
        else:
            error_msg = result.get("error", "Unknown error")
            logger.error("Error compiling project: %s", error_msg)
            self.send_json_response({
                "success": False,
                "error": error_msg
            }, 500)
        
        
    def handle_pou_create(self, params):
        """Handle pou/create endpoint."""
        required = ["name", "type", "language"]
        for field in required:
            if field not in params:
                self.send_json_response({
                    "success": False,
                    "error": "Missing required parameter: " + field
                }, 400)
                return
                
        name = params.get("name", "")
        pou_type = params.get("type", "FunctionBlock")
        language = params.get("language", "ST")
        parent_path = params.get("parentPath", "")
        
        logger.info("POU create request for '%s' (executing script in CODESYS)", name)
        
        # Generate and execute POU creation script
        script = self.script_generator.generate_pou_create_script(params)
        result = self.script_executor.execute_script(script, timeout=30)
        
        if result.get("success", False):
            logger.info("POU creation successful")
            self.send_json_response(result)
        else:
            error_msg = result.get("error", "Unknown error")
            logger.error("Error creating POU: %s", error_msg)
            self.send_json_response({
                "success": False,
                "error": error_msg
            }, 500)
        
        
    def handle_pou_code(self, params):
        """Handle pou/code endpoint."""
        required = ["path", "code"]
        for field in required:
            if field not in params:
                self.send_json_response({
                    "success": False,
                    "error": "Missing required parameter: " + field
                }, 400)
                return
                
        path = params.get("path", "")
        code = params.get("code", "")
        
        logger.info("POU code update request for '%s' (executing script in CODESYS)", path)
        
        # Generate and execute POU code setting script
        script = self.script_generator.generate_pou_code_script(params)
        result = self.script_executor.execute_script(script, timeout=30)
        
        if result.get("success", False):
            logger.info("POU code update successful")
            self.send_json_response(result)
        else:
            error_msg = result.get("error", "Unknown error")
            logger.error("Error updating POU code: %s", error_msg)
            self.send_json_response({
                "success": False,
                "error": error_msg
            }, 500)
        
        
    def handle_pou_list(self, params):
        """Handle pou/list endpoint."""
        parent_path = params.get("parentPath", "")
        
        logger.info("POU list request (executing script in CODESYS)")
        
        # Generate and execute POU listing script
        script = self.script_generator.generate_pou_list_script(params)
        result = self.script_executor.execute_script(script, timeout=30)
        
        if result.get("success", False):
            logger.info("POU listing successful")
            self.send_json_response(result)
        else:
            error_msg = result.get("error", "Unknown error")
            logger.error("Error listing POUs: %s", error_msg)
            self.send_json_response({
                "success": False,
                "error": error_msg
            }, 500)
        
        
    def handle_script_execute(self, params):
        """Handle script/execute endpoint."""
        if "script" not in params:
            self.send_json_response({
                "success": False,
                "error": "Missing required parameter: script"
            }, 400)
            return
            
        # Get script to execute
        script = params.get("script", "")
        first_line = script.split('\n')[0] if script else ""
        
        logger.info("Script execute request: %s", 
                    first_line[:50] + "..." if len(first_line) > 50 else first_line)
        
        # Actually execute the script in CODESYS
        result = self.script_executor.execute_script(script)
        
        # Return the result from execution
        self.send_json_response(result)
        
    def handle_system_info(self):
        """Handle system/info endpoint."""
        info = {
            "version": "0.1",
            "process_manager": {
                "status": self.process_manager.is_running()
            },
            "codesys_path": CODESYS_PATH,
            "persistent_script": PERSISTENT_SCRIPT
        }
        
        self.send_json_response({
            "success": True,
            "info": info
        })
        
    def handle_system_logs(self):
        """Handle system/logs endpoint."""
        logs = []
        
        if os.path.exists(LOG_FILE):
            try:
                with open(LOG_FILE, 'r') as f:
                    logs = f.readlines()
            except:
                pass
                
        self.send_json_response({
            "success": True,
            "logs": logs
        })


def run_server():
    """Run the HTTP server."""
    try:
        # Create managers
        process_manager = CodesysProcessManager(CODESYS_PATH, PERSISTENT_SCRIPT)
        script_executor = ScriptExecutor(REQUEST_DIR, RESULT_DIR)
        script_generator = ScriptGenerator()
        api_key_manager = ApiKeyManager(API_KEY_FILE)
        
        # Create server
        def handler(*args):
            return CodesysApiHandler(
                process_manager=process_manager,
                script_executor=script_executor,
                script_generator=script_generator,
                api_key_manager=api_key_manager,
                *args
            )
            
        server = HTTPServer((SERVER_HOST, SERVER_PORT), handler)
        
        print("Starting server on {0}:{1}".format(SERVER_HOST, SERVER_PORT))
        logger.info("Starting server on %s:%d", SERVER_HOST, SERVER_PORT)
        
        # Run server
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped")
    except Exception as e:
        print("Error starting server: " + str(e))
        logger.error("Error starting server: %s", str(e))
    finally:
        # Stop CODESYS process
        if 'process_manager' in locals():
            process_manager.stop()
            

if __name__ == "__main__":
    run_server()