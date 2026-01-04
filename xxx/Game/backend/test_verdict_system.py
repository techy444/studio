"""
Test script for Verdict System
Tests basic functionality of the verdict service
"""

import requests
import json

BASE_URL = "http://localhost:8001"

def test_verdict_run_without_auth():
    """Test RUN action without authentication (should work as guest)"""
    print("\n=== Test 1: RUN without authentication ===")
    
    # Simple working code
    wrapped_code = """#include <iostream>
#include <vector>
using namespace std;

vector<int> parseIntArray(string line) {
    vector<int> result;
    result.push_back(2);
    result.push_back(7);
    result.push_back(11);
    result.push_back(15);
    return result;
}

int parseInt(string line) {
    return 9;
}

void printIntArray(vector<int> arr) {
    cout << "[";
    for (int i = 0; i < arr.size(); i++) {
        cout << arr[i];
        if (i < arr.size() - 1) cout << ",";
    }
    cout << "]";
}

class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        vector<int> result;
        result.push_back(0);
        result.push_back(1);
        return result;
    }
};

int main() {
    string line1;
    getline(cin, line1);
    vector<int> nums = parseIntArray(line1);
    
    string line2;
    getline(cin, line2);
    int target = parseInt(line2);
    
    Solution solution;
    vector<int> result = solution.twoSum(nums, target);
    
    printIntArray(result);
    
    return 0;
}"""
    
    payload = {
        "problemId": "two-sum",
        "wrappedCode": wrapped_code,
        "mode": "practice",
        "action": "run"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/code/verdict", json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Success: {data.get('success')}")
            print(f"✓ Verdict: {data.get('verdict')}")
            print(f"✓ Tests Passed: {data.get('testsPassed')}/{data.get('totalTests')}")
            print(f"✓ Action: {data.get('action')}")
            
            if data.get('testResults'):
                print(f"✓ Test Results Count: {len(data['testResults'])}")
                for test in data['testResults']:
                    print(f"  - Test {test['testCase']}: {'✓ Passed' if test['passed'] else '✗ Failed'}")
        else:
            print(f"✗ Failed: {response.text}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def test_verdict_submit_without_auth():
    """Test SUBMIT action without authentication (should fail with 401)"""
    print("\n=== Test 2: SUBMIT without authentication (should fail) ===")
    
    payload = {
        "problemId": "two-sum",
        "wrappedCode": "#include <iostream>\nint main() { return 0; }",
        "mode": "practice",
        "action": "submit"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/code/verdict", json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 401:
            print("✓ Correctly returned 401 Unauthorized")
            print(f"✓ Message: {response.json().get('detail')}")
        else:
            print(f"✗ Expected 401, got {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def test_verdict_invalid_problem():
    """Test with invalid problem ID"""
    print("\n=== Test 3: Invalid problem ID ===")
    
    payload = {
        "problemId": "invalid-problem-xyz",
        "wrappedCode": "#include <iostream>\nint main() { return 0; }",
        "mode": "practice",
        "action": "run"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/code/verdict", json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 500:
            data = response.json()
            print(f"✓ Correctly returned error")
            print(f"✓ Detail: {data.get('detail')}")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def test_verdict_compilation_error():
    """Test with code that has compilation error"""
    print("\n=== Test 4: Compilation Error ===")
    
    # Code with missing semicolon
    wrapped_code = """#include <iostream>
using namespace std;

int main() {
    cout << "Hello" // Missing semicolon
    return 0;
}"""
    
    payload = {
        "problemId": "two-sum",
        "wrappedCode": wrapped_code,
        "mode": "practice",
        "action": "run"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/code/verdict", json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Success: {data.get('success')}")
            print(f"✓ Verdict: {data.get('verdict')}")
            
            if data.get('verdict') == 'Compilation Error':
                print("✓ Correctly identified compilation error")
            else:
                print(f"✗ Expected 'Compilation Error', got '{data.get('verdict')}'")
        else:
            print(f"✗ Failed: {response.text}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def test_health_check():
    """Test if backend is running"""
    print("\n=== Test 0: Health Check ===")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Backend is running")
            print(f"✓ Message: {data.get('message')}")
        else:
            print(f"✗ Backend not responding correctly")
    except Exception as e:
        print(f"✗ Backend not reachable: {str(e)}")


if __name__ == "__main__":
    print("=" * 60)
    print("VERDICT SYSTEM TEST SUITE")
    print("=" * 60)
    
    # Run tests
    test_health_check()
    test_verdict_run_without_auth()
    test_verdict_submit_without_auth()
    test_verdict_invalid_problem()
    test_verdict_compilation_error()
    
    print("\n" + "=" * 60)
    print("TEST SUITE COMPLETED")
    print("=" * 60)
