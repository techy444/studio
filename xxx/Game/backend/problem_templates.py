"""
Problem Templates and Utilities for Code Wrapper Generation
Provides input parsing and output formatting helpers for C++ code generation
"""

from typing import Dict, List, Any


class CppHelpers:
    """
    Generate C++ helper functions for parsing inputs and formatting outputs
    """
    
    @staticmethod
    def get_required_headers(input_types: List[str], output_type: str) -> List[str]:
        """
        Determine required C++ headers based on input/output types
        """
        headers = set(['<iostream>', '<string>', '<sstream>'])
        
        all_types = input_types + [output_type]
        
        for type_str in all_types:
            if 'vector' in type_str or 'array' in type_str:
                headers.add('<vector>')
            if 'string' in type_str:
                headers.add('<string>')
            if 'map' in type_str or 'unordered_map' in type_str:
                headers.add('<unordered_map>')
                headers.add('<map>')
        
        return sorted(list(headers))
    
    @staticmethod
    def generate_parse_int_function() -> str:
        """Generate C++ function to parse integer from string"""
        return """
// Parse integer from string
int parseInt(const string& s) {
    return stoi(s);
}
"""
    
    @staticmethod
    def generate_parse_string_function() -> str:
        """Generate C++ function to parse string (remove quotes if present)"""
        return """
// Parse string (removes quotes if present)
string parseString(const string& s) {
    string result = s;
    // Remove leading/trailing whitespace
    size_t start = result.find_first_not_of(" \\t\\n\\r");
    size_t end = result.find_last_not_of(" \\t\\n\\r");
    if (start != string::npos && end != string::npos) {
        result = result.substr(start, end - start + 1);
    }
    // Remove quotes if present
    if (result.length() >= 2 && result.front() == '"' && result.back() == '"') {
        result = result.substr(1, result.length() - 2);
    }
    return result;
}
"""
    
    @staticmethod
    def generate_parse_int_array_function() -> str:
        """Generate C++ function to parse integer array from string"""
        return """
// Parse integer array from string like "[1,2,3]" or "1,2,3"
vector<int> parseIntArray(const string& s) {
    vector<int> result;
    string clean = s;
    
    // Remove brackets if present
    if (!clean.empty() && clean.front() == '[') clean = clean.substr(1);
    if (!clean.empty() && clean.back() == ']') clean.pop_back();
    
    if (clean.empty()) return result;
    
    stringstream ss(clean);
    string item;
    while (getline(ss, item, ',')) {
        // Remove whitespace
        item.erase(0, item.find_first_not_of(" \\t\\n\\r"));
        item.erase(item.find_last_not_of(" \\t\\n\\r") + 1);
        if (!item.empty()) {
            result.push_back(stoi(item));
        }
    }
    return result;
}
"""
    
    @staticmethod
    def generate_parse_string_array_function() -> str:
        """Generate C++ function to parse string array from string"""
        return """
// Parse string array from string like '["hello","world"]' or "hello,world"
vector<string> parseStringArray(const string& s) {
    vector<string> result;
    string clean = s;
    
    // Remove brackets if present
    if (!clean.empty() && clean.front() == '[') clean = clean.substr(1);
    if (!clean.empty() && clean.back() == ']') clean.pop_back();
    
    if (clean.empty()) return result;
    
    stringstream ss(clean);
    string item;
    bool inQuotes = false;
    string current = "";
    
    for (char c : clean) {
        if (c == '"') {
            inQuotes = !inQuotes;
        } else if (c == ',' && !inQuotes) {
            if (!current.empty()) {
                // Remove quotes and whitespace
                string trimmed = current;
                trimmed.erase(0, trimmed.find_first_not_of(" \\t\\n\\r\\""));
                trimmed.erase(trimmed.find_last_not_of(" \\t\\n\\r\\"") + 1);
                result.push_back(trimmed);
                current = "";
            }
        } else if (c != '"') {
            current += c;
        }
    }
    
    // Add last item
    if (!current.empty()) {
        string trimmed = current;
        trimmed.erase(0, trimmed.find_first_not_of(" \\t\\n\\r\\""));
        trimmed.erase(trimmed.find_last_not_of(" \\t\\n\\r\\"") + 1);
        result.push_back(trimmed);
    }
    
    return result;
}
"""
    
    @staticmethod
    def generate_print_int_function() -> str:
        """Generate C++ function to print integer"""
        return """
// Print integer
void printInt(int value) {
    cout << value << endl;
}
"""
    
    @staticmethod
    def generate_print_string_function() -> str:
        """Generate C++ function to print string"""
        return """
// Print string
void printString(const string& value) {
    cout << value << endl;
}
"""
    
    @staticmethod
    def generate_print_int_array_function() -> str:
        """Generate C++ function to print integer array"""
        return """
// Print integer array in format [1,2,3]
void printIntArray(const vector<int>& arr) {
    cout << "[";
    for (size_t i = 0; i < arr.size(); i++) {
        cout << arr[i];
        if (i < arr.size() - 1) cout << ",";
    }
    cout << "]" << endl;
}
"""
    
    @staticmethod
    def generate_print_string_array_function() -> str:
        """Generate C++ function to print string array"""
        return """
// Print string array in format ["hello","world"]
void printStringArray(const vector<string>& arr) {
    cout << "[";
    for (size_t i = 0; i < arr.size(); i++) {
        cout << "\\"" << arr[i] << "\\"";
        if (i < arr.size() - 1) cout << ",";
    }
    cout << "]" << endl;
}
"""
    
    @staticmethod
    def generate_print_bool_function() -> str:
        """Generate C++ function to print boolean"""
        return """
// Print boolean as true/false
void printBool(bool value) {
    cout << (value ? "true" : "false") << endl;
}
"""


