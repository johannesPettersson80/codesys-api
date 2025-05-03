#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CODESYS API HTTP Server (Python 3 Compatible)

This script implements a HTTP server for the CODESYS API wrapper.
It provides RESTful endpoints to interact with CODESYS through
a persistent session.

Note: This version is adapted for Python 3.x compatibility
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
CODESYS_PATH = r"C:\Program Files\CODESYS 3.5\CODESYS\CODESYS.exe"  # Update this path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PERSISTENT_SCRIPT = os.path.join(SCRIPT_DIR, "PERSISTENT_SESSION_PY3.py")
API_KEY_FILE = os.path.join(SCRIPT_DIR, "api_keys.json")
REQUEST_DIR = os.path.join(SCRIPT_DIR, "requests")
RESULT_DIR = os.path.join(SCRIPT_DIR, "results")
TERMINATION_SIGNAL_FILE = os.path.join(SCRIPT_DIR, "terminate.signal")
STATUS_FILE = os.path.join(SCRIPT_DIR, "session_status.json")
LOG_FILE = os.path.join(SCRIPT_DIR, "session.log")

# Ensure directories exist
for directory in [REQUEST_DIR, RESULT_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

class CodesysProcessManager:
    """Manages the CODESYS process."""
    
    def __init__(self, codesys_path, script_path):
        self.codesys_path = codesys_path
        self.script_path = script_path
        self.process = None
        self.running = False
        self.lock = threading.Lock()
        
    def start(self):
        """Start the CODESYS process."""
        with self.lock:
            try:
                if self.is_running():
                    logger.info("CODESYS process already running")
                    return True
                    
                logger.info("Starting CODESYS process")
                
                # Start CODESYS with script
                self.process = subprocess.Popen(
                    [self.codesys_path, "-script", self.script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                
                # Wait for process to initialize
                time.sleep(5)
                
                # Check if process is still running
                if not self.is_running():
                    stdout, stderr = self.process.communicate()
                    logger.error("CODESYS process failed to start: %s", stderr)
                    return False
                    
                self.running = True
                logger.info("CODESYS process started")
                return True
            except Exception as e:
                logger.error("Error starting CODESYS process: %s", str(e))
                return False
                
    def stop(self):
        """Stop the CODESYS process."""
        with self.lock:
            if not self.is_running():
                logger.info("CODESYS process not running")
                return True
                
            try:
                logger.info("Stopping CODESYS process")
                
                # Signal termination
                with open(TERMINATION_SIGNAL_FILE, 'w') as f:
                    f.write("TERMINATE")
                    
                # Wait for process to terminate
                for _ in range(20):
                    if not self.is_running():
                        break
                    time.sleep(0.5)
                    
                # Force termination if still running
                if self.is_running():
                    self.process.terminate()
                    time.sleep(2)
                    
                    if self.is_running():
                        self.process.kill()
                        
                self.process = None
                self.running = False
                logger.info("CODESYS process stopped")
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
        
    def execute_script(self, script_content, timeout=30):
        """Execute a script and return the result."""
        try:
            # Create unique ID for this request
            request_id = str(uuid.uuid4())
            
            # Create temporary script file
            script_path = os.path.join(tempfile.gettempdir(), "codesys_script_{0}.py".format(request_id))
            with open(script_path, 'w') as f:
                f.write(script_content)
                
            # Create result file path
            result_path = os.path.join(tempfile.gettempdir(), "codesys_result_{0}.json".format(request_id))
            
            # Create request file
            request_path = os.path.join(self.request_dir, "{0}.request".format(request_id))
            with open(request_path, 'w') as f:
                f.write(json.dumps({
                    "script_path": script_path,
                    "result_path": result_path,
                    "timestamp": time.time()
                }))
                
            # Wait for result
            start_time = time.time()
            while time.time() - start_time < timeout:
                if os.path.exists(result_path):
                    # Read result
                    with open(result_path, 'r') as f:
                        try:
                            result = json.loads(f.read())
                            
                            # Cleanup files
                            self._cleanup_files(script_path, result_path, request_path)
                            
                            return result
                        except:
                            pass
                            
                time.sleep(0.1)
                
            # Timeout
            self._cleanup_files(script_path, result_path, request_path)
            return {"success": False, "error": "Script execution timed out"}
        except Exception as e:
            logger.error("Error executing script: %s", str(e))
            return {"success": False, "error": str(e)}
            
    def _cleanup_files(self, script_path, result_path, request_path):
        """Clean up temporary files."""
        for path in [script_path, result_path, request_path]:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except:
                pass


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
        except Exception as e:
            logger.error("Error handling GET request: %s", str(e))
            self.send_error(500, str(e))
            
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
        except Exception as e:
            logger.error("Error handling POST request: %s", str(e))
            self.send_error(500, str(e))
            
    def authenticate(self):
        """Validate API key."""
        auth_header = self.headers.get('Authorization', '')
        
        if auth_header.startswith('ApiKey '):
            api_key = auth_header[7:]  # Remove 'ApiKey ' prefix
            return self.api_key_manager.validate_key(api_key)
            
        return False
        
    def send_json_response(self, data, status=200):
        """Send JSON response."""
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
        
    # Handler methods
    
    def handle_session_start(self):
        """Handle session/start endpoint."""
        if not self.process_manager.start():
            self.send_json_response({
                "success": False,
                "error": "Failed to start CODESYS session"
            }, 500)
            return
            
        # Execute session start script
        script = self.script_generator.generate_session_start_script()
        result = self.script_executor.execute_script(script)
        
        if result.get("success", False):
            self.send_json_response({
                "success": True,
                "message": "Session started"
            })
        else:
            self.send_json_response({
                "success": False,
                "error": result.get("error", "Unknown error")
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
            
        # Execute session start script
        script = self.script_generator.generate_session_start_script()
        result = self.script_executor.execute_script(script)
        
        if result.get("success", False):
            self.send_json_response({
                "success": True,
                "message": "Session restarted"
            })
        else:
            self.send_json_response({
                "success": False,
                "error": result.get("error", "Unknown error")
            }, 500)
            
    def handle_session_status(self):
        """Handle session/status endpoint."""
        # Check process status
        process_running = self.process_manager.is_running()
        process_status = self.process_manager.get_status()
        
        # Execute status script if process is running
        session_status = {"active": False}
        if process_running:
            script = self.script_generator.generate_session_status_script()
            result = self.script_executor.execute_script(script)
            
            if result.get("success", False):
                session_status = result.get("status", {"active": False})
                
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
            
        script = self.script_generator.generate_project_create_script(params)
        result = self.script_executor.execute_script(script)
        
        self.send_json_response(result, 500 if not result.get("success", False) else 200)
        
    def handle_project_open(self, params):
        """Handle project/open endpoint."""
        if "path" not in params:
            self.send_json_response({
                "success": False,
                "error": "Missing required parameter: path"
            }, 400)
            return
            
        script = self.script_generator.generate_project_open_script(params)
        result = self.script_executor.execute_script(script)
        
        self.send_json_response(result, 500 if not result.get("success", False) else 200)
        
    def handle_project_save(self):
        """Handle project/save endpoint."""
        script = self.script_generator.generate_project_save_script()
        result = self.script_executor.execute_script(script)
        
        self.send_json_response(result, 500 if not result.get("success", False) else 200)
        
    def handle_project_close(self):
        """Handle project/close endpoint."""
        script = self.script_generator.generate_project_close_script()
        result = self.script_executor.execute_script(script)
        
        self.send_json_response(result, 500 if not result.get("success", False) else 200)
        
    def handle_project_list(self):
        """Handle project/list endpoint."""
        script = self.script_generator.generate_project_list_script()
        result = self.script_executor.execute_script(script)
        
        self.send_json_response(result, 500 if not result.get("success", False) else 200)
        
    def handle_project_compile(self, params):
        """Handle project/compile endpoint."""
        script = self.script_generator.generate_project_compile_script(params)
        result = self.script_executor.execute_script(script)
        
        self.send_json_response(result, 500 if not result.get("success", False) else 200)
        
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
                
        script = self.script_generator.generate_pou_create_script(params)
        result = self.script_executor.execute_script(script)
        
        self.send_json_response(result, 500 if not result.get("success", False) else 200)
        
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
                
        script = self.script_generator.generate_pou_code_script(params)
        result = self.script_executor.execute_script(script)
        
        self.send_json_response(result, 500 if not result.get("success", False) else 200)
        
    def handle_pou_list(self, params):
        """Handle pou/list endpoint."""
        script = self.script_generator.generate_pou_list_script(params)
        result = self.script_executor.execute_script(script)
        
        self.send_json_response(result, 500 if not result.get("success", False) else 200)
        
    def handle_script_execute(self, params):
        """Handle script/execute endpoint."""
        if "script" not in params:
            self.send_json_response({
                "success": False,
                "error": "Missing required parameter: script"
            }, 400)
            return
            
        script = self.script_generator.generate_script_execute_script(params)
        result = self.script_executor.execute_script(script)
        
        self.send_json_response(result, 500 if not result.get("success", False) else 200)
        
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