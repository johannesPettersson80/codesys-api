#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CODESYS API POU Creation Debugger

This script specifically debugs the POU (Program Organization Unit) creation 
and code setting functionality of the CODESYS API.
"""

import requests
import json
import time
import os
import sys
import argparse
import logging
import uuid

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='debug_pou_creation.log'
)
logger = logging.getLogger('debug_pou_creation')

# Add console handler
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)

# Default API settings
DEFAULT_API_URL = "http://localhost:8080"
DEFAULT_API_KEY = "admin"  # This is the default key created by ApiKeyManager

class POUCreationDebugger:
    """Debugger for POU creation in CODESYS API."""
    
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"ApiKey {api_key}",
            "Content-Type": "application/json"
        }
        self.session_active = False
        self.project_created = False
        self.project_path = None
        self.pou_created = False
        self.pou_name = None
        self.pou_code_set = False
        
    def request(self, method, endpoint, data=None, params=None, description=None):
        """Send a request to the API with detailed logging."""
        url = f"{self.base_url}/{endpoint}"
        desc = description or endpoint
        
        try:
            logger.info(f"Sending {method.upper()} request to {endpoint}")
            logger.debug(f"Request URL: {url}")
            logger.debug(f"Request headers: {self.headers}")
            
            if data:
                logger.debug(f"Request data: {json.dumps(data, indent=2)}")
                
            start_time = time.time()
            
            if method.lower() == "get":
                response = requests.get(url, headers=self.headers, params=params, timeout=120)
            elif method.lower() == "post":
                response = requests.post(url, headers=self.headers, json=data, timeout=120)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            elapsed_time = time.time() - start_time
            logger.debug(f"Request completed in {elapsed_time:.2f} seconds")
            logger.debug(f"Response status code: {response.status_code}")
            logger.debug(f"Response headers: {dict(response.headers)}")
                
            # Try to parse JSON response
            try:
                result = response.json()
                logger.debug(f"Response body: {json.dumps(result, indent=2)}")
            except json.JSONDecodeError:
                result = {"text": response.text}
                logger.debug(f"Response body (non-JSON): {response.text}")
                
            # Add status code and elapsed time to the result
            result["status_code"] = response.status_code
            result["elapsed_seconds"] = elapsed_time
            
            # Check response flags
            bypass_script = result.get("bypass_script", False)
            mock_response = result.get("mock_response", False)
            
            # Log outcome
            if response.status_code == 200 and result.get("success", False):
                if bypass_script or mock_response:
                    logger.warning(f"⚠️ {desc}: SUCCESS (BYPASSED or MOCKED) ({elapsed_time:.2f}s)")
                    logger.warning(f"The API is not executing the actual script in CODESYS!")
                else:
                    logger.info(f"✅ {desc}: SUCCESS ({elapsed_time:.2f}s)")
            else:
                error_message = result.get("error", "Unknown error")
                logger.error(f"❌ {desc}: FAILED - {error_message} ({elapsed_time:.2f}s)")
            
            return result
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ {desc}: CONNECTION ERROR - {str(e)}")
            return {"success": False, "error": str(e), "status_code": 0}
        except Exception as e:
            logger.error(f"❌ {desc}: ERROR - {str(e)}")
            return {"success": False, "error": str(e), "status_code": 0}
    
    def start_session(self):
        """Start a CODESYS session."""
        logger.info("Starting CODESYS session")
        result = self.request("post", "api/v1/session/start", description="Start Session")
        
        # Check for bypass
        if result.get("bypass_script", False) or result.get("mock_response", False):
            logger.warning("Session start was bypassed or mocked - may not be fully initialized")
        
        # Additional validation
        if result.get("success", False):
            logger.info("Session started successfully")
            self.session_active = True
        else:
            logger.error(f"Failed to start session: {result.get('error', 'Unknown error')}")
            
        return result
    
    def check_session_status(self):
        """Check the current session status."""
        logger.info("Checking session status")
        result = self.request("get", "api/v1/session/status", description="Session Status")
        
        # Additional validation
        if result.get("success", False):
            status = result.get("status", {})
            process_running = status.get("process", {}).get("running", False)
            session_active = status.get("session", {}).get("active", False)
            
            logger.info(f"Process running: {process_running}")
            logger.info(f"Session active: {session_active}")
            
            self.session_active = session_active
            
        return result
    
    def create_project(self, path=None):
        """Create a new CODESYS project with debugging."""
        # Generate a default path if none provided
        if not path:
            unique_id = str(uuid.uuid4())[:8]
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            path = os.path.abspath(f"CODESYS_POUDebug_{timestamp}_{unique_id}.project")
            
        self.project_path = path
        logger.info(f"Creating project at path: {path}")
        
        # Create the project
        data = {"path": path}
        logger.info(f"Sending project creation request for path: {path}")
        result = self.request("post", "api/v1/project/create", data, description="Create Project")
        
        # Check for bypass
        if result.get("bypass_script", False) or result.get("mock_response", False):
            logger.warning("Project creation was bypassed or mocked - project may not exist")
        
        # Additional validation
        if result.get("success", False):
            logger.info(f"Project creation API call succeeded")
            self.project_created = True
            
            # Check if the project file actually exists
            if os.path.exists(path):
                logger.info(f"Verified project file exists: {path}")
                logger.debug(f"Project file size: {os.path.getsize(path)} bytes")
            else:
                logger.warning(f"Project file does not exist on disk: {path}")
        else:
            logger.error(f"Failed to create project: {result.get('error', 'Unknown error')}")
            
        return result
    
    def create_pou(self, name=None, pou_type="FunctionBlock", language="ST"):
        """Create a POU in the project."""
        if not self.project_created:
            logger.error("Cannot create POU - no project created yet")
            return {"success": False, "error": "No project created"}
            
        # Generate a default name if none provided
        if not name:
            unique_id = str(uuid.uuid4())[:8]
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            name = f"TestPOU_{timestamp}_{unique_id}"
            
        self.pou_name = name
        logger.info(f"Creating POU: {name} (Type: {pou_type}, Language: {language})")
        
        # Create the POU
        data = {
            "name": name,
            "type": pou_type,
            "language": language,
            "parentPath": ""
        }
        result = self.request("post", "api/v1/pou/create", data, description="Create POU")
        
        # Check for bypass
        if result.get("bypass_script", False) or result.get("mock_response", False):
            logger.warning("POU creation was bypassed or mocked - POU may not exist")
        
        # Additional validation
        if result.get("success", False):
            logger.info(f"POU creation API call succeeded")
            self.pou_created = True
            
            # Note: We cannot directly verify POU creation in filesystem
            # as it's embedded in project file format
        else:
            logger.error(f"Failed to create POU: {result.get('error', 'Unknown error')}")
            
        return result
    
    def set_pou_code(self, code=None):
        """Set code for the POU."""
        if not self.pou_created or not self.pou_name:
            logger.error("Cannot set POU code - no POU created yet")
            return {"success": False, "error": "No POU created"}
            
        # Generate default code if none provided
        if not code:
            code = f"""
