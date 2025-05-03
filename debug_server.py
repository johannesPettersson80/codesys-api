#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CODESYS API Debug Server

This script runs the HTTP server with detailed console output for debugging.
It helps diagnose issues with CODESYS API integration.
"""

import sys
import os
import logging
import time
import HTTP_SERVER

# Configure logging to output to console
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for detailed output
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),  # Log to console
        logging.FileHandler('debug_server.log')  # Also log to file
    ]
)

# Set logger levels for different components
logging.getLogger('codesys_api_server').setLevel(logging.DEBUG)
logger = logging.getLogger('debug_server')

def run_debug_server():
    """Run the HTTP server with debug output."""
    try:
        # Print system information
        logger.info("=== CODESYS API Debug Server ===")
        logger.info("Python version: %s", sys.version)
        logger.info("Current directory: %s", os.getcwd())
        
        # Print server configuration
        logger.info("Server configuration:")
        logger.info("  HOST: %s", HTTP_SERVER.SERVER_HOST)
        logger.info("  PORT: %s", HTTP_SERVER.SERVER_PORT)
        logger.info("  CODESYS_PATH: %s", HTTP_SERVER.CODESYS_PATH)
        logger.info("  PERSISTENT_SCRIPT: %s", HTTP_SERVER.PERSISTENT_SCRIPT)
        logger.info("  REQUEST_DIR: %s", HTTP_SERVER.REQUEST_DIR)
        logger.info("  RESULT_DIR: %s", HTTP_SERVER.RESULT_DIR)
        
        # Verify directories exist
        for directory in [HTTP_SERVER.REQUEST_DIR, HTTP_SERVER.RESULT_DIR]:
            if os.path.exists(directory):
                logger.info("Directory exists: %s", directory)
            else:
                logger.warning("Directory does not exist: %s", directory)
                try:
                    os.makedirs(directory)
                    logger.info("Created directory: %s", directory)
                except Exception as e:
                    logger.error("Failed to create directory: %s", str(e))
        
        # Check CODESYS executable
        if os.path.exists(HTTP_SERVER.CODESYS_PATH):
            logger.info("CODESYS executable found: %s", HTTP_SERVER.CODESYS_PATH)
        else:
            logger.error("CODESYS executable NOT found: %s", HTTP_SERVER.CODESYS_PATH)
            
        # Check PERSISTENT_SESSION script
        if os.path.exists(HTTP_SERVER.PERSISTENT_SCRIPT):
            logger.info("PERSISTENT_SCRIPT found: %s", HTTP_SERVER.PERSISTENT_SCRIPT)
        else:
            logger.error("PERSISTENT_SCRIPT NOT found: %s", HTTP_SERVER.PERSISTENT_SCRIPT)
        
        # Create managers
        process_manager = HTTP_SERVER.CodesysProcessManager(
            HTTP_SERVER.CODESYS_PATH, 
            HTTP_SERVER.PERSISTENT_SCRIPT
        )
        script_executor = HTTP_SERVER.ScriptExecutor(
            HTTP_SERVER.REQUEST_DIR, 
            HTTP_SERVER.RESULT_DIR
        )
        script_generator = HTTP_SERVER.ScriptGenerator()
        api_key_manager = HTTP_SERVER.ApiKeyManager(HTTP_SERVER.API_KEY_FILE)
        
        # Create server
        from http.server import HTTPServer
        
        def handler(*args):
            return HTTP_SERVER.CodesysApiHandler(
                process_manager=process_manager,
                script_executor=script_executor,
                script_generator=script_generator,
                api_key_manager=api_key_manager,
                *args
            )
            
        server = HTTPServer((HTTP_SERVER.SERVER_HOST, HTTP_SERVER.SERVER_PORT), handler)
        
        logger.info("Starting server on %s:%d", HTTP_SERVER.SERVER_HOST, HTTP_SERVER.SERVER_PORT)
        logger.info("Press Ctrl+C to stop server")
        
        # Start server
        server.serve_forever()
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error("Error starting server: %s", str(e), exc_info=True)
    finally:
        # Cleanup
        logger.info("Cleaning up...")
        try:
            process_manager.stop()
            logger.info("CODESYS process stopped")
        except:
            pass
            
if __name__ == "__main__":
    run_debug_server()