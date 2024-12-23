import re
import sys

def parse_unity_log(log_path):
    errors = []
    warnings = []

    try:
        with open(log_path, 'r', encoding='utf-8') as log_file:
            log_content = log_file.readlines()
        
        # Matches lines containing the "ERROR", "Error" or "error" word followed by the error message.
        error_pattern = re.compile(r'\b(ERROR|Error|error)\b:? (.+)')
        # Matches lines containing the "WARNING", "Warning" or "warning" word followed by the warning message.
        warning_pattern = re.compile(r'\b(WARNING|Warning|warning)\b:? (.+)')

        for line_number, line in enumerate(log_content, start=1):
            if error_match := error_pattern.search(line):
                errors.append(f"Line {line_number}: {error_match.group(2).strip()}")
            if warning_match := warning_pattern.search(line):
                warnings.append(f"Line {line_number}: {warning_match.group(2).strip()}")
        return errors, warnings

    except FileNotFoundError:
        print(f"Error: Log file not found at {log_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading log file: {e}")
        sys.exit(1)

# Log the errors and warnings as annotations
def output_github_annotations(errors, warnings, log_file_path):
    for error in errors:
        print(f"::error file={log_file_path}::{error}")
    for warning in warnings:
        print(f"::warning file={log_file_path}::{warning}")

# Set errors as action output
def set_github_output(key, value):
    """ 
    $GITHUB_OUTPUT
    key=value structure
    Multiline string output 
    """
    with open("output.txt", "a") as f:
        if isinstance(value, list):
            for item in value:
                f.write(f"{key}={item}\n")
        else:
            f.write(f"{key}={value}\n")

if __name__ == "__main__":
    # Read log file path from input arguments
    if len(sys.argv) < 2:
        print("Error: Log file path is required.")
        sys.exit(1)

    log_file_path = sys.argv[1]

    # Parse the Unity log file
    errors, warnings = parse_unity_log(log_file_path)

    # Output annotations
    output_github_annotations(errors, warnings, log_file_path)

    # Set action outputs
    set_github_output("Error", errors)