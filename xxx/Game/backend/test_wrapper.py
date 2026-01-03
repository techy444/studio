"""
Test script to demonstrate the Code Wrapper Generator
Shows how Practice and Battle modes can use the SAME wrapper function
"""

from code_wrapper import generate_wrapper


def test_two_sum_problem():
    """
    Test Case 1: Two Sum Problem
    - Input: array of integers, target integer
    - Output: array of integers
    """
    print("=" * 80)
    print("TEST 1: Two Sum Problem")
    print("=" * 80)
    
    # User code (what they write in Monaco editor)
    user_code = """vector<int> result;
        for (int i = 0; i < nums.size(); i++) {
            for (int j = i + 1; j < nums.size(); j++) {
                if (nums[i] + nums[j] == target) {
                    result.push_back(i);
                    result.push_back(j);
                    return result;
                }
            }
        }
        return result;"""
    
    # Problem metadata (from MongoDB)
    problem_metadata = {
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
    
    # Generate wrapper (SAME function for Practice and Battle)
    result = generate_wrapper(user_code, problem_metadata, "cpp")
    
    if result["success"]:
        print("✅ Wrapper generated successfully!\n")
        print("FULL COMPILABLE C++ PROGRAM:")
        print("-" * 80)
        print(result["wrappedCode"])
        print("-" * 80)
    else:
        print(f"❌ Error: {result['error']}")


def test_valid_parentheses():
    """
    Test Case 2: Valid Parentheses
    - Input: string
    - Output: boolean
    """
    print("\n\n")
    print("=" * 80)
    print("TEST 2: Valid Parentheses Problem")
    print("=" * 80)
    
    user_code = """stack<char> st;
        for (char c : s) {
            if (c == '(' || c == '{' || c == '[') {
                st.push(c);
            } else {
                if (st.empty()) return false;
                char top = st.top();
                st.pop();
                if ((c == ')' && top != '(') ||
                    (c == '}' && top != '{') ||
                    (c == ']' && top != '[')) {
                    return false;
                }
            }
        }
        return st.empty();"""
    
    problem_metadata = {
        "functionName": "isValid",
        "className": "Solution",
        "returnType": "bool",
        "parameters": [
            {"name": "s", "type": "string"}
        ],
        "inputFormat": ["string"],
        "outputFormat": "bool"
    }
    
    result = generate_wrapper(user_code, problem_metadata, "cpp")
    
    if result["success"]:
        print("✅ Wrapper generated successfully!\n")
        print("FULL COMPILABLE C++ PROGRAM:")
        print("-" * 80)
        print(result["wrappedCode"])
        print("-" * 80)
    else:
        print(f"❌ Error: {result['error']}")


def test_reverse_string():
    """
    Test Case 3: Reverse String
    - Input: array of strings
    - Output: array of strings
    """
    print("\n\n")
    print("=" * 80)
    print("TEST 3: Reverse String Array Problem")
    print("=" * 80)
    
    user_code = """vector<string> result;
        for (int i = words.size() - 1; i >= 0; i--) {
            result.push_back(words[i]);
        }
        return result;"""
    
    problem_metadata = {
        "functionName": "reverseWords",
        "className": "Solution",
        "returnType": "vector<string>",
        "parameters": [
            {"name": "words", "type": "vector<string>&"}
        ],
        "inputFormat": ["array_string"],
        "outputFormat": "array_string"
    }
    
    result = generate_wrapper(user_code, problem_metadata, "cpp")
    
    if result["success"]:
        print("✅ Wrapper generated successfully!\n")
        print("FULL COMPILABLE C++ PROGRAM:")
        print("-" * 80)
        print(result["wrappedCode"])
        print("-" * 80)
    else:
        print(f"❌ Error: {result['error']}")


def demonstrate_mode_agnostic():
    """
    Demonstrate that BOTH Practice and Battle use the SAME wrapper function
    """
    print("\n\n")
    print("=" * 80)
    print("DEMONSTRATION: Mode-Agnostic Design")
    print("=" * 80)
    
    user_code = "return nums[0] + nums[1];"
    
    problem_metadata = {
        "functionName": "sum",
        "className": "Solution",
        "returnType": "int",
        "parameters": [
            {"name": "nums", "type": "vector<int>&"}
        ],
        "inputFormat": ["array_int"],
        "outputFormat": "int"
    }
    
    print("\n📝 PRACTICE MODE calls:")
    print("   result = generate_wrapper(user_code, problem_metadata)")
    practice_result = generate_wrapper(user_code, problem_metadata)
    print(f"   ✅ Success: {practice_result['success']}")
    
    print("\n⚔️  BATTLE MODE calls:")
    print("   result = generate_wrapper(user_code, problem_metadata)")
    battle_result = generate_wrapper(user_code, problem_metadata)
    print(f"   ✅ Success: {battle_result['success']}")
    
    print("\n🎯 SAME FUNCTION, SAME OUTPUT!")
    print("   Practice and Battle both use the exact same wrapper generator.")
    print("   The modes only differ in HOW they handle the results:")
    print("   - Practice: Shows test case results, allows retry")
    print("   - Battle: Evaluates against opponent, tracks time")


if __name__ == "__main__":
    # Run all tests
    test_two_sum_problem()
    test_valid_parentheses()
    test_reverse_string()
    demonstrate_mode_agnostic()
    
    print("\n\n")
    print("=" * 80)
    print("✅ ALL TESTS COMPLETED")
    print("=" * 80)
    print("\nThe wrapper generator is ready for both Practice and Battle modes!")
    print("Next steps:")
    print("1. Store problem metadata in MongoDB problems collection")
    print("2. Frontend calls /api/code/generate-wrapper with user code")
    print("3. Send wrapped code to Judge0 or execution engine")
