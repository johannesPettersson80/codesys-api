#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CODESYS API Test Suite

This script provides a comprehensive test suite for the CODESYS API,
testing all endpoints and functionality.
"""

import requests
import json
import time
import os
import sys
import argparse
import uuid
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='api_test_suite.log'
)
logger = logging.getLogger('api_test_suite')

# Add console handler
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)

# Default API settings
DEFAULT_API_URL = "http://localhost:8080"
DEFAULT_API_KEY = "admin"  # This is the default key created by ApiKeyManager

class CodesysApiTester:
    """Test client for the CODESYS API."""
    
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"ApiKey {api_key}",
            "Content-Type": "application/json"
        }
        self.project_path = None
        self.project_name = None
        self.test_results = {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "tests": []
        }
        
    def request(self, method, endpoint, data=None, params=None, description=None):
        """Send a request to the API."""
        url = f"{self.base_url}/{endpoint}"
        test_name = description or endpoint
        self.test_results["total"] += 1
        
        try:
            logger.info(f"Sending {method.upper()} request to {endpoint}")
            if data:
                logger.info(f"Request data: {data}")
                
            start_time = time.time()
            
            if method.lower() == "get":
                response = requests.get(url, headers=self.headers, params=params, timeout=120)
            elif method.lower() == "post":
                response = requests.post(url, headers=self.headers, json=data, timeout=120)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            elapsed_time = time.time() - start_time
                
            # Try to parse JSON response
            try:
                result = response.json()
            except json.JSONDecodeError:
                result = {"text": response.text}
                
            # Add status code and elapsed time to the result
            result["status_code"] = response.status_code
            result["elapsed_seconds"] = elapsed_time
            
            # Determine if the test passed
            passed = response.status_code == 200 and result.get("success", False)
            
            # Log the result
            if passed:
                logger.info(f"✅ {test_name}: SUCCESS ({elapsed_time:.2f}s)")
                self.test_results["passed"] += 1
            else:
                error_message = result.get("error", "Unknown error")
                logger.error(f"❌ {test_name}: FAILED - {error_message} ({elapsed_time:.2f}s)")
                self.test_results["failed"] += 1
            
            # Store test result
            self.test_results["tests"].append({
                "name": test_name,
                "endpoint": endpoint,
                "method": method.upper(),
                "status_code": response.status_code,
                "elapsed_seconds": elapsed_time,
                "success": passed,
                "result": result
            })
            
            return result
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ {test_name}: CONNECTION ERROR - {str(e)}")
            self.test_results["failed"] += 1
            
            # Store test result
            error_result = {"success": False, "error": str(e), "status_code": 0}
            self.test_results["tests"].append({
                "name": test_name,
                "endpoint": endpoint,
                "method": method.upper(),
                "status_code": 0,
                "elapsed_seconds": 0,
                "success": False,
                "result": error_result
            })
            
            return error_result
        except Exception as e:
            logger.error(f"❌ {test_name}: ERROR - {str(e)}")
            self.test_results["failed"] += 1
            
            # Store test result
            error_result = {"success": False, "error": str(e), "status_code": 0}
            self.test_results["tests"].append({
                "name": test_name,
                "endpoint": endpoint,
                "method": method.upper(),
                "status_code": 0,
                "elapsed_seconds": 0,
                "success": False,
                "result": error_result
            })
            
            return error_result
    
    def system_info(self):
        """Get system information."""
        return self.request("get", "api/v1/system/info", description="Get System Information")
    
    def system_logs(self):
        """Get system logs."""
        return self.request("get", "api/v1/system/logs", description="Get System Logs")
        
    def session_status(self):
        """Get the status of the CODESYS session."""
        return self.request("get", "api/v1/session/status", description="Get Session Status")
    
    def session_start(self):
        """Start a CODESYS session."""
        return self.request("post", "api/v1/session/start", description="Start CODESYS Session")
    
    def session_stop(self):
        """Stop the CODESYS session."""
        return self.request("post", "api/v1/session/stop", description="Stop CODESYS Session")
    
    def session_restart(self):
        """Restart the CODESYS session."""
        return self.request("post", "api/v1/session/restart", description="Restart CODESYS Session")
    
    def create_project(self, path=None):
        """Create a new CODESYS project."""
        # Generate a default path if none provided
        if not path:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            # Use absolute path for reliability
            path = os.path.abspath(f"CODESYS_TestProject_{timestamp}.project")
            
        self.project_path = path
        self.project_name = os.path.basename(path)
            
        # Create the project
        data = {"path": path}
        return self.request("post", "api/v1/project/create", data, description=f"Create Project: {path}")
    
    def open_project(self, path=None):
        """Open an existing CODESYS project."""
        # Use the recently created project path if none provided
        if not path and self.project_path:
            path = self.project_path
            
        if not path:
            logger.error("No project path provided and no project has been created")
            return {"success": False, "error": "No project path provided"}
            
        data = {"path": path}
        return self.request("post", "api/v1/project/open", data, description=f"Open Project: {path}")
    
    def save_project(self):
        """Save the current project."""
        return self.request("post", "api/v1/project/save", description="Save Project")
    
    def close_project(self):
        """Close the current project."""
        return self.request("post", "api/v1/project/close", description="Close Project")
    
    def list_projects(self):
        """List recent projects."""
        return self.request("get", "api/v1/project/list", description="List Projects")
    
    def compile_project(self, clean_build=False):
        """Compile the current project."""
        data = {"clean_build": clean_build}
        description = "Compile Project" if not clean_build else "Clean Build Project"
        return self.request("post", "api/v1/project/compile", data, description=description)
    
    def create_pou(self, name, pou_type="FunctionBlock", language="ST", parent_path=""):
        """Create a new POU (Program Organization Unit)."""
        data = {
            "name": name,
            "type": pou_type,
            "language": language,
            "parentPath": parent_path
        }
        description = f"Create POU: {name} ({pou_type}, {language})"
        return self.request("post", "api/v1/pou/create", data, description=description)
    
    def set_pou_code(self, path, code):
        """Set the code for a POU."""
        data = {
            "path": path,
            "code": code
        }
        description = f"Set POU Code: {path}"
        return self.request("post", "api/v1/pou/code", data, description=description)
    
    def list_pous(self, parent_path=""):
        """List POUs in the project."""
        params = {}
        if parent_path:
            params["parentPath"] = parent_path
        description = f"List POUs" + (f" in {parent_path}" if parent_path else "")
        return self.request("get", "api/v1/pou/list", params=params, description=description)
    
    def execute_script(self, script):
        """Execute a custom script in CODESYS."""
        data = {"script": script}
        return self.request("post", "api/v1/script/execute", data, description="Execute Custom Script")
    
    def run_basic_test_suite(self):
        """Run the basic test suite."""
        logger.info("=== Starting Basic Test Suite ===")
        
        try:
            # System tests
            self.system_info()
            
            # Session tests
            self.session_status()
            self.session_start()
            time.sleep(5)  # Wait for session to initialize
            self.session_status()
            
            # Project tests
            self.create_project()
            time.sleep(2)
            self.save_project()
            self.list_projects()
            
            # Create a simple POU
            pou_name = f"TestPOU_{int(time.time())}"
            self.create_pou(pou_name)
            time.sleep(1)
            
            # Set POU code (simple function block)
            pou_code = f"""
