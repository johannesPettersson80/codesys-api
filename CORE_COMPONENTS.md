# Core Components Implementation Guide

This document provides detailed implementation guidance for the core components of the CODESYS REST API wrapper.

## 1. HTTP REST API Server

### BaseHTTPServer Implementation

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading
import ssl

class CodesysApiRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests."""
        # Parse path to determine endpoint
        endpoint = self.path.strip('/').split('/')
        
        # Check authentication
        if not self.authenticate():
            self.send_error(401, "Unauthorized")
            return
            
        # Route request to appropriate handler
        try:
            response, status_code = self.route_request("GET", endpoint)
            self.send_response(status_code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except Exception as e:
            self.send_error(500, str(e))
    
    def do_POST(self):
        """Handle POST requests."""
        # Similar to GET but read request body
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            request_body = json.loads(post_data.decode('utf-8'))
            # Process similar to GET
            # ...
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
    
    def authenticate(self):
        """Validate API key."""
        auth_header = self.headers.get('Authorization', '')
        # Check API key
        # ...
        return True  # Placeholder
        
    def route_request(self, method, endpoint):
        """Route request to appropriate handler."""
        # Map endpoints to handler functions
        # ...
        return {"success": True, "message": "Handler not implemented"}, 501


class CodesysApiServer:
    def __init__(self, host='localhost', port=8080, use_ssl=False):
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.server = None
        self.server_thread = None
        
    def start(self):
        """Start the HTTP server."""
        self.server = HTTPServer((self.host, self.port), CodesysApiRequestHandler)
        
        # Configure SSL if needed
        if self.use_ssl:
            self.server.socket = ssl.wrap_socket(
                self.server.socket,
                keyfile='path/to/key.pem',
                certfile='path/to/cert.pem',
                server_side=True
            )
            
        # Start server in a separate thread
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        
    def stop(self):
        """Stop the HTTP server."""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
```

### API Endpoint Handlers

Implement handlers for each API endpoint:

```python
class ApiHandlers:
    """Handlers for API endpoints."""
    
    @staticmethod
    def session_start(params):
        """Handle session/start endpoint."""
        try:
            # Start CODESYS session
            success = codesys_manager.start_session()
            
            if success:
                return {"success": True, "message": "Session started"}, 200
            else:
                return {"success": False, "error": "Failed to start session"}, 500
        except Exception as e:
            return {"success": False, "error": str(e)}, 500
            
    @staticmethod
    def project_create(params):
        """Handle project/create endpoint."""
        try:
            # Validate parameters
            if "path" not in params:
                return {"success": False, "error": "Missing required parameter: path"}, 400
                
            # Create project
            result = codesys_manager.create_project(params["path"])
            
            if result["success"]:
                return result, 200
            else:
                return result, 500
        except Exception as e:
            return {"success": False, "error": str(e)}, 500
    
    # Implement other handlers similarly
```

## 2. CODESYS Session Manager

### Process Management

```python
import subprocess
import os
import signal
import time
import threading

class CodesysProcessManager:
    """Manages the CODESYS process."""
    
    def __init__(self, codesys_path, script_path, timeout=30):
        self.codesys_path = codesys_path
        self.script_path = script_path
        self.timeout = timeout
        self.process = None
        self.monitor_thread = None
        self.running = False
        
    def start(self):
        """Start the CODESYS process."""
        try:
            # Start CODESYS with script
            self.process = subprocess.Popen(
                [self.codesys_path, "-script", self.script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Start monitoring thread
            self.running = True
            self.monitor_thread = threading.Thread(target=self._monitor)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
            
            # Wait for process to initialize
            time.sleep(2)
            
            # Check if process is still running
            if self.process.poll() is not None:
                # Process already terminated
                stdout, stderr = self.process.communicate()
                raise Exception(f"CODESYS process failed to start: {stderr.decode('utf-8')}")
                
            return True
        except Exception as e:
            self.running = False
            if self.process:
                self.process.terminate()
            raise e
            
    def stop(self):
        """Stop the CODESYS process."""
        if self.process:
            self.running = False
            
            # Try graceful termination
            try:
                # Send termination signal to script
                with open(self._get_termination_signal_path(), 'w') as f:
                    f.write("TERMINATE")
                    
                # Wait for process to terminate
                for _ in range(10):
                    if self.process.poll() is not None:
                        break
                    time.sleep(0.5)
            except:
                pass
                
            # Force termination if still running
            if self.process.poll() is None:
                self.process.terminate()
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.process.kill()
                    
            self.process = None
            
    def _monitor(self):
        """Monitor the CODESYS process and restart if needed."""
        while self.running:
            # Check if process is still running
            if self.process.poll() is not None:
                # Process terminated unexpectedly
                try:
                    # Try to restart
                    self.process = subprocess.Popen(
                        [self.codesys_path, "-script", self.script_path],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                except:
                    # Failed to restart
                    self.running = False
                    break
                    
            time.sleep(5)
            
    def _get_termination_signal_path(self):
        """Get path for termination signal file."""
        return os.path.join(os.path.dirname(self.script_path), "terminate.signal")
```

### Script Execution Engine

```python
import os
import tempfile
import uuid
import time

class ScriptExecutionEngine:
    """Executes Python scripts in CODESYS environment."""
    
    def __init__(self, temp_dir=None):
        self.temp_dir = temp_dir or tempfile.gettempdir()
        
    def execute(self, script_content, timeout=30):
        """Execute a script and return the result."""
        try:
            # Create temporary script file
            script_path = self._create_temp_script(script_content)
            
            # Create result file path
            result_path = script_path + ".result"
            
            # Create execution request
            request_path = self._create_execution_request(script_path, result_path)
            
            # Wait for execution to complete
            result = self._wait_for_result(result_path, timeout)
            
            # Cleanup
            self._cleanup_files(script_path, result_path, request_path)
            
            return result
        except Exception as e:
            raise Exception(f"Script execution failed: {str(e)}")
            
    def _create_temp_script(self, script_content):
        """Create a temporary script file."""
        script_id = str(uuid.uuid4())
        script_path = os.path.join(self.temp_dir, f"codesys_script_{script_id}.py")
        
        with open(script_path, 'w') as f:
            f.write(script_content)
            
        return script_path
        
    def _create_execution_request(self, script_path, result_path):
        """Create execution request file."""
        request_path = script_path + ".request"
        
        with open(request_path, 'w') as f:
            f.write(json.dumps({
                "script_path": script_path,
                "result_path": result_path,
                "timestamp": time.time()
            }))
            
        return request_path
        
    def _wait_for_result(self, result_path, timeout):
        """Wait for result file and read result."""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if os.path.exists(result_path):
                # Read result
                with open(result_path, 'r') as f:
                    try:
                        return json.loads(f.read())
                    except json.JSONDecodeError:
                        # Result file exists but is not valid JSON
                        return {"success": False, "error": "Invalid result format"}
                        
            time.sleep(0.1)
            
        raise Exception("Script execution timed out")
        
    def _cleanup_files(self, script_path, result_path, request_path):
        """Clean up temporary files."""
        for path in [script_path, result_path, request_path]:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except:
                pass
```

## 3. Script Generator Component

### Template-Based Script Generator

```python
from string import Template

class ScriptTemplateManager:
    """Manages script templates."""
    
    def __init__(self):
        self.templates = self._load_templates()
        
    def _load_templates(self):
        """Load script templates."""
        return {
            "session_start": Template("""
