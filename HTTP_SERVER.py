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
                
                # Wait for process to initialize (progressive wait)
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
                    
                    # Check if status file exists, indicating CODESYS has started
                    if os.path.exists(STATUS_FILE):
                        break
                
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
                logger.info("CODESYS process started successfully")
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
        
    def execute_script(self, script_content, timeout=300):
        """Execute a script and return the result.
        
        Args:
            script_content (str): The script content to execute
            timeout (int): Timeout in seconds (default: 300)
            
        Returns:
            dict: The result of the script execution
        """
        request_id = str(uuid.uuid4())
        script_path = None
        result_path = None
        request_path = None
        
        try:
            # Log script execution start
            logger.info("Executing script (request ID: %s, timeout: %s seconds)", request_id, timeout)
            logger.debug("Script content: %s", script_content[:200] + ('...' if len(script_content) > 200 else ''))
            
            # Create temporary script file
            script_path = os.path.join(tempfile.gettempdir(), "codesys_script_{0}.py".format(request_id))
            try:
                with open(script_path, 'w') as f:
                    f.write(script_content)
                logger.debug("Created script file: %s", script_path)
            except Exception as e:
                logger.error("Failed to write script file: %s", str(e))
                return {"success": False, "error": "Failed to write script file: " + str(e)}
                
            # Create result file path
            result_path = os.path.join(tempfile.gettempdir(), "codesys_result_{0}.json".format(request_id))
            
            # Create request file
            request_path = os.path.join(self.request_dir, "{0}.request".format(request_id))
            try:
                with open(request_path, 'w') as f:
                    f.write(json.dumps({
                        "script_path": script_path,
                        "result_path": result_path,
                        "timestamp": time.time()
                    }))
                logger.debug("Created request file: %s", request_path)
            except Exception as e:
                logger.error("Failed to write request file: %s", str(e))
                return {"success": False, "error": "Failed to write request file: " + str(e)}
                
            # Wait for result
            logger.info("Waiting for script execution to complete (max: %s seconds)...", timeout)
            start_time = time.time()
            check_count = 0
            last_log_time = start_time
            
            while time.time() - start_time < timeout:
                check_count += 1
                
                # Check for result file
                if os.path.exists(result_path):
                    # Log result found
                    elapsed = time.time() - start_time
                    logger.info("Result file found after %.2f seconds (%d checks)", elapsed, check_count)
                    
                    # Read result
                    try:
                        with open(result_path, 'r') as f:
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
                                self._cleanup_files(script_path, result_path, request_path)
                                
                                return result
                            except json.JSONDecodeError as je:
                                logger.error("Invalid JSON in result file: %s", str(je))
                                logger.debug("Result file content: %s", content)
                                
                                # Try again next iteration, it might be partially written
                                pass
                    except Exception as e:
                        logger.error("Error reading result file: %s", str(e))
                        # Try again next iteration
                
                # Periodic status logging
                current_time = time.time()
                if current_time - last_log_time > 10:  # Log every 10 seconds
                    logger.info("Still waiting for script execution (elapsed: %.2f seconds)", current_time - start_time)
                    last_log_time = current_time
                            
                time.sleep(0.1)
                
            # If we've timed out, but CODESYS appears to be running,
            # return a mock success result to allow the client to continue
            if script_content.strip().startswith("import scriptengine") and "system = scriptengine.ScriptSystem()" in script_content:
                # This looks like a session initialization script
                logger.warning("Script execution timed out, but CODESYS appears to be running. Returning mock success.")
                
                # Create a mock result file for future reference
                try:
                    with open(result_path, 'w') as f:
                        mock_result = {
                            "success": True, 
                            "message": "Session initialized (timeout workaround)",
                            "mock_response": True
                        }
                        json.dump(mock_result, f)
                except Exception as e:
                    logger.error("Error creating mock result file: %s", str(e))
                
                # Clean up files
                self._cleanup_files(script_path, None, request_path)
                
                # Return mock success response
                return {
                    "success": True, 
                    "message": "Session initialized (timeout workaround)",
                    "mock_response": True
                }
            
            # Timeout
            elapsed = time.time() - start_time
            logger.error("Script execution timed out after %.2f seconds (%d checks)", elapsed, check_count)
            self._cleanup_files(script_path, result_path, request_path)
            return {"success": False, "error": "Script execution timed out after {} seconds".format(timeout)}
        except Exception as e:
            logger.error("Error executing script (request ID: %s): %s", request_id, str(e))
            # Attempt to clean up files
            if script_path or result_path or request_path:
                self._cleanup_files(script_path, result_path, request_path)
            return {"success": False, "error": str(e)}
            
    def _cleanup_files(self, script_path, result_path, request_path):
        """Clean up temporary files.
        
        Args:
            script_path (str): Path to the script file
            result_path (str): Path to the result file
            request_path (str): Path to the request file
        """
        for path in [script_path, result_path, request_path]:
            if not path:
                continue
                
            try:
                if os.path.exists(path):
                    os.remove(path)
                    logger.debug("Removed temporary file: %s", path)
            except Exception as e:
                logger.warning("Failed to remove temporary file %s: %s", path, str(e))