FUNCTION_BLOCK {pou_name}
VAR_INPUT
    iValue : INT;
END_VAR
VAR_OUTPUT
    oResult : INT;
END_VAR
VAR
    InternalVar : INT;
END_VAR

oResult := iValue * 2;  // Simple calculation
            """
            self.set_pou_code(pou_name, pou_code)
            time.sleep(1)
            
            # List POUs
            self.list_pous()
            
            # Compile the project
            self.compile_project()
            
            # Close the project
            self.close_project()
            
        except Exception as e:
            logger.error(f"Error during test suite: {str(e)}")
        finally:
            # Always try to stop the session at the end
            try:
                self.session_stop()
            except:
                pass
                
        # Print test summary
        self.print_test_summary()
        
        return self.test_results
    
    def run_advanced_test_suite(self):
        """Run the advanced test suite with more tests."""
        logger.info("=== Starting Advanced Test Suite ===")
        
        try:
            # System tests
            self.system_info()
            self.system_logs()
            
            # Session tests
            self.session_status()
            self.session_start()
            time.sleep(5)  # Wait for session to initialize
            self.session_status()
            
            # Project tests
            self.create_project()
            time.sleep(2)
            self.save_project()
            
            # Create multiple POUs with different types
            pou_types = [
                {"name": f"TestProgram_{int(time.time())}", "type": "Program", "language": "ST"},
                {"name": f"TestFB_{int(time.time())}", "type": "FunctionBlock", "language": "ST"},
                {"name": f"TestFunction_{int(time.time())}", "type": "Function", "language": "ST"}
            ]
            
            for pou in pou_types:
                self.create_pou(pou["name"], pou["type"], pou["language"])
                time.sleep(1)
                
                # Set appropriate code based on POU type
                if pou["type"] == "Program":
                    code = f"""
