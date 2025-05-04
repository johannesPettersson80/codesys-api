#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CODESYS Simple API Client

A simplified client for manual testing of the CODESYS API.
"""

import requests
import json
import time
import os
import sys
import argparse

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
            print(f"Sending {method.upper()} request to {url}")
            if data:
                print(f"Request data: {json.dumps(data, indent=2)}")
                
            if method.lower() == "get":
                response = requests.get(url, headers=self.headers, params=params, timeout=120)
            elif method.lower() == "post":
                response = requests.post(url, headers=self.headers, json=data, timeout=120)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
            # Try to parse JSON response
            try:
                result = response.json()
                print(f"Response: {json.dumps(result, indent=2)}")
            except json.JSONDecodeError:
                result = {"text": response.text}
                print(f"Response (non-JSON): {response.text}")
                
            # Add status code to the result
            result["status_code"] = response.status_code
            return result
                
        except requests.exceptions.RequestException as e:
            print(f"Error sending request to {url}: {str(e)}")
            return {"success": False, "error": str(e), "status_code": 0}
    
    def session_start(self):
        """Start a CODESYS session."""
        print("\n=== Starting CODESYS session ===")
        return self.request("post", "api/v1/session/start")
    
    def session_status(self):
        """Get the status of the CODESYS session."""
        print("\n=== Getting session status ===")
        return self.request("get", "api/v1/session/status")
    
    def create_project(self, path=None):
        """Create a new CODESYS project."""
        print("\n=== Creating a new project ===")
        
        # Generate a default path if none provided
        if not path:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            path = os.path.abspath(f"CODESYS_TestProject_{timestamp}.project")
            
        # Create the project
        data = {"path": path}
        return self.request("post", "api/v1/project/create", data)
    
    def stop_session(self):
        """Stop the CODESYS session."""
        print("\n=== Stopping CODESYS session ===")
        return self.request("post", "api/v1/session/stop")
    
    def run_basic_test(self, project_path=None):
        """Run a basic test sequence."""
        try:
            print("\n*** Starting Basic Test Sequence ***\n")
            
            # Check session status
            self.session_status()
            
            # Start session
            self.session_start()
            print("Waiting 5 seconds for session to initialize...")
            time.sleep(5)
            
            # Check session status again
            self.session_status()
            
            # Create project
            self.create_project(project_path)
            
            # Final status check
            print("Waiting 2 seconds...")
            time.sleep(2)
            self.session_status()
            
        except KeyboardInterrupt:
            print("\nTest interrupted by user.")
        finally:
            # Always try to stop the session at the end
            try:
                print("\n*** Cleaning up ***")
                self.stop_session()
            except:
                pass

def main():
    """Run the simple client."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="CODESYS Simple API Client")
    parser.add_argument("--url", default=DEFAULT_API_URL, help="API server URL (default: %(default)s)")
    parser.add_argument("--key", default=DEFAULT_API_KEY, help="API key (default: %(default)s)")
    parser.add_argument("--project-path", help="Path for creating project")
    
    args = parser.parse_args()
    
    # Create API client
    client = CodesysApiClient(args.url, args.key)
    
    # Run basic test
    client.run_basic_test(args.project_path)

if __name__ == "__main__":
    main()