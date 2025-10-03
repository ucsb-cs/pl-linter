#!/usr/bin/env python3
"""
Linter for PL HTML files.

This script checks HTML files for:
1. General XML syntax (proper tags, nesting, attributes)
2. Custom PL-specific rules (extensible)
"""

import sys
import os
import glob
from xml.etree import ElementTree as ET
from pathlib import Path


def find_html_files(root_dir="."):
    """Find all HTML files in the repository."""
    html_files = []
    for pattern in ["**/*.html", "**/*.HTML"]:
        html_files.extend(glob.glob(os.path.join(root_dir, pattern), recursive=True))
    
    # Filter out .git directory
    html_files = [f for f in html_files if ".git" not in f]
    return sorted(html_files)


def check_xml_syntax(file_path):
    """
    Check if the HTML file has valid XML syntax.
    This includes:
    - Properly formatted tags
    - Properly nested elements
    - Correct attribute syntax
    """
    errors = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to parse as XML
        try:
            ET.fromstring(content)
        except ET.ParseError as e:
            errors.append(f"XML syntax error: {str(e)}")
    
    except FileNotFoundError:
        errors.append(f"File not found: {file_path}")
    except Exception as e:
        errors.append(f"Error reading file: {str(e)}")
    
    return errors


def check_custom_rules(file_path):
    """
    Check custom PL-specific rules.
    
    This function can be extended with additional rules as needed.
    """
    errors = []
    
    # Placeholder for custom rules
    # Add specific rule checks here as they are defined
    
    return errors


def lint_file(file_path):
    """Lint a single HTML file."""
    all_errors = []
    
    # Check XML syntax
    syntax_errors = check_xml_syntax(file_path)
    if syntax_errors:
        all_errors.extend(syntax_errors)
    
    # Check custom rules
    custom_errors = check_custom_rules(file_path)
    if custom_errors:
        all_errors.extend(custom_errors)
    
    return all_errors


def main():
    """Main entry point for the linter."""
    # Get the repository root directory
    repo_root = os.getenv("GITHUB_WORKSPACE", ".")
    
    print(f"Scanning for HTML files in: {repo_root}")
    html_files = find_html_files(repo_root)
    
    if not html_files:
        print("No HTML files found.")
        return 0
    
    print(f"Found {len(html_files)} HTML file(s) to lint:")
    for f in html_files:
        print(f"  - {f}")
    print()
    
    has_errors = False
    for file_path in html_files:
        print(f"Linting: {file_path}")
        errors = lint_file(file_path)
        
        if errors:
            has_errors = True
            print(f"  ❌ FAILED with {len(errors)} error(s):")
            for error in errors:
                print(f"    - {error}")
        else:
            print(f"  ✓ PASSED")
        print()
    
    if has_errors:
        print("❌ Linting failed! Please fix the errors above.")
        return 1
    else:
        print("✓ All files passed linting!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
