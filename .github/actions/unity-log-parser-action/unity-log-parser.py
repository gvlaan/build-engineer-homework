import re
import sys
import os

def parse_unity_log(log_path):
    errors = []
    warnings = []
    error_count = 0
    warning_count = 0

    try:
        with open(log_path, 'r', encoding='utf-8') as log_file:
            log_content = log_file.readlines()
        
        # Matches lines containing "ERROR" or "Error" followed by the error message.
        error_pattern = re.compile(r'(ERROR|Error):? (.+)')
        # Matches lines containing "WARNING" or "Warning" followed by the warning message.
        warning_pattern = re.compile(r'(WARNING|Warning):? (.+)')

        for line_number, line in enumerate(log_content, start=1):
            if error_match := error_pattern.search(line):
                error_count += 1
                errors.append(f"Line {line_number}: {error_match.group(2).strip()}")
            if warning_match := warning_pattern.search(line):
                warning_count += 1
                warnings.append(f"Line {line_number}: {warning_match.group(2).strip()}")
        return errors, warnings, error_count, warning_count

    except FileNotFoundError:
        print(f"Error: Log file not found at {log_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading log file: {e}")
        sys.exit(1)

def output_github_annotations(errors, warnings, log_file_path):
    for error in errors:
        print(f"::error file={log_file_path}::{error}")
    for warning in warnings:
        print(f"::warning file={log_file_path}::{warning}")

def set_github_output(data):
    with open("errors_output.txt", "w") as f:
        f.write("\n".join(data))

if __name__ == "__main__":
    # Read log file path from input arguments
    if len(sys.argv) < 2:
        print("Error: Log file path is required.")
        sys.exit(1)

    log_file_path = sys.argv[1]

    # Parse the Unity log file
    errors, warnings, error_count, warning_count = parse_unity_log(log_file_path)

    # Output GitHub Annotations
    output_github_annotations(errors, warnings, log_file_path)

    # Set GitHub Action Outputs
    set_github_output(errors)