FUNCTION_BLOCK {self.pou_name}
VAR_INPUT
    iValue : INT;
END_VAR
VAR_OUTPUT
    oResult : INT;
END_VAR
VAR
    InternalVar : INT;
END_VAR

// Simple code for testing POU creation
oResult := iValue * 2;  // Multiply input by 2
            """
            
        logger.info(f"Setting code for POU: {self.pou_name}")
        logger.debug(f"POU code to set: {code}")
        
        # Set the POU code
        data = {
            "path": self.pou_name,
            "code": code
        }
        result = self.request("post", "api/v1/pou/code", data, description="Set POU Code")
        
        # Check for bypass
        if result.get("bypass_script", False) or result.get("mock_response", False):
            logger.warning("POU code setting was bypassed or mocked - code may not be set")
        
        # Additional validation
        if result.get("success", False):
            logger.info(f"POU code setting API call succeeded")
            self.pou_code_set = True
        else:
            logger.error(f"Failed to set POU code: {result.get('error', 'Unknown error')}")
            
        return result
    
    def list_pous(self):
        """List POUs in the project."""
        if not self.project_created:
            logger.error("Cannot list POUs - no project created yet")
            return {"success": False, "error": "No project created"}
            
        logger.info("Listing POUs in the project")
        
        result = self.request("get", "api/v1/pou/list", description="List POUs")
        
        # Check for bypass
        if result.get("bypass_script", False) or result.get("mock_response", False):
            logger.warning("POU listing was bypassed or mocked - result may not reflect actual POUs")
        
        # Additional validation
        if result.get("success", False):
            pous = result.get("pous", [])
            logger.info(f"Found {len(pous)} POUs in the project")
            
            # Check if our created POU is in the list
            if self.pou_created and self.pou_name:
                found = False
                for pou in pous:
                    if pou.get("name") == self.pou_name:
                        found = True
                        logger.info(f"Found our created POU '{self.pou_name}' in the list")
                        break
                        
                if not found:
                    logger.warning(f"Our created POU '{self.pou_name}' was not found in the POU list")
            
            # Log all found POUs
            for i, pou in enumerate(pous):
                logger.info(f"POU {i+1}: {pou.get('name')} (Type: {pou.get('type')}, Language: {pou.get('language')})")
        else:
            logger.error(f"Failed to list POUs: {result.get('error', 'Unknown error')}")
            
        return result
    
    def compile_project(self):
        """Compile the project."""
        if not self.project_created:
            logger.error("Cannot compile project - no project created yet")
            return {"success": False, "error": "No project created"}
            
        logger.info("Compiling project")
        
        data = {"clean_build": False}
        result = self.request("post", "api/v1/project/compile", data, description="Compile Project")
        
        # Check for bypass
        if result.get("bypass_script", False) or result.get("mock_response", False):
            logger.warning("Project compilation was bypassed or mocked - project may not be compiled")
        
        # Additional validation
        if result.get("success", False):
            logger.info("Project compilation API call succeeded")
            compilation = result.get("compilation", {})
            logger.info(f"Compilation info: {json.dumps(compilation, indent=2)}")
        else:
            logger.error(f"Failed to compile project: {result.get('error', 'Unknown error')}")
            
        return result
    
    def stop_session(self):
        """Stop the CODESYS session."""
        logger.info("Stopping CODESYS session")
        result = self.request("post", "api/v1/session/stop", description="Stop Session")
        
        # Additional validation
        if result.get("success", False):
            logger.info("Session stopped successfully")
            self.session_active = False
        else:
            logger.error(f"Failed to stop session: {result.get('error', 'Unknown error')}")
            
        return result
    
    def execute_diagnostic_script(self):
        """Execute a diagnostic script to check if script execution is working."""
        logger.info("Executing diagnostic script")
        
        # Create a simple diagnostic script that will output some debug info
        script = """
