#!/usr/bin/env python3
"""
Validate JSON Schema files against the JSON Schema draft 2020-12 specification.
"""

import json
import sys
from pathlib import Path
from typing import List

try:
    import jsonschema
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import SchemaError, ValidationError
except ImportError as e:
    print(f"Error: Required package not installed: {e}")
    print("Please install jsonschema: pip install jsonschema>=4.17.0")
    sys.exit(1)


def validate_schema_file(schema_path: Path) -> bool:
    """
    Validate a single JSON schema file against draft 2020-12.
    
    Args:
        schema_path: Path to the schema file to validate
        
    Returns:
        True if valid, False if invalid
    """
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_content = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ {schema_path}: Invalid JSON syntax - {e}")
        return False
    except Exception as e:
        print(f"❌ {schema_path}: Error reading file - {e}")
        return False

    try:
        # Validate the schema against the draft 2020-12 meta-schema
        Draft202012Validator.check_schema(schema_content)
        print(f"✅ {schema_path}: Valid JSON Schema (draft 2020-12)")
        return True
    except SchemaError as e:
        print(f"❌ {schema_path}: Invalid JSON Schema - {e.message}")
        if hasattr(e, 'path') and e.path:
            print(f"   Path: {' -> '.join(str(p) for p in e.path)}")
        return False
    except Exception as e:
        print(f"❌ {schema_path}: Unexpected error - {e}")
        return False


def main(file_paths: List[str]) -> int:
    """
    Main function to validate multiple schema files.
    
    Args:
        file_paths: List of file paths to validate
        
    Returns:
        Exit code: 0 if all valid, 1 if any invalid
    """
    if not file_paths:
        print("No schema files provided for validation")
        return 0

    print(f"Validating {len(file_paths)} JSON Schema file(s) against draft 2020-12...")
    print()

    all_valid = True
    for file_path in file_paths:
        schema_path = Path(file_path)
        if not schema_path.exists():
            print(f"❌ {schema_path}: File not found")
            all_valid = False
            continue
            
        is_valid = validate_schema_file(schema_path)
        if not is_valid:
            all_valid = False

    print()
    if all_valid:
        print("🎉 All schema files are valid!")
        return 0
    else:
        print("💥 Some schema files have validation errors")
        return 1


if __name__ == "__main__":
    exit_code = main(sys.argv[1:])
    sys.exit(exit_code) 