def get_helper_functions(input_formats: List[str], output_format: str) -> str:
    """
    Generate all required helper functions based on input/output formats
    
    Args:
        input_formats: List of input types (e.g., ['int', 'array_int', 'string'])
        output_format: Output type (e.g., 'array_int', 'string', 'int')
    
    Returns:
        C++ code with all necessary helper functions
    """
    helpers = []
    generated = set()
    
    # Mapping of formats to helper functions
    format_to_parse = {
        'int': CppHelpers.generate_parse_int_function,
        'string': CppHelpers.generate_parse_string_function,
        'array_int': CppHelpers.generate_parse_int_array_function,
        'array_string': CppHelpers.generate_parse_string_array_function,
    }
    
    format_to_print = {
        'int': CppHelpers.generate_print_int_function,
        'string': CppHelpers.generate_print_string_function,
        'bool': CppHelpers.generate_print_bool_function,
        'array_int': CppHelpers.generate_print_int_array_function,
        'array_string': CppHelpers.generate_print_string_array_function,
    }
    
    # Generate parse functions for inputs
    for input_format in input_formats:
        if input_format in format_to_parse and input_format not in generated:
            helpers.append(format_to_parse[input_format]())
            generated.add(input_format)
    
    # Generate print function for output
    if output_format in format_to_print and f"print_{output_format}" not in generated:
        helpers.append(format_to_print[output_format]())
        generated.add(f"print_{output_format}")
    
    return '\n'.join(helpers)


def cpp_type_to_format(cpp_type: str) -> str:
    """
    Convert C++ type to format string
    
    Args:
        cpp_type: C++ type like 'int', 'string', 'vector<int>', 'vector<string>'
    
    Returns:
        Format string like 'int', 'string', 'array_int', 'array_string'
    """
    cpp_type = cpp_type.strip()
    
    # Remove reference and const qualifiers
    cpp_type = cpp_type.replace('&', '').replace('const', '').strip()
    
    if cpp_type == 'int':
        return 'int'
    elif cpp_type == 'string':
        return 'string'
    elif cpp_type == 'bool':
        return 'bool'
    elif 'vector<int>' in cpp_type:
        return 'array_int'
    elif 'vector<string>' in cpp_type:
        return 'array_string'
    else:
        # Default to string for unknown types
        return 'string'


def format_to_cpp_type(format_str: str) -> str:
    """
    Convert format string to C++ type
    
    Args:
        format_str: Format like 'int', 'string', 'array_int', 'array_string'
    
    Returns:
        C++ type like 'int', 'string', 'vector<int>', 'vector<string>'
    """
    format_map = {
        'int': 'int',
        'string': 'string',
        'bool': 'bool',
        'array_int': 'vector<int>',
        'array_string': 'vector<string>',
    }
    
    return format_map.get(format_str, 'string')