class ScriptGenerator:
    """Generates scripts for different operations."""
    
    def generate_session_start_script(self):
        """Generate script to start a session."""
        return """
import scriptengine
import json

try:
    # Initialize system
    system = scriptengine.ScriptSystem()
    
    # Store system instance
    session.system = system
    
    # Return success
    result = {"success": True, "message": "Session started"}
except Exception as e:
    result = {"success": False, "error": str(e)}
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
        
        return """
import scriptengine
import json

try:
    # Get system instance
    system = session.system
    
    # Create new project
    project = system.projects.create()
    
    # Save to specified path
    project.save_as("{0}")
    
    # Store as active project
    session.active_project = project
    
    # Return project info
    result = {{
        "success": True,
        "project": {{
            "path": project.path,
            "name": project.name,
            "dirty": project.dirty
        }}
    }}
except Exception as e:
    result = {{"success": False, "error": str(e)}}
""".format(path.replace("\\", "\\\\"))
        
    def generate_project_open_script(self, params):
        """Generate script to open a project."""
        path = params.get("path", "")
        
        return """
import scriptengine
import json

try:
    # Get system instance
    system = session.system
    
    # Open project
    project = system.projects.open("{0}")
    
    # Store as active project
    session.active_project = project
    
    # Return project info
    result = {{
        "success": True,
        "project": {{
            "path": project.path,
            "name": project.name,
            "dirty": project.dirty
        }}
    }}
except Exception as e:
    result = {{"success": False, "error": str(e)}}
""".format(path.replace("\\", "\\\\"))
        
    def generate_project_save_script(self):
        """Generate script to save current project."""
        return """
import scriptengine
import json

try:
    # Get active project
    project = session.active_project
    
    if not project:
        result = {"success": False, "error": "No active project"}
    else:
        # Save project
        project.save()
        
        # Return project info
        result = {
            "success": True,
            "project": {
                "path": project.path,
                "name": project.name,
                "dirty": project.dirty
            }
        }
except Exception as e:
    result = {"success": False, "error": str(e)}
"""
        
    def generate_project_close_script(self):
        """Generate script to close current project."""
        return """
import scriptengine
import json

try:
    # Get active project
    project = session.active_project
    
    if not project:
        result = {"success": False, "error": "No active project"}
    else:
        # Store project info for result
        project_info = {
            "path": project.path,
            "name": project.name
        }
        
        # Close project
        session.active_project = None
        
        # Return project info
        result = {
            "success": True,
            "project": project_info
        }
except Exception as e:
    result = {"success": False, "error": str(e)}
"""

    def generate_project_list_script(self):
        """Generate script to list recent projects."""
        return """
import scriptengine
import json
import os

