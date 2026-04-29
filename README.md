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

## Using the Reusable Workflow

This repository provides a **reusable GitHub Actions workflow** that can be called from other repositories containing PrairieLearn content.

### In Your Repository

To use the linter in your own repository, create a workflow file (e.g., `.github/workflows/lint-html.yml`):

```yaml
name: Lint HTML Files

'on':
  workflow_dispatch:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  lint:
    uses: ucsb-cs/pl-linter/.github/workflows/lint-html.yml@main
```

This will automatically lint all HTML files in your repository and fail the workflow if any errors are found.

### In This Repository (Test Mode)

This repository uses a special test mode to validate that the linter correctly detects errors. The workflow in this repo expects certain files to fail:

```yaml
name: Test Linter

'on':
  workflow_dispatch:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  test-lint:
    uses: ./.github/workflows/lint-html.yml
    with:
      test-mode: true
      expected-failures: 'example_invalid.html,example_pl_invalid.html'
```

In test mode:
- Files listed in `expected-failures` must fail linting (to verify error detection works)
- All other files must pass linting
- The workflow succeeds only if this behavior is correct

## Running Locally

### Normal Mode

To run the linter locally in normal mode (all files must pass):

```bash
python3 lint_html.py
```

### Test Mode

To run the linter in test mode (for testing the linter itself):

```bash
TEST_MODE=true EXPECTED_FAILURES="example_invalid.html,example_pl_invalid.html" python3 lint_html.py
```

The script will:
1. Find all `.html` and `.HTML` files in the repository (excluding `.git` directory)
2. Validate each file for XML syntax
3. Apply any custom PL-specific rules
4. Report errors with line numbers and descriptions

## Exit Codes

**Normal Mode:**
- `0`: All files passed linting
- `1`: One or more files failed linting

**Test Mode:**
- `0`: Files that should fail did fail, and files that should pass did pass
- `1`: Unexpected pass/fail results

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
