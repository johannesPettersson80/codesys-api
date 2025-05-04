#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CODESYS API Debugging Script

This script executes specific diagnostic scripts in CODESYS to debug
issues with POU creation and project operations.
"""

import requests
import json
import time
import os
import sys
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("codesys_api_debug.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("codesys_api_debug")

# Default API settings
DEFAULT_API_URL = "http://localhost:8080"
DEFAULT_API_KEY = "admin"  # Default API key

def execute_custom_script(script, base_url=DEFAULT_API_URL, api_key=DEFAULT_API_KEY):
    """Execute a custom script through the CODESYS API."""
    url = f"{base_url}/api/v1/script/execute"
    headers = {
        "Authorization": f"ApiKey {api_key}",
        "Content-Type": "application/json"
    }
    data = {"script": script}
    
    try:
        logger.info("Executing custom script")
        if script:
            logger.debug(f"Script preview: {script[:200]}...")
        
        response = requests.post(url, headers=headers, json=data, timeout=60)
        
        try:
            result = response.json()
            logger.debug(f"Response: {json.dumps(result, indent=2)}")
            return result
        except json.JSONDecodeError:
            logger.error(f"Non-JSON response: {response.text}")
            return {"success": False, "error": "Non-JSON response"}
    
    except Exception as e:
        logger.error(f"Error executing script: {str(e)}")
        return {"success": False, "error": str(e)}

def start_session(base_url=DEFAULT_API_URL, api_key=DEFAULT_API_KEY):
    """Start a CODESYS session."""
    url = f"{base_url}/api/v1/session/start"
    headers = {
        "Authorization": f"ApiKey {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        logger.info("Starting CODESYS session")
        response = requests.post(url, headers=headers, timeout=60)
        
        try:
            result = response.json()
            logger.debug(f"Response: {json.dumps(result, indent=2)}")
            return result
        except json.JSONDecodeError:
            logger.error(f"Non-JSON response: {response.text}")
            return {"success": False, "error": "Non-JSON response"}
    
    except Exception as e:
        logger.error(f"Error starting session: {str(e)}")
        return {"success": False, "error": str(e)}

def create_project(path, base_url=DEFAULT_API_URL, api_key=DEFAULT_API_KEY):
    """Create a CODESYS project."""
    url = f"{base_url}/api/v1/project/create"
    headers = {
        "Authorization": f"ApiKey {api_key}",
        "Content-Type": "application/json"
    }
    data = {"path": path}
    
    try:
        logger.info(f"Creating project at {path}")
        response = requests.post(url, headers=headers, json=data, timeout=60)
        
        try:
            result = response.json()
            logger.debug(f"Response: {json.dumps(result, indent=2)}")
            return result
        except json.JSONDecodeError:
            logger.error(f"Non-JSON response: {response.text}")
            return {"success": False, "error": "Non-JSON response"}
    
    except Exception as e:
        logger.error(f"Error creating project: {str(e)}")
        return {"success": False, "error": str(e)}

def stop_session(base_url=DEFAULT_API_URL, api_key=DEFAULT_API_KEY):
    """Stop the CODESYS session."""
    url = f"{base_url}/api/v1/session/stop"
    headers = {
        "Authorization": f"ApiKey {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        logger.info("Stopping CODESYS session")
        response = requests.post(url, headers=headers, timeout=60)
        
        try:
            result = response.json()
            logger.debug(f"Response: {json.dumps(result, indent=2)}")
            return result
        except json.JSONDecodeError:
            logger.error(f"Non-JSON response: {response.text}")
            return {"success": False, "error": "Non-JSON response"}
    
    except Exception as e:
        logger.error(f"Error stopping session: {str(e)}")
        return {"success": False, "error": str(e)}

def run_script_tests():
    """Run a series of diagnostic script tests."""
    # Start a session
    start_result = start_session()
    if not start_result.get("success", False):
        logger.error("Failed to start session, aborting tests")
        return
    
    # Wait for session to initialize
    logger.info("Waiting 5 seconds for session to initialize...")
    time.sleep(5)
    
    # Create a test project
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    project_path = os.path.abspath(f"CODESYS_ScriptTest_{timestamp}.project")
    create_result = create_project(project_path)
    if not create_result.get("success", False):
        logger.error("Failed to create project, aborting tests")
        try:
            stop_session()
        except:
            pass
        return
    
    # Wait for project to be created
    logger.info("Waiting 2 seconds for project creation...")
    time.sleep(2)
    
    try:
        # Test 1: Diagnose session.active_project and scriptengine.system
        logger.info("=== Running Script Test 1: Diagnose session.active_project ===")
        test_script_1 = """
import scriptengine
import sys
import json

