#!/bin/bash

log_file="$1"

error_count=0
warning_count=0

while IFS= read -r line; do
  if [[ $line =~ Error: ]]; then
    echo "::error title=Error:: $line"
    ((error_count++))
  elif [[ $line =~ Warning: ]]; then
    echo "::warning title=Warning:: $line"
    ((warning_count++))
  fi
done < "$log_file"

echo "::set-output name=error-count::$error_count"