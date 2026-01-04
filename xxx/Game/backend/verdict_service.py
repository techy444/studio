"""
Verdict Service - LeetCode-style Judging System
Handles code execution, output comparison, and verdict determination
Works for BOTH Practice Mode and Battle Mode
"""

import time
from typing import Dict, List, Any, Optional
from datetime import datetime
from database import problems_collection, submissions_collection
from judge0_service import execute_code as judge0_execute_code


class VerdictService:
    """
    LeetCode-style verdict system
    Executes code against test cases and determines verdict
    """
    
    # Verdict constants
    VERDICT_ACCEPTED = "Accepted"
    VERDICT_WRONG_ANSWER = "Wrong Answer"
    VERDICT_COMPILATION_ERROR = "Compilation Error"
    VERDICT_RUNTIME_ERROR = "Runtime Error"
    VERDICT_TIME_LIMIT_EXCEEDED = "Time Limit Exceeded"
    VERDICT_INTERNAL_ERROR = "Internal Error"
    
    @staticmethod
    def normalize_output(output: str) -> str:
        """
        Normalize output for comparison
        - Trim leading/trailing whitespace
        - Remove extra line breaks
        - Standardize spacing
        """
        if not output:
            return ""
        
        # Split into lines, strip each line, remove empty lines
        lines = [line.strip() for line in output.strip().split('\n')]
        lines = [line for line in lines if line]  # Remove empty lines
        
        # Join back with single newline
        return '\n'.join(lines)
    
    @staticmethod
    def compare_outputs(actual: str, expected: str) -> bool:
        """
        Compare actual output with expected output after normalization
        """
        normalized_actual = VerdictService.normalize_output(actual)
        normalized_expected = VerdictService.normalize_output(expected)
        
        return normalized_actual == normalized_expected
    
    @staticmethod
    def execute_with_retry(wrapped_code: str, stdin_input: str, mode: str) -> Dict[str, Any]:
        """
        Execute code with Judge0, retry once on network failure
        
        Args:
            wrapped_code: Full C++ program
            stdin_input: Input for the test case
            mode: "practice" or "battle"
        
        Returns:
            Execution result from Judge0
        """
        max_retries = 2
        retry_delay = 1.0  # seconds
        
        for attempt in range(max_retries):
            result = judge0_execute_code(wrapped_code, stdin_input, mode)
            
            # Check if it's a network/timeout error that should be retried
            if result.get("status") in ["timeout", "connection_error", "polling_timeout"]:
                if attempt < max_retries - 1:
                    # Retry after delay
                    time.sleep(retry_delay)
                    continue
                else:
                    # Final attempt failed - return internal error
                    return {
                        "success": False,
                        "status": "internal_error",
                        "stdout": "",
                        "stderr": "",
                        "compile_output": "",
                        "execution_time": 0.0,
                        "memory": 0,
                        "status_id": 0,
                        "error_message": f"Judge0 service unavailable after {max_retries} attempts"
                    }
            
            # If not a retry-able error, return immediately
            return result
        
        # Should never reach here
        return result
    
    @staticmethod
    def determine_verdict(
        problem_id: str,
        wrapped_code: str,
        mode: str,
        action: str
    ) -> Dict[str, Any]:
        """
        Main verdict determination function
        
        Args:
            problem_id: ID of the problem
            wrapped_code: Full compiled C++ program
            mode: "practice" or "battle"
            action: "run" or "submit"
        
        Returns:
            Verdict result dictionary with:
            - verdict: Final verdict string
            - action: "run" or "submit"
            - testResults: List of test results (only for "run")
            - testsPassed: Number of tests passed
            - totalTests: Total number of tests
            - executionTime: Total execution time
            - memory: Max memory used
            - error_message: Error message if failed
        """
        # Step 1: Fetch problem from database
        problem = problems_collection.find_one({"problem_id": problem_id})
        
        if not problem:
            return {
                "success": False,
                "verdict": VerdictService.VERDICT_INTERNAL_ERROR,
                "error_message": f"Problem '{problem_id}' not found in database"
            }
        
        # Step 2: Select test cases based on action
        if action == "run":
            test_cases = problem.get("sampleTestCases", [])
        elif action == "submit":
            test_cases = problem.get("hiddenTestCases", [])
        else:
            return {
                "success": False,
                "verdict": VerdictService.VERDICT_INTERNAL_ERROR,
                "error_message": f"Invalid action: {action}. Must be 'run' or 'submit'"
            }
        
        if not test_cases:
            return {
                "success": False,
                "verdict": VerdictService.VERDICT_INTERNAL_ERROR,
                "error_message": f"No test cases found for action '{action}'"
            }
        
        # Step 3: Execute code against each test case (STOP ON FIRST FAILURE)
        test_results = []
        tests_passed = 0
        total_execution_time = 0.0
        max_memory = 0
        final_verdict = VerdictService.VERDICT_ACCEPTED
        error_message = ""
        
        for idx, test_case in enumerate(test_cases):
            test_input = test_case.get("input", "")
            expected_output = test_case.get("expectedOutput", "")
            
            # Format input for Judge0 (convert comma-separated to newlines)
            # Example: "[1,2,3], 5" -> "[1,2,3]\n5"
            stdin_input = test_input.replace(", ", "\n")
            
            # Execute code with retry logic
            execution_result = VerdictService.execute_with_retry(
                wrapped_code=wrapped_code,
                stdin_input=stdin_input,
                mode=mode
            )
            
            # Update metrics
            total_execution_time += execution_result.get("execution_time", 0.0)
            max_memory = max(max_memory, execution_result.get("memory", 0))
            
            # Check for compilation error
            if execution_result.get("status") == "compilation_error":
                final_verdict = VerdictService.VERDICT_COMPILATION_ERROR
                error_message = execution_result.get("error_message", "Compilation failed")
                
                test_results.append({
                    "testCase": idx + 1,
                    "input": test_input if action == "run" else None,
                    "expectedOutput": expected_output if action == "run" else None,
                    "actualOutput": None,
                    "passed": False,
                    "verdict": final_verdict,
                    "executionTime": 0.0,
                    "memory": 0,
                    "error": error_message
                })
                break  # STOP ON FIRST FAILURE
            
            # Check for runtime error
            if execution_result.get("status") == "runtime_error":
                final_verdict = VerdictService.VERDICT_RUNTIME_ERROR
                error_message = execution_result.get("error_message", "Runtime error occurred")
                
                test_results.append({
                    "testCase": idx + 1,
                    "input": test_input if action == "run" else None,
                    "expectedOutput": expected_output if action == "run" else None,
                    "actualOutput": execution_result.get("stderr", ""),
                    "passed": False,
                    "verdict": final_verdict,
                    "executionTime": execution_result.get("execution_time", 0.0),
                    "memory": execution_result.get("memory", 0),
                    "error": error_message
                })
                break  # STOP ON FIRST FAILURE
            
            # Check for time limit exceeded
            if execution_result.get("status") == "time_limit_exceeded":
                final_verdict = VerdictService.VERDICT_TIME_LIMIT_EXCEEDED
                error_message = execution_result.get("error_message", "Time limit exceeded")
                
                test_results.append({
                    "testCase": idx + 1,
                    "input": test_input if action == "run" else None,
                    "expectedOutput": expected_output if action == "run" else None,
                    "actualOutput": None,
                    "passed": False,
                    "verdict": final_verdict,
                    "executionTime": execution_result.get("execution_time", 0.0),
                    "memory": execution_result.get("memory", 0),
                    "error": error_message
                })
                break  # STOP ON FIRST FAILURE
            
            # Check for internal/network errors
            if execution_result.get("status") == "internal_error":
                final_verdict = VerdictService.VERDICT_INTERNAL_ERROR
                error_message = execution_result.get("error_message", "Internal error")
                
                test_results.append({
                    "testCase": idx + 1,
                    "input": test_input if action == "run" else None,
                    "expectedOutput": expected_output if action == "run" else None,
                    "actualOutput": None,
                    "passed": False,
                    "verdict": final_verdict,
                    "executionTime": 0.0,
                    "memory": 0,
                    "error": error_message
                })
                break  # STOP ON FIRST FAILURE
            
            # Code executed successfully - check output
            actual_output = execution_result.get("stdout", "")
            output_matches = VerdictService.compare_outputs(actual_output, expected_output)
            
            if output_matches:
                # Test passed
                tests_passed += 1
                test_results.append({
                    "testCase": idx + 1,
                    "input": test_input if action == "run" else None,
                    "expectedOutput": expected_output if action == "run" else None,
                    "actualOutput": actual_output if action == "run" else None,
                    "passed": True,
                    "verdict": VerdictService.VERDICT_ACCEPTED,
                    "executionTime": execution_result.get("execution_time", 0.0),
                    "memory": execution_result.get("memory", 0),
                    "error": None
                })
            else:
                # Wrong answer - STOP ON FIRST FAILURE
                final_verdict = VerdictService.VERDICT_WRONG_ANSWER
                error_message = f"Output does not match expected output"
                
                test_results.append({
                    "testCase": idx + 1,
                    "input": test_input if action == "run" else None,
                    "expectedOutput": expected_output if action == "run" else None,
                    "actualOutput": actual_output if action == "run" else None,
                    "passed": False,
                    "verdict": final_verdict,
                    "executionTime": execution_result.get("execution_time", 0.0),
                    "memory": execution_result.get("memory", 0),
                    "error": error_message
                })
                break  # STOP ON FIRST FAILURE
        
        # Step 4: Build response based on action
        if action == "run":
            # For RUN: Return detailed test results
            return {
                "success": final_verdict == VerdictService.VERDICT_ACCEPTED,
                "action": "run",
                "verdict": final_verdict,
                "testResults": test_results,
                "testsPassed": tests_passed,
                "totalTests": len(test_cases),
                "executionTime": round(total_execution_time, 3),
                "memory": max_memory,
                "error_message": error_message if error_message else None
            }
        else:
            # For SUBMIT: Return only verdict and counts (no outputs)
            return {
                "success": final_verdict == VerdictService.VERDICT_ACCEPTED,
                "action": "submit",
                "verdict": final_verdict,
                "testsPassed": tests_passed,
                "totalTests": len(test_cases),
                "executionTime": round(total_execution_time, 3),
                "memory": max_memory,
                "error_message": error_message if error_message else None
            }
    
    @staticmethod
    def store_submission(
        user_id: Optional[str],
        problem_id: str,
        mode: str,
        action: str,
        verdict: str,
        tests_passed: int,
        total_tests: int,
        execution_time: float,
        memory: int,
        battle_id: Optional[str] = None
    ) -> str:
        """
        Store submission result in database
        
        Args:
            user_id: User ID (None for guest)
            problem_id: Problem ID
            mode: "practice" or "battle"
            action: "run" or "submit"
            verdict: Final verdict
            tests_passed: Number of tests passed
            total_tests: Total number of tests
            execution_time: Execution time in seconds
            memory: Memory used in KB
            battle_id: Battle ID (for battle mode only)
        
        Returns:
            Submission ID
        """
        import uuid
        
        submission_id = str(uuid.uuid4())
        
        submission_data = {
            "_id": submission_id,
            "userId": user_id if user_id else "guest",
            "problemId": problem_id,
            "mode": mode,
            "action": action,
            "verdict": verdict,
            "testsPassed": tests_passed,
            "totalTests": total_tests,
            "executionTime": execution_time,
            "memory": memory,
            "submittedAt": datetime.utcnow().isoformat(),
            "battleId": battle_id
        }
        
        submissions_collection.insert_one(submission_data)
        
        return submission_id


