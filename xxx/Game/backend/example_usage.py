"""
Example: How Practice and Battle Modes Use the Same Execution Function

This demonstrates that BOTH modes call the EXACT SAME execution logic.
The only difference is the 'mode' parameter, which is used for context/logging.
"""

from judge0_service import execute_code

# Example wrapped C++ code (output from wrapper generator)
WRAPPED_CODE = """
#include <iostream>
#include <vector>
#include <sstream>
using namespace std;

vector<int> parseIntArray(const string& line) {
    vector<int> result;
    string cleaned = line;
    cleaned.erase(0, cleaned.find_first_not_of(" ["));
    cleaned.erase(cleaned.find_last_not_of(" ]") + 1);
    
    stringstream ss(cleaned);
    string token;
    while (getline(ss, token, ',')) {
        result.push_back(stoi(token));
    }
    return result;
}

int parseInt(const string& line) {
    return stoi(line);
}

void printIntArray(const vector<int>& arr) {
    cout << "[";
    for (size_t i = 0; i < arr.size(); i++) {
        cout << arr[i];
        if (i < arr.size() - 1) cout << ",";
    }
    cout << "]" << endl;
}

class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        // User's code would go here
        vector<int> result;
        result.push_back(0);
        result.push_back(1);
        return result;
    }
};

int main() {
    string line1, line2;
    getline(cin, line1);
    getline(cin, line2);
    
    vector<int> nums = parseIntArray(line1);
    int target = parseInt(line2);
    
    Solution solution;
    vector<int> result = solution.twoSum(nums, target);
    
    printIntArray(result);
    
    return 0;
}
"""

# ============================================================
# PRACTICE MODE USAGE
# ============================================================

def practice_mode_execute(user_code_wrapped, test_input):
    """
    Practice Mode: Test user's solution against sample test cases
    """
    print("=" * 60)
    print("PRACTICE MODE EXECUTION")
    print("=" * 60)
    
    # Call the SHARED execute_code function
    result = execute_code(
        source_code=user_code_wrapped,
        stdin_input=test_input,
        mode="practice"  # ← Only difference is this parameter
    )
    
    # Display results
    print(f"Status: {result['status']}")
    print(f"Success: {result['success']}")
    
    if result['success']:
        print(f"✅ Output: {result['stdout']}")
        print(f"⏱️  Time: {result['execution_time']}s")
        print(f"💾 Memory: {result['memory']} KB")
    else:
        print(f"❌ Error: {result['error_message']}")
        if result['compile_output']:
            print(f"Compilation: {result['compile_output']}")
    
    return result


# ============================================================
# BATTLE MODE USAGE
# ============================================================

def battle_mode_execute(user_code_wrapped, battle_test_input):
    """
    Battle Mode: Test user's solution against battle test cases
    """
    print("\n" + "=" * 60)
    print("BATTLE MODE EXECUTION")
    print("=" * 60)
    
    # Call the SAME execute_code function
    result = execute_code(
        source_code=user_code_wrapped,
        stdin_input=battle_test_input,
        mode="battle"  # ← Only difference is this parameter
    )
    
    # Display results (same logic as Practice)
    print(f"Status: {result['status']}")
    print(f"Success: {result['success']}")
    
    if result['success']:
        print(f"✅ Output: {result['stdout']}")
        print(f"⏱️  Time: {result['execution_time']}s")
        print(f"💾 Memory: {result['memory']} KB")
    else:
        print(f"❌ Error: {result['error_message']}")
        if result['compile_output']:
            print(f"Compilation: {result['compile_output']}")
    
    return result


# ============================================================
# DEMONSTRATION
# ============================================================

if __name__ == "__main__":
    # Sample test case input
    test_input = "[2,7,11,15]\n9"
    
    print("\n🔥 Demonstrating Mode-Agnostic Execution\n")
    
    # 1. Practice Mode calls execute_code with mode="practice"
    practice_result = practice_mode_execute(WRAPPED_CODE, test_input)
    
    # 2. Battle Mode calls execute_code with mode="battle"
    battle_result = battle_mode_execute(WRAPPED_CODE, test_input)
    
    # 3. Verify both use the same function
    print("\n" + "=" * 60)
    print("VERIFICATION")
    print("=" * 60)
    print("✅ Practice and Battle both called judge0_service.execute_code()")
    print("✅ Execution logic is IDENTICAL")
    print("✅ Only the 'mode' parameter differs (for logging/context)")
    print("\n🎯 Result: Mode-agnostic design achieved!")
    print("=" * 60)