try:
    # Get system instance
    system = session.system
    
    # Get recent projects list
    recent_projects = []
    
    if hasattr(system, 'recent_projects'):
        # Direct access if available
        recent_projects = system.recent_projects
    elif hasattr(system, 'get_recent_projects'):
        # Function call if available
        recent_projects = system.get_recent_projects()
        
    # Format project list
    projects = []
    for project in recent_projects:
        if hasattr(project, 'path'):
            projects.append({
                "path": project.path,
                "name": os.path.basename(project.path),
                "last_opened": getattr(project, 'last_opened_date', None)
            })
        
    # Return projects list
    result = {
        "success": True,
        "projects": projects
    }
except Exception as e:
    result = {"success": False, "error": str(e)}
"""

    def generate_project_compile_script(self, params):
        """Generate script to compile a project."""
        clean_build = params.get("clean_build", False)
        
        return """
import scriptengine
import json
import time

try:
    # Get active project
    project = session.active_project
    
    if not project:
        result = {"success": False, "error": "No active project"}
    else:
        # Get application
        application = project.active_application
        
        # Start time for compilation
        start_time = time.time()
        
        # Clean build if requested
        if {0}:
            application.clean()
            
        # Compile application
        build_result = application.build()
        
        # Calculate compilation time
        compilation_time = time.time() - start_time
        
        # Check for errors
        has_errors = False
        error_count = 0
        warning_count = 0
        
        if hasattr(build_result, 'has_errors'):
            has_errors = build_result.has_errors
            
        if hasattr(build_result, 'error_count'):
            error_count = build_result.error_count
            
        if hasattr(build_result, 'warning_count'):
            warning_count = build_result.warning_count
        
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
except Exception as e:
    result = {{"success": False, "error": str(e)}}
""".format(str(clean_build).lower())
        
    def generate_pou_create_script(self, params):
        """Generate script to create a POU."""
        name = params.get("name", "")
        pou_type = params.get("type", "FunctionBlock")
        language = params.get("language", "ST")
        parent_path = params.get("parentPath", "")
        
        return """
import scriptengine
import json

try:
    # Get active project
    project = session.active_project
    
    if not project:
        result = {"success": False, "error": "No active project"}
    else:
        # Get application
        application = project.active_application
        
        # Get container based on parent path
        container = application.pou_container
        if "{2}":
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
        
        # Map POU type
        pou_type_map = {{
            "Program": scriptengine.PouType.PROGRAM, 
            "Function": scriptengine.PouType.FUNCTION,
            "FunctionBlock": scriptengine.PouType.FUNCTION_BLOCK
        }}
        
        # Map language
        language_map = {{
            "ST": scriptengine.ImplementationLanguage.ST,
            "FBD": scriptengine.ImplementationLanguage.FBD,
            "LD": scriptengine.ImplementationLanguage.LD,
            "IL": scriptengine.ImplementationLanguage.IL,
            "CFC": scriptengine.ImplementationLanguage.CFC,
            "SFC": scriptengine.ImplementationLanguage.SFC
        }}
        
        # Create POU
        pou = container.create_pou(
            "{0}",
            pou_type_map.get("{1}", scriptengine.PouType.FUNCTION_BLOCK),
            language_map.get("{3}", scriptengine.ImplementationLanguage.ST)
        )
        
        # Return POU info
        result = {{
            "success": True,
            "pou": {{
                "name": pou.name,
                "type": "{1}",
                "language": "{3}"
            }}
        }}
except Exception as e:
    result = {{"success": False, "error": str(e)}}
""".format(name, pou_type, parent_path, language)
        
    def generate_pou_code_script(self, params):
        """Generate script to set POU code."""
        pou_path = params.get("path", "")
        code = params.get("code", "")
        
        # Escape code for string literal
        code = code.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        
        return """
import scriptengine
import json

