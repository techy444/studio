"""
API Test Script
Demonstrates how to call the wrapper generator API endpoints
Can be used by frontend developers as a reference
"""

import requests
import json


def test_generate_wrapper_endpoint():
    """
    Test the /api/code/generate-wrapper endpoint
    """
    print("=" * 80)
    print("TEST: POST /api/code/generate-wrapper")
    print("=" * 80)
    
    # Test data
    request_data = {
        "userCode": """vector<int> result;
        for (int i = 0; i < nums.size(); i++) {
            for (int j = i + 1; j < nums.size(); j++) {
                if (nums[i] + nums[j] == target) {
                    result.push_back(i);
                    result.push_back(j);
                    return result;
                }
            }
        }
        return result;""",
        "language": "cpp",
        "problemMetadata": {
            "functionName": "twoSum",
            "className": "Solution",
            "returnType": "vector<int>",
            "parameters": [
                {"name": "nums", "type": "vector<int>&"},
                {"name": "target", "type": "int"}
            ],
            "inputFormat": ["array_int", "int"],
            "outputFormat": "array_int"
        }
    }
    
    print("\n📤 REQUEST:")
    print(json.dumps(request_data, indent=2))
    
    try:
        # Make API call
        response = requests.post(
            "http://localhost:8001/api/code/generate-wrapper",
            json=request_data,
            timeout=10
        )
        
        print(f"\n📥 RESPONSE STATUS: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ SUCCESS!")
            print("\nGenerated C++ Code:")
            print("-" * 80)
            print(result.get("wrappedCode", "No code returned"))
            print("-" * 80)
        else:
            print(f"\n❌ ERROR: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\n⚠️  Backend server not running!")
        print("Start the server with: cd /app/xxx/Game/backend && uvicorn server:app --host 0.0.0.0 --port 8001")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")


def test_with_curl():
    """
    Show curl command for testing
    """
    print("\n\n")
    print("=" * 80)
    print("CURL COMMAND FOR TESTING")
    print("=" * 80)
    
    curl_command = """
curl -X POST http://localhost:8001/api/code/generate-wrapper \\
  -H "Content-Type: application/json" \\
  -d '{
    "userCode": "vector<int> result;\\nreturn result;",
    "language": "cpp",
    "problemMetadata": {
      "functionName": "twoSum",
      "className": "Solution",
      "returnType": "vector<int>",
      "parameters": [
        {"name": "nums", "type": "vector<int>&"},
        {"name": "target", "type": "int"}
      ],
      "inputFormat": ["array_int", "int"],
      "outputFormat": "array_int"
    }
  }'
"""
    
    print(curl_command)


def show_frontend_integration():
    """
    Show how frontend should integrate
    """
    print("\n\n")
    print("=" * 80)
    print("FRONTEND INTEGRATION EXAMPLE (TypeScript)")
    print("=" * 80)
    
    frontend_code = """
// Extract user code from Monaco editor
const userCode = extractUserCode(editorInstance);

// Get problem metadata (from database or props)
const problemMetadata = {
  functionName: "twoSum",
  className: "Solution",
  returnType: "vector<int>",
  parameters: [
    { name: "nums", type: "vector<int>&" },
    { name: "target", type: "int" }
  ],
  inputFormat: ["array_int", "int"],
  outputFormat: "array_int"
};

// Call API to generate wrapper
const response = await fetch(
  `${API_URL}/api/code/generate-wrapper`,
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}` // Optional
    },
    body: JSON.stringify({
      userCode: userCode,
      language: "cpp",
      problemMetadata: problemMetadata
    })
  }
);

const result = await response.json();

if (result.success) {
  // Send to Judge0 or execution engine
  const wrappedCode = result.wrappedCode;
  
  // For Practice Mode:
  const testResults = await executeCode(wrappedCode, testCases);
  showResults(testResults);
  
  // For Battle Mode:
  const battleResults = await executeCode(wrappedCode, hiddenTestCases);
  updateBattleStatus(battleResults);
} else {
  console.error("Wrapper generation failed:", result.error);
}
"""
    
    print(frontend_code)


if __name__ == "__main__":
    print("\n🚀 Backend Wrapper Generator API Test\n")
    
    # Show integration examples
    test_with_curl()
    show_frontend_integration()
    
    # Try to test the actual API
    print("\n\n")
    test_generate_wrapper_endpoint()
    
    print("\n\n")
    print("=" * 80)
    print("✅ API DOCUMENTATION COMPLETE")
    print("=" * 80)
    print("\nNext Steps:")
    print("1. Start backend: sudo supervisorctl start backend")
    print("2. Test with curl or Postman")
    print("3. Integrate in frontend (Practice/Battle pages)")
    print("4. Connect to Judge0 for code execution")