PROGRAM {pou["name"]}
VAR
    TestVar : INT := 0;
END_VAR

// Test program code
TestVar := TestVar + 1;
                    """
                elif pou["type"] == "FunctionBlock":
                    code = f"""
FUNCTION_BLOCK {pou["name"]}
VAR_INPUT
    iValue : INT;
END_VAR
VAR_OUTPUT
    oResult : INT;
END_VAR

// Test function block code
oResult := iValue * 2;
                    """
                elif pou["type"] == "Function":
                    code = f"""
FUNCTION {pou["name"]} : INT
VAR_INPUT
    iValue : INT;
END_VAR

// Test function code
{pou["name"]} := iValue * 3;
                    """
                
                self.set_pou_code(pou["name"], code)
                time.sleep(1)
            
            # List POUs
            self.list_pous()
            
            # Compile the project
            self.compile_project()
            
            # Close the project
            self.close_project()
            
            # Test project reopening
            self.open_project()
            time.sleep(2)
            
            # List POUs again to verify they're still there
            self.list_pous()
            
            # Close the project
            self.close_project()
            
            # Test session restart
            self.session_restart()
            time.sleep(5)  # Wait for restart
            self.session_status()
            
        except Exception as e:
            logger.error(f"Error during advanced test suite: {str(e)}")
        finally:
            # Always try to stop the session at the end
            try:
                self.session_stop()
            except:
                pass
                
        # Print test summary
        self.print_test_summary()
        
        return self.test_results
    
    def print_test_summary(self):
        """Print a summary of test results."""
        total = self.test_results["total"]
        passed = self.test_results["passed"]
        failed = self.test_results["failed"]
        pass_rate = (passed / total) * 100 if total > 0 else 0
        
        summary = f"""
=============================================
           CODESYS API TEST RESULTS
=============================================
Total Tests: {total}
Passed:      {passed}
Failed:      {failed}
Pass Rate:   {pass_rate:.2f}%
=============================================
"""
        logger.info(summary)
        
    def save_test_results(self, filename=None):
        """Save test results to a JSON file."""
        if not filename:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"test_results_{timestamp}.json"
            
        # Add timestamp to results
        self.test_results["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.test_results, f, indent=2)
            logger.info(f"Test results saved to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving test results: {str(e)}")
            return False

def main():
    """Run the test suite."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="CODESYS API Test Suite")
    parser.add_argument("--url", default=DEFAULT_API_URL, help="API server URL (default: %(default)s)")
    parser.add_argument("--key", default=DEFAULT_API_KEY, help="API key (default: %(default)s)")
    parser.add_argument("--project-path", help="Path for creating project")
    parser.add_argument("--advanced", action="store_true", help="Run advanced test suite")
    parser.add_argument("--output", help="Output file for test results")
    
    args = parser.parse_args()
    
    # Create API tester
    tester = CodesysApiTester(args.url, args.key)
    
    try:
        # Run tests
        if args.advanced:
            tester.run_advanced_test_suite()
        else:
            tester.run_basic_test_suite()
        
        # Save test results
        tester.save_test_results(args.output)
        
    except KeyboardInterrupt:
        logger.info("\nTest interrupted by user.")
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}")

if __name__ == "__main__":
    main()