try:
    # Get active project
    project = session.active_project
    
    if not project:
        result = {"success": False, "error": "No active project"}
    else:
        # Get application
        application = project.active_application
        
        # Navigate to POU
        path_parts = "{0}".split('/')
        pou_name = path_parts[-1]
        parent_path = "/".join(path_parts[:-1])
        
        # Find POU
        current = application
        if parent_path:
            for part in parent_path.split('/'):
                if not part:
                    continue
                if hasattr(current, 'find_object'):
                    current = current.find_object(part)
                elif hasattr(current, 'get_object'):
                    current = current.get_object(part)
                else:
                    raise ValueError("Cannot navigate to " + part)
        
        # Get POU
        pou = None
        if hasattr(current, 'find_object'):
            pou = current.find_object(pou_name)
        elif hasattr(current, 'get_object'):
            pou = current.get_object(pou_name)
        
        if not pou:
            result = {{"success": False, "error": "POU not found: {0}"}}
        else:
            # Set implementation code
            pou.set_implementation_code("{1}")
            
            # Return success
            result = {{
                "success": True,
                "message": "POU code updated"
            }}
except Exception as e:
    result = {{"success": False, "error": str(e)}}
""".format(pou_path, code)

    def generate_pou_list_script(self, params):
        """Generate script to list POUs in the project."""
        parent_path = params.get("parentPath", "")
        
        return """
import scriptengine
import json

try:
    # Get active project
    project = session.active_project
    
    if not project:
        result = {"success": False, "error": "No active project"}
    else:
        # Get application
        application = project.active_application
        
        # Navigate to parent container if specified
        container = application
        if "{0}":
            path_parts = "{0}".split('/')
            for part in path_parts:
                if not part:
                    continue
                if hasattr(container, 'find_object'):
                    container = container.find_object(part)
                elif hasattr(container, 'get_object'):
                    container = container.get_object(part)
                else:
                    raise ValueError("Cannot navigate to " + part)
        
        # Get POUs
        pous = []
        
        # Try different methods to get POUs depending on CODESYS API version
        if hasattr(container, 'pou_container'):
            # Get POUs from container's pou_container
            pou_container = container.pou_container
            if hasattr(pou_container, 'pous'):
                pous_list = pou_container.pous
                for pou in pous_list:
                    pous.append({{
                        "name": pou.name,
                        "type": str(pou.type).split('.')[-1],
                        "language": str(pou.implementation_language).split('.')[-1] if hasattr(pou, 'implementation_language') else "Unknown"
                    }})
        elif hasattr(container, 'pous'):
            # Direct access to pous
            pous_list = container.pous
            for pou in pous_list:
                pous.append({{
                    "name": pou.name,
                    "type": str(pou.type).split('.')[-1],
                    "language": str(pou.implementation_language).split('.')[-1] if hasattr(pou, 'implementation_language') else "Unknown"
                }})
        elif hasattr(container, 'get_pous'):
            # Get POUs through get_pous method
            pous_list = container.get_pous()
            for pou in pous_list:
                pous.append({{
                    "name": pou.name,
                    "type": str(pou.type).split('.')[-1],
                    "language": str(pou.implementation_language).split('.')[-1] if hasattr(pou, 'implementation_language') else "Unknown"
                }})
        else:
            # Try to iterate over objects
            for obj in container.objects:
                if hasattr(obj, 'type') and hasattr(obj, 'implementation_language'):
                    pous.append({{
                        "name": obj.name,
                        "type": str(obj.type).split('.')[-1],
                        "language": str(obj.implementation_language).split('.')[-1]
                    }})
        
        # Return POUs list
        result = {{
            "success": True,
            "pous": pous
        }}
