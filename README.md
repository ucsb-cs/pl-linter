# PL HTML Linter

This repository contains a linter for PL (PrairieLearn) HTML files.

## Features

The linter checks HTML files for:

1. **XML Syntax Validation**: Ensures that HTML files have valid XML syntax, including:
   - Properly formatted tags
   - Properly nested elements
   - Correct attribute syntax

2. **Custom PL Rules**: Framework for adding PrairieLearn-specific validation rules (extensible)

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

## Requirements

- Python 3.x (uses standard library modules)

## Extending the Linter

To add custom validation rules, modify the `check_custom_rules()` function in `lint_html.py`.