import scriptengine
import json
import sys
import os

try:
    print("Diagnostic script started")
    print("Python version: " + sys.version)
    
    # Check if system and projects are available
    print("Checking scriptengine.system availability")
    system_available = hasattr(scriptengine, 'system') and scriptengine.system is not None
    print("scriptengine.system available: " + str(system_available))
    
    print("Checking scriptengine.projects availability")
    projects_available = hasattr(scriptengine, 'projects') and scriptengine.projects is not None
    print("scriptengine.projects available: " + str(projects_available))
    
    # Try to get active project
    active_project = None
    if hasattr(session, 'active_project') and session.active_project is not None:
        active_project = session.active_project
        print("Active project: " + active_project.name)
    else:
        print("No active project in session")
    
    # Try to list POUs if project is active
    pous = []
    if active_project is not None:
        if hasattr(active_project, 'active_application') and active_project.active_application is not None:
            app = active_project.active_application
            print("Active application found")
            
            # Try different methods to get POUs
            try:
                if hasattr(app, 'pou_container') and app.pou_container is not None:
                    print("POU container found")
                    pou_container = app.pou_container
                    if hasattr(pou_container, 'pous'):
                        print("POU container has pous attribute")
                        pous = pou_container.pous
                        print("POUs retrieved: " + str(len(pous)))
                    else:
                        print("POU container does not have pous attribute")
                else:
                    print("No POU container found")
            except Exception as e:
                print("Error accessing POUs: " + str(e))
    
    # Return diagnostic result
    result = {
        "success": True,
        "diagnostic_info": {
            "system_available": system_available,
            "projects_available": projects_available,
            "active_project": active_project is not None,
            "pous_found": len(pous)
        }
    }
except Exception as e:
    print("Error in diagnostic script: " + str(e))
    result = {
        "success": False,
        "error": str(e)
    }