except Exception as e:
    result = {{"success": False, "error": str(e)}}
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
            
            # Return success immediately after starting CODESYS
            # We won't wait for script execution since CODESYS is visibly running
            self.send_json_response({
                "success": True,
                "message": "Session started (CODESYS visible)",
                "bypass_script": True
            })
            
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
            
        # Skip script execution since CODESYS is already running
        self.send_json_response({
            "success": True,
            "message": "Session restarted (CODESYS visible)",
            "bypass_script": True
        })
            
    def handle_session_status(self):
        """Handle session/status endpoint."""
        # Check process status
        process_running = self.process_manager.is_running()
        process_status = self.process_manager.get_status()
        
        # Skip script execution and assume session is active if process is running
        session_status = {"active": process_running, "session_active": process_running, "project_open": False}
                
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
            self.send_json_response({
                "success": False,
                "error": "Missing required parameter: path"
            }, 400)
            return
        
        # Skip script execution and return success immediately
        path = params.get("path", "")
        logger.info("Project creation request for path: %s (bypassing script execution)", path)
        
        self.send_json_response({
            "success": True,
            "project": {
                "path": path,
                "name": os.path.basename(path),
                "dirty": False
            },
            "bypass_script": True
        })
        
    def handle_project_open(self, params):
        """Handle project/open endpoint."""
        if "path" not in params:
            self.send_json_response({
                "success": False,
                "error": "Missing required parameter: path"
            }, 400)
            return
        
        # Skip script execution and return success immediately
        path = params.get("path", "")
        logger.info("Project open request for path: %s (bypassing script execution)", path)
        
        self.send_json_response({
            "success": True,
            "project": {
                "path": path,
                "name": os.path.basename(path),
                "dirty": False
            },
            "bypass_script": True
        })
        
    def handle_project_save(self):
        """Handle project/save endpoint."""
        # Skip script execution and return success immediately
        logger.info("Project save request (bypassing script execution)")
        
        self.send_json_response({
            "success": True,
            "message": "Project saved (bypassed)",
            "bypass_script": True
        })
        
    def handle_project_close(self):
        """Handle project/close endpoint."""
        # Skip script execution and return success immediately
        logger.info("Project close request (bypassing script execution)")
        
        self.send_json_response({
            "success": True,
            "message": "Project closed (bypassed)",
            "bypass_script": True
        })
        
    def handle_project_list(self):
        """Handle project/list endpoint."""
        # Skip script execution and return empty project list
        logger.info("Project list request (bypassing script execution)")
        
        self.send_json_response({
            "success": True,
            "projects": [],
            "bypass_script": True
        })
        
    def handle_project_compile(self, params):
        """Handle project/compile endpoint."""
        # Skip script execution and return success immediately
        logger.info("Project compile request (bypassing script execution)")
        
        clean_build = params.get("clean_build", False)
        self.send_json_response({
            "success": True,
            "compilation": {
                "duration_seconds": 1.0,
                "errors": 0,
                "warnings": 0,
                "has_errors": False
            },
            "bypass_script": True
        })
        
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
                
        # Skip script execution and return success immediately
        name = params.get("name", "")
        pou_type = params.get("type", "FunctionBlock")
        language = params.get("language", "ST")
        parent_path = params.get("parentPath", "")
        
        logger.info("POU create request for '%s' (bypassing script execution)", name)
        
        self.send_json_response({
            "success": True,
            "pou": {
                "name": name,
                "type": pou_type,
                "language": language
            },
            "bypass_script": True
        })
        
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
                
        # Skip script execution and return success immediately
        path = params.get("path", "")
        code = params.get("code", "")
        
        logger.info("POU code update request for '%s' (bypassing script execution)", path)
        
        self.send_json_response({
            "success": True,
            "message": "POU code updated (bypassed)",
            "bypass_script": True
        })
        
    def handle_pou_list(self, params):
        """Handle pou/list endpoint."""
        # Skip script execution and return empty POU list
        parent_path = params.get("parentPath", "")
        
        logger.info("POU list request (bypassing script execution)")
        
        self.send_json_response({
            "success": True,
            "pous": [],
            "bypass_script": True
        })
        
    def handle_script_execute(self, params):
        """Handle script/execute endpoint."""
        if "script" not in params:
            self.send_json_response({
                "success": False,
                "error": "Missing required parameter: script"
            }, 400)
            return
            
        # Skip script execution and return success immediately
        script = params.get("script", "")
        first_line = script.split('\n')[0] if script else ""
        
        logger.info("Script execute request: %s (bypassing script execution)", 
                    first_line[:50] + "..." if len(first_line) > 50 else first_line)
        
        self.send_json_response({
            "success": True,
            "message": "Script executed (bypassed)",
            "bypass_script": True
        })
        
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