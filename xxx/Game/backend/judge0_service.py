"""
Judge0 Service - Safe and Fault-Tolerant Code Execution
Integrates with RapidAPI Judge0 for compiling and running C++ code
Works for BOTH Practice and Battle modes
"""

import os
import time
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class Judge0Service:
    """
    RapidAPI Judge0 integration service
    Handles code submission, polling, and result retrieval
    """
    
    # Judge0 Language IDs
    LANGUAGE_CPP = 54  # C++ (GCC 9.2.0)
    
    # Execution limits
    MAX_EXECUTION_TIME = 2.0  # seconds
    COMPILATION_TIMEOUT = 5.0  # seconds
    MEMORY_LIMIT = 256 * 1024  # 256 MB in KB
    POLLING_TIMEOUT = 10.0  # seconds
    POLLING_INTERVAL = 0.5  # seconds between polls
    
    # Judge0 Status IDs
    STATUS_IN_QUEUE = 1
    STATUS_PROCESSING = 2
    STATUS_ACCEPTED = 3
    STATUS_WRONG_ANSWER = 4
    STATUS_TIME_LIMIT_EXCEEDED = 5
    STATUS_COMPILATION_ERROR = 6
    STATUS_RUNTIME_ERROR_SIGSEGV = 7
    STATUS_RUNTIME_ERROR_SIGXFSZ = 8
    STATUS_RUNTIME_ERROR_SIGFPE = 9
    STATUS_RUNTIME_ERROR_SIGABRT = 10
    STATUS_RUNTIME_ERROR_NZEC = 11
    STATUS_RUNTIME_ERROR_OTHER = 12
    STATUS_INTERNAL_ERROR = 13
    STATUS_EXEC_FORMAT_ERROR = 14
    
    def __init__(self):
        """Initialize Judge0 service with API credentials from environment"""
        self.api_url = os.getenv('JUDGE0_API_URL', 'https://judge0-ce.p.rapidapi.com')
        self.api_key = os.getenv('JUDGE0_API_KEY', '')
        
        # Don't raise error during init - handle it during execution
        # This allows the server to start even without API key configured
        
        self.headers = {
            'Content-Type': 'application/json',
            'X-RapidAPI-Key': self.api_key,
            'X-RapidAPI-Host': 'judge0-ce.p.rapidapi.com'
        }
    
    def execute_code(
        self,
        source_code: str,
        stdin_input: str = "",
        mode: str = "practice"
    ) -> Dict[str, Any]:
        """
        Main execution function - submits code to Judge0 and waits for results
        
        Args:
            source_code: Full compilable C++ program (wrapped code)
            stdin_input: Input to provide via stdin
            mode: "practice" or "battle" (for context/logging)
        
        Returns:
            Dictionary with execution results:
            {
                "success": bool,
                "status": str,  # "accepted", "compilation_error", "runtime_error", "tle", "internal_error"
                "stdout": str,
                "stderr": str,
                "compile_output": str,
                "execution_time": float,  # seconds
                "memory": int,  # KB
                "status_id": int,
                "error_message": str  # Only if failed
            }
        """
        try:
            # Step 1: Submit code to Judge0
            submission_token = self._submit_code(source_code, stdin_input)
            
            if not submission_token:
                return {
                    "success": False,
                    "status": "submission_failed",
                    "stdout": "",
                    "stderr": "",
                    "compile_output": "",
                    "execution_time": 0.0,
                    "memory": 0,
                    "status_id": 0,
                    "error_message": "Failed to submit code to Judge0"
                }
            
            # Step 2: Poll for results
            result = self._poll_submission(submission_token)
            
            return result
            
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "status": "timeout",
                "stdout": "",
                "stderr": "",
                "compile_output": "",
                "execution_time": 0.0,
                "memory": 0,
                "status_id": 0,
                "error_message": "Judge0 API request timed out"
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "status": "connection_error",
                "stdout": "",
                "stderr": "",
                "compile_output": "",
                "execution_time": 0.0,
                "memory": 0,
                "status_id": 0,
                "error_message": "Failed to connect to Judge0 API"
            }
        except Exception as e:
            return {
                "success": False,
                "status": "internal_error",
                "stdout": "",
                "stderr": "",
                "compile_output": "",
                "execution_time": 0.0,
                "memory": 0,
                "status_id": 0,
                "error_message": f"Unexpected error: {str(e)}"
            }
    
    def _submit_code(self, source_code: str, stdin_input: str) -> Optional[str]:
        """
        Submit code to Judge0 and get submission token
        
        Returns:
            Submission token (string) or None if failed
        """
        try:
            # Prepare submission payload
            payload = {
                "language_id": self.LANGUAGE_CPP,
                "source_code": source_code,
                "stdin": stdin_input,
                "cpu_time_limit": self.MAX_EXECUTION_TIME,
                "cpu_extra_time": 0.5,
                "wall_time_limit": self.COMPILATION_TIMEOUT,
                "memory_limit": self.MEMORY_LIMIT,
                "enable_network": False
            }
            
            # Submit to Judge0
            response = requests.post(
                f"{self.api_url}/submissions",
                json=payload,
                headers=self.headers,
                params={"base64_encoded": "false", "wait": "false"},
                timeout=5.0
            )
            
            response.raise_for_status()
            data = response.json()
            
            return data.get('token')
            
        except requests.exceptions.HTTPError as e:
            print(f"[Judge0] HTTP error during submission: {e}")
            return None
        except Exception as e:
            print(f"[Judge0] Error submitting code: {e}")
            return None
    
    def _poll_submission(self, token: str) -> Dict[str, Any]:
        """
        Poll Judge0 for submission results until completion or timeout
        
        Args:
            token: Submission token from Judge0
        
        Returns:
            Execution result dictionary
        """
        start_time = time.time()
        
        while True:
            elapsed = time.time() - start_time
            
            # Check polling timeout
            if elapsed > self.POLLING_TIMEOUT:
                return {
                    "success": False,
                    "status": "polling_timeout",
                    "stdout": "",
                    "stderr": "",
                    "compile_output": "",
                    "execution_time": 0.0,
                    "memory": 0,
                    "status_id": 0,
                    "error_message": f"Polling timeout after {self.POLLING_TIMEOUT}s"
                }
            
            try:
                # Get submission status
                response = requests.get(
                    f"{self.api_url}/submissions/{token}",
                    headers=self.headers,
                    params={"base64_encoded": "false"},
                    timeout=3.0
                )
                
                response.raise_for_status()
                data = response.json()
                
                status_id = data.get('status', {}).get('id', 0)
                
                # Check if still processing
                if status_id in [self.STATUS_IN_QUEUE, self.STATUS_PROCESSING]:
                    time.sleep(self.POLLING_INTERVAL)
                    continue
                
                # Execution completed - parse results
                return self._parse_submission_result(data)
                
            except requests.exceptions.HTTPError as e:
                return {
                    "success": False,
                    "status": "api_error",
                    "stdout": "",
                    "stderr": "",
                    "compile_output": "",
                    "execution_time": 0.0,
                    "memory": 0,
                    "status_id": 0,
                    "error_message": f"Judge0 API error: {str(e)}"
                }
            except Exception as e:
                return {
                    "success": False,
                    "status": "polling_error",
                    "stdout": "",
                    "stderr": "",
                    "compile_output": "",
                    "execution_time": 0.0,
                    "memory": 0,
                    "status_id": 0,
                    "error_message": f"Error polling submission: {str(e)}"
                }
    
    def _parse_submission_result(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse Judge0 submission result and categorize by status
        
        Args:
            data: Raw JSON response from Judge0
        
        Returns:
            Standardized execution result
        """
        status_info = data.get('status', {})
        status_id = status_info.get('id', 0)
        status_description = status_info.get('description', 'Unknown')
        
        # Extract output fields (handle None values)
        stdout = data.get('stdout') or ""
        stderr = data.get('stderr') or ""
        compile_output = data.get('compile_output') or ""
        execution_time = float(data.get('time') or 0.0)
        memory = int(data.get('memory') or 0)
        
        # Determine success and categorize status
        if status_id == self.STATUS_ACCEPTED:
            return {
                "success": True,
                "status": "accepted",
                "stdout": stdout,
                "stderr": stderr,
                "compile_output": compile_output,
                "execution_time": execution_time,
                "memory": memory,
                "status_id": status_id,
                "error_message": ""
            }
        
        elif status_id == self.STATUS_COMPILATION_ERROR:
            return {
                "success": False,
                "status": "compilation_error",
                "stdout": stdout,
                "stderr": stderr,
                "compile_output": compile_output,
                "execution_time": 0.0,
                "memory": 0,
                "status_id": status_id,
                "error_message": f"Compilation failed: {compile_output or stderr}"
            }
        
        elif status_id == self.STATUS_TIME_LIMIT_EXCEEDED:
            return {
                "success": False,
                "status": "time_limit_exceeded",
                "stdout": stdout,
                "stderr": stderr,
                "compile_output": compile_output,
                "execution_time": execution_time,
                "memory": memory,
                "status_id": status_id,
                "error_message": f"Time limit exceeded (>{self.MAX_EXECUTION_TIME}s)"
            }
        
        elif status_id in [
            self.STATUS_RUNTIME_ERROR_SIGSEGV,
            self.STATUS_RUNTIME_ERROR_SIGXFSZ,
            self.STATUS_RUNTIME_ERROR_SIGFPE,
            self.STATUS_RUNTIME_ERROR_SIGABRT,
            self.STATUS_RUNTIME_ERROR_NZEC,
            self.STATUS_RUNTIME_ERROR_OTHER
        ]:
            return {
                "success": False,
                "status": "runtime_error",
                "stdout": stdout,
                "stderr": stderr,
                "compile_output": compile_output,
                "execution_time": execution_time,
                "memory": memory,
                "status_id": status_id,
                "error_message": f"Runtime error: {status_description} - {stderr}"
            }
        
        elif status_id == self.STATUS_INTERNAL_ERROR:
            return {
                "success": False,
                "status": "internal_error",
                "stdout": stdout,
                "stderr": stderr,
                "compile_output": compile_output,
                "execution_time": 0.0,
                "memory": 0,
                "status_id": status_id,
                "error_message": f"Judge0 internal error: {status_description}"
            }
        
        else:
            # Unknown or other error
            return {
                "success": False,
                "status": "unknown_error",
                "stdout": stdout,
                "stderr": stderr,
                "compile_output": compile_output,
                "execution_time": execution_time,
                "memory": memory,
                "status_id": status_id,
                "error_message": f"Unknown status: {status_description}"
            }


# Singleton instance for reuse
_judge0_service = None

def get_judge0_service() -> Judge0Service:
    """
    Get or create Judge0 service instance (singleton pattern)
    
    Returns:
        Judge0Service instance
    """
    global _judge0_service
    if _judge0_service is None:
        _judge0_service = Judge0Service()
    return _judge0_service


def execute_code(source_code: str, stdin_input: str = "", mode: str = "practice") -> Dict[str, Any]:
    """
    Convenience function to execute code using Judge0
    
    Args:
        source_code: Full compilable C++ program
        stdin_input: Input to provide via stdin
        mode: "practice" or "battle"
    
    Returns:
        Execution result dictionary
    """
    service = get_judge0_service()
    return service.execute_code(source_code, stdin_input, mode)
