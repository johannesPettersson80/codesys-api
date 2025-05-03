#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CODESYS API Debug Project Creation

This script provides detailed debugging for the project creation functionality
of the CODESYS API. It executes a project creation request with extensive logging
and output to help diagnose any issues with script execution in CODESYS.
"""

import sys
import os
import time
import json
import logging
import requests
import uuid
import tempfile

# Setup logging - more verbose than the test script
logging.basicConfig(
    level=logging.DEBUG,  # Debug level for more details
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("debug_project_creation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('codesys_api_debug')

# API configuration
API_BASE_URL = "http://localhost:8080/api/v1"
API_KEY = "admin"  # Default API key

# Configure requests session
session = requests.Session()
session.headers.update({
    'Authorization': 'ApiKey ' + API_KEY,
    'Content-Type': 'application/json'
})


def call_api(method, endpoint, data=None, params=None, timeout=60):
    """Make an API call to the CODESYS REST API with detailed logging."""
    url = "{0}/{1}".format(API_BASE_URL, endpoint)
    
    logger.debug(f"API Request: {method} {url}")
    if data:
        logger.debug(f"Request Data: {json.dumps(data, indent=2)}")
    if params:
        logger.debug(f"Request Params: {json.dumps(params, indent=2)}")
    
    try:
        logger.debug(f"Making {method} request to {url} (timeout: {timeout}s)")
        
        if method.upper() == 'GET':
            response = session.get(url, params=params, timeout=timeout)
        elif method.upper() == 'POST':
            response = session.post(url, json=data, timeout=timeout)
        else:
            raise ValueError("Unsupported HTTP method: {0}".format(method))
        
        logger.debug(f"Response Status Code: {response.status_code}")
        logger.debug(f"Response Headers: {dict(response.headers)}")
        
        # Check if the response is JSON
        try:
            result = response.json()
            logger.debug(f"Response JSON: {json.dumps(result, indent=2)}")
        except:
            logger.error(f"Non-JSON response: {response.text}")
            return {'success': False, 'error': 'Non-JSON response from server'}
            
        # Log results
        if result.get('success', False):
            logger.info(f"{method} {endpoint} - Success")
        else:
            logger.error(f"{method} {endpoint} - Error: {result.get('error', 'Unknown error')}")
            
        return result
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}", exc_info=True)
        return {'success': False, 'error': str(e)}


def start_session():
    """Start a CODESYS session with detailed logging."""
    logger.info("Starting CODESYS session...")
    
    # Try up to 3 times with increasing timeouts
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        logger.info(f"Attempt {attempt} of {max_attempts} to start session...")
        try:
            result = call_api('POST', 'session/start', timeout=60)
            if result.get('success', False):
                logger.info("Session started successfully")
                return True
            else:
                error = result.get('error', 'Unknown error')
                logger.warning(f"Attempt {attempt} failed: {error}")
                if attempt < max_attempts:
                    logger.info(f"Waiting before retry...")
                    time.sleep(5)  # Wait 5 seconds before retry
        except Exception as e:
            logger.warning(f"Attempt {attempt} exception: {str(e)}")
            if attempt < max_attempts:
                logger.info(f"Waiting before retry...")
                time.sleep(5)  # Wait 5 seconds before retry
    
    logger.error("Failed to start session after multiple attempts")
    return False


def get_session_status():
    """Get the status of the CODESYS session."""
    logger.info("Getting session status...")
    result = call_api('GET', 'session/status')
    logger.info(f"Session status: {json.dumps(result.get('status', {}), indent=2)}")
    return result


def create_project(path):
    """Create a new CODESYS project."""
    logger.info(f"Creating new project at {path}...")
    return call_api('POST', 'project/create', {'path': path}, timeout=30)  # Shorter timeout for quicker testing


def stop_session():
    """Stop the CODESYS session."""
    logger.info("Stopping CODESYS session...")
    return call_api('POST', 'session/stop')


def check_paths_and_permissions():
    """Check paths and permissions that are important for script execution."""
    logger.info("Checking paths and permissions...")
    
    paths_to_check = [
        os.path.dirname(os.path.abspath(__file__)),  # Script directory
        tempfile.gettempdir(),  # Temp directory
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "requests"),  # Request directory
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")   # Result directory
    ]
    
    for path in paths_to_check:
        try:
            exists = os.path.exists(path)
            is_dir = os.path.isdir(path) if exists else False
            is_writable = os.access(path, os.W_OK) if exists else False
            
            logger.info(f"Path: {path}")
            logger.info(f"  - Exists: {exists}")
            logger.info(f"  - Is Directory: {is_dir}")
            logger.info(f"  - Is Writable: {is_writable}")
            
            if exists and is_dir:
                # Check contents
                try:
                    contents = os.listdir(path)
                    logger.info(f"  - Contents: {contents[:10]} {'...' if len(contents) > 10 else ''}")
                    logger.info(f"  - Item Count: {len(contents)}")
                except Exception as e:
                    logger.warning(f"  - Could not list contents: {str(e)}")
            
            # Test write access by creating a test file
            if exists:
                test_file = os.path.join(path, f"write_test_{uuid.uuid4()}.txt")
                try:
                    with open(test_file, 'w') as f:
                        f.write("Test write access")
                    logger.info(f"  - Write test: Success")
                    try:
                        os.remove(test_file)
                        logger.info(f"  - Remove test: Success")
                    except Exception as e:
                        logger.warning(f"  - Could not remove test file: {str(e)}")
                except Exception as e:
                    logger.warning(f"  - Write test failed: {str(e)}")
        except Exception as e:
            logger.error(f"Error checking path {path}: {str(e)}")
        
        logger.info("-" * 40)
    
    # Special check for the project destination path
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    project_path = f"C:/Users/Public/Documents/CODESYS_Test_{timestamp}.project"
    project_dir = os.path.dirname(project_path)
    
    logger.info(f"Project directory: {project_dir}")
    try:
        if os.path.exists(project_dir):
            is_writable = os.access(project_dir, os.W_OK)
            logger.info(f"  - Exists: True")
            logger.info(f"  - Is Writable: {is_writable}")
        else:
            logger.warning(f"  - Project directory doesn't exist")
    except Exception as e:
        logger.error(f"Error checking project directory: {str(e)}")


def debug_project_creation():
    """Debug project creation functionality with detailed logging."""
    log_separator = "=" * 80
    logger.info(log_separator)
    logger.info("CODESYS API Debug Project Creation")
    logger.info(log_separator)
    
    # Step 1: Check paths and permissions
    check_paths_and_permissions()
    
    # Step 2: Start CODESYS session
    logger.info(log_separator)
    logger.info("Starting CODESYS Session")
    logger.info(log_separator)
    
    if not start_session():
        logger.error("Failed to start CODESYS session, aborting test")
        return False
    
    # Step 3: Get session status to verify CODESYS is running
    logger.info(log_separator)
    logger.info("Checking CODESYS Session Status")
    logger.info(log_separator)
    
    status_result = get_session_status()
    if not status_result.get('success', False):
        logger.error("Failed to get session status, aborting test")
        return False
    
    process_running = status_result.get('status', {}).get('process', {}).get('running', False)
    if not process_running:
        logger.error("CODESYS process not running according to status, aborting test")
        return False
    
    logger.info("CODESYS process is running, proceeding with project creation test")
    
    # Step 4: Create a test project with debug information
    logger.info(log_separator)
    logger.info("Creating Test Project")
    logger.info(log_separator)
    
    # Use a path relative to the installation folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    project_path = os.path.join(script_dir, f"CODESYS_Debug_{timestamp}.project")
    # Convert to forward slashes for the API
    project_path = project_path.replace("\\", "/")
    
    logger.info(f"Creating test project at: {project_path}")
    
    # Create the project with detailed logging
    start_time = time.time()
    project_result = create_project(project_path)
    elapsed_time = time.time() - start_time
    
    # Step 5: Display detailed results
    logger.info(log_separator)
    logger.info(f"Project Creation Results (Elapsed Time: {elapsed_time:.2f} seconds)")
    logger.info(log_separator)
    
    logger.info(f"Success: {project_result.get('success', False)}")
    
    if project_result.get('success', False):
        project_info = project_result.get('project', {})
        logger.info(f"Project path: {project_info.get('path', 'N/A')}")
        logger.info(f"Project name: {project_info.get('name', 'N/A')}")
        logger.info(f"Project dirty: {project_info.get('dirty', 'N/A')}")
        
        # Check all returned fields
        logger.info("All project fields:")
        for key, value in project_info.items():
            logger.info(f"  - {key}: {value}")
        
        # Verify the file exists if a path was returned
        if 'path' in project_info:
            actual_path = project_info.get('path')
            try:
                if os.path.exists(actual_path):
                    file_size = os.path.getsize(actual_path)
                    logger.info(f"Project file verified to exist on disk")
                    logger.info(f"  - Path: {actual_path}")
                    logger.info(f"  - Size: {file_size} bytes")
                    logger.info(f"  - Last Modified: {time.ctime(os.path.getmtime(actual_path))}")
                else:
                    logger.warning(f"Project file does not exist on disk at: {actual_path}")
            except Exception as e:
                logger.warning(f"Could not verify project file existence: {str(e)}")
    else:
        logger.error(f"Project creation failed: {project_result.get('error', 'Unknown error')}")
        if 'traceback' in project_result:
            logger.error(f"Traceback: {project_result.get('traceback')}")
        
        # Log all error fields
        logger.info("All error fields:")
        for key, value in project_result.items():
            if key not in ['success', 'error', 'traceback']:
                logger.info(f"  - {key}: {value}")
    
    # Step 6: Stop CODESYS session
    logger.info(log_separator)
    logger.info("Stopping CODESYS Session")
    logger.info(log_separator)
    
    stop_result = stop_session()
    if not stop_result.get('success', False):
        logger.error(f"Failed to stop CODESYS session: {stop_result.get('error', 'Unknown error')}")
    
    # Step 7: Final result
    logger.info(log_separator)
    logger.info("Final Debug Result")
    logger.info(log_separator)
    
    if project_result.get('success', False):
        logger.info("PROJECT CREATION DEBUG: SUCCESS")
    else:
        logger.error("PROJECT CREATION DEBUG: FAILED")
    
    logger.info(f"See log file for detailed information: debug_project_creation.log")
    
    # Return overall test result
    return project_result.get('success', False)


if __name__ == "__main__":
    try:
        if debug_project_creation():
            logger.info("DEBUG COMPLETED SUCCESSFULLY")
            sys.exit(0)
        else:
            logger.error("DEBUG COMPLETED WITH ERRORS")
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Debug interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        sys.exit(1)