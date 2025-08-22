#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CODESYS API Test Client

This script tests the CODESYS API by sending various HTTP requests
to the API server and verifying the responses.
"""

import requests
import json
import time
import os
import argparse
import sys

# Default API settings
DEFAULT_API_URL = "http://localhost:8080"
DEFAULT_API_KEY = "admin"  # This is the default key created by ApiKeyManager

class CodesysApiClient:
    """Client for the CODESYS API."""
    
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"ApiKey {api_key}",
            "Content-Type": "application/json"
        }
    
    def request(self, method, endpoint, data=None, params=None):
        """Send a request to the API."""
        url = f"{self.base_url}/{endpoint}"
        try:
            if method.lower() == "get":
                response = requests.get(url, headers=self.headers, params=params)
            elif method.lower() == "post":
                response = requests.post(url, headers=self.headers, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
            # Try to parse JSON response
            try:
                result = response.json()
            except json.JSONDecodeError:
                result = {"text": response.text}
                
            # Add status code to the result
            result["status_code"] = response.status_code
            return result
                
        except requests.exceptions.RequestException as e:
            print(f"Error sending request to {url}: {str(e)}")
            return {"success": False, "error": str(e), "status_code": 0}
    
    def session_start(self):
        """Start a CODESYS session."""
        print("Starting CODESYS session...")
        result = self.request("post", "api/v1/session/start")
        print(f"Session start result: {json.dumps(result, indent=2)}")
        return result
    
    def session_status(self):
        """Get the status of the CODESYS session."""
        print("Getting session status...")
        result = self.request("get", "api/v1/session/status")
        print(f"Session status result: {json.dumps(result, indent=2)}")
        return result
    
    def create_project(self, path=None):
        """Create a new CODESYS project."""
        print("Creating a new project...")
        
        # Generate a default path if none provided
        if not path:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            path = os.path.join(os.getcwd(), f"CODESYS_TestProject_{timestamp}.project")
            
        # Create the project
        data = {"path": path}
        result = self.request("post", "api/v1/project/create", data)
        print(f"Project creation result: {json.dumps(result, indent=2)}")
        return result
    
    def stop_session(self):
        """Stop the CODESYS session."""
        print("Stopping CODESYS session...")
        result = self.request("post", "api/v1/session/stop")
        print(f"Session stop result: {json.dumps(result, indent=2)}")
        return result

def main():
    """Run the test client."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="CODESYS API Test Client")
    parser.add_argument("--url", default=DEFAULT_API_URL, help="API server URL (default: %(default)s)")
    parser.add_argument("--key", default=DEFAULT_API_KEY, help="API key (default: %(default)s)")
    parser.add_argument("--project-path", help="Path for creating project")
    
    args = parser.parse_args()
    
    # Create API client
    client = CodesysApiClient(args.url, args.key)
    
    try:
        # Run tests
        client.session_status()
        client.session_start()
        time.sleep(2)  # Wait for session to fully initialize
        client.session_status()
        client.create_project(args.project_path)
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
    finally:
        # Always try to stop the session at the end
        try:
            client.stop_session()
        except:
            pass

if __name__ == "__main__":
    main()