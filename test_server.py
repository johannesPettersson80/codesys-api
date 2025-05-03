#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CODESYS API Test Server

This is a simplified version of the HTTP server that only tests basic HTTP functionality
without CODESYS integration. This helps isolate whether the issue is with the HTTP server
or with the CODESYS integration.
"""

import sys
import os
import json
import time
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='test_server.log'
)
logger = logging.getLogger('test_server')

# Constants
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080

# Create a simple API key checker
API_KEYS = {"admin": {"name": "Admin", "created": time.time()}}

class TestApiHandler(BaseHTTPRequestHandler):
    """Test HTTP request handler."""
    
    server_version = "TestApiServer/0.1"
    
    def do_GET(self):
        """Handle GET requests."""
        try:
            # Check authentication
            if not self.authenticate():
                self.send_error(401, "Unauthorized")
                return
                
            # Route based on path
            if self.path == "/api/v1/system/info":
                self.handle_system_info()
            elif self.path == "/api/v1/session/status":
                self.handle_session_status()
            else:
                self.send_error(404, "Not Found")
        except Exception as e:
            logger.error("Error handling GET request: %s", str(e))
            self.send_error(500, str(e))
            
    def do_POST(self):
        """Handle POST requests."""
        try:
            # Check authentication
            if not self.authenticate():
                self.send_error(401, "Unauthorized")
                return
            
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            params = {}
            if content_length > 0:
                params = json.loads(post_data)
                
            # Route based on path
            if self.path == "/api/v1/session/start":
                self.handle_session_start()
            elif self.path == "/api/v1/script/execute":
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
            return api_key in API_KEYS
            
        return False
        
    def send_json_response(self, data, status=200):
        """Send JSON response."""
        response = json.dumps(data)
        
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(response.encode('utf-8')))
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))
    
    # Handler methods
    
    def handle_system_info(self):
        """Handle system/info endpoint."""
        self.send_json_response({
            "success": True,
            "info": {
                "version": "0.1",
                "test_server": True
            }
        })
        
    def handle_session_status(self):
        """Handle session/status endpoint."""
        self.send_json_response({
            "success": True,
            "status": {
                "process": {
                    "running": True,
                    "state": "running",
                    "timestamp": time.time()
                },
                "session": {
                    "active": True
                }
            }
        })
        
    def handle_session_start(self):
        """Handle session/start endpoint."""
        # Simulate a slow operation
        logger.info("Simulating slow session start (5 seconds)")
        time.sleep(5)
        
        self.send_json_response({
            "success": True,
            "message": "Session started (test server)"
        })
        
    def handle_script_execute(self, params):
        """Handle script/execute endpoint."""
        script = params.get("script", "")
        
        # Log the script
        logger.info("Received script execution request")
        logger.debug("Script content: %s", script[:200] + ('...' if len(script) > 200 else ''))
        
        # Simulate a slow operation
        logger.info("Simulating slow script execution (10 seconds)")
        time.sleep(10)
        
        self.send_json_response({
            "success": True,
            "result": {
                "message": "Script executed (test server)",
                "script_length": len(script)
            }
        })

def run_server():
    """Run the test HTTP server."""
    try:
        server = HTTPServer((SERVER_HOST, SERVER_PORT), TestApiHandler)
        
        print(f"Starting test server on {SERVER_HOST}:{SERVER_PORT}")
        logger.info("Starting test server on %s:%d", SERVER_HOST, SERVER_PORT)
        
        # Run server
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped")
    except Exception as e:
        print(f"Error starting server: {str(e)}")
        logger.error("Error starting server: %s", str(e))
        
if __name__ == "__main__":
    run_server()