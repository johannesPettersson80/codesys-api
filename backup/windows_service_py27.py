#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CODESYS API Windows Service

This script allows the CODESYS API to run as a Windows service.
It handles service installation, start, stop, and other lifecycle events.

Usage:
    python windows_service.py install   - Install the service
    python windows_service.py remove    - Remove the service
    python windows_service.py start     - Start the service
    python windows_service.py stop      - Stop the service
    python windows_service.py restart   - Restart the service
    python windows_service.py update    - Update the service

Note:
    Requires pywin32 to be installed:
    pip install pywin32
"""

import sys
import os
import logging
import time
import servicemanager
import win32event
import win32service
import win32serviceutil

# Python 3 compatibility imports
try:
    from http.server import HTTPServer
except ImportError:
    from BaseHTTPServer import HTTPServer

import HTTP_SERVER

# Setup logging for the Windows service
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='codesys_api_service.log'
)
logger = logging.getLogger('codesys_api_service')

class CodesysAPIService(win32serviceutil.ServiceFramework):
    """Windows Service for CODESYS API."""
    
    _svc_name_ = "CodesysAPIService"
    _svc_display_name_ = "CODESYS API Service"
    _svc_description_ = "Provides RESTful API access to CODESYS automation software"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.is_alive = True
        
    def SvcStop(self):
        """Stop the service."""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.is_alive = False
        
    def SvcDoRun(self):
        """Run the service."""
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        
        # Setup HTTP Server and other components
        try:
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
            def handler(*args):
                HTTP_SERVER.CodesysApiHandler(
                    process_manager=process_manager,
                    script_executor=script_executor,
                    script_generator=script_generator,
                    api_key_manager=api_key_manager,
                    *args
                )
                
            server = HTTPServer((HTTP_SERVER.SERVER_HOST, HTTP_SERVER.SERVER_PORT), handler)
            
            logger.info("Starting server on %s:%d", HTTP_SERVER.SERVER_HOST, HTTP_SERVER.SERVER_PORT)
            
            # Start the server in a separate thread
            import threading
            server_thread = threading.Thread(target=server.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            
            # Main service loop
            while self.is_alive:
                # Check if we should stop
                result = win32event.WaitForSingleObject(self.stop_event, 1000)
                if result == win32event.WAIT_OBJECT_0:
                    break
                    
                # Check health of CODESYS process
                if not process_manager.is_running():
                    logger.warning("CODESYS process is not running, attempting to start...")
                    process_manager.start()
                    
            # Cleanup when service is stopping
            logger.info("Service is stopping, shutting down components...")
            
            # Shutdown HTTP server
            server.shutdown()
            
            # Stop CODESYS process
            process_manager.stop()
            
            logger.info("Service stopped")
        except Exception as e:
            logger.error("Error in service: %s", str(e))
            
            # Attempt to stop any running components
            try:
                if 'process_manager' in locals():
                    process_manager.stop()
            except:
                pass
                
            servicemanager.LogErrorMsg("Error in CODESYS API Service: " + str(e))
            
def main():
    """Main function to handle service commands."""
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(CodesysAPIService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(CodesysAPIService)
        
if __name__ == '__main__':
    main()