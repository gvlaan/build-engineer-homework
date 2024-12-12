import os
import re
import sys

def parse_unity_log(log_path):
    errors = []
    warnings = []
    error_count = 0
    warning_count = 0

    try:
        with open(log_path, 'r') as log_file:
            log_content = log_file.readlines()
        
        # Matches lines containing "ERROR" or "Error" followed by the error message.
        error_pattern = re.compile(r'(ERROR|Error):? (.+)')
        # Matches lines containing "WARNING" or "Warning" followed by the warning message.
        warning_pattern = re.compile(r'(WARNING|Warning):? (.+)')

        for line_number, line in enumerate(log_content, start=1):
            error_match = error_pattern.search(line)
            warning_match = warning_pattern.search(line)
            
            if error_match:
                error_count += 1
                errors.append({
                    'message': error_match.group(2).strip(),
                    'line_number': line_number
                })

            if warning_match:
                warning_count += 1
                warnings.append({
                    'message': warning_match.group(2).strip(),
                    'line_number': line_number
                })

        return errors, warnings, error_count, warning_count

    except FileNotFoundError:
        print(f"Error: Log file not found at {log_path}")
        sys.exit(1)

log_file_path = os.environ.get("LOG_PATH")
errors, warnings, error_count, warning_count = parse_unity_log(log_file_path)

# GitHub Annotations
for error in errors:
    print(f"::error file=,line={error['line_number']}::{error['message']}")

for warning in warnings:
    print(f"::warning file=,line={warning['line_number']}::{warning['message']}")

# Set outputs
print(f"::set-output name=error-count::{error_count}")
print(f"::set-output name=warning-count::{warning_count}")