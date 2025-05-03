#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CODESYS API Project Creation Test

This script tests the project creation functionality of the CODESYS API,
focusing specifically on ensuring that scripts are properly executed in CODESYS.
"""

import sys
import os
import time
import json
import logging
import requests
import tempfile

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('codesys_api_test')

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
    """Make an API call to the CODESYS REST API."""
    url = "{0}/{1}".format(API_BASE_URL, endpoint)
    
    try:
        if method.upper() == 'GET':
            response = session.get(url, params=params, timeout=timeout)
        elif method.upper() == 'POST':
            response = session.post(url, json=data, timeout=timeout)
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
    return call_api('POST', 'project/create', {'path': path}, timeout=600)


def stop_session():
    """Stop the CODESYS session."""
    logger.info("Stopping CODESYS session...")
    return call_api('POST', 'session/stop')


def test_project_creation():
    """Test project creation functionality."""
    logger.info("=" * 80)
    logger.info("Starting project creation test")
    logger.info("=" * 80)
    
    # Step 1: Start CODESYS session
    if not start_session():
        logger.error("Failed to start CODESYS session, aborting test")
        return False
    
    # Step 2: Get session status to verify CODESYS is running
    status_result = get_session_status()
    if not status_result.get('success', False):
        logger.error("Failed to get session status, aborting test")
        return False
    
    process_running = status_result.get('status', {}).get('process', {}).get('running', False)
    if not process_running:
        logger.error("CODESYS process not running according to status, aborting test")
        return False
    
    logger.info("CODESYS process is running, proceeding with project creation test")
    
    # Step 3: Create a test project
    # Use a unique path for this test to avoid conflicts
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    project_path = f"C:/Users/Public/Documents/CODESYS_Test_{timestamp}.project"
    
    logger.info(f"Creating test project at: {project_path}")
    
    project_result = create_project(project_path)
    
    # Step 4: Display detailed results
    logger.info("=" * 80)
    logger.info("Project creation test result")
    logger.info("=" * 80)
    logger.info(f"Success: {project_result.get('success', False)}")
    
    if project_result.get('success', False):
        project_info = project_result.get('project', {})
        logger.info(f"Project path: {project_info.get('path', 'N/A')}")
        logger.info(f"Project name: {project_info.get('name', 'N/A')}")
        logger.info(f"Project dirty: {project_info.get('dirty', 'N/A')}")
        if 'file_exists' in project_info:
            logger.info(f"Project file exists: {project_info.get('file_exists', False)}")
        
        # Optionally, verify the file exists if a path was returned
        if 'path' in project_info:
            actual_path = project_info.get('path')
            try:
                if os.path.exists(actual_path):
                    logger.info(f"Project file verified to exist on disk at: {actual_path}")
                else:
                    logger.warning(f"Project file does not exist on disk at: {actual_path}")
            except Exception as e:
                logger.warning(f"Could not verify project file existence: {str(e)}")
    else:
        logger.error(f"Project creation failed: {project_result.get('error', 'Unknown error')}")
        if 'traceback' in project_result:
            logger.error(f"Traceback: {project_result.get('traceback')}")
    
    # Step 5: Stop CODESYS session
    stop_result = stop_session()
    if not stop_result.get('success', False):
        logger.error(f"Failed to stop CODESYS session: {stop_result.get('error', 'Unknown error')}")
    
    # Return overall test result
    return project_result.get('success', False)


if __name__ == "__main__":
    try:
        if test_project_creation():
            logger.info("PROJECT CREATION TEST PASSED")
            sys.exit(0)
        else:
            logger.error("PROJECT CREATION TEST FAILED")
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        sys.exit(1)