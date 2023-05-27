#!/bin/bash

# Script to recursively change names of directories, subdirectories, and files

# Function to display script usage
usage() {
    echo "Usage: $0 [OPTIONS] old_name new_name"
    echo
    echo "OPTIONS:"
    echo "  -h, --help    Display this help and exit"
    echo
    echo "DESCRIPTION:"
    echo "  This script recursively changes the names of directories, subdirectories, and files"
    echo "  by replacing occurrences of 'old_name' with 'new_name'. It also updates the contents"
    echo "  of files to reflect the new name."
    echo
    echo "EXAMPLES:"
    echo "  $0 old_dir new_dir      # Rename 'old_dir' to 'new_dir' recursively"
    echo "  $0 -h                   # Display script usage"
    echo
    exit 1
}

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            ;;
        *)
            break
            ;;
    esac
done

# Check if old_name and new_name arguments are provided
if [[ $# -lt 2 ]]; then
    echo "Error: Missing required arguments."
    usage
fi

old_name="$1"
new_name="$2"

# Default values for the arguments if not provided
if [[ -z $old_name ]]; then
    old_name="old_name"
fi

if [[ -z $new_name ]]; then
    new_name="new_name"
fi

# Rename directories and files
find . -depth -name "*$old_name*" -execdir bash -c 'mv "$0" "${0//$old_name/$new_name}"' {} \;

# Rename occurrences inside files
find . -type f -exec sed -i "s/$old_name/$new_name/g" {} +
