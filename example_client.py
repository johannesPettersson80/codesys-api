#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CODESYS API Example Client (Python 3 Compatible)

This script demonstrates how to use the CODESYS REST API
to perform common operations like starting a session, creating
a project, adding POUs, etc.

Note: This version is compatible with Python 3.x
"""

import sys
import os
import json
import time
import requests
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('codesys_api_client')

# API configuration
API_BASE_URL = "http://localhost:8080/api/v1"
API_KEY = "admin"  # Default API key, change in production

# Configure requests session
session = requests.Session()
session.headers.update({
    'Authorization': 'ApiKey ' + API_KEY,
    'Content-Type': 'application/json'
})

def call_api(method, endpoint, data=None, params=None):
    """Make an API call to the CODESYS REST API."""
    url = "{0}/{1}".format(API_BASE_URL, endpoint)
    
    try:
        if method.upper() == 'GET':
            response = session.get(url, params=params)
        elif method.upper() == 'POST':
            response = session.post(url, json=data)
        else:
            raise ValueError("Unsupported HTTP method: {0}".format(method))
            
        # Check if the response is JSON
        try:
            result = response.json()
        except:
            logger.error("Non-JSON response: %s", response.text)
            return {'success': False, 'error': 'Non-JSON response from server'}
            
        # Log successful requests
        if result.get('success', False):
            logger.info("%s %s - Success", method, endpoint)
        else:
            logger.error("%s %s - Error: %s", method, endpoint, result.get('error', 'Unknown error'))
            
        return result
    except requests.exceptions.RequestException as e:
        logger.error("Request error: %s", str(e))
        return {'success': False, 'error': str(e)}

def start_session():
    """Start a CODESYS session."""
    return call_api('POST', 'session/start')

def get_session_status():
    """Get the status of the CODESYS session."""
    return call_api('GET', 'session/status')

def stop_session():
    """Stop the CODESYS session."""
    return call_api('POST', 'session/stop')

def restart_session():
    """Restart the CODESYS session."""
    return call_api('POST', 'session/restart')

def create_project(path):
    """Create a new CODESYS project."""
    return call_api('POST', 'project/create', {'path': path})

def open_project(path):
    """Open an existing CODESYS project."""
    return call_api('POST', 'project/open', {'path': path})

def save_project():
    """Save the current project."""
    return call_api('POST', 'project/save')

def close_project():
    """Close the current project."""
    return call_api('POST', 'project/close')

def compile_project(clean_build=False):
    """Compile the current project."""
    return call_api('POST', 'project/compile', {'clean_build': clean_build})

def list_projects():
    """List recent projects."""
    return call_api('GET', 'project/list')

def create_pou(name, pou_type, language, parent_path=""):
    """Create a new POU in the current project."""
    data = {
        'name': name,
        'type': pou_type,
        'language': language
    }
    
    if parent_path:
        data['parentPath'] = parent_path
        
    return call_api('POST', 'pou/create', data)

def set_pou_code(path, code):
    """Set the code of a POU."""
    return call_api('POST', 'pou/code', {'path': path, 'code': code})

def list_pous(parent_path=""):
    """List POUs in the current project."""
    params = {}
    if parent_path:
        params['parentPath'] = parent_path
        
    return call_api('GET', 'pou/list', params=params)

def execute_script(script):
    """Execute a custom script in the CODESYS environment."""
    return call_api('POST', 'script/execute', {'script': script})

def get_system_info():
    """Get system information."""
    return call_api('GET', 'system/info')

def get_system_logs():
    """Get system logs."""
    return call_api('GET', 'system/logs')

def example_workflow():
    """Run an example workflow demonstrating key API capabilities."""
    # Step 1: Start CODESYS session
    logger.info("Starting CODESYS session...")
    result = start_session()
    if not result.get('success', False):
        logger.error("Failed to start session: %s", result.get('error', 'Unknown error'))
        return False
        
    # Step 2: Get session status
    logger.info("Getting session status...")
    result = get_session_status()
    if not result.get('success', False):
        logger.error("Failed to get session status: %s", result.get('error', 'Unknown error'))
        return False
        
    # Step 3: Create a new project
    project_path = "C:/Temp/ExampleProject.project"
    logger.info("Creating new project at %s...", project_path)
    result = create_project(project_path)
    if not result.get('success', False):
        logger.error("Failed to create project: %s", result.get('error', 'Unknown error'))
        return False
        
    # Step 4: Create a POU
    logger.info("Creating a new FunctionBlock POU...")
    result = create_pou("MotorController", "FunctionBlock", "ST")
    if not result.get('success', False):
        logger.error("Failed to create POU: %s", result.get('error', 'Unknown error'))
        return False
        
    # Step 5: Set POU code
    st_code = """
    VAR_INPUT
        Enable : BOOL;
        Speed : INT;
    END_VAR
    
    VAR_OUTPUT
        Running : BOOL;
        ActualSpeed : INT;
    END_VAR
    
    IF Enable THEN
        Running := TRUE;
        ActualSpeed := Speed;
    ELSE
        Running := FALSE;
        ActualSpeed := 0;
    END_IF
    """
    
    logger.info("Setting POU code...")
    result = set_pou_code("Application/MotorController", st_code)
    if not result.get('success', False):
        logger.error("Failed to set POU code: %s", result.get('error', 'Unknown error'))
        return False
        
    # Step 6: List POUs
    logger.info("Listing POUs...")
    result = list_pous()
    if not result.get('success', False):
        logger.error("Failed to list POUs: %s", result.get('error', 'Unknown error'))
        return False
    else:
        logger.info("Available POUs: %s", json.dumps(result.get('pous', []), indent=2))
        
    # Step 7: Compile project
    logger.info("Compiling project...")
    result = compile_project()
    if not result.get('success', False):
        logger.error("Failed to compile project: %s", result.get('error', 'Unknown error'))
        return False
        
    # Step 8: Save project
    logger.info("Saving project...")
    result = save_project()
    if not result.get('success', False):
        logger.error("Failed to save project: %s", result.get('error', 'Unknown error'))
        return False
        
    # Step 9: Close project
    logger.info("Closing project...")
    result = close_project()
    if not result.get('success', False):
        logger.error("Failed to close project: %s", result.get('error', 'Unknown error'))
        return False
        
    # Step 10: Execute custom script
    logger.info("Executing custom script...")
    custom_script = """
    import scriptengine
    
    try:
        # Get system version
        system = scriptengine.ScriptSystem()
        version = system.version if hasattr(system, 'version') else "Unknown"
        
        # Return result
        result = {"success": True, "version": version}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    """
    
    result = execute_script(custom_script)
    if not result.get('success', False):
        logger.error("Failed to execute script: %s", result.get('error', 'Unknown error'))
        return False
    else:
        logger.info("Script execution result: %s", json.dumps(result, indent=2))
        
    # Step 11: Stop CODESYS session
    logger.info("Stopping CODESYS session...")
    result = stop_session()
    if not result.get('success', False):
        logger.error("Failed to stop session: %s", result.get('error', 'Unknown error'))
        return False
        
    logger.info("Example workflow completed successfully!")
    return True
    
if __name__ == "__main__":
    # Run the example workflow
    try:
        if example_workflow():
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Example workflow interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error("Unexpected error: %s", str(e))
        sys.exit(1)