try:
    # Log Python version and environment
    print("Python version: " + sys.version)
    print("ScriptEngine available: " + str('scriptengine' in sys.modules))
    
    # Check if system and projects are available
    system_exists = hasattr(scriptengine, 'system')
    projects_exists = hasattr(scriptengine, 'projects')
    print("scriptengine.system exists: " + str(system_exists))
    print("scriptengine.projects exists: " + str(projects_exists))
    
    # Check the session object
    session_exists = 'session' in globals()
    print("session object exists: " + str(session_exists))
    
    # Check active project
    if session_exists:
        active_project_attr = hasattr(session, 'active_project')
        print("session.active_project attribute exists: " + str(active_project_attr))
        
        if active_project_attr:
            active_project = session.active_project
            print("session.active_project is None: " + str(active_project is None))
            
            if active_project is not None:
                # Inspect active project
                project_attrs = [attr for attr in dir(active_project) if not attr.startswith('_')]
                print("Project attributes: " + str(project_attrs))
                
                # Check name
                if hasattr(active_project, 'name'):
                    print("Project name: " + str(active_project.name))
                else:
                    print("Project does not have name attribute")
                
                # Check path
                if hasattr(active_project, 'path'):
                    print("Project path: " + str(active_project.path))
                else:
                    print("Project does not have path attribute")
                
                # Check application
                if hasattr(active_project, 'active_application'):
                    app = active_project.active_application
                    print("Project has active_application: " + str(app is not None))
                    
                    if app is not None:
                        # Check POU container
                        if hasattr(app, 'pou_container'):
                            pou_container = app.pou_container
                            print("Application has pou_container: " + str(pou_container is not None))
                        else:
                            print("Application does not have pou_container attribute")
                else:
                    print("Project does not have active_application attribute")
    
    # Return diagnostic information
    result = {
        "success": True,
        "diagnostic_info": {
            "system_exists": system_exists,
            "projects_exists": projects_exists,
            "session_exists": session_exists,
            "active_project_exists": session_exists and hasattr(session, 'active_project') and session.active_project is not None
        }
    }
except Exception as e:
    print("Error: " + str(e))
    result = {
        "success": False,
        "error": str(e)
    }
"""
        execute_custom_script(test_script_1)
        
        # Test 2: Try to create a POU with debug info
        logger.info("=== Running Script Test 2: Debug POU Creation ===")
        test_script_2 = """
import scriptengine
import json
import sys

try:
    # Check if we have an active project
    if not hasattr(session, 'active_project') or session.active_project is None:
        print("No active project in session")
        raise ValueError("No active project in session")
    
    # Get the active project
    project = session.active_project
    print("Got active project: " + str(project is not None))
    
    # Try to get application
    if not hasattr(project, 'active_application') or project.active_application is None:
        print("Project has no active application")
        raise ValueError("Project has no active application")
    
    application = project.active_application
    print("Got active application: " + str(application is not None))
    
    # Try to get POU container
    if not hasattr(application, 'pou_container') or application.pou_container is None:
        print("Application has no POU container")
        raise ValueError("Application has no POU container")
    
    container = application.pou_container
    print("Got POU container: " + str(container is not None))
    
    # Check if POU types are defined
    print("Checking POU types...")
    if hasattr(scriptengine, 'PouType'):
        print("PouType enum exists")
        print("Available POU types: " + str(dir(scriptengine.PouType)))
    else:
        print("PouType enum does not exist")
        # Try to find all enums
        for attr in dir(scriptengine):
            if not attr.startswith('_'):
                val = getattr(scriptengine, attr)
                if str(type(val)).endswith('EnumType'):
                    print("Found enum: " + attr)
    
    # Check if language types are defined
    print("Checking language types...")
    if hasattr(scriptengine, 'ImplementationLanguage'):
        print("ImplementationLanguage enum exists")
        print("Available languages: " + str(dir(scriptengine.ImplementationLanguage)))
    else:
        print("ImplementationLanguage enum does not exist")
        # Try to find language enum
        for attr in dir(scriptengine):
            if not attr.startswith('_') and 'language' in attr.lower():
                print("Possible language enum: " + attr)
    
    # Try creating a POU
    print("Attempting to create a POU...")
    try:
        # Try to find the create_pou method
        if hasattr(container, 'create_pou'):
            print("create_pou method exists on container")
            
            # Get enum values
            pou_type = None
            if hasattr(scriptengine, 'PouType') and hasattr(scriptengine.PouType, 'FUNCTION_BLOCK'):
                pou_type = scriptengine.PouType.FUNCTION_BLOCK
                print("Using PouType.FUNCTION_BLOCK")
            else:
                print("PouType.FUNCTION_BLOCK not found")
                # Try to search for it
                for attr in dir(scriptengine):
                    if 'FUNCTION_BLOCK' in attr:
                        print("Found possible match: " + attr)
            
            language = None
            if hasattr(scriptengine, 'ImplementationLanguage') and hasattr(scriptengine.ImplementationLanguage, 'ST'):
                language = scriptengine.ImplementationLanguage.ST
                print("Using ImplementationLanguage.ST")
            else:
                print("ImplementationLanguage.ST not found")
                # Try to search for it
                for attr in dir(scriptengine):
                    if '.ST' in attr:
                        print("Found possible match: " + attr)
            
            # Only proceed if we have both type and language
            if pou_type is not None and language is not None:
                # Create POU
                pou_name = "TestPOU_Debug"
                print("Creating POU: " + pou_name)
                pou = container.create_pou(pou_name, pou_type, language)
                print("POU created successfully: " + str(pou is not None))
                
                if pou is not None:
                    # Try setting code
                    if hasattr(pou, 'set_implementation_code'):
                        print("set_implementation_code method exists")
                        code = """
FUNCTION_BLOCK TestPOU_Debug
VAR_INPUT
    iValue : INT;
END_VAR
VAR_OUTPUT
    oResult : INT;
END_VAR

oResult := iValue * 2;
"""
                        pou.set_implementation_code(code)
                        print("Code set successfully")
                    else:
                        print("set_implementation_code method does not exist")
                        # Look for alternatives
                        for attr in dir(pou):
                            if 'code' in attr.lower() or 'implementation' in attr.lower():
                                print("Possible code setting method: " + attr)
            else:
                print("Missing POU type or language enum values")
        else:
            print("create_pou method does not exist on container")
            # Look for alternatives
            for attr in dir(container):
                if 'create' in attr.lower() or 'pou' in attr.lower():
                    print("Possible POU creation method: " + attr)
    except Exception as e:
        print("Error creating POU: " + str(e))
    
    # Return success
    result = {
        "success": True,
        "message": "Debug script executed"
    }
