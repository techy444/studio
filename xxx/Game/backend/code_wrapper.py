"""
Code Wrapper Generator - Mode-Agnostic
Generates full compilable C++ programs from user function code
Works for BOTH Practice Mode and Battle Mode
"""

from typing import Dict, List, Any, Optional
from problem_templates import (
    CppHelpers,
    get_helper_functions,
    cpp_type_to_format,
    format_to_cpp_type
)


class CodeWrapperGenerator:
    """
    Mode-agnostic code wrapper generator
    Converts user function code into full compilable C++ program
    """
    
    @staticmethod
    def generate_cpp_wrapper(
        user_code: str,
        problem_metadata: Dict[str, Any],
        language: str = "cpp"
    ) -> Dict[str, Any]:
        """
        Generate full compilable C++ program from user code
        
        Args:
            user_code: User's function implementation (just the logic)
            problem_metadata: Problem information including:
                - functionName: Name of the function (e.g., 'twoSum')
                - className: Name of the class (default: 'Solution')
                - returnType: C++ return type (e.g., 'vector<int>')
                - parameters: List of parameter dicts with 'name' and 'type'
                - inputFormat: List of input formats (e.g., ['array_int', 'int'])
                - outputFormat: Output format (e.g., 'array_int')
            language: Programming language (currently only 'cpp' supported)
        
        Returns:
            Dictionary with:
                - wrappedCode: Full compilable C++ program
                - success: Boolean indicating success
                - error: Error message if failed
        
        Example problem_metadata:
        {
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
        """
        if language != "cpp":
            return {
                "success": False,
                "error": f"Language '{language}' not supported yet. Only 'cpp' is supported.",
                "wrappedCode": None
            }
        
        try:
            # Extract metadata
            function_name = problem_metadata.get("functionName", "solve")
            class_name = problem_metadata.get("className", "Solution")
            return_type = problem_metadata.get("returnType", "int")
            parameters = problem_metadata.get("parameters", [])
            input_formats = problem_metadata.get("inputFormat", [])
            output_format = problem_metadata.get("outputFormat", "int")
            
            # Validate metadata
            if not function_name:
                return {
                    "success": False,
                    "error": "Missing 'functionName' in problem metadata",
                    "wrappedCode": None
                }
            
            if len(parameters) != len(input_formats):
                return {
                    "success": False,
                    "error": f"Mismatch: {len(parameters)} parameters but {len(input_formats)} input formats",
                    "wrappedCode": None
                }
            
            # Generate the wrapped code
            wrapped_code = CodeWrapperGenerator._build_cpp_program(
                user_code=user_code,
                function_name=function_name,
                class_name=class_name,
                return_type=return_type,
                parameters=parameters,
                input_formats=input_formats,
                output_format=output_format
            )
            
            return {
                "success": True,
                "wrappedCode": wrapped_code,
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to generate wrapper: {str(e)}",
                "wrappedCode": None
            }
    
    @staticmethod
    def _build_cpp_program(
        user_code: str,
        function_name: str,
        class_name: str,
        return_type: str,
        parameters: List[Dict[str, str]],
        input_formats: List[str],
        output_format: str
    ) -> str:
        """
        Build the complete C++ program
        """
        # 1. Generate headers
        headers = CppHelpers.get_required_headers(input_formats, output_format)
        headers_code = '\n'.join([f'#include {header}' for header in headers])
        
        # 2. Using namespace
        using_code = "using namespace std;"
        
        # 3. Generate helper functions
        helpers_code = get_helper_functions(input_formats, output_format)
        
        # 4. Generate Solution class with user function
        solution_class = CodeWrapperGenerator._generate_solution_class(
            user_code=user_code,
            function_name=function_name,
            class_name=class_name,
            return_type=return_type,
            parameters=parameters
        )
        
        # 5. Generate main function
        main_function = CodeWrapperGenerator._generate_main_function(
            function_name=function_name,
            class_name=class_name,
            return_type=return_type,
            parameters=parameters,
            input_formats=input_formats,
            output_format=output_format
        )
        
        # Combine all parts
        full_program = f"""{headers_code}
{using_code}

{helpers_code}

{solution_class}

{main_function}
"""
        
        return full_program
    
    @staticmethod
    def _generate_solution_class(
        user_code: str,
        function_name: str,
        class_name: str,
        return_type: str,
        parameters: List[Dict[str, str]]
    ) -> str:
        """
        Generate the Solution class with user's function
        """
        # Build parameter list
        param_list = ', '.join([f"{p['type']} {p['name']}" for p in parameters])
        
        # Indent user code
        indented_user_code = '\n'.join(['        ' + line for line in user_code.split('\n')])
        
        solution_class = f"""class {class_name} {{
public:
    {return_type} {function_name}({param_list}) {{
{indented_user_code}
    }}
}};"""
        
        return solution_class
    
    @staticmethod
    def _generate_main_function(
        function_name: str,
        class_name: str,
        return_type: str,
        parameters: List[Dict[str, str]],
        input_formats: List[str],
        output_format: str
    ) -> str:
        """
        Generate the main function that reads input, calls user function, prints output
        """
        # Generate input reading code
        input_reading = []
        for i, (param, input_format) in enumerate(zip(parameters, input_formats)):
            param_name = param['name']
            param_type = param['type'].replace('&', '').replace('const', '').strip()
            
            input_reading.append(f"    // Read input {i+1}: {param_name}")
            input_reading.append(f"    string line{i+1};")
            input_reading.append(f"    getline(cin, line{i+1});")
            
            # Parse based on format
            if input_format == 'int':
                input_reading.append(f"    {param_type} {param_name} = parseInt(line{i+1});")
            elif input_format == 'string':
                input_reading.append(f"    {param_type} {param_name} = parseString(line{i+1});")
            elif input_format == 'array_int':
                input_reading.append(f"    {param_type} {param_name} = parseIntArray(line{i+1});")
            elif input_format == 'array_string':
                input_reading.append(f"    {param_type} {param_name} = parseStringArray(line{i+1});")
            else:
                input_reading.append(f"    {param_type} {param_name}; // Unknown format: {input_format}")
            
            input_reading.append("")
        
        input_reading_code = '\n'.join(input_reading)
        
        # Generate function call
        param_names = ', '.join([p['name'] for p in parameters])
        function_call = f"    {class_name} solution;\n"
        function_call += f"    {return_type} result = solution.{function_name}({param_names});"
        
        # Generate output printing code
        output_printing = "    // Print output"
        if output_format == 'int':
            output_printing += "\n    printInt(result);"
        elif output_format == 'string':
            output_printing += "\n    printString(result);"
        elif output_format == 'bool':
            output_printing += "\n    printBool(result);"
        elif output_format == 'array_int':
            output_printing += "\n    printIntArray(result);"
        elif output_format == 'array_string':
            output_printing += "\n    printStringArray(result);"
        else:
            output_printing += f"\n    cout << result << endl; // Unknown format: {output_format}"
        
        main_function = f"""int main() {{
{input_reading_code}
{function_call}
    
{output_printing}
    
    return 0;
}}"""
        
        return main_function


# Convenience function for direct usage
def generate_wrapper(user_code: str, problem_metadata: Dict[str, Any], language: str = "cpp") -> Dict[str, Any]:
    """
    Convenience function to generate code wrapper
    
    Args:
        user_code: User's function implementation
        problem_metadata: Problem metadata dictionary
        language: Programming language (default: 'cpp')
    
    Returns:
        Dictionary with wrappedCode, success, and error fields
    """
    return CodeWrapperGenerator.generate_cpp_wrapper(user_code, problem_metadata, language)