"""
        
        data = {"script": script}
        result = self.request("post", "api/v1/script/execute", data, description="Execute Diagnostic Script")
        
        # Check for bypass
        if result.get("bypass_script", False) or result.get("mock_response", False):
            logger.warning("Script execution was bypassed or mocked - diagnostics not performed")
        
        # Additional validation
        if result.get("success", False):
            logger.info("Diagnostic script execution API call succeeded")
            diagnostic_info = result.get("diagnostic_info", {})
            if diagnostic_info:
                logger.info(f"Diagnostic info: {json.dumps(diagnostic_info, indent=2)}")
            else:
                logger.warning("No diagnostic info returned, script may not have executed properly")
        else:
            logger.error(f"Failed to execute diagnostic script: {result.get('error', 'Unknown error')}")
            
        return result
    
    def check_for_bypassed_calls(self, result):
        """Check if an API call is being bypassed."""
        if result.get("bypass_script", False):
            logger.warning("API call is BYPASSED - script is not actually executed in CODESYS")
            return True
        if result.get("mock_response", False):
            logger.warning("API response is MOCKED - not from actual CODESYS execution")
            return True
        return False
    
    def run_debug_sequence(self, project_path=None, wait_time=5):
        """Run a debug sequence for POU creation."""
        try:
            logger.info("=== Starting POU Creation Debug Sequence ===")
            
            # Check session status
            self.check_session_status()
            
            # Start session if not active
            if not self.session_active:
                self.start_session()
                logger.info(f"Waiting {wait_time} seconds for session initialization...")
                time.sleep(wait_time)
                self.check_session_status()
            
            # Execute diagnostic script to check script execution
            self.execute_diagnostic_script()
            
            # Create project
            self.create_project(project_path)
            time.sleep(2)
            
            # Create POU
            self.create_pou()
            time.sleep(1)
            
            # Set POU code
            self.set_pou_code()
            time.sleep(1)
            
            # List POUs to verify creation
            self.list_pous()
            
            # Try to compile the project
            self.compile_project()
            
            # Check for bypassed calls
            logger.info("=== Checking for Bypassed API Calls ===")
            logger.info("A major issue could be that the server is returning 'success' without actually executing scripts.")
            logger.info("This would explain why POUs appear to be created (API returns success) but aren't visible in CODESYS.")
            
            # Look at HTTP_SERVER.py for bypass flags
            if os.path.exists("HTTP_SERVER.py"):
                try:
                    with open("HTTP_SERVER.py", "r") as f:
                        content = f.read()
                        if "bypass_script" in content and "return success immediately" in content:
                            logger.critical("HTTP_SERVER.py contains code that bypasses script execution!")
                            logger.critical("This is likely the cause of POUs not appearing in projects.")
                            
                            # Find specific endpoints that are bypassed
                            bypassed_endpoints = []
                            if "\"bypass_script\": True" in content and "handle_pou_create" in content:
                                bypassed_endpoints.append("POU creation")
                            if "\"bypass_script\": True" in content and "handle_pou_code" in content:
                                bypassed_endpoints.append("POU code setting")
                            
                            if bypassed_endpoints:
                                logger.critical(f"Found bypassed endpoints: {', '.join(bypassed_endpoints)}")
                except Exception as e:
                    logger.error(f"Error checking HTTP_SERVER.py for bypass flags: {str(e)}")
            
            # Final summary
            logger.info("=== Debug Sequence Summary ===")
            logger.info(f"Session active: {self.session_active}")
            logger.info(f"Project created: {self.project_created}")
            if self.project_created:
                logger.info(f"Project path: {self.project_path}")
                logger.info(f"Project file exists: {os.path.exists(self.project_path)}")
            logger.info(f"POU created (API success): {self.pou_created}")
            if self.pou_created:
                logger.info(f"POU name: {self.pou_name}")
            logger.info(f"POU code set (API success): {self.pou_code_set}")
            
        except KeyboardInterrupt:
            logger.info("Debug sequence interrupted by user")
        except Exception as e:
            logger.error(f"Unhandled error in debug sequence: {str(e)}", exc_info=True)
        finally:
            # Always try to stop the session at the end
            if self.session_active:
                logger.info("Cleaning up - stopping session")
                self.stop_session()

def main():
    """Run the POU creation debugger."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="CODESYS API POU Creation Debugger")
    parser.add_argument("--url", default=DEFAULT_API_URL, help="API server URL (default: %(default)s)")
    parser.add_argument("--key", default=DEFAULT_API_KEY, help="API key (default: %(default)s)")
    parser.add_argument("--project-path", help="Path for creating project")
    parser.add_argument("--wait", type=int, default=5, help="Wait time in seconds for session initialization (default: 5)")
    
    args = parser.parse_args()
    
    # Create debugger
    debugger = POUCreationDebugger(args.url, args.key)
    
    # Run debug sequence
    debugger.run_debug_sequence(args.project_path, args.wait)

if __name__ == "__main__":
    main()