# Convenience function for direct usage
def get_verdict(
    problem_id: str,
    wrapped_code: str,
    mode: str,
    action: str,
    user_id: Optional[str] = None,
    battle_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Main entry point for verdict determination
    
    Args:
        problem_id: ID of the problem
        wrapped_code: Full compiled C++ program
        mode: "practice" or "battle"
        action: "run" or "submit"
        user_id: User ID (optional, None for guest)
        battle_id: Battle ID (optional, for battle mode)
    
    Returns:
        Verdict result with submission ID
    """
    # Get verdict
    verdict_result = VerdictService.determine_verdict(
        problem_id=problem_id,
        wrapped_code=wrapped_code,
        mode=mode,
        action=action
    )
    
    # Store submission (only for SUBMIT, not for RUN)
    if action == "submit" and verdict_result.get("success") is not None:
        submission_id = VerdictService.store_submission(
            user_id=user_id,
            problem_id=problem_id,
            mode=mode,
            action=action,
            verdict=verdict_result["verdict"],
            tests_passed=verdict_result["testsPassed"],
            total_tests=verdict_result["totalTests"],
            execution_time=verdict_result["executionTime"],
            memory=verdict_result["memory"],
            battle_id=battle_id
        )
        verdict_result["submissionId"] = submission_id
    
    return verdict_result