import scriptengine

# Initialize system
system = scriptengine.ScriptSystem()

# Store system instance
# This is a placeholder - actual implementation depends on how
# the persistent session is managed

# Return success
result = {"success": True, "message": "Session started"}

# Write result to file
with open("$result_path", "w") as f:
    f.write(json.dumps(result))
"""),
            "project_create": Template("""
import scriptengine
import json

try:
    # Get system instance
    system = scriptengine.ScriptSystem()
    
    # Create new project
    project = system.projects.create()
    
    # Save to specified path
    project.save_as("$project_path")
    
    # Return project info
    result = {
        "success": True,
        "project": {
            "path": project.path,
            "name": project.name,
            "is_dirty": project.dirty
        }
    }
except Exception as e:
    result = {"success": False, "error": str(e)}
    
# Write result to file
with open("$result_path", "w") as f:
    f.write(json.dumps(result))
"""),
            # Add more templates for other operations
        }
        
    def get_template(self, template_name):
        """Get a script template by name."""
        if template_name not in self.templates:
            raise ValueError(f"Unknown template: {template_name}")
            
        return self.templates[template_name]
        
    def render_template(self, template_name, **kwargs):
        """Render a template with parameters."""
        template = self.get_template(template_name)
        return template.substitute(**kwargs)
```

### Script Generator for Different Operations

```python
class ScriptGenerator:
    """Generates scripts for different operations."""
    
    def __init__(self):
        self.template_manager = ScriptTemplateManager()
        
    def generate_session_start_script(self, result_path):
        """Generate script to start a session."""
        return self.template_manager.render_template(
            "session_start",
            result_path=result_path
        )
        
    def generate_project_create_script(self, project_path, result_path):
        """Generate script to create a project."""
        return self.template_manager.render_template(
            "project_create",
            project_path=project_path,
            result_path=result_path
        )
        
    def generate_project_open_script(self, project_path, result_path):
        """Generate script to open a project."""
        return self.template_manager.render_template(
            "project_open",
            project_path=project_path,
            result_path=result_path
        )
        
    # Implement other script generators
```

## 4. Authentication & Authorization

### API Key Management

```python
import hashlib
import os
import json
import time

class ApiKeyManager:
    """Manages API keys for authentication."""
    
    def __init__(self, key_file_path):
        self.key_file_path = key_file_path
        self.keys = self._load_keys()
        
    def _load_keys(self):
        """Load API keys from file."""
        if not os.path.exists(self.key_file_path):
            # Create empty key file
            self._save_keys({})
            return {}
            
        try:
            with open(self.key_file_path, 'r') as f:
                return json.loads(f.read())
        except:
            return {}
            
    def _save_keys(self, keys):
        """Save API keys to file."""
        with open(self.key_file_path, 'w') as f:
            f.write(json.dumps(keys))
            
    def generate_key(self, name, expiration=None):
        """Generate a new API key."""
        # Generate random key
        key = hashlib.sha256(os.urandom(32)).hexdigest()
        
        # Store key info
        self.keys[key] = {
            "name": name,
            "created": time.time(),
            "expiration": expiration,
            "last_used": None
        }
        
        # Save keys
        self._save_keys(self.keys)
        
        return key
        
    def validate_key(self, key):
        """Validate an API key."""
        if key not in self.keys:
            return False
            
        key_info = self.keys[key]
        
        # Check expiration
        if key_info["expiration"] and time.time() > key_info["expiration"]:
            return False
            
        # Update last used
        key_info["last_used"] = time.time()
        self._save_keys(self.keys)
        
        return True
        
    def revoke_key(self, key):
        """Revoke an API key."""
        if key in self.keys:
            del self.keys[key]
            self._save_keys(self.keys)
            return True
        return False
```

### Request Validation

```python
class RequestValidator:
    """Validates API requests."""
    
    def validate_project_create(self, params):
        """Validate project create parameters."""
        if "path" not in params:
            return False, "Missing required parameter: path"
            
        # Validate path
        if not self._is_valid_path(params["path"]):
            return False, "Invalid project path"
            
        return True, ""
        
    def validate_pou_create(self, params):
        """Validate POU create parameters."""
        required = ["name", "type", "language"]
        
        for field in required:
            if field not in params:
                return False, f"Missing required parameter: {field}"
                
        # Validate POU type
        valid_types = ["Program", "Function", "FunctionBlock"]
        if params["type"] not in valid_types:
            return False, f"Invalid POU type. Must be one of: {', '.join(valid_types)}"
            
        # Validate language
        valid_languages = ["ST", "FBD", "LD", "IL", "CFC", "SFC"]
        if params["language"] not in valid_languages:
            return False, f"Invalid language. Must be one of: {', '.join(valid_languages)}"
            
        return True, ""
        
    def _is_valid_path(self, path):
        """Check if a path is valid."""
        # Implement path validation
        # This is a placeholder
        return True
```

## 5. Logging & Monitoring System

### Logging Component

```python
import logging
import os
import time
from logging.handlers import RotatingFileHandler

class LoggingSystem:
    """Handles logging for the API server."""
    
    def __init__(self, log_dir, max_size=10*1024*1024, backup_count=5):
        self.log_dir = log_dir
        self.max_size = max_size
        self.backup_count = backup_count
        
        # Create loggers
        self.api_logger = self._create_logger("api")
        self.codesys_logger = self._create_logger("codesys")
        self.script_logger = self._create_logger("script")
        self.access_logger = self._create_logger("access")
        
    def _create_logger(self, name):
        """Create a logger with specified name."""
        # Ensure log directory exists
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            
        # Create logger
        logger = logging.getLogger(f"codesys_api.{name}")
        logger.setLevel(logging.INFO)
        
        # Create handler
        log_file = os.path.join(self.log_dir, f"{name}.log")
        handler = RotatingFileHandler(
            log_file,
            maxBytes=self.max_size,
            backupCount=self.backup_count
        )
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(handler)
        
        return logger
        
    def log_api_request(self, method, endpoint, params=None, status_code=None, error=None):
        """Log an API request."""
        message = f"Request: {method} {endpoint}"
        
        if params:
            # Omit sensitive fields
            safe_params = self._sanitize_params(params)
            message += f" - Params: {json.dumps(safe_params)}"
            
        if status_code:
            message += f" - Status: {status_code}"
            
        if error:
            message += f" - Error: {error}"
            
        self.api_logger.info(message)
        
    def log_codesys_operation(self, operation, success, message=None):
        """Log a CODESYS operation."""
        log_message = f"Operation: {operation} - Success: {success}"
        
        if message:
            log_message += f" - Message: {message}"
            
        if success:
            self.codesys_logger.info(log_message)
        else:
            self.codesys_logger.error(log_message)
            
    def log_script_execution(self, script_path, success, duration=None, error=None):
        """Log script execution."""
        message = f"Script: {os.path.basename(script_path)} - Success: {success}"
        
        if duration:
            message += f" - Duration: {duration:.2f}s"
            
        if error:
            message += f" - Error: {error}"
            
        if success:
            self.script_logger.info(message)
        else:
            self.script_logger.error(message)
            
    def log_access(self, client_ip, authenticated, request_path):
        """Log access to the API."""
        message = f"Access from {client_ip} - Authenticated: {authenticated} - Path: {request_path}"
        self.access_logger.info(message)
        
    def _sanitize_params(self, params):
        """Remove sensitive information from parameters."""
        # Create copy of params
        safe_params = params.copy()
        
        # Remove sensitive fields
        sensitive_fields = ["password", "api_key", "credentials"]
        for field in sensitive_fields:
            if field in safe_params:
                safe_params[field] = "***"
                
        return safe_params
```

### Monitoring Component

```python
import threading
import time
import psutil
import os
import json

class MonitoringSystem:
    """Monitors system performance and health."""
    
    def __init__(self, codesys_process_manager, metrics_file, interval=60):
        self.codesys_process_manager = codesys_process_manager
        self.metrics_file = metrics_file
        self.interval = interval
        self.running = False
        self.monitor_thread = None
        self.metrics = {
            "start_time": time.time(),
            "api_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0,
            "codesys_restarts": 0,
            "last_metrics_update": time.time(),
            "cpu_usage": [],
            "memory_usage": [],
            "disk_usage": []
        }
        
    def start(self):
        """Start the monitoring system."""
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
    def stop(self):
        """Stop the monitoring system."""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
            
    def record_request(self, success, response_time):
        """Record an API request."""
        self.metrics["api_requests"] += 1
        
        if success:
            self.metrics["successful_requests"] += 1
        else:
            self.metrics["failed_requests"] += 1
            
        # Update average response time
        current_avg = self.metrics["average_response_time"]
        current_count = self.metrics["api_requests"]
        
        if current_count == 1:
            self.metrics["average_response_time"] = response_time
        else:
            self.metrics["average_response_time"] = (
                (current_avg * (current_count - 1) + response_time) / current_count
            )
            
    def record_codesys_restart(self):
        """Record a CODESYS restart."""
        self.metrics["codesys_restarts"] += 1
        
    def get_metrics(self):
        """Get current metrics."""
        return self.metrics.copy()
        
    def _monitor_loop(self):
        """Main monitoring loop."""
        while self.running:
            try:
                # Update system metrics
                self._update_system_metrics()
                
                # Save metrics to file
                self._save_metrics()
                
                # Check CODESYS process health
                self._check_codesys_health()
                
                # Wait for next interval
                time.sleep(self.interval)
            except Exception as e:
                # Log error but continue monitoring
                print(f"Monitoring error: {e}")
                
    def _update_system_metrics(self):
        """Update system metrics."""
        # Update timestamp
        self.metrics["last_metrics_update"] = time.time()
        
        # Get CPU usage
        cpu_percent = psutil.cpu_percent()
        self.metrics["cpu_usage"].append({
            "timestamp": time.time(),
            "value": cpu_percent
        })
        
        # Limit history
        if len(self.metrics["cpu_usage"]) > 100:
            self.metrics["cpu_usage"] = self.metrics["cpu_usage"][-100:]
            
        # Get memory usage
        memory = psutil.virtual_memory()
        self.metrics["memory_usage"].append({
            "timestamp": time.time(),
            "value": memory.percent
        })
        
        # Limit history
        if len(self.metrics["memory_usage"]) > 100:
            self.metrics["memory_usage"] = self.metrics["memory_usage"][-100:]
            
        # Get disk usage
        disk = psutil.disk_usage('/')
        self.metrics["disk_usage"].append({
            "timestamp": time.time(),
            "value": disk.percent
        })
        
        # Limit history
        if len(self.metrics["disk_usage"]) > 100:
            self.metrics["disk_usage"] = self.metrics["disk_usage"][-100:]
            
    def _save_metrics(self):
        """Save metrics to file."""
        with open(self.metrics_file, 'w') as f:
            json.dump(self.metrics, f)
            
    def _check_codesys_health(self):
        """Check health of CODESYS process."""
        if not self.codesys_process_manager.process:
            return
            
        # Get process
        process = self.codesys_process_manager.process
        
        # Check if process is still running
        if process.poll() is not None:
            # Process has terminated
            print("CODESYS process has terminated unexpectedly")
            
            # Record restart
            self.record_codesys_restart()
            
            # Restart process
            self.codesys_process_manager.start()
```

## Conclusion

These core component implementations provide a foundation for building the CODESYS REST API wrapper. Each component is designed to work together to create a robust, secure, and maintainable system that follows the architecture outlined in the design document.

The implementation focuses on:

1. Providing a clean, RESTful API interface
2. Managing the CODESYS process robustly
3. Executing scripts in a controlled and secure manner
4. Implementing proper authentication and authorization
5. Providing comprehensive logging and monitoring

Additional components such as error handling, performance optimization, and specific API endpoint implementations would be built on top of these core components.