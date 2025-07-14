#!/usr/bin/env python3
"""
Automatically update index.json with current schema files.
"""

import json
import os
from pathlib import Path
from typing import List, Dict


def find_schema_files(schemas_dir: Path) -> List[str]:
    """
    Find all schema files in the schemas directory.
    
    Args:
        schemas_dir: Path to the schemas directory
        
    Returns:
        List of relative paths to schema files
    """
    schema_files = []
    
    if not schemas_dir.exists():
        print(f"Warning: schemas directory {schemas_dir} does not exist")
        return schema_files
    
    # Find all .schema.json files except _main.schema.json
    for schema_file in schemas_dir.glob("*.schema.json"):
        if schema_file.name != "_main.schema.json":
            relative_path = f"schemas/{schema_file.name}"
            schema_files.append(relative_path)
    
    # Sort for consistent ordering
    schema_files.sort()
    return schema_files


def update_index_file(index_path: Path, schema_files: List[str], main_schema: str) -> bool:
    """
    Update the index.json file with current schema files.
    
    Args:
        index_path: Path to index.json
        schema_files: List of schema file paths
        main_schema: Path to main schema file
        
    Returns:
        True if file was updated, False if no changes needed
    """
    new_index = {
        "events": schema_files,
        "main": main_schema
    }
    
    # Check if index.json exists and load current content
    current_index = {}
    if index_path.exists():
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                current_index = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not read current index.json: {e}")
    
    # Check if update is needed
    if current_index == new_index:
        print("📄 index.json is already up to date")
        return False
    
    # Write updated index
    try:
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(new_index, f, indent=2)
            f.write('\n')  # Add trailing newline
        
        print(f"✅ Updated index.json with {len(schema_files)} event schema(s)")
        
        # Show what changed
        old_events = set(current_index.get("events", []))
        new_events = set(schema_files)
        
        added = new_events - old_events
        removed = old_events - new_events
        
        if added:
            print(f"   Added: {', '.join(sorted(added))}")
        if removed:
            print(f"   Removed: {', '.join(sorted(removed))}")
            
        return True
        
    except IOError as e:
        print(f"❌ Error writing index.json: {e}")
        return False


def main():
    """Main function to update the index."""
    # Get project root (assuming script is in scripts/ subdirectory)
    project_root = Path(__file__).parent.parent
    schemas_dir = project_root / "schemas"
    index_path = project_root / "index.json"
    main_schema = "schemas/_main.schema.json"
    
    print("🔍 Scanning for schema files...")
    
    # Check if main schema exists
    main_schema_path = project_root / main_schema
    if not main_schema_path.exists():
        print(f"❌ Main schema file not found: {main_schema}")
        return 1
    
    # Find all event schema files
    schema_files = find_schema_files(schemas_dir)
    
    print(f"📋 Found {len(schema_files)} event schema file(s):")
    for schema_file in schema_files:
        print(f"   - {schema_file}")
    
    # Update index.json
    if update_index_file(index_path, schema_files, main_schema):
        print("🎉 Index update completed!")
    else:
        print("ℹ️ No changes needed")
    
    return 0


if __name__ == "__main__":
    exit(main()) 