except Exception as e:
    print("Error: " + str(e))
    result = {
        "success": False,
        "error": str(e)
    }
"""
        execute_custom_script(test_script_2)
        
        # Test 3: Try to inspect available POU types more closely
        logger.info("=== Running Script Test 3: Inspect POU Types ===")
        test_script_3 = """
import scriptengine
import json
import sys
import inspect

try:
    # Inspect the scriptengine module
    print("Inspecting scriptengine module...")
    
    # Get all module attributes
    module_attrs = [attr for attr in dir(scriptengine) if not attr.startswith('_')]
    print("Module attributes: " + str(module_attrs))
    
    # Check for enums that might define POU types
    enum_names = []
    for attr_name in module_attrs:
        attr = getattr(scriptengine, attr_name)
        if 'enum' in str(type(attr)).lower():
            enum_names.append(attr_name)
    
    print("Enums found: " + str(enum_names))
    
    # Look for POU type definitions
    pou_type_candidates = []
    for attr_name in module_attrs:
        if 'pou' in attr_name.lower() or 'type' in attr_name.lower():
            pou_type_candidates.append(attr_name)
    
    print("Potential POU type definitions: " + str(pou_type_candidates))
    
    # Inspect each candidate
    for name in pou_type_candidates:
        attr = getattr(scriptengine, name)
        print(f"Inspecting {name}: {type(attr)}")
        if hasattr(attr, '__members__'):
            print(f"Members of {name}: {attr.__members__}")
        elif hasattr(attr, '__dict__'):
            print(f"Dict of {name}: {attr.__dict__}")
    
    # Look for language definitions
    lang_candidates = []
    for attr_name in module_attrs:
        if 'language' in attr_name.lower() or 'impl' in attr_name.lower():
            lang_candidates.append(attr_name)
    
    print("Potential language definitions: " + str(lang_candidates))
    
    # Inspect language candidates
    for name in lang_candidates:
        attr = getattr(scriptengine, name)
        print(f"Inspecting {name}: {type(attr)}")
        if hasattr(attr, '__members__'):
            print(f"Members of {name}: {attr.__members__}")
        elif hasattr(attr, '__dict__'):
            print(f"Dict of {name}: {attr.__dict__}")
    
    # Return success
    result = {
        "success": True,
        "message": "POU type inspection complete"
    }
except Exception as e:
    print("Error: " + str(e))
    result = {
        "success": False,
        "error": str(e)
    }
"""
        execute_custom_script(test_script_3)
        
    finally:
        # Always try to stop the session
        logger.info("Stopping session...")
        stop_session()

def main():
    """Main function to run diagnostic tests."""
    parser = argparse.ArgumentParser(description="CODESYS API Debugging Script")
    parser.add_argument("--url", default=DEFAULT_API_URL, help="API server URL")
    parser.add_argument("--key", default=DEFAULT_API_KEY, help="API key")
    
    args = parser.parse_args()
    
    # Run the script tests
    run_script_tests()

if __name__ == "__main__":
    main()