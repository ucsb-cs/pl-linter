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
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to parse the file as XML
        try:
            tree = ET.fromstring(content)
        except ET.ParseError:
            # If XML parsing fails, we can't check custom rules
            # The XML syntax error will be caught by check_xml_syntax
            return errors
        
        # Rule: <pl-multiple-choice> must NOT be nested inside another element
        # It must be the root element (have no parent)
        def check_pl_multiple_choice_nesting(element, is_root=True):
            """Recursively check if pl-multiple-choice is properly placed."""
            local_errors = []
            
            if element.tag == 'pl-multiple-choice' and not is_root:
                # pl-multiple-choice found but it's not the root element
                local_errors.append(
                    f"<pl-multiple-choice> element must not be nested inside other elements. "
                    f"It must be the root element of the document."
                )
            
            # Recursively check children (they are not root)
            for child in element:
                local_errors.extend(check_pl_multiple_choice_nesting(child, False))
            
            return local_errors
        
        # Check the rule starting from the root
        errors.extend(check_pl_multiple_choice_nesting(tree, True))
    
    except FileNotFoundError:
        errors.append(f"File not found: {file_path}")
    except Exception as e:
        errors.append(f"Error checking custom rules: {str(e)}")
    
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
    
    # Check if we're in test mode
    test_mode = os.getenv("TEST_MODE", "").lower() in ["true", "1", "yes"]
    expected_failures_str = os.getenv("EXPECTED_FAILURES", "")
    expected_failures = set()
    
    if test_mode and expected_failures_str:
        # Parse expected failures (comma-separated list of filenames)
        expected_failures = set(f.strip() for f in expected_failures_str.split(",") if f.strip())
        print(f"🧪 TEST MODE: Expecting these files to fail: {', '.join(sorted(expected_failures))}")
        print()
    
    print(f"Scanning for HTML files in: {repo_root}")
    html_files = find_html_files(repo_root)
    
    if not html_files:
        print("No HTML files found.")
        return 0
    
    print(f"Found {len(html_files)} HTML file(s) to lint:")
    for f in html_files:
        print(f"  - {f}")
    print()
    
    # Track results
    results = {}
    
    for file_path in html_files:
        print(f"Linting: {file_path}")
        errors = lint_file(file_path)
        
        # Get just the filename for comparison
        filename = os.path.basename(file_path)
        results[filename] = {"has_errors": bool(errors), "errors": errors}
        
        if errors:
            print(f"  ❌ FAILED with {len(errors)} error(s):")
            for error in errors:
                print(f"    - {error}")
        else:
            print(f"  ✓ PASSED")
        print()
    
    # Determine overall pass/fail based on mode
    if test_mode:
        # In test mode: verify that expected failures actually fail
        # and files not in expected failures pass
        test_passed = True
        
        print("=" * 60)
        print("TEST MODE VALIDATION")
        print("=" * 60)
        
        for filename, result in sorted(results.items()):
            should_fail = filename in expected_failures
            did_fail = result["has_errors"]
            
            if should_fail and did_fail:
                print(f"✓ {filename}: Correctly detected as INVALID")
            elif not should_fail and not did_fail:
                print(f"✓ {filename}: Correctly detected as VALID")
            elif should_fail and not did_fail:
                print(f"✗ {filename}: Expected to FAIL but PASSED")
                test_passed = False
            else:  # not should_fail and did_fail
                print(f"✗ {filename}: Expected to PASS but FAILED")
                test_passed = False
        
        print("=" * 60)
        
        if test_passed:
            print("✓ Test mode: All validations passed!")
            return 0
        else:
            print("❌ Test mode: Some validations failed!")
            return 1
    else:
        # Normal mode: all files must pass
        has_errors = any(result["has_errors"] for result in results.values())
        
        if has_errors:
            print("❌ Linting failed! Please fix the errors above.")
            return 1
        else:
            print("✓ All files passed linting!")
            return 0


if __name__ == "__main__":
    sys.exit(main())
