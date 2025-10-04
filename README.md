# PL HTML Linter

This repository contains a linter for PL (PrairieLearn) HTML files.

## Features

The linter checks HTML files for:

1. **XML Syntax Validation**: Ensures that HTML files have valid XML syntax, including:
   - Properly formatted tags
   - Properly nested elements
   - Correct attribute syntax

2. **PrairieLearn-Specific Rules**:
   - `<pl-multiple-choice>` elements must be the root element of the document (not nested inside any other element)

3. **Extensible Framework**: Additional custom validation rules can be easily added

## Automated Linting

The linter runs automatically via GitHub Actions on:
- Manual workflow dispatch
- Push to the `main` branch
- Pull requests to the `main` branch

## Running Locally

To run the linter locally:

```bash
python3 lint_html.py
```

The script will:
1. Find all `.html` and `.HTML` files in the repository (excluding `.git` directory)
2. Validate each file for XML syntax
3. Apply any custom PL-specific rules
4. Report errors with line numbers and descriptions

## Exit Codes

- `0`: All files passed linting
- `1`: One or more files failed linting

## Example Files

The repository includes example HTML files to demonstrate the linter's functionality:

- `example.html` - A valid HTML file that passes all checks
- `example_invalid.html` - An invalid HTML file with mismatched tags (XML syntax error)
- `example_pl_valid.html` - A valid PrairieLearn file with `<pl-multiple-choice>` as root element
- `example_pl_invalid.html` - An invalid PrairieLearn file with nested `<pl-multiple-choice>` element

## Requirements

- Python 3.x (uses standard library modules)

## Extending the Linter

To add custom validation rules, modify the `check_custom_rules()` function in `lint_html.py`.

### Example: Adding a Custom Rule

To add a new rule (e.g., checking for specific attributes or element patterns), edit the `check_custom_rules()` function:

```python
def check_custom_rules(file_path):
    """Check custom PL-specific rules."""
    errors = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Example: Check for specific pattern
        # if 'pattern' not in content:
        #     errors.append("Missing required pattern")
        
    except Exception as e:
        errors.append(f"Error checking custom rules: {str(e)}")
    
    return errors
```

The linter will automatically run your custom rules on all